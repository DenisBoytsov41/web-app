from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Login
from .forms import LoginForm
from .forms import RegisterForm
from django.shortcuts import render
import re
from django.contrib.auth.hashers import check_password
from .models import Register
import jwt
import requests
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
import json

def index(request):
    registration_form = RegisterForm()
    login_form = LoginForm()
    context = {'login_form': login_form, 'registration_form': registration_form}
    return render(request, 'main/index.html', context)

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            if Register.objects.filter(login=login).exists():
                return JsonResponse({'errors': {'login': [{'message': 'Регистрация с таким логином уже существует.', 'code': 'unique'}]}}, status=400)
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            form.instance.password = hashed_password
            form.save()
            return JsonResponse({'success': 'Регистрация успешно завершена'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        return JsonResponse({'errors': 'Метод запроса должен быть POST'}, status=405)

def email_validator(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

@csrf_exempt
def authorization(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_username = form.cleaned_data['login']
            login_password = form.cleaned_data['password']
            captcha_response = request.POST.get('g-recaptcha-response')

            secret_key = "6LeUYYgpAAAAANCdLoYzoZr3xse00GJaKvQxaiTt"
            captcha_data = {
                'secret': secret_key,
                'response': captcha_response
            }
            captcha_response_data = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
            captcha_result = captcha_response_data.json()

            if not captcha_result['success']:
                return JsonResponse({'errors': 'Подтвердите, что вы не робот.'}, status=403)

            # Поиск пользователя по логину
            users = Register.objects.filter(login=login_username)

            if users.exists():
                user = users.first()
                if check_password(login_password, user.password):
                    jwt_payload = {
                        'login': user.login,
                        'email': user.email
                    }
                    jwt_secret = "5A8xGvK2TQnS7z"
                    jwt_token = jwt.encode(jwt_payload, jwt_secret, algorithm='HS256')
                    return JsonResponse({'success': 'Вы успешно вошли в систему.', 'token': jwt_token})
                else:
                    return JsonResponse({'errors': 'Неверный логин или пароль.'}, status=401)
            else:
                return JsonResponse({'errors': 'Пользователь с таким логином не существует.'}, status=402)
        else:
            return JsonResponse({'errors': form.errors}, status=406)
    else:
        return JsonResponse({'errors': 'Метод запроса должен быть POST'}, status=405)