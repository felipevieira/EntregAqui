# -*- coding: utf-8 -*-

import sys
import os
## Setup to import models from Django app ##
sys.path.append(os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] ='EntregAqui.settings'

from django.core.management import setup_environ
from EntregAqui import settings
from EntregAqui.delivery.models import *
setup_environ(settings)

def main():
    enderecos = {}
    enderecos["danilo"] = Endereco(logradouro=u"Rua Julio Ferreira Tavares", numero=550,
                              cep="58411060", bairro=u"Itarar�", cidade=u"Campina Grande",
                              estado=u"Paraiba")
    enderecos["amaury"] = Endereco(logradouro=u"Rua Estelita Cruz", numero=1184,
                              cep="58102587", bairro=u"Alto Branco", cidade=u"Campina Grande",
                              estado=u"Paraiba")
    enderecos["sapore"] = Endereco(logradouro=u"Rua Santo Ant�nio", numero=74,
                              cep="58103355", bairro=u"Santo Ant�nio",
                              cidade=u"Campina Grande", estado=u"Paraiba")
    enderecos["pitts"] = Endereco(logradouro=u"Avenida Manoel Tavares", numero=445,
                              cep="58401402", bairro=u"Alto Branco",
                              cidade=u"Campina Grande", estado=u"Paraiba")
    alimento = Categoria(nome="Alimentos")
    lazer = Categoria(nome="Lazer")
    danilo = Usuario(nome=u"Danilo Ara�jo de Freitas", email="dsurviver@gmail.com",
                     cpf="12345678910", senha="123")
    amaury = Usuario(nome=u"Amaury Medeiros", email="amaurymedeiros@gmail.com",
                     cpf="12312312312", senha="123")
    pitts = Loja(nome=u"Pittsburg")
    sapore = Loja(nome=u"Sapore DItalia")
    catalogo_sapore = Catalogo()
    catalogo_pitts = Catalogo()
    pizzas = [Produto(nome="Pizza Grande de Frango", descricao="", preco=3300),
              Produto(nome="Lasanha de Frango", descricao="", preco=3300)]
    sanduiches = [Produto(nome="Pitts Picanha", descricao="", preco=800),
                  Produto(nome="Pitts Cheddar", descricao="", preco=700)]
    
    for endereco in enderecos.values():
        endereco.save()
    danilo.endereco = Endereco.objects.get(numero=550)
    amaury.endereco = Endereco.objects.get(numero=1184)
    danilo.save()
    amaury.save()
    alimento.save()
    lazer.save()
    pitts.categoria = Categoria.objects.get(nome="Alimentos")
    pitts.endereco = Endereco.objects.get(numero=445)
    sapore.categoria = Categoria.objects.get(nome="Alimentos")
    sapore.endereco = Endereco.objects.get(numero=74)
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
    
    