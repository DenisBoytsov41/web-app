import jwt
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserTheme


def personal_cabinet(request):
    token = request.GET.get('token', '')
    username = ''
    guest_mode = True

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
        user = User.objects.get(username=username)
        user_theme, created = UserTheme.objects.get_or_create(user=user)

        if request.method == 'POST':
            theme = request.POST.get('theme', '')
            user_theme.theme = theme
            user_theme.save()

    context = {
        'username': username,
        'guest_mode': guest_mode,
        'current_theme': user_theme.theme if not guest_mode else 'light',  # Используйте тему по умолчанию для гостей
    }
    return render(request, 'cabinet/personal_cabinet.html', context)


def index(request):
    return render(request, 'cabinet/personal_cabinet.html')

class PersonalCabinetView(TemplateView):
    template_name = 'cabinet/personal_cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.GET.get('token', '')
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            context['username'] = decoded_token.get('login', '')
            print('Username:', context['username'])
        except jwt.ExpiredSignatureError:
            context['error'] = 'Токен истек'
        except jwt.InvalidTokenError:
            context['error'] = 'Недействительный токен'
        return context
