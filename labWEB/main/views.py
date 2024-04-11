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


from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
import json

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
