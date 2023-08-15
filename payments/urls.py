from django.urls import path
from payments.views import (
    PaymentListView,
    PaymentDetailView,
    CheckoutSessionView
)

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("create-checkout-session/", CheckoutSessionView.as_view(), name="create-checkout-session"),
]

app_name = "payment"
