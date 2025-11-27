from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

logger = logging.getLogger('taqueria')


def send_order_confirmation(order, request=None):
    """Send an order confirmation email synchronously."""
    if not order.user or not order.user.email:
        logger.warning("Skipping order confirmation: missing user email for order %s", order.id)
        return

    subject = f"Confirmación de pedido #{order.id}"
    to = [order.user.email]
    context = {
        'order': order,
        'user': order.user,
        'request': request,
    }

    text_body = render_to_string('emails/order_confirmation.txt', context)
    html_body = render_to_string('emails/order_confirmation.html', context)

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost')
    msg = EmailMultiAlternatives(subject, text_body, from_email, to)
    msg.attach_alternative(html_body, 'text/html')
    try:
        msg.send()
        logger.info("Sent order confirmation email for order %s to %s", order.id, to[0])
    except Exception:
        logger.exception("Failed sending order confirmation for order %s", order.id)


def send_order_confirmation_async(order, request=None):
    """Send order confirmation in a background thread (simple async)."""
    import threading

    threading.Thread(target=send_order_confirmation, args=(order, request), daemon=True).start()
