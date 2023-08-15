from decouple import config
from django.http import JsonResponse
from rest_framework import generics
from borrowings.models import Borrowing
from payments.models import Payment
from payments.serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from payments.permissions import IsOwnerOrAdmin
from django.conf import settings
from rest_framework.views import APIView

import stripe

stripe.api_key = config("STRIPE_SECRET_KEY")


class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(borrowing=self.request.user)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwnerOrAdmin]


class CheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        borrowing_id = self.kwargs["pk"]
        borrowing = Borrowing.objects.get(id=borrowing_id)
        delta = borrowing.actual_return_date - borrowing.expected_return_date
        total_cost = delta.days * borrowing.book.daily_fee * 100
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": borrowing.book.title,
                        },
                        "unit_amount_decimal": total_cost,
                    },
                    "quantity": 1,
                }
            ],
            metadata={"borrowing_id": borrowing.id},
            mode="payment",
            success_url=settings.SITE_URL + "/?success=true&session_id="
                                            "{CHECKOUT_SESSION_ID}",
            cancel_url=settings.SITE_URL + "/?canceled=true",
        )
        return JsonResponse(
            {
                "id": checkout_session.id,
                "url": checkout_session.url
            }
        )
