#!/usr/bin/env python
# -*- coding: utf-8 -*-

import members
import random

class AmigoOculto:
    def __init__(self, members_by_email):
        self.members_by_email = members_by_email
        self.emails = {}
        self.not_chosen = []
        self.final = {}
        self.current = None

    def select(self):
        self.read_members_by_email()
        if not self.valid():
            print 'Invalid members'
            return
        while len(self.not_chosen) > 0:
            if self.current is None:
                self.current = self.get_current()
            self.final[self.current] = None
            while True:
                chosen_i = random.randint(0, len(self.not_chosen) - 1)
                if self.try_with(chosen_i):
                    break
        self.print_final()
        self.print_for_mailer()

    def read_members_by_email(self):
        for email in self.members_by_email:
            for member in self.members_by_email[email]:
                self.emails[member] = email
                self.not_chosen.append(member)

    def try_with(self, chosen_i):
        chosen = self.not_chosen[chosen_i]
        del self.not_chosen[chosen_i]
        if self.emails[chosen] != self.emails[self.current] and self.valid():
            self.final[self.current] = chosen
            self.current = chosen
            # The chosen person has already selected someone.
            if self.final.has_key(self.current):
                self.current = None
            return True
        self.not_chosen.append(chosen)
        return False

    # Select someone to get a friend in the beginning or when the person that was selected had
    # already selected someone.
    def get_current(self):
        for member in self.not_chosen:
            if not self.final.has_key(member):
                return member

    # People that have the same e-mail address can't get each other.  This function checks if its
    # still possible to get a valid arrangement.
    def valid(self):
        # If everyone is alread chosen, it's a valid arrangement.
        if len(self.not_chosen) == 0:
            return True
        # Checks the e-mail that has the higher number of members.  There must be at least one
        # member outside this e-mail for each person in it, so that each person outside this e-mail
        # has someone to get.  So, the number of persons in this e-mail must be at most half of the
        # not_chosen people.
        max = 0
        emails_count = {}
        for member in self.not_chosen:
            # If this person has already selected someone, for instance, if it was the first person
            # to get someone, it shouldn't be counted in the largest e-mail, because it does not
            # need someone outside the email to select still.
            if self.final.has_key(member):
                continue
            email = self.emails[member]
            if emails_count.has_key(email):
                emails_count[email] += 1
            else:
                emails_count[email] = 1
            if emails_count[email] > max:
                max = emails_count[email]
        return max <= len(self.not_chosen) / 2

    def print_final(self):
        with open('backup.txt', 'w') as f:
            for member in self.final:
                f.write(member + ' -> ' + self.final[member] + '\n')

    def print_for_mailer(self):
        mailer_input = {}
        for email in self.members_by_email:
            members = {}
            for member in self.members_by_email[email]:
                members[member] = self.final[member]
            mailer_input[email] = members
        with open('mailer_input.py', 'w') as f:
            f.write(str(mailer_input))
    
def main():
    amigo_oculto = AmigoOculto(members.members_by_email)
    amigo_oculto.select()


if __name__ == '__main__':
    main()
