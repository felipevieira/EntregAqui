from django.db import models

class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20, blank=True)
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    referencia = models.CharField(max_length=200, blank=True)

class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    cpf = models.CharField(max_length=11)
    senha = models.CharField(max_length=64)
    endereco = models.ForeignKey(Endereco)

class Categoria(models.Model):
    nome = models.CharField(max_length=20)

class Loja(models.Model):
    nome = models.CharField(max_length=30)
    categoria = models.ForeignKey(Categoria)
    endereco = models.ForeignKey(Endereco)

class Catalogo(models.Model):
    loja = models.OneToOneField(Loja, related_name="catalogo")

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200)
    preco = models.IntegerField()
    catalogo = models.ForeignKey(Catalogo, related_name="produtos")
    
class Funcionario(models.Model):
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=64)
    loja = models.ForeignKey(Loja, related_name="funcionarios")

class Atendente(Funcionario):
    pass

class Gerente(Funcionario):
    pass
