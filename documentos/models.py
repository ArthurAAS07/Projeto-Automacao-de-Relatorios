from django.db import models
from django.contrib.auth.models import User

class Documento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='documentos/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome