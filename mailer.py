#!/usr/bin/env python
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
    for mail in mailer_input:
        body = prefix
        for member in mailer_input[mail]:
            body += 'O amigo oculto de ' + member + ' é ' + mailer_input[mail][member] + ".\n"
        message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (me, mail, 'Amigo oculto Natal 2019', body)
        server.sendmail(me, [mail], message)
    server.close()

def main():
    with open('mailer_input.py') as f:
        mailer_input = eval(f.read())
    send_mails(mailer_input)

if __name__ == '__main__':
    main()
