from django.db import models
from django.contrib.auth.models import User

class CustomUsuario(models.Model):
    conta = models.OneToOneField(User, related_name="usuario")

class Usuario(CustomUsuario):
    cpf = models.CharField(max_length=11, unique=True)
    chave_de_ativacao = models.CharField(max_length=50)
    expiracao_chave = models.DateTimeField()
    
    def __unicode__(self):
        return self.usuario.username

class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20, blank=True)
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    referencia = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(Usuario, related_name="enderecos")
    
    def __unicode__(self):
        return self.logradouro + ", N" + unicode(self.numero) + " - " + self.cidade + " - " + self.estado

class Categoria(models.Model):
    nome = models.CharField(max_length=20, unique=True)
    
    def __unicode__(self):
        return self.nome

class Loja(models.Model):
    nome = models.CharField(max_length=30)
    categoria = models.ForeignKey(Categoria)
    endereco = models.ForeignKey(Endereco)
    
    def __unicode__(self):
        return self.nome + " - " + unicode(self.categoria)

class Catalogo(models.Model):
    loja = models.OneToOneField(Loja, related_name="catalogo")
    
    def __unicode__(self):
        return "Catalogo da loja " + self.loja.nome

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200, blank=True)
    preco = models.IntegerField()
    catalogo = models.ForeignKey(Catalogo, related_name="produtos")
    
    def __unicode__(self):
        return self.nome + " - " + self.catalogo.loja.nome
    
class Funcionario(CustomUsuario):
    loja = models.ForeignKey(Loja, related_name="funcionarios")
    cnpj = models.CharField(max_length=14)
    
    def __unicode__(self):
        return self.nome

class Atendente(Funcionario):
    pass

class Gerente(Funcionario):
    pass
