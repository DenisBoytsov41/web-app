# Generated by Django 5.0.3 on 2024-04-12 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_login_recaptcha_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='recaptcha_response',
            field=models.TextField(verbose_name='Ответ reCAPTCHA'),
        ),
    ]