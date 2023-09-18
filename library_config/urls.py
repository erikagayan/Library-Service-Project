from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("books.urls", namespace="book")),
    path("api/users/", include("users.urls", namespace="user")),
    path("api/borrowings/", include("borrowings.urls", namespace="borrowing")),
    path("api/payments/", include("payments.urls", namespace="payment")),

    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/doc/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    path("debug/", include("debug_toolbar.urls")),

]
