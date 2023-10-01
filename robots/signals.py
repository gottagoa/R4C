




from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def email_notification(sender, instance, created, **kwargs):
    print("Signal working!")
    if created: # Если был создан новый robots
        print(instance.serial)
        orders = Order.objects.filter(
            is_abcent=False, 
            is_notificated=False
            ).filter(robot_serial=instance.serial)
        if orders:
            print("Заказы найдены")
            email_subject = "Новое поступление роботов"
            message = render_to_string("email_notification.html", {"robot": instance})
            email_list = list(orders.values_list("customer__email", flat=True))
            email = EmailMessage(email_subject, message, to=email_list)
            email.content_subtype = "html"
            email.send()
            orders.update(is_apcent=True, is_notificated=True)