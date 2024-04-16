from audioop import reverse

import jwt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UserTheme,UserToken
from main.models import Register
from django.http import JsonResponse
from .models import UserTheme
import json


class PersonalCabinetView(TemplateView):
    template_name = 'cabinet/personal_cabinet.html'

    def dispatch(self, request, *args, **kwargs):
        if 'token' in request.GET:
            token = request.GET.get('token')
            try:
                user_token = UserToken.objects.get(token=token)
                request.user = user_token.user
            except UserToken.DoesNotExist:
                return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.GET.get('token', '')
        username = ''
        guest_mode = True
        error = ''
        user = ''

        user_theme = None  # Инициализируем переменную user_theme значением None

        if token:
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                username = decoded_token.get('login', '')
                guest_mode = False
            except jwt.ExpiredSignatureError:
                error = 'Токен истек'
            except jwt.InvalidTokenError:
                error = 'Недействительный токен'

        if username:
            user = Register.objects.get(login=username)
            user_theme, created = UserTheme.objects.get_or_create(user=user)
            user_token, token_created = UserToken.objects.get_or_create(user=user)
            user_token.token = token
            user_token.save()

            if self.request.method == 'POST':
                theme = self.request.POST.get('theme', '')
                user_theme.theme = theme
                user_theme.save()

        context['username'] = username
        context['guest_mode'] = guest_mode
        context['error'] = error
        context['jwt_token'] = token
        if user_theme:
            context['current_theme'] = user_theme.theme
        else:
            context['current_theme'] = 'light'
            context['username'] = None
            context['guest_mode'] = 'true'
            context['jwt_token'] = None

        return context


def save_theme_view(request):
    if request.method == 'POST' and request.body:
        data = json.loads(request.body)
        username = data.get('username')
        new_theme = data.get('theme')
        print('Логин пользователя:', username)
        user = Register.objects.get(login=username)

        user_theme, created = UserTheme.objects.get_or_create(user=user)
        user_theme.theme = new_theme
        user_theme.save()

        return JsonResponse({'message': 'Тема успешно сохранена'}, status=200)
    else:
        return JsonResponse({'error': 'Некорректный запрос'}, status=400)


def logout_view(request):
    if request.method == 'POST' and request.body:
        data = json.loads(request.body)
        username = data.get('username')
        token = data.get('token')
        try:
            user_token = UserToken.objects.get(user=username, token=token)
            user_token.token = None
            user_token.save()
            return JsonResponse({'success': True})
        except UserToken.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Токен пользователя не найден'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Метод не поддерживается'}, status=405)
def protected_resource(request):
    if request.method == 'GET':
        jwt_token = request.headers.get('Authorization', '').split(' ')[1]
        try:
            decoded = jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            login = decoded.get['login', '']
            return JsonResponse({"message": f"Доступ разрешен для пользователя: {login}"})
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Время действия токена истекло"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Недействительный токен"}, status=401)
    return JsonResponse({"error": "Недопустимый метод запроса"}, status=405)

def index(request):
    return render(request, 'cabinet/personal_cabinet.html')