from django.contrib.auth.models import User       # ➊
from django.utils import timezone
from django.conf import settings
from django.db import models
from PIL import  Image

# Create your models here.
class Avalia(models.Model):
    id_avalia = models.AutoField(primary_key=True)
    valor_avalia = models.CharField("Avaliação", max_length=255)

    def __str__(self):
        return self.valor_avalia

class Postagem(models.Model):
    titulo_postagem   = models.CharField(max_length=200)
    conteudo_postagem = models.TextField()
    id_avalia = models.ForeignKey(Avalia, on_delete=models.CASCADE, default=1)
    autor_postagem    = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE)
    data_postagem     = models.DateTimeField(default=timezone.now)
    ordering = ['-data_postagem']
    tags_sugeridas = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.titulo_postagem

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nome_perfil = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    matricula_perfil = models.CharField(max_length=255)
    foto_perfil =models.ImageField(blank=True)

    def __str__(self):
        return self.nome_perfil

    def save(self):
        super().save()
        im = Image.open(self.foto_perfil.path)
        novo_tamanho = (100, 100)
        im.thumbnail(novo_tamanho)
        im.save(self.foto_perfil.path)

    def foto_url(self):
        if self.foto_perfil and hasattr(self.foto_perfil, 'url'):
            return self.foto_perfil.url
        else:
            return self.nome_perfil

class Telefone(models.Model):
    id_telefone = models.AutoField(primary_key=True)
    numero_telefone = models.CharField(max_length=255)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    def __str__(self):
        return self.numero_telefone
class Perfil_post(models.Model):
    id_perfil_post = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    id_postagem = models.ForeignKey(Postagem, models.DO_NOTHING, db_column='id_postagem')

    def __str__(self):
        return str(self.id_perfil)
    
class Curtida(models.Model):
    post = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name="curtidas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "usuario")
    

class Comentario(models.Model):
    post     = models.ForeignKey(Postagem,
                                 on_delete=models.CASCADE,
                                 related_name="comentarios")
    autor    = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    conteudo = models.TextField()
    data     = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["data"]