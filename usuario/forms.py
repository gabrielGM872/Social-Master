from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Informe um e-mail válido.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # password1 e password2 já tratam a confirmação
