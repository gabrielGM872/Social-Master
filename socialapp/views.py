from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

from socialapp.forms import (AvaliaForms,PostagemForms,ComentarioForm)
from socialapp.models import (Avalia,Postagem,Comentario,Curtida)
@csrf_exempt
def sugerir_tags(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        conteudo = data.get('conteudo', '')

        # 🔮 Aqui vem o toque mágico: me envia esse conteúdo!
        # Por enquanto, podemos simular com base em palavras:
        palavras_chave = {
        # 🐍 Programação & Tech
        "python": "Python",
        "django": "Django",
        "flask": "Flask",
        "javascript": "JavaScript",
        "html": "HTML",
        "css": "CSS",
        "frontend": "Front-end",
        "backend": "Back-end",
        "api": "API",
        "terminal": "CLI",
        "git": "Git",
        "github": "GitHub",
        "sql": "Banco de Dados",
        "mysql": "Banco de Dados",
        "postgres": "Banco de Dados",

        # 📈 Desenvolvimento & Projeto
        "bug": "Erro",
        "projeto": "Desenvolvimento",
        "deploy": "Publicação",
        "debug": "Depuração",
        "refatorar": "Melhoria de Código",
        "documentação": "Documentação",
        "produtivo": "Produtividade",

        # 📚 Estudo & Aprendizado
        "estudo": "Estudos",
        "curso": "Aprendizado",
        "tutorial": "Aprendizado",
        "resumo": "Resumo",
        "trabalho": "Escola",
        "aula": "Educação",
        "faculdade": "Educação",
        "dica": "Dica",
        "exercício": "Prática",
        "revisão": "Revisão",

        # ✨ Motivação & Emoções
        "força": "Motivacional",
        "motivação": "Motivacional",
        "superação": "Inspirador",
        "acreditar": "Reflexão",
        "parabéns": "Reconhecimento",
        "conquista": "Conquista",
        "desabafo": "Pessoal",
        "ansiedade": "Saúde Mental",
        "felicidade": "Humor Positivo",

        # 🎬 Cultura & Lazer
        "filme": "Cinema",
        "cinema": "Cinema",
        "série": "Entretenimento",
        "livro": "Literatura",
        "música": "Música",
        "jogo": "Game",
        "anime": "Anime",
        "mangá": "Anime",

        # 🌐 Web & Redes
        "instagram": "Social Media",
        "tiktok": "Social Media",
        "linkedin": "Carreira",
        "hashtag": "Social Media",
        "viral": "Tendência",
        "streaming": "Entretenimento",
        "podcast": "Podcast",

        # 💬 Vida & Cotidiano
        "rotina": "Dia a Dia",
        "café": "Cotidiano",
        "sono": "Cotidiano",
        "frio": "Clima",
        "calor": "Clima",
        "chuva": "Clima",
        "viagem": "Viagem",
        "trânsito": "Cidade",
        "bicicleta": "Mobilidade",

        # 💼 Profissão & Carreira
        "emprego": "Carreira",
        "vaga": "Oportunidade",
        "currículo": "Carreira",
        "entrevista": "Emprego",
        "estágio": "Carreira",

        # 🧠 Outros úteis
        "curiosidade": "Curiosidade",
        "pergunta": "Ajuda",
        "resposta": "Ajuda",
        "conselho": "Ajuda",
        "duvida": "Ajuda",
        "hack": "Truque",
        "atualização": "Notícia",
        # 👋 Cumprimentos e expressões informais
        "bom dia": "Cumprimento",
        "boa tarde": "Cumprimento",
        "boa noite": "Cumprimento",
        "e aí": "Informal",
        "opa": "Informal",
        "oi": "Cumprimento",
        "olá": "Cumprimento",
        "valeu": "Gratidão",
        "obrigado": "Gratidão",
        "agradeço": "Gratidão",
        "kkk": "Humor",
        "haha": "Humor",
        "nossa": "Expressão",
        "caraca": "Surpresa",
        "top": "Popular",
        "massa": "Popular",
        "show": "Empolgação",
        "finalmente": "Alívio",
        "aff": "Frustração",
        "será": "Dúvida",
        "help": "Ajuda",
        "socorro": "Ajuda",
        "alguém sabe": "Ajuda",
        }


        sugeridas = [tag for palavra, tag in palavras_chave.items() if palavra in conteudo.lower()]
        return JsonResponse({'tags': sugeridas})


# === AVALIAÇÕES ===

@login_required(login_url='login')
def new_avalia(request):
    avas = Avalia.objects.all()
    form = AvaliaForms(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Avaliação criada com sucesso!')
        return redirect('new_avalia')
    return render(request, 'social/new_avalia.html', {
        'form': form,
        'avas': avas
    })


@login_required(login_url='login')
def editar_avalia(request, id):
    avaliado = get_object_or_404(Avalia, pk=id)
    form     = AvaliaForms(request.POST or None, instance=avaliado)
    avas     = Avalia.objects.all()
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Avaliação atualizada com sucesso!')
        return redirect('new_avalia')
    return render(request, 'social/editar_avalia.html', {
        'form': form,
        'avas': avas,
        'avaliado': avaliado
    })


@login_required(login_url='login')
def deleta_avalia(request, id):
    avaliado = get_object_or_404(Avalia, pk=id)
    if request.method == "POST":
        avaliado.delete()
        messages.success(request, 'Avaliação deletada com sucesso!')
        return redirect('new_avalia')
    return render(request, 'social/deleta_avalia.html', {
        'avaliado': avaliado
    })


# === POSTAGENS ===

def index(request):
    postagens = Postagem.objects.order_by('-data_postagem')
    return render(request, 'social/index.html', {
        'postagens': postagens
    })


def post_detail(request, id):
    post = get_object_or_404(Postagem, pk=id)
    comentarios = post.comentarios.order_by("-data")

    form = ComentarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comentario = form.save(commit=False)
        comentario.post = post
        comentario.autor = request.user
        comentario.data = timezone.now()
        comentario.save()
        return redirect("post_detail", id=id)

    return render(request, "social/post_detail.html", {
        "post": post,
        "comentarios": comentarios,
        "form": form
    })


@login_required(login_url='login')
def new_post(request):
    form = PostagemForms(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.autor_postagem = request.user
        post.data_postagem  = timezone.now()
        post.tags_sugeridas = request.POST.get('tags_sugeridas')
        post.save()
        messages.success(request, 'Post criado com sucesso!')
        return redirect('index')
    

    postagens = Postagem.objects.order_by('-data_postagem')
    return render(request, 'social/new_post.html', {
        'form': form,
        'postagens': postagens
    })


@login_required(login_url='login')
def editar_post(request, id):
    post = get_object_or_404(Postagem, pk=id, autor_postagem=request.user)
    form = PostagemForms(
        request.POST or None,
        request.FILES or None,
        instance=post
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Post atualizado com sucesso!')
        return redirect('post_detail', id=id)

    postagens = Postagem.objects.order_by('-data_postagem')
    return render(request, 'social/editar_post.html', {
        'form': form,
        'postagens': postagens,
        'post': post
    })


@login_required(login_url='login')
def deleta_post(request, id):
    post = get_object_or_404(Postagem, pk=id, autor_postagem=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deletado com sucesso!')
        return redirect('index')
    return render(request, 'social/deleta_post.html', {
        'post': post
    })


@login_required(login_url='login')
def toggle_like(request, id):
    post = get_object_or_404(Postagem, pk=id)
    curtida, created = Curtida.objects.get_or_create(post=post, usuario=request.user)
    if not created:
        curtida.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required(login_url='login')
def add_comment(request, id):
    post = get_object_or_404(Postagem, pk=id)
    form = ComentarioForm(request.POST or None)
    if form.is_valid():
        c        = form.save(commit=False)
        c.autor  = request.user
        c.post   = post
        c.save()
        messages.success(request, 'Comentário adicionado!')
    return redirect('post_detail', id=id)


# === ESTÁTICAS ===

def contato(request):
    return render(request, 'social/contact.html')


def sobre(request):
    return render(request, 'social/about.html')