from django import forms
from .models import Register
from .models import Login

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['login', 'name', 'surname', 'email', 'password', 'confirm_password', 'gender', 'age_confirmation', 'rules_acceptance']
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'username', 'name': 'username', 'required': True, 'minlength': 6}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'firstName', 'name': 'firstName', 'required': True, 'minlength': 2, 'maxlength': 15}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'lastName', 'name': 'lastName', 'required': True, 'minlength': 2, 'maxlength': 15}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'email', 'name': 'email', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'password', 'name': 'password', 'required': True, 'minlength': 8}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'confirmPassword', 'name': 'confirmPassword', 'required': True}),
            'gender': forms.RadioSelect(choices=(('male', 'Мужской'), ('female', 'Женский')), attrs={'class': 'form-check-input', 'autocomplete': 'off', 'required': True}),
            'age_confirmation': forms.Select(choices=(('yes', 'Да'), ('no', 'Нет')), attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'age', 'name': 'age', 'required': True}),
            'rules_acceptance': forms.CheckboxInput(attrs={'class': 'form-check-input', 'autocomplete': 'off', 'id': 'agreeTerms', 'name': 'agreeTerms', 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['login', 'password']

        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'loginUsername', 'name': 'loginUsername', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'loginPassword', 'name': 'loginPassword', 'required': True, 'minlength': 8}),
        }

