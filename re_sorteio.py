#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sorteio
import members
import mailer

def main():
    amigo_oculto = sorteio.AmigoOculto(members.members_by_email)
    amigo_oculto.read_members_by_email()
    with open("sorteadores.txt") as f:
        sorteadores = f.readlines()
    with open("sorteados.txt") as f:
        sorteados = f.readlines()
    if len(sorteados) != len(sorteadores):
        print "Different number of lines"
        return
    mailer_input = {}
    for i in range(len(sorteados)):
        sorteador = sorteadores[i].strip()
        if not sorteador:
            continue
        sorteado = sorteados[i].strip()
        email_sorteador = amigo_oculto.emails[sorteador]
        email_sorteado = amigo_oculto.emails[sorteado]
        if email_sorteador == email_sorteado:
            print "The person got itself"
            return
        if not mailer_input.has_key(email_sorteador):
            mailer_input[email_sorteador] = {}
        mailer_input[email_sorteador][sorteador] = sorteado
    mailer.send_mails(mailer_input)

if __name__ == '__main__':
    main()
