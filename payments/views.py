import stripe
from decouple import config
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models import Payment
from payments.serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from payments.permissions import IsOwnerOrAdmin

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


class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = kwargs.get("session_id")
        try:
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                payment = Payment.objects.get(session_id=session_id)
                payment.status = "PAID"
                payment.save()
                return Response(
                    {"message": "Payment was successful."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Payment was not successful."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except stripe.error.StripeError:
            return Response(
                {"message": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Payment can be completed later."},
            status=status.HTTP_200_OK
        )
