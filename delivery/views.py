from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from delivery.models import *
from delivery.forms import *

def home(request):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("home.html", { 'enderecos': enderecos })

def visualizar_categorias(request, cidade):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("categorias.html",
                {'cidade': cidade,
                 'categorias': Categoria.objects.all(),
                 'enderecos': enderecos
                 })

def listar_lojas(request, cidade, categoria):
    enderecos = Endereco.objects.values('cidade').annotate()
    lojas = Loja.objects.filter(endereco__cidade=cidade, categoria__nome=categoria)
    return render_to_response("lojas.html",
                {"lojas" : lojas,
                 'cidade': cidade,
                 'categorias': Categoria.objects.all(),
                 'categoria': categoria,
                 'enderecos': enderecos
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
                 'enderecos': enderecos
                 })

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            return HttpResponse('Ok')
    else:
        form = UsuarioForm()
    return render_to_response('cadastro.html', { 'form' : form },
                              context_instance=RequestContext(request))