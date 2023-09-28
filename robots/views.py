from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot
from datetime import datetime  
from robots.utils import validate_data



@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            # Проверка валидации данных модели, версии и даты создания
            errors = validate_data(model, version,created)
            if errors:
                return JsonResponse({"errors": errors, "message":"Invalid Data"}, status=400)
            # Создание и сохранение объекта "робот"
            robot = Robot.objects.create(
                model=model,
                version=version,
                created=datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
            )
            
            # Создание словаря с информацией о роботе
            robot_data = {
                "model": robot.model,
                "version": robot.version,
                "created": robot.created.strftime('%Y-%m-%d %H:%M:%S')
            }

            return JsonResponse({robot_data})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid json"}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)







