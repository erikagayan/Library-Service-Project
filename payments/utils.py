import stripe
from decouple import config
from django.conf import settings

from borrowings.models import Borrowing
from payments.models import Payment

stripe.api_key = config("STRIPE_SECRET_KEY")


def payment_helper(borrowing_id, *args, **kwargs):
    """
    Creates Stripe session for the borrowing.
    Writes session_id and session_url into Payment.
    """
    borrowing = Borrowing.objects.get(id=borrowing_id)
    delta = borrowing.expected_return_date - borrowing.borrow_date
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

    Payment.objects.create(
        status="PENDING",
        type="PAYMENT",
        borrowing_id=borrowing_id,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=total_cost
    )
