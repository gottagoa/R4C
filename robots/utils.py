from datetime import datetime, timedelta

from robots.models import Robot

"""
1. Создана функция filter_and_sort_robots_by_data для фильтрации роботов по дате создания 
за последнюю неделю и сортировки по дате. Берет отсчет с сегодняшнего дня и за предыдущие 7 дней. 
Вытаскивает созданных роботов за этот период
2. Создана функция sort_robots_by_model_and_version для сортировки роботов по моделям с версиями
Внутри нее создан словарь robot_data для хранения данных по моделям и версиям. Итерируя по циклу,
добавляет модели по версиям
3. Создана функция sort_robots_by_version для сортировки роботов по версиям, которые попадают в словарь
"""

def filter_and_sort_robots_by_data():
  
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    return Robot.objects.filter(created__gte=start_of_week, created__lte=today).order_by('-created')


def sort_robots_by_model_and_version(robots):
    robot_data = {}
    for robot in robots:
        model = robot.model
        version = robot.version
        count = robot_data.get((model, version), 0)
        robot_data[(model, version)] = count + 1

    return robot_data

def sort_robots_by_version(robots):
    robot_data = {}
    for robot in robots:
        version = robot.version
        count = robot_data.get(version, 0)
        robot_data[version] = count + 1

    return robot_data