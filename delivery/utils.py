# -*- coding: utf-8 -*-

from django.core.mail import EmailMessage

def enviar_reclamacao(conteudo, autor):    
    assunto = "[Reclamacao EntregAqui] Autor: " + autor
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