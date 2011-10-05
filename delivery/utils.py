def enviarReclamacao(conteudo, autor):
    from django.core.mail import EmailMessage
    assunto = "[Reclamação EntregAqui] Autor: " + autor
    email = EmailMessage(assunto, conteudo, to=['entregaqui.mailer@gmail.com'])
    