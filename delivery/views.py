from django.http import HttpResponse
from django.shortcuts import render_to_response
from delivery.models import *

def home(request):
    return render_to_response("home.html")

def detalhar_catalogo_produtos(request, nome_cidade, nome_loja):
#    return HttpResponse("Voce esta procurando pela cidade %s e pela loja %s. " % (nome_cidade,nome_loja))
    produtos = Produto.objects.filter(catalogo__loja__nome=nome_loja, catalogo__loja__endereco__cidade=nome_cidade)
    print produtos
    return render_to_response("produtos.html", {"produtos" : produtos})

