import datetime

from decouple import config
from django.http import JsonResponse
from rest_framework import generics
from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment
from payments.serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from payments.permissions import IsOwnerOrAdmin
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import redirect

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
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Test Book Title',
                    },
                    'unit_amount': 2000,  # Amount in cents (test value)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=settings.SITE_URL + "/?success=true&session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.SITE_URL + "/?canceled=true",
        )
        return JsonResponse({'session_id': session.id})
