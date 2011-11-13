from django.db import models
from django.contrib.auth.models import User

class CustomUsuario(models.Model):
    conta = models.OneToOneField(User, related_name="usuario", null=True)

class Usuario(CustomUsuario):
    sexo_choices = (("M", "Masculino"), ("F", "Feminino"))
    cpf = models.CharField(max_length=11, unique=True)
    nascimento = models.DateField()
    sexo = models.CharField(max_length=9, choices=sexo_choices)
    chave_de_ativacao = models.CharField(max_length=50)
    expiracao_chave = models.DateTimeField()
    
    def __unicode__(self):
        return self.conta.username

class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=20, blank=True)
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.logradouro + ", N" + unicode(self.numero) + " - " + self.cidade + " - " + self.estado

class EnderecoUsuario(Endereco):
    usuario = models.ForeignKey(Usuario, related_name="enderecos")
    referencia = models.CharField(max_length=200, blank=True)

class EnderecoLoja(Endereco):
    pass

class Categoria(models.Model):
    nome = models.CharField(max_length=20, unique=True)
    descricao = models.CharField(max_length=300)
    imagem = models.ImageField(upload_to='/static/images/')
    
    
    def __unicode__(self):
        return self.nome

class Loja(models.Model):
    STATUS_CHOICES = (("A", "Aberta"), ("F", "Fechada"))
    cnpj = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=30)
    nome_curto = models.CharField(max_length=15, unique=True)
    categoria = models.ForeignKey(Categoria)
    endereco = models.ForeignKey(EnderecoLoja)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    imagem = models.ImageField(upload_to='/static/images/')
    
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
    
    def __unicode__(self):
        return self.nome

class Atendente(Funcionario):
    pass

class Gerente(Funcionario):
    pass

class Pedido(models.Model):
    STATUS_CHOICES = (("ABERTO", "Em Aberto"), ("PEDIDO_REALIZADO", "Pedido Realizado"), ("DESPACHADO", "Saiu para entrega"),
                      ("DESPACHADO", "Despachado"), ("ENTREGUE", "Entregue"))
    
    comprador = models.ForeignKey(Usuario, related_name='pedidos')
    data_criacao = models.DateTimeField()
    loja = models.ForeignKey(Loja, related_name='Pedidos')
    produtos = models.ManyToManyField(Produto, through='ProdutosPedido')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    total_pago = models.IntegerField(default=0)
    
    def __unicode__(self):
        result = "["
        sep = ""
        for produto in self.produtos.all():
            result += sep + str(produto.nome)  
            sep = ", "
        
        result += "]"
        result = "Produtos: " + result + "; Loja: " + str(self.loja.nome) + "; "   
        result += " Status: " + self.status + " - " + str(self.total_pago) + "; "
        return result

class ProdutosPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="produtos_pedido")
    produto = models.ForeignKey(Produto, related_name="produtos_pedido")
    quantidade = models.IntegerField();
    
    def __unicode__(self):
        return unicode(self.pedido) + " - " + self.produto.nome + ": " + str(self.quantidade)

class SolicitacaoCidade(models.Model):
    nomeUsuario = models.CharField(max_length=50);
    emailUsuario = models.EmailField();
    cidade = models.CharField(max_length=100);
    
    def __unicode__(self):
        return self.cidade

class Carrinho(models.Model):
    comprador = models.ForeignKey(Usuario, related_name='carrinho')
    loja = models.ForeignKey(Loja)
    produtos = models.ManyToManyField(Produto, through='ProdutosCarrinho')
    status = models.CharField(max_length=30)
    total_pago = models.IntegerField()
    
    def __unicode__(self):
        result = "["
        sep = ""
        for produto in self.produtos.all():
            result += sep + str(produto.nome)  
            sep = ", "
        
        result += "]"
        result = "Produtos: " + result + "; Loja: " + str(self.loja.nome) + "; "   
        result += " Status: " + self.status + " - " + str(self.total_pago) + "; "
        return result

class ProdutosCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name="produtos_carrinho")
    produto = models.ForeignKey(Produto, related_name="produtos_carrinho")
    quantidade = models.IntegerField();
    
    def __unicode__(self):
        return unicode(self.carrinho) + " - " + self.produto.nome + ": " + str(self.quantidade)
