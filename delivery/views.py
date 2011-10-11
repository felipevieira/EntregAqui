# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from delivery.models import *
from delivery.forms import *
from delivery.utils import *

import datetime, random, sha

usuario_logado = "Visitante"

mensagem_email = "Obrigado por se cadastrar no PreguiçaDelivery.\n\n" \
           "Por favor, clique no link http://127.0.0.1:8000/cadastro/%s para ativar" \
           "a sua conta.\n\n" \
           "Caso não ative sua conta em 48 horas, a mesma será apagada.\n\n" \
           "Caso não consiga acessar o link, copie e cole o mesmo na barra de " \
           "endereço do seu navegador.\n\nObrigado.\n\n Equipe PreguiçaDelivery"

def home(request):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("home.html", 
                { 'enderecos': enderecos,
                 'usuario_logado' : usuario_logado })

def visualizar_categorias(request, cidade):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("categorias.html",
                {'cidade': cidade,
                 'categorias': Categoria.objects.all(),
                 'enderecos': enderecos,
                 'usuario_logado' : usuario_logado
                 })

def listar_lojas(request, cidade, categoria):
    enderecos = Endereco.objects.values('cidade').annotate()
    lojas = Loja.objects.filter(endereco__cidade=cidade, categoria__nome=categoria)
    return render_to_response("lojas.html",
                {"lojas" : lojas,
                 'cidade': cidade,
                 'categorias': Categoria.objects.all(),
                 'categoria': categoria,
                 'enderecos': enderecos,
                 'usuario_logado' : usuario_logado
                 })

def detalhar_catalogo_produtos(request, cidade, categoria, loja):
    enderecos = Endereco.objects.values('cidade').annotate()
    produtos = Produto.objects.filter(catalogo__loja__nome=loja, catalogo__loja__endereco__cidade=cidade, catalogo__loja__categoria__nome=categoria)
    return render_to_response("produtos.html",
                {"produtos" : produtos,
                 'cidade': cidade,
                 'loja': loja,
                 'categorias': Categoria.objects.all(),
                 'categoria': categoria,
                 'enderecos': enderecos,
                 'usuario_logado' : usuario_logado
                 })

def cadastrar_usuario(request):
    print request.user
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            u = form.save()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            chave = sha.new(salt+u.username).hexdigest()
            expira = datetime.datetime.today() + datetime.timedelta(2)
            usuario = Usuario.objects.create(usuario=u,
                                             cpf=form.cleaned_data['cpf'],
                                             chave_de_ativacao=chave,
                                             expiracao_chave=expira)
            from django.core.mail import EmailMessage
            email = EmailMessage("teste", mensagem_email % chave, to=[usuario.usuario.email])
            email.send()
            return HttpResponse('Ok')
    else:
        form = UsuarioForm()
    return render_to_response('cadastro.html', { 'form' : form },
                              context_instance=RequestContext(request))

def ativar_usuario(request, chave):
    if request.user.is_authenticated():
        return HttpResponse("Logado com " + request.user.username)
    usuario = get_object_or_404(Usuario, chave_de_ativacao=chave)
    if usuario.usuario.is_active:
        return HttpResponse("Conta ja ativada!")
    if usuario.expiracao_chave < datetime.datetime.today():
        return HttpResponse("expirou!")
    conta = usuario.usuario
    conta.is_active = True
    conta.save()
    return HttpResponse("Ok!")

def visualizar_painel_usuario(request):
    return render_to_response("painel_usuario.html",
                              {'usuario_logado' : usuario_logado})
    
def exibir_reclamacao(request):
    if request.method == 'POST':
        form = ReclamacaoForm(request.POST)
        if form.is_valid():
            enviar_reclamacao(form.cleaned_data['reclamacao'], usuario_logado)
            return HttpResponse('Reclamação enviada com sucesso.');
    else:
        form = ReclamacaoForm()
        
    return render_to_response("reclamar.html",
                              {'usuario_logado' : usuario_logado,
                               'form': form}, context_instance=RequestContext(request))
