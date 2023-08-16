import stripe
from django.conf import settings
from django.db import transaction

from borrowings.models import Borrowing
from payments.models import Payment


@transaction.atomic
def payment_helper(
        borrowing_id,
        date,
        type_of_payment,
        fine_multiplier=None,
        *args,
        **kwargs
):
    """
    Creates Stripe session for the borrowing.
    Writes session_id and session_url into Payment.
    """
    borrowing = Borrowing.objects.get(id=borrowing_id)
    delta = date - borrowing.borrow_date
    total_cost = delta.days * borrowing.book.daily_fee * 100
    if fine_multiplier:
        days_of_overdue = (
                borrowing.actual_return_date
                - borrowing.expected_return_date
        )
        total_cost = (
                             days_of_overdue
                             * fine_multiplier
                             * borrowing.book.daily_fee
                             * 100
                     ) + (
            borrowing.expected_return_date
            - borrowing.borrow_date
        ) * borrowing.book.daily_fee * 100
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
        success_url=settings.SITE_URL + "payments/success/"
                                        "{CHECKOUT_SESSION_ID}",
        cancel_url=settings.SITE_URL + "payments/cancel",
    )

    Payment.objects.create(
        status="PENDING",
        type=type_of_payment,
        borrowing_id=borrowing_id,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=total_cost
    )
