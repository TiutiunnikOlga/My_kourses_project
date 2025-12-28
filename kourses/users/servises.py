import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_price(amount):
    """Создаем цену в stripe"""
    return stripe.Price.create(
        currency="RUB",
        unit_amount=int(amount * 100),
        product_data={"name": "Pay for courses"},
    )


def create_stripe_session(price):
    """Создаем сессию на оплату в stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
