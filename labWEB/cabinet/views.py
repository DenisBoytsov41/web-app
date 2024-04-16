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
        token = request.GET.get('token')
        login = request.GET.get('login')
        print(f"Login: {login}, Token: {token}")

        if token:
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                login = decoded_token.get('login', None)
                user_token = UserToken.objects.get(token=token)
                request.login = user_token.user
                return self.handle_authenticated_request(request, *args, **kwargs)
            except UserToken.DoesNotExist:
                pass
        if login:
            try:
                user = UserToken.objects.get(user=login)
                if user:
                    try:
                        user_token = UserToken.objects.get(user=user)
                        request.login = user
                        return self.handle_guest_request(request, *args, **kwargs)
                    except UserToken.DoesNotExist:
                        request.login = user
                        request.token = None
                        return self.handle_authenticated_request(request, *args, **kwargs)
            except UserToken.DoesNotExist:
                return self.handle_authenticated_request(request, *args, **kwargs)
        return self.handle_authenticated_request(request, *args, **kwargs)

    def handle_authenticated_request(self, request, *args, **kwargs):
        print("Я ТУТ4")
        return super().dispatch(request, *args, **kwargs)

    def handle_guest_request(self, request, *args, **kwargs):
        print("Я ТУТ3")
        token_value = request.GET.get('token')
        login_value = request.GET.get('login')
        request.GET = request.GET.copy()
        request.GET['guest'] = 'true'
        print(request.GET['guest'])

        context = self.get_context_data(**kwargs)
        context['guest_mode'] = True
        print(context.get('guest_mode'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.GET.get('token', '')
        guest = self.request.GET.get('guest')
        username = self.request.GET.get('login')
        error = ''
        user = ''
        print(guest)
        user_theme = None
        if token and not guest:
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                username = decoded_token.get('login', '')
                guest_mode = False
            except jwt.ExpiredSignatureError:
                error = 'Токен истек'
            except jwt.InvalidTokenError:
                error = 'Недействительный токен'

        if username and not guest:
            user = Register.objects.get(login=username)
            user_theme, created = UserTheme.objects.get_or_create(user=user)
            user_token, token_created = UserToken.objects.get_or_create(user=user)
            user_token.token = token
            user_token.save()

            if self.request.method == 'POST':
                if 'logout' in self.request.POST:
                    user_token.delete()
                else:
                    theme = self.request.POST.get('theme', '')
                    user_theme.theme = theme
                    user_theme.save()
        context['username'] = username
        context['guest_mode'] = False
        context['error'] = error
        context['jwt_token'] = token
        if user_theme and token is not None:
            context['current_theme'] = user_theme.theme
        else:
            context['current_theme'] = 'light'
            context['guest_mode'] = True
            context['username'] = username
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
        token = data.get('token')
        username = data.get('username')
        if token is None:
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                username = decoded_token.get('login', '')
            except jwt.InvalidTokenError:
                return JsonResponse({'success': False, 'message': 'Неверный токен'}, status=400)

        try:
            print("Я тут6")
            print(username)
            user_token = UserToken.objects.get(user=username)
            print(user_token.token)
            user_token.delete()
            print("Я тут7")
            return JsonResponse({'success': True})
        except UserToken.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Токен пользователя не найден'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Метод не поддерживается или отсутствуют данные в теле запроса'}, status=405)
def delete_token(request):
    if request.method == 'POST' and request.body:
        data = json.loads(request.body)
        username = data.get('username')
        print("Я тут 5")
        print(username)
        if username:
            try:
                user_token = UserToken.objects.get(user=username)
                user_token.token = None
                user_token.save()
                return JsonResponse({'success': True})
            except UserToken.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Токен пользователя не найден'}, status=404)
        else:
            return JsonResponse({'success': False, 'message': 'Недостаточно данных для выполнения запроса'}, status=400)
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