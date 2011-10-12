# -*- coding: utf-8 -*-

def enviar_reclamacao(conteudo, autor):
    from django.core.mail import EmailMessage
    assunto = "[Reclamação EntregAqui] Autor: " + autor
    email = EmailMessage(assunto, conteudo, to=['entregaqui.mailer@gmail.com'])
    email.send()

def envia_email_confirmacao(usuario):
    pass