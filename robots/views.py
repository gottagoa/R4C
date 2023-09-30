from django.http import HttpResponse
import csv
from openpyxl import Workbook
from robots.models import Robot
from datetime import datetime, timedelta
from robots.utils import *

"""
1. С utils.py были импортированы функции, написанные для предварительной сортировки роботов по дате создания и версиям
2. Создана функция generate_robot_summary_excel для создания Excel-файла (workbook)
Внутри функции фильтруем роботов и создаем  сет с уникальными моделями по значеню модели
3. В цикле функции generate_robot_summary_excel создаем для каждой модели свой excel sheet, в котором указываем заголовки таблиц
4. Фильтруем роботов для текущей модели в переменной model_robots
5. Создаем словарь с информацией о роботах для текущей модели в переменной robot_data
6. В цикле начинается заполнение таблицы значениями моделей и соответсвующих версий. Отсчет начинается
со второй строки, так как на первой заголовки
7. Создаем HTTP-ответ с файлом Excel. Указываем в Content-Disposition-attachment для автоматического 
скачивания файла после перехда по ссылке
8. Была создана также функция generate_robot_summary_csv для создания CSV-файла при необходимости перевода
файлов на другие форматы
"""


def generate_robot_summary_excel(request):
    workbook = Workbook()
    robots = filter_and_sort_robots_by_data()
    unique_models = set(robots.values_list('model', flat=True))
    
    for model in unique_models:
        sheet = workbook.create_sheet(title=model)
        sheet['A1'] = "Модель"
        sheet['B1'] = "Версия"
        sheet['C1'] = "Количество за неделю"
        
        model_robots = robots.filter(model=model)
        robot_data = sort_robots_by_version(model_robots)
        
        row_num = 2  
        for (version, count) in robot_data.items():
            sheet.cell(row=row_num, column=1, value=model)
            sheet.cell(row=row_num, column=2, value=version)
            sheet.cell(row=row_num, column=3, value=count)
            row_num += 1
    
    del workbook['Sheet']
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'
    workbook.save(response)

    return response



def generate_robot_summary_csv(request):
    robots = filter_and_sort_robots_by_data()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="robot_summary.csv"'

    writer = csv.writer(response)
    writer.writerow(['Модель', 'Версия', 'Количество за неделю'])
    robot_data = sort_robots_by_model_and_version(robots)
    for (model, version), count in robot_data.items():
        writer.writerow([model, version, count])

    return response
