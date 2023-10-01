import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from customers.models import Customer
from orders.models import Order
from robots.models import Robot

"""
Функция создает заказ на робота. Клиент указывает свой электронный адрес исерийный номер робота. Все это хранится в json файле
которую функция пытается вытащить. Далее вытаскивается клиент по его почте, если такого нет в базе,
то используется customer, _, чтобы избежать повторных созданий клиента.Затем создается заказ клиента.
is_robot_exist = Robot.objects.filter(serial=serial).exists() показывает,есть ли робот, если есть, то заказ
создается, в противном случае заказ тоже сохраняется, но уже с полями order.is_abcent = False, order.is_notificated = False
Помимо этого, создан файл templait с html файлом email.notification.html, который содержит в себе сообщение,
которое будет отправлено клиенту при наличии робота, на который он оставлял заказ
Создан также маршрут path("create/", create_order, name="create_order") в файле urls.py и регистрация в
админ панели для создания заказа

"""
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get("email")
            serial = data.get("serial")
            customer, _ = Customer.objects.get_or_create(email=email)
            order = Order(customer=customer, robot_serial=serial)
            is_robot_exist = Robot.objects.filter(serial=serial).exists()
            if is_robot_exist:
                order.save()
            else:
                order.is_abcent = False
                order.is_notificated = False
                order.save()
            return JsonResponse({"message": "Order successfully created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid json"}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
        