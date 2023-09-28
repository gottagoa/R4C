
#Функции для валидации модели, версии и даты создания
import datetime


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

    # Проверка валидации версии
    if not validate_version(version):
        errors['version'] = 'Неверная версия'

    # Проверка валидации даты создания
    if not validate_created(created):
        errors['created'] = 'Неверная дата создания'
    
    return errors