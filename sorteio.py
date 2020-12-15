#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

class AmigoOculto:
    def __init__(self, members):
        self.members_by_email = {}
        self.member_by_name = {}
        for member in members:
            if member.email not in self.members_by_email:
                self.members_by_email[member.email] = []
            self.members_by_email[member.email].append(member)
            self.member_by_name[member.name] = member
        self.not_chosen = []
        self.final = {}
        self.current = None

    def select(self):
        self.read_members_by_email()
        if not self.valid():
            print('Invalid members')
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
        for email, members in self.members_by_email.items():
            for member in members:
                self.not_chosen.append(member.name)

    def try_with(self, chosen_i):
        chosen = self.not_chosen[chosen_i]
        del self.not_chosen[chosen_i]
        if self.member_by_name[chosen].email != self.member_by_name[self.current].email and self.valid():
            self.final[self.current] = chosen
            self.current = chosen
            # The chosen person has already selected someone.
            if self.current in self.final:
                self.current = None
            return True
        self.not_chosen.append(chosen)
        return False

    # Select someone to get a friend in the beginning or when the person that was selected had
    # already selected someone.
    def get_current(self):
        for name in self.member_by_name:
            if name not in self.final:
                return name

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
        for name in self.not_chosen:
            # If this person has already selected someone, for instance, if it was the first person
            # to get someone, it shouldn't be counted in the largest e-mail, because it does not
            # need someone outside the email to select still.
            if name in self.final:
                continue
            email = self.member_by_name[name].email
            if email in emails_count:
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
                members[member.name] = self.member_by_name[self.final[member.name]].to_list()
            mailer_input[email] = members
        with open('mailer_input.py', 'w') as f:
            f.write(str(mailer_input))


class Address:
    def __init__(self):
        self.names = []

    def add_name(self, name):
        self.names.append(name)

    def create_fake_receiver(self):
        shuffled = self.names.copy()
        random.shuffle(shuffled)
        self.fake_receiver = {}
        for i in range(len(self.names)):
            self.fake_receiver[self.names[i]] = shuffled[i]


def build_addresses(lines):
    addresses = {}
    for line in lines:
        fields = line.strip().split('\t')
        if fields[0] == 'Nome':
            continue
        name = fields[0]
        address = fields[2]
        if address not in addresses:
            addresses[address] = Address()
        addresses[address].add_name(name)
    for address in addresses.values():
        address.create_fake_receiver()
    return addresses


class Member:
    def __init__(self, name, email, address, fake_receiver):
        self.name = name
        self.email = email
        self.address = address
        self.fake_receiver = fake_receiver

    def to_list(self):
        return [self.name, self.email, self.address, self.fake_receiver]


def build_members(lines, addresses):
    members = []
    for line in lines:
        fields = line.strip().split('\t')
        if fields[0] == 'Nome':
            continue
        name = fields[0]
        email = fields[1]
        address = fields[2]
        members.append(Member(name, email, address, addresses[address].fake_receiver[name]))
    return members


def main():
    lines = open('members.tsv').readlines()
    addresses = build_addresses(lines)
    print(len(addresses))
    members = build_members(lines, addresses)
    amigo_oculto = AmigoOculto(members)
    amigo_oculto.select()


if __name__ == '__main__':
    main()
