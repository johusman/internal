#!/usr/bin/python

import common
import datetime
import random

# Collisions are so unlikely that we don't care enough to check for them
def make_civic_regno():
    birthdatetime = common.get_random_datetime(datetime.datetime(1900,1,1), datetime.datetime(2010,1,1))
    birthdate = "%04d%02d%02d" % (birthdatetime.year, birthdatetime.month, birthdatetime.day) 
    short_birthdate = birthdate[-6:]
    birth_number = "%03d" % (int(random.random() * 500)*2)

    checksum_string = short_birthdate + birth_number
    odd = False
    checksum = 0
    for i in range(0, len(checksum_string)):
        value = int(checksum_string[i])
        if not odd:
            value = value * 2
        checksum = checksum + (value % 10) + (value / 10)
        odd = not odd

    check_digit = (10 - (checksum % 10)) % 10
    return birthdate + '-' + birth_number + str(check_digit)

def make_phone_number():
    if random.random() > 0.5:
        prefix = "08"
    else:
        prefix = "073"

    number = prefix
    for i in range(1, 8):
        number = number + str(int(random.random() * 10))

    return number

class Member:
    created = None
    updated = None
    email = None
    password = None
    firstname = None
    lastname = None
    civicregno = None
    country = None
    phone = None

def generate(db, count):
    with open("firstnames.txt") as f:
        firstnames = f.readlines()
    with open("lastnames.txt") as f:
        lastnames = f.readlines()

    generated_ids = []
    for i in range(1, count+1):
        member = Member()
        member.created = common.get_random_datetime(datetime.datetime(2013,1,1), datetime.datetime.now())
        member.updated = common.get_random_datetime(datetime.datetime(2013,1,1), datetime.datetime.now())
        member.email = common.get_short_unique_string() + '@test.makerspace.se'
        member.firstname = firstnames[int(random.random()*len(firstnames))].strip()
        member.lastname = lastnames[int(random.random()*len(lastnames))].strip()
        member.civicregno = make_civic_regno()
        member.country = 'SE'
        member.phone = make_phone_number()
        try:
            generated_ids.append(common.insert_into_table(db, 'members', member))
        except:
            print "Failed to insert members"
            raise

    return generated_ids

