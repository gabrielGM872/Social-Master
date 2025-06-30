from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


from socialapp.models import Postagem
from .forms import CadastroUsuarioForm

def home_usuario(request):
    return render(request, 'usuario/home.html')  # crie esse template depois


def cadastro_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo(a).')
            return redirect('index')  # ou 'home', o que for sua página inicial
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CadastroUsuarioForm()
    return render(request, 'usuario/usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')  # nome do campo no template (ver abaixo)
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'usuario/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('index')

