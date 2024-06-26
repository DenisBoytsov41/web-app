from audioop import reverse
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UserTheme, UserToken,Users
from main.models import Register
from django.http import JsonResponse
from .models import UserTheme
import json
from django.utils import timezone

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

def retrieve_data(request):
    registers = Register.objects.all()
    return render(request, 'cabinet/retrieve_data.html', {'registers': registers})

def total_records(request):
    total_users = Register.objects.count()
    return render(request, 'cabinet/total_records.html', {'total_users': total_users})

def count_records_last_month(request):
    today = timezone.now()
    begin_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = begin_date.replace(month=begin_date.month + 1) - timezone.timedelta(days=1)

    record_count = Users.objects.filter(created__range=(begin_date, end_date)).count()
    return render(request, 'cabinet/count_records_last_month.html', {'record_count': record_count})

def last_added_record(request):
    try:
        # Получаем последнюю добавленную запись
        last_record = Users.objects.latest('created')
        context = {
            'last_record': last_record
        }
        return render(request, 'cabinet/last_added_record.html', context)
    except Users.DoesNotExist:
        return render(request, 'cabinet/last_added_record.html', {'error_message': 'Записей не найдено'})

def display_results(request):
    try:
        total_records = Users.objects.count()
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        records_last_month = Users.objects.filter(created__range=[start_date, end_date]).count()
        last_record = Users.objects.latest('created')
        context = {
            'total_records': total_records,
            'records_last_month': records_last_month,
            'last_record': last_record
        }

        return render(request, 'cabinet/display_results.html', context)
    except Users.DoesNotExist:
        return render(request, 'cabinet/display_results.html', {'error_message': 'Записей не найдено'})

def search_results(request):
    if 'usersearch' in request.GET:
        user_search = request.GET['usersearch']
        if user_search:
            search_results = Users.objects.filter(name__icontains=user_search)
            return render(request, 'cabinet/search_results.html', {'search_results': search_results, 'user_search': user_search})
    return render(request, 'cabinet/search_results.html', {'error_message': 'Пожалуйста, введите ключевое слово для поиска.'})


def search_results_2(request):
    if 'usersearch' in request.GET:
        user_search = request.GET['usersearch']
        search_words = user_search.split()
        print(search_words)
        results = []
        for word in search_words:
            results += Users.objects.filter(name__icontains=word)

        print(results)
        return render(request, 'cabinet/search_results_2.html', {'results': results})

    return render(request, 'cabinet/search_results_2.html', {'error_message': 'Введите запрос в поле поиска.'})
