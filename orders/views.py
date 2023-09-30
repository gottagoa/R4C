import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
# Create your views here.

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


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
        