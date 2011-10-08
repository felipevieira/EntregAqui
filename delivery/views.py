from django.http import HttpResponse
from django.shortcuts import render_to_response
from delivery.models import *

usuario_logado="Visitante"

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
