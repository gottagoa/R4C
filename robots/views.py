from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot
from datetime import datetime  
from robots.utils import validate_data


"""
1. С utils.py импортированы функции для проверки валидации и внесены в функцию create_robot
2. В функции create_robot ставим условие о POST запросе и прописываем условие о создании json файла
3. Передаем в файл поля- модель, версия и дата создания. В errors проверяем соответсвует ли условиям валидации
4. Создаем робота, указав все поля, данные в модели. Указываем серийный номер, при этом не передавая его в json файл
5. В словарь robot_data передаем данные для создания json файла
"""
@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            errors = validate_data(model, version,created)
            if errors:
                return JsonResponse({"errors": errors, "message":"Invalid Data"}, status=400)
           

            serial = f"{model}-{version}"
            robot = Robot.objects.create(
                serial=serial,
                model=model,
                version=version,
                created=datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
            )
            
           
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







