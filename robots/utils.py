import datetime

"""
1. Создаем три поля для валидации трех поей для передачи в json файд: модель, версия и дата создания
2. Каждая модель и версия состоят из двух символов. Поэтому в условиях прописываем проверку на
количество символов, а также, чтобы поля не были пустыми
3. В функции валидации даты создания указываем формат даты datetime
4. Прописываем функцию validate_data для соответствия условий валидации всех ранее прописсанных функций
"""

def validate_model(model):
    return model and len(model) == 2

def validate_version(version):
    return version and len(version) == 2

def validate_created(created):
    try:
        datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
    

def validate_data(model,version, created):
    errors = {}
    if not validate_model(model):
        errors['model'] = 'Неверная модель'

    if not validate_version(version):
        errors['version'] = 'Неверная версия'

    if not validate_created(created):
        errors['created'] = 'Неверная дата создания'
    
    return errors