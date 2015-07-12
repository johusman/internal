#!/usr/bin/python

import common
import datetime
import random

# Real "personnummer" can have a + instead of a -, indicating that the person is over 100 years old,
# but since we use four digits for the year, we ignore this and just use -.
def make_civic_regno_naive(is_female, is_samordningsnummer):
    birthdatetime = common.get_random_datetime(datetime.datetime(1900,1,1), datetime.datetime(2010,1,1))
    birthdate = "%04d%02d%02d" % (birthdatetime.year, birthdatetime.month, birthdatetime.day + (60 if is_samordningsnummer else 0)) 
    short_birthdate = birthdate[-6:]
    birth_number = "%03d" % (int(random.random() * 500)*2 + (1 if not is_female else 0))

    checksum_string = short_birthdate + birth_number
    odd = False
    checksum = 0
    for i in range(len(checksum_string)):
        value = int(checksum_string[i])
        if not odd:
            value = value * 2
        checksum = checksum + (value % 10) + (value / 10)
        odd = not odd

    check_digit = (10 - (checksum % 10)) % 10
    return birthdate + '-' + birth_number + str(check_digit)

def make_civic_regno(db, is_female, is_samordningsnummer):
    regno = make_civic_regno_naive(is_female, is_samordningsnummer)
    while not common.ensure_unique_value(db, 'members', 'civicregno', regno):
        print "Civic registration number collision: randomized number already in database: %s. Randomizing again, no worries." % (regno)
        regno = make_civic_regno_naive(is_female, is_samordningsnummer)
    return regno
    

def make_phone_number():
    if common.chance(0.5):
        prefix = "+468"
    else:
        prefix = "+4673"

    return prefix + common.get_random_digit_string(8)

def make_address(force_extra, force_apartment_number):
    extras = ['A', 'B']

    with open("streetnames.txt") as f:
        streetnames = f.readlines()

    streetname = common.get_random_item(streetnames).strip()
    streetnumber = int(random.random() * 100) + 1

    if force_extra or common.chance(0.1):
        extra = common.get_random_item(extras)
    else:
        extra = ""

    if force_apartment_number or common.chance(0.1):
        apartment_number = " Lgh %02d%02d" % (random.random()*10+8, random.random()*10+1)
    else:
        apartment_number = ""

    return "%s %s%s%s" % (streetname, streetnumber, extra, apartment_number)

def make_address2(force, firstnames, lastnames):
    extras = ["c/o", "att:"]

    if force or common.chance(0.05):
        return "%s %s %s" % (common.get_random_item(extras), common.get_random_item(firstnames).strip(), common.get_random_item(lastnames).strip())
    else:
        return None

class Member:
    created_at = None
    updated_at = None
    email = None
    password = None
    firstname = None
    lastname = None
    civicregno = None
    country = None
    phone = None

def generate(db, count):
    print "Populating table: members"

    with open("firstnames_female.txt") as f:
        firstnames_female = f.readlines()
    with open("firstnames_male.txt") as f:
        firstnames_male = f.readlines()
    with open("lastnames.txt") as f:
        lastnames = f.readlines()
    with open("cities.txt") as f:
        cities = f.readlines()

    # At least one member per call should use a "samordningsnummer"
    # http://www.skatteverket.se/privat/sjalvservice/blanketterbroschyrer/broschyrer/info/707.4.39f16f103821c58f680007997.html
    samordning_index = int(random.random() * count)

    # At least one member per call should use extra letter after street number
    extra_address_letter_index = int(random.random() * count)

    # At least one member per call should use apartment number information in address
    apartment_number_index = int(random.random() * count)

    # At least one member per call should use extra info such as c/o or att: in address
    address_extra_info_index = int(random.random() * count)

    members = {}
    for i in xrange(count):
        is_female = common.chance(0.5)

        member = Member()
        member.created_at = common.get_random_datetime(datetime.datetime(2013,1,1), datetime.datetime.now())
        member.updated_at = common.get_random_datetime(member.created_at, datetime.datetime.now())
        member.email = common.get_short_unique_string() + '@test.makerspace.se'
        if is_female:
            member.firstname = common.get_random_item(firstnames_female).strip()
        else:
            member.firstname = common.get_random_item(firstnames_male).strip()
        member.lastname = common.get_random_item(lastnames).strip()
        member.civicregno = make_civic_regno(db, is_female, i == samordning_index or common.chance(0.01))
        member.country = 'SE'
        member.phone = make_phone_number()
        member.address = make_address(i == extra_address_letter_index, i == apartment_number_index)
        member.city = common.get_random_item(cities).strip()
        # Apparently the connection between city and zip code is intellectual property in Sweden
        member.zipcode = "%03d%02d" % (int(random.random()*900)+100, int(random.random()*100))
        member.address2 = make_address2(i == address_extra_info_index, firstnames_female, lastnames)

        try:
            member_id = common.insert_into_table(db, 'members', member)
            members[member_id] = member
        except:
            print "Failed to populate members table"
            raise

    return members

