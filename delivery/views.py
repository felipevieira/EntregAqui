# -*- coding: utf-8 -*-

from Carrinho import Carrinho
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UsuarioForm, ReclamacaoForm, EnderecoForm, LoginForm
from models import Usuario, Endereco, Categoria, Loja, Produto
from utils import enviar_reclamacao
import datetime
import random
import sha
from django.contrib.auth import authenticate, login as authlogin

def nome_usuario_logado(request):
    if request.user.is_authenticated():
        return request.user.first_name
    return "Visitante"

mensagem_email = "Obrigado por se cadastrar no PreguiçaDelivery.\n\n" \
           "Por favor, clique no link http://127.0.0.1:8000/cadastro/%s para ativar" \
           "a sua conta.\n\n" \
           "Caso não ative sua conta em 48 horas, a mesma será apagada.\n\n" \
           "Caso não consiga acessar o link, copie e cole o mesmo na barra de " \
           "endereço do seu navegador.\n\nObrigado.\n\n Equipe PreguiçaDelivery"

def testaFuncionamentoCarrinho(request):
    loja_id = 1
    produto_id = 2
    carrinho = Carrinho(request,loja_id)
    carrinho.adiciona(produto_id, 5)
    print(carrinho)

def home(request):
    print nome_usuario_logado(request)
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("home.html", 
                { 'enderecos': enderecos,
                 'usuario_logado' : nome_usuario_logado(request) },
)

def visualizar_categorias(request, cidade):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("categorias.html",
                {'cidade': cidade,
                 'categorias': Categoria.objects.all(),
                 'enderecos': enderecos,
                 'usuario_logado' : nome_usuario_logado(request)
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
                 'usuario_logado' : nome_usuario_logado(request)
                 })

def detalhar_catalogo_produtos(request, cidade, categoria, loja):
    if request.method == 'POST':
        pass
    enderecos = Endereco.objects.values('cidade').annotate()
    produtos = Produto.objects.filter(catalogo__loja__nome=loja, catalogo__loja__endereco__cidade=cidade, catalogo__loja__categoria__nome=categoria)
    return render_to_response("produtos.html",
                {"produtos" : produtos,
                 'cidade': cidade,
                 'loja': loja,
                 'categorias': Categoria.objects.all(),
                 'categoria': categoria,
                 'enderecos': enderecos,
                 'usuario_logado' : nome_usuario_logado(request)
                 })

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            u = form.save()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            chave = sha.new(salt+u.username).hexdigest()
            expira = datetime.datetime.today() + datetime.timedelta(2)
            usuario = Usuario.objects.create(conta=u,
                                             cpf=form.cleaned_data['cpf'],
                                             chave_de_ativacao=chave,
                                             expiracao_chave=expira)
            from django.core.mail import EmailMessage
            email = EmailMessage("Obrigado por se cadastrar no Preguiça Delivery",
                                 mensagem_email % chave, to=[usuario.conta.email])
            email.send()
            return HttpResponse('Ok')
    else:
        form = UsuarioForm()
    return render_to_response('cadastro.html', { 'form' : form },
                              context_instance=RequestContext(request))

def ativar_usuario(request, chave):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    try:
        usuario = Usuario.objects.get(chave_de_ativacao=chave)
    except Usuario.DoesNotExist:
        return HttpResponseRedirect("/")
    if usuario.conta.is_active:
        return HttpResponseRedirect("/")
    if usuario.expiracao_chave < datetime.datetime.today():
        return HttpResponse("expirou!")
    conta = usuario.conta
    conta.is_active = True
    conta.save()
    usuario.chave_de_ativacao = ""
    usuario.save()
    return HttpResponseRedirect("/adicionar_endereco")

def visualizar_painel_usuario(request):
    return render_to_response("painel_usuario.html",
                              {'usuario_logado' : nome_usuario_logado(request)})
    
def exibir_pedidos(request):
    return render_to_response("ultimos_pedidos.html",
                              {'usuario_logado' : nome_usuario_logado(request)})
    
def exibir_reclamacao(request):
    if request.method == 'POST':
        form = ReclamacaoForm(request.POST)
        if form.is_valid():
            enviar_reclamacao(form.cleaned_data['reclamacao'], nome_usuario_logado(request))
            return HttpResponse('Reclamação enviada com sucesso.');
    else:
        form = ReclamacaoForm()
        
    return render_to_response("reclamar.html",
                              {'usuario_logado' : nome_usuario_logado(request),
                               'form': form}, context_instance=RequestContext(request))

def exibir_parceria(request):
    return render_to_response("parceria.html")

def exibir_disponibilidade(request):
    return render_to_response("disponibilidade_cidade.html")
    
def adicionar_endereco(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = Endereco(logradouro=form.cleaned_data['logradouro'],
                                numero=form.cleaned_data['numero'],
                                complement=form.cleaned_data['complemento'],
                                bairro=form.cleaned_data['bairro'],
                                cep=form.cleaned_data['cep'],
                                cidade=form.cleaned_data['cidade'],
                                estado=form.cleaned_data['estado'],
                                referencia=form.cleaned_data['referencia'],
                                usuario=request.user)
            endereco.save()
            return HttpResponse("Endereco adicionado com sucesso!")
    return render_to_response("adicionar_endereco.html",
                              {'form' : EnderecoForm()},
                              context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            conta = authenticate(username=form.cleaned_data['login'],
                                 password=form.cleaned_data['senha'])
            authlogin(request, conta)
            return HttpResponse("Login efetuado com sucesso!")
    else:
        form = LoginForm()
    return render_to_response("login.html",
                              {'form' : form},
                              context_instance=RequestContext(request))
