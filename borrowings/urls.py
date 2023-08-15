from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingViewSet, CreateBorrowingView

router = routers.DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("create/", CreateBorrowingView.as_view(), name='create-borrowing'),
]


app_name = "borrowing"
