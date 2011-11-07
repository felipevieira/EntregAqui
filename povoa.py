# -*- coding: utf-8 -*-

import os
import sys

## Setup to import models from Django app ##
sys.path.append(os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] ='EntregAqui.settings'

from EntregAqui import settings
from EntregAqui.delivery.models import *
from django.core.management import setup_environ

setup_environ(settings)

def main():
    enderecos = {}
    enderecos["sapore"] = EnderecoLoja(logradouro=u"Rua Santo Ant�nio", numero=74,
                              cep="58103355", bairro=u"Santo Ant�nio",
                              cidade=u"Campina Grande", estado=u"Paraiba")
    enderecos["pitts"] = EnderecoLoja(logradouro=u"Avenida Manoel Tavares", numero=445,
                              cep="58401402", bairro=u"Alto Branco",
                              cidade=u"Campina Grande", estado=u"Paraiba")
    alimento = Categoria(nome="Alimentos", descricao="Aqui estao todos os restaurantes da cidade" ,imagem="/static/images/categorias_alimentos.jpg")
    lazer = Categoria(nome="Lazer", descricao= "Aqui estao todos os estabelecimentos de lazer da cidade", imagem="/static/images/categorias_lazer.jpg")
    pitts = Loja(nome=u"Pittsburg", nome_curto="pitts", cnpj="1", imagem="/static/images/logo_pittsburg_temp.jpg")
    sapore = Loja(nome=u"Sapore DItalia", nome_curto="sapore", cnpj="2", imagem="/static/images/logo_sapore_temp.jpg")
    catalogo_sapore = Catalogo()
    catalogo_pitts = Catalogo()
    pizzas = [Produto(nome="Pizza Grande de Frango", descricao="", preco=3300),
              Produto(nome="Lasanha de Frango", descricao="", preco=3300)]
    sanduiches = [Produto(nome="Pitts Picanha", descricao="", preco=800),
                  Produto(nome="Pitts Cheddar", descricao="", preco=700)]
    
    for endereco in enderecos.values():
        endereco.save()
    alimento.save()
    lazer.save()
    pitts.categoria = Categoria.objects.get(nome="Alimentos")
    pitts.endereco = EnderecoLoja.objects.get(numero=445)
    sapore.categoria = Categoria.objects.get(nome="Alimentos")
    sapore.endereco = EnderecoLoja.objects.get(numero=74)
    pitts.save()
    sapore.save()
    catalogo_sapore.loja = Loja.objects.get(nome="Sapore DItalia")
    catalogo_pitts.loja = Loja.objects.get(nome="Pittsburg")
    catalogo_sapore.save()
    catalogo_pitts.save()
    for pizza in pizzas:
        pizza.catalogo = Catalogo.objects.get(loja__nome="Sapore DItalia")
        pizza.save()
    for sanduiche in sanduiches:
        sanduiche.catalogo = Catalogo.objects.get(loja__nome="Pittsburg")
        sanduiche.save()

if __name__ == "__main__":
    main()
    
    