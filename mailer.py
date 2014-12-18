#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

prefix='''Olá!

Houve um erro no e-mail anterior, por favor desconsiderem ele e só considerem esse agora.

Apaguem o e-mail anterior para não confundir, esse é o certo.

Esse e-mail é para informá-lo quem é o seu amigo oculto para o Natal de 2014 na casa da vó.  Por
favor, confirme com o Marco Túlio que você recebeu esse e-mail.  Você pode confirmar de várias
formas.  Em ordem de preferência:

1. Mandando um outro e-mail para marcotmarcot@gmail.com falando que recebeu o e-mail do amigo
oculto.

2. Respondendo esse e-mail.

3. Mandando uma mensagem para o Marco Túlio no Facebook http://facebook.com/marcotmarcot.

4. Mandando um Whatsapp para (31) 9722-2006.

5. Mandando um SMS para o mesmo telefone.

6. Ligando para o mesmo telefone.


'''

me='Marco Túlio Gontijo e Silva <marcotmarcot@gmail.com>'

def send_mails(mailer_input):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('marcotmarcot@gmail.com', '')
    for mail in mailer_input:
        body = prefix
        for member in mailer_input[mail]:
            body += 'O amigo oculto de ' + member + ' é ' + mailer_input[mail][member] + " (OFICIAL).\n"
        message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (me, mail, 'OFICIAL: Amigo oculto CERTO da casa da vó', body)
        server.sendmail(me, [mail], message)
    server.close()

def main():
    with open('mailer_input.py') as f:
        mailer_input = eval(f.read())
    send_mails(mailer_input)

if __name__ == '__main__':
    main()
