# -*- coding: utf-8 -*-

import os
import sys

## Setup to import models from Django app ##
sys.path.append(os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'EntregAqui.settings'

from EntregAqui import settings
from EntregAqui.delivery.models import *
from django.core.management import setup_environ

setup_environ(settings)

def main():
    enderecos = {}
    enderecos["sapore"] = EnderecoLoja(logradouro=u"Rua Santo Antï¿½nio", numero=74,
                              cep="58103355", bairro=u"Santo Antï¿½nio",
                              cidade=u"Campina Grande", estado=u"Paraiba")
    enderecos["pitts"] = EnderecoLoja(logradouro=u"Avenida Manoel Tavares", numero=445,
                              cep="58401402", bairro=u"Alto Branco",
                              cidade=u"Campina Grande", estado=u"Paraiba")
    alimento = Categoria(nome="Alimentos", descricao="Aqui estao todos os restaurantes da cidade" , imagem="/static/images/categorias_alimentos.jpg")
    lazer = Categoria(nome="Lazer", descricao="Aqui estao todos os estabelecimentos de lazer da cidade", imagem="/static/images/categorias_lazer.jpg")
    pitts = Loja(nome=u"Pittsburg", nome_curto="pitts", cnpj="1", imagem="/static/images/logo_pittsburg_temp.jpg", email="dsurviver@gmail.com", preco_entrega=4.00)
    sapore = Loja(nome=u"Giraffas", nome_curto="sapore", cnpj="2", imagem="/static/images/logo_sapore_temp.jpg", email="dsurviver@gmail.com", preco_entrega=5.00)
    catalogo_sapore = Catalogo()
    catalogo_pitts = Catalogo()
    pizzas = [ Produto(nome="Brutus", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/Brutus.png"),
              Produto(nome="Cheese", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/Cheese.png"),
              Produto(nome="Cheese Egg", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/CheeseEgg.png"),
              Produto(nome="Cheese Frango", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/CheeseFrango.png"),
              Produto(nome="Cheese Salada", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/CheeseSalada.png"),
              Produto(nome="Clone Frango", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/CloneFrango.png"),
              Produto(nome="Clona Hamburguer", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/CloneHamburguer.png"),
              Produto(nome="Coca Cola", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/Coca.png"),
              Produto(nome="Fanta", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/Fanta.png"),
              Produto(nome="Kuat", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/Kuat.png"),
              Produto(nome="Mega Gringo", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/MegaGringo.png"),
              Produto(nome="Milk Shake Baunilha", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/MilkBaunilha.png"),
              Produto(nome="Milk Shake Chocolate", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/MilkChocolate.png"),
              Produto(nome="Mousse de Chocolate", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/MousseChocolate.png"),
              Produto(nome="Mouse de Coco", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Giraffas/MousseCoco.png")
              ]
    
    sanduiches = [ Produto(nome="Pitts Bacon", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsBacon.jpg"),
                  Produto(nome="Pitts Carne", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsCarne.jpg"),
                  Produto(nome="Pitts Cheddar", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsCheddar.jpg"),
                  Produto(nome="Pitts Cheese", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsCheese.jpg"),
                  Produto(nome="Pitts Double", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsDouble.jpg"),
                  Produto(nome="Pitts Egg", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsEgg.jpg"),
                  Produto(nome="Pitts Especial", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsEspecial.jpg"),
                  Produto(nome="Pitts Frango", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsFrango.jpg"),
                  Produto(nome="Pitts Peixe", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsPeixe.jpg"),
                  Produto(nome="Pitts Picanha", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsPicanha.jpg"),
                  Produto(nome="Pitts Carne de Sol", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsSol.jpg"),
                  Produto(nome="Pitts Tudo", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/PittsTudo.jpg"),
                  Produto(nome="Prato Executivo Camarao", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoCamarao.jpg"),
                  Produto(nome="Prato Executivo Carne de Sol", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoCarneSol.jpg"),
                  Produto(nome="Prato Executivo File Grelhado", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoGrelhado.jpg"),
                  Produto(nome="Prato Executivo Hamburguer", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoHamburguer.jpg"),
                  Produto(nome="Prato Executivo Medalhao", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoMedalhao.jpg"),
                  Produto(nome="Prato Executivo Nuggets", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoNuggets.jpg"),
                  Produto(nome="Prato Executivo File a Parmegiana", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/ExecutivoParmegiana.jpg"),
                  Produto(nome="Agua Mineral", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/Agua.jpg"),
                  Produto(nome="Agua Tonica", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/AguaTonica.jpg"),
                  Produto(nome="Coca Cola", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/CocaCola.jpg"),
                  Produto(nome="Coca Cola Zero", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/CocaZero.jpg"),
                  Produto(nome="Cerveja", descricao="", preco=8.50, imagem="/static/images/Produtos/Pequeno/Pittsburg/SkolLata.jpg")                  
                  ]
    
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
    catalogo_sapore.loja = Loja.objects.get(nome="Giraffas")
    catalogo_pitts.loja = Loja.objects.get(nome="Pittsburg")
    catalogo_sapore.save()
    catalogo_pitts.save()
    for pizza in pizzas:
        pizza.catalogo = Catalogo.objects.get(loja__nome="Giraffas")
        pizza.save()
    for sanduiche in sanduiches:
        sanduiche.catalogo = Catalogo.objects.get(loja__nome="Pittsburg")
        sanduiche.save()

if __name__ == "__main__":
    main()
    
    