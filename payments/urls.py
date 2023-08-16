from django.urls import path
from payments.views import (
    PaymentListView,
    PaymentDetailView,
    PaymentSuccessView,
    PaymentCancelView,
)

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path(
        "success/<str:session_id>",
        PaymentSuccessView.as_view(),
        name="success"
    ),
    path("cancel", PaymentCancelView.as_view(), name="cancel"),
]

app_name = "payment"
