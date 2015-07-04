#!/usr/bin/python

import MySQLdb
import datetime
import time
import random
import uuid

def insert_into_table(table_name, obj):
    excluded = ['__doc__', '__module__']
    cursor = db.cursor()
    fields = []
    placeholders = []
    values = []
    for member, value in vars(obj).iteritems():
        if member not in excluded:
            fields.append(member)
            placeholders.append("%s")
            values.append(value)

    query = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ', '.join(fields), ', '.join(placeholders))
    print values
    cursor.execute(query, tuple(values))

def get_random_datetime(from_date, to_date):
    first_timestamp = time.mktime(from_date.timetuple())
    last_timestamp = time.mktime(to_date.timetuple())
    random_timestamp = first_timestamp + (last_timestamp - first_timestamp) * random.random()
    return datetime.datetime.fromtimestamp(random_timestamp)

def get_short_unique_string():
    return str(uuid.uuid4())[:8]

#
# Members
#

# Collisions are so unlikely that we don't care enough to check for them
def make_civic_regno():
    birthdatetime = get_random_datetime(datetime.datetime(1900,1,1), datetime.datetime(2010,1,1))
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

def generate_members(count):
    with open("firstnames.txt") as f:
        firstnames = f.readlines()
    with open("lastnames.txt") as f:
        lastnames = f.readlines()


    for i in range(1, count+1):
        member = Member()
        member.created = get_random_datetime(datetime.datetime(2013,1,1), datetime.datetime.now())
        member.updated = get_random_datetime(datetime.datetime(2013,1,1), datetime.datetime.now())
        member.email = get_short_unique_string() + '@test.makerspace.se'
        member.firstname = firstnames[int(random.random()*len(firstnames))].strip()
        member.lastname = lastnames[int(random.random()*len(lastnames))].strip()
        member.civicregno = make_civic_regno()
        member.country = 'SE'
        member.phone = '0735046226'
        try:
            insert_into_table('members', member)
        except:
            print "Failed to insert members"
            raise


db = MySQLdb.connect(user='internal', passwd='g34Api5C9L', host='127.0.0.1', db='internal', charset='utf8')

try:
    generate_members(50)
    db.commit()
except:
    db.rollback()
    raise 

db.close()

