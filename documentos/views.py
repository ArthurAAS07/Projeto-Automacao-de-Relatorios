import os
from django.conf import settings
from django.http import HttpResponse
from docxtpl import DocxTemplate
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Documento
from django.contrib.auth.models import User

def cadastro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "cadastro.html", {"erro": "Usuário já existe"})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/gerar/')

    return render(request, "cadastro.html")

@login_required
def meus_documentos(request):
    documentos = Documento.objects.filter(usuario=request.user)
    return render(request, "meus_documentos.html", {"documentos": documentos})

def logout_view(request):
    logout(request)
    return redirect('/login/')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/gerar/")
        else:
            return render(request, "login.html", {"erro": "Login inválido"})

    return render(request, "login.html")

@login_required
def gerar_doc(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        idade = request.POST.get("idade")

        caminho_template = os.path.join(settings.BASE_DIR, "template.docx")
        doc = DocxTemplate(caminho_template)

        contexto = {
            "nome": nome,
            "idade": idade
        }

        doc.render(contexto)

        nome_arquivo = f"{nome}_documento.docx"
        caminho_saida = os.path.join(settings.MEDIA_ROOT, nome_arquivo)

        doc.save(caminho_saida)

        # salvar no banco
        Documento.objects.create(
            usuario=request.user,
            nome=nome_arquivo,
            arquivo=f"documentos/{nome_arquivo}"
        )

        with open(caminho_saida, "rb") as arquivo:
            response = HttpResponse(
                arquivo.read(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            response["Content-Disposition"] = f"attachment; filename={nome_arquivo}"
            return response

    return render(request, "formulario.html")