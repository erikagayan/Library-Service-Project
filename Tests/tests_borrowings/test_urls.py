from django.test import SimpleTestCase
from django.urls import reverse, resolve
from borrowings.views import BorrowingViewSet


class TestBorrowingUrls(SimpleTestCase):
    def test_list_url_resolves(self):
        url = reverse("borrowing:borrowing-list")
        self.assertEqual(resolve(url).func.cls, BorrowingViewSet)

    def test_detail_url_resolves(self):
        borrowing_id = 1
        url = reverse("borrowing:borrowing-detail", args=[borrowing_id])
        self.assertEqual(resolve(url).func.cls, BorrowingViewSet)

    def test_create_url_resolves(self):
        url = reverse("borrowing:borrowing-list")
        self.assertEqual(resolve(url).func.cls, BorrowingViewSet)
