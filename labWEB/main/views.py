from django.shortcuts import render
from .models import Login
from .forms import LoginForm
from .forms import RegisterForm
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password
from .models import Register
import json
import re


# Create your views here.

def index(request):
    registration_form = RegisterForm()
    login_form = LoginForm()
    context = {'login_form': login_form, 'registration_form': registration_form}
    return render(request, 'main/index.html', context)


def registration(request):
    error = ''
    if request.method == 'POST':
        # Получение данных из POST запроса (переданных через AJAX)
        data = json.loads(request.body.decode('utf-8'))

        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')
        username = data.get('username', '')
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        agree_terms = data.get('agreeTerms', False)
        age = data.get('age', '')
        gender = data.get('gender', '')

        # Проверка данных
        errors = []

        if not (2 <= len(first_name) <= 15) or not first_name.isalpha():
            errors.append("Недопустимое имя")

        if not (2 <= len(last_name) <= 15) or not last_name.isalpha():
            errors.append("Недопустимая фамилия")

        if not email:
            errors.append("Email не указан")
        elif not email_validator(email):
            errors.append("Недопустимый email")

        if len(username) < 6:
            errors.append("Логин должен содержать не менее 6 символов")

        if len(password) < 8:
            errors.append("Пароль должен содержать не менее 8 символов")
        elif not any(c.isupper() for c in password) or not any(c.islower() for c in password) \
                or not any(c.isdigit() for c in password) or not any(c.isalnum() for c in password):
            errors.append("Пароль должен включать хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ")

        if password != confirm_password:
            errors.append("Пароли не совпадают")

        if not agree_terms:
            errors.append("Вы должны принять правила")

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # Хеширование пароля
        hashed_password = make_password(password)

        # Сохранение пользователя
        try:
            user = Register.objects.create(
                name=first_name,
                surname=last_name,
                email=email,
                login=username,
                password=hashed_password,
                gender=gender
            )
            user.save()
            return JsonResponse({'success': 'Регистрация успешно завершена'})
        except Exception as e:
            return JsonResponse({'errors': 'Ошибка при регистрации пользователя: ' + str(e)}, status=500)

    elif request.method == 'POST':
        return JsonResponse({'errors': 'Метод запроса должен быть POST ' + request.method}, status=405)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def email_validator(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False



def authorization(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = 'Форма была неверной'
    else:
        form = LoginForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/authorization.html', data)
