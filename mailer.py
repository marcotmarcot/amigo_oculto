#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

prefix=''

me='Marco Túlio Gontijo e Silva <marcotmarcot@gmail.com>'

def send_mails(mailer_input):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('marcotmarcot@gmail.com', '')
    print(mailer_input)
    for mail, members in mailer_input.items():
        body = prefix
        for name, member in members.items():
            body += 'O amigo oculto de ' + name + ' é ' + member[0] + ".\n\nO endereço é " + member[2] + ".\n\nO presente deve ser endereçado a " + member[3] + "."
        message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (me, mail, 'Amigo oculto Natal 2020', body)
        server.sendmail(me, [mail], message)
    server.close()

def main():
    with open('mailer_input.py') as f:
        mailer_input = eval(f.read())
    send_mails(mailer_input)

if __name__ == '__main__':
    main()
