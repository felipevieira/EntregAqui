from delivery.models import *
from django.contrib import admin
from models import Usuario, Loja, Funcionario, Catalogo, Produto, Endereco, \
    Categoria, Atendente, Gerente, Carrinho, ProdutosCarrinho

admin.site.register(Usuario)
admin.site.register(Loja)
admin.site.register(Funcionario)
admin.site.register(Catalogo)
admin.site.register(Produto)
admin.site.register(Endereco)
admin.site.register(Categoria)
admin.site.register(Atendente)
admin.site.register(Gerente)
admin.site.register(Carrinho)
admin.site.register(ProdutosCarrinho)
