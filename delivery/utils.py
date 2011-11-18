# -*- coding: utf-8 -*-

from django.core.mail import EmailMessage
from models import EnderecoUsuario

def enviar_reclamacao(conteudo, autor):    
    assunto = "[Reclamacao EntregAqui] Autor: " + autor
    email = EmailMessage(assunto, conteudo, to=['entregaqui.mailer@gmail.com'])
    email.send()

def enviar_contato(nome, email, assunto, telefone, texto):
    assunto = "[Preguica Delivery - " + assunto + "]"
    conteudo = "Autor: " + nome + "\n"
    conteudo += "Email: " + email + "\n"
    conteudo += "Telefone: " + telefone + "\n\n"
    conteudo += texto
    email = EmailMessage(assunto, conteudo, to=['entregaqui.mailer@gmail.com'])
    email.send()
    
def enviar_email_confirmacao(usuario):
    pass

def getConteudoEmailPedido(empresa, email, contato):
    return "Ola! \n\nA empresa " + empresa + " deseja realizar uma parceria com o Preguica Delivery, seguem os dados da mesma: \n" \
    "Nome da empresa: " + empresa + "\nEmail para contato: " + email + "\nTelefone para contato: " + contato

def enviar_pedido_parceria(conteudo, empresa):
    assunto = "[Pedido de Parceria] Empresa: " + empresa
    email = EmailMessage(assunto, conteudo, to=['entregaqui.mailer@gmail.com'])
    email.send()

def enviar_pedido_loja(pedido, loja):
    assunto = "[Preguica Delivery] - Pedido recebido!"
    mensagem = "Olá, " + loja.nome.encode('utf-8') + "! Você recebeu mais um pedido!\n\n"
    mensagem += "Detalhes do pedido:\n"
    comprador = pedido.comprador
    endereco = EnderecoUsuario.objects.get(usuario=comprador)
    for produto in pedido.produtos_pedido.all():
        mensagem += "Produto: " + produto.produto.nome.encode('utf-8')
        mensagem += " - Quantidade: " + str(produto.quantidade)
        mensagem += " - Valor: R$" + str(produto.valor) + "\n"
    mensagem += "\nCuto de entrega: R$" + str(loja.preco_entrega)
    mensagem += "\n\nPreco total: R$" + str(pedido.total_pago)
    mensagem += "\n\nLocal de entrega:\n"
    mensagem += endereco.logradouro.encode('utf-8')
    mensagem += ", N" + str(endereco.numero)
    mensagem += " - " + endereco.bairro.encode('utf-8')
    if not endereco.complemento == "":
        mensagem += "\nComplemento: " + endereco.complemento.encode('utf-8')
    mensagem += "\n" + endereco.cidade.encode('utf-8') + " - CEP: " + str(endereco.cep)
    mensagem += "\nReferencia: " + endereco.referencia.encode('utf-8')
#    mensagem += "\n\nContato com o comprador: " + str(comprador.telefone)
    mensagem += "\n\nObrigado!"
    email = EmailMessage(assunto, mensagem, to=[loja.email])
    email.send()
