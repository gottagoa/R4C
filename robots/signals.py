




from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from orders.models import Order
from robots.models import Robot

"""
Функция использует триггер сигналов Django, чтобы получить сигнал от функции с файла Orders. Когда создается
робот, на который оставлял заказ клиент, то из заказов с помощью фильтра вытаскиваетмя его заказ
и клиенту приходит уведомление на его почту уведомление о производстве данного робота
"""
@receiver(post_save, sender=Robot)
def email_notification(sender, instance, created, **kwargs):
    if created: # Если был создан новый robots
        orders = Order.objects.filter(
            is_abcent=False, 
            is_notificated=False
            ).filter(robot_serial=instance.serial)
        if orders:
            email_subject = "Новое поступление роботов"
            message = render_to_string("email_notification.html", {"robot": instance})
            email_list = list(orders.values_list("customer__email", flat=True))
            email = EmailMessage(email_subject, message, to=email_list)
            email.content_subtype = "html"
            email.send()
            orders.update(is_apcent=True, is_notificated=True)