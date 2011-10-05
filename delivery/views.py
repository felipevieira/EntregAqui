from django.http import HttpResponse
from django.shortcuts import render_to_response
from delivery.models import *

def home(request):
    enderecos = Endereco.objects.values('cidade').annotate()
    return render_to_response("home.html", { 'enderecos': enderecos })

def detalhar_catalogo_produtos(request, nome_cidade, nome_loja):
    produtos = Produto.objects.filter(catalogo__loja__nome=nome_loja, catalogo__loja__endereco__cidade=nome_cidade)
    return render_to_response("produtos.html", {"produtos" : produtos})
