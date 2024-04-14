import jwt
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render
from .models import UserTheme
from main.models import Register


class PersonalCabinetView(TemplateView):
    template_name = 'cabinet/personal_cabinet.html'
    print("я тут")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.GET.get('token', '')
        username = ''
        guest_mode = True
        error = ''
        print(context)

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
            user_theme, created = UserTheme.objects.get_or_create(user=username)

            if self.request.method == 'POST':
                theme = self.request.POST.get('theme', '')
                user_theme.theme = theme
                user_theme.save()

        context['username'] = username
        context['guest_mode'] = guest_mode
        context['current_theme'] = user_theme.theme if user_theme and not guest_mode else 'light'
        context['error'] = error
        context['jwt_token'] = token

        return context
def index(request):
    return render(request, 'cabinet/personal_cabinet.html')