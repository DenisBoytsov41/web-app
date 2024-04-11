from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator, RegexValidator


class Register(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    LOGIN_MIN_LENGTH = 6
    PASSWORD_MIN_LENGTH = 8

    login_validator = MinLengthValidator(limit_value=LOGIN_MIN_LENGTH,
                                         message=f'Логин должен содержать не менее {LOGIN_MIN_LENGTH} символов')
    password_validator = MinLengthValidator(limit_value=PASSWORD_MIN_LENGTH,
                                            message=f'Пароль должен содержать не менее {PASSWORD_MIN_LENGTH} символов')
    password_regex_validator = RegexValidator(
        regex='^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+]).{8,}$',
        message='Пароль должен содержать хотя бы одну цифру, одну прописную и одну строчную букву, один специальный символ')

    login = models.CharField('Логин', max_length=20, primary_key=True, validators=[login_validator])
    name = models.CharField('Имя', max_length=15,
                            validators=[MinLengthValidator(2, 'Имя должно содержать не менее 2 символов')])
    surname = models.CharField('Фамилия', max_length=15,
                               validators=[MinLengthValidator(2, 'Фамилия должна содержать не менее 2 символов')])
    email = models.EmailField('Email', validators=[EmailValidator(message='Некорректный формат email')])
    password = models.CharField('Пароль', max_length=20, validators=[password_validator, password_regex_validator])
    confirm_password = models.CharField('Подтверждение пароля', max_length=20)
    gender = models.CharField('Пол', max_length=6, choices=GENDER_CHOICES)
    age_confirmation = models.BooleanField('Мне 18 лет', default=False)
    rules_acceptance = models.BooleanField('Принимаю правила', default=False)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'


class Login(models.Model):
    login = models.CharField('Логин', max_length=20, primary_key=True)
    password = models.CharField('Пароль', max_length=20)
    recaptcha_response = models.CharField('Ответ reCAPTCHA', max_length=100)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Вход в систему'
        verbose_name_plural = 'Входы в систему'
