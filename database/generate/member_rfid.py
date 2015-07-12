#!/usr/bin/python

import common
import datetime
import random

def make_unique_rfid(db, length):
    rfid = common.get_random_digit_string(length).zfill(16)
    while not common.ensure_unique_value(db, 'member_rfid', 'tagid', rfid):
        print "RFID collision: randomized tagid already in database: %s. Randomizing again, no worries." % (rfid)
        rfid = common.get_random_digit_string(length).zfill(16)
    return rfid

class MemberRFID:
    created_at = None
    updated_at = None
    member_id = None
    active = None
    tagid = None
    description = None

def generate(db, members):
    print "Populating table: member_rfid"

    descriptions = ["Work tag", "Surgically implanted in hand", "Cell phone chip", "Sewn into wallet", "Of unknown extra-terrestrial origin"]

    # At least one member per call should have an inactive tag
    inactive_tag_index = int(random.random() * len(members))

    # At least one member per call should have three rfid keys
    three_key_index = int(random.random() * len(members)) 

    # At least one member per call should have a full length rfid
    full_rfid_index = int(random.random() * len(members))

    i = 0
    for member_id in members:
        member = members[member_id]
        if i == three_key_index:
            number_of_ids = 3
        elif i == full_rfid_index:
            number_of_ids = 2
        else:
            number_of_ids = int(1 + 3*random.random()**5) # about 20% with two keys, 8% with three keys

        for j in range(number_of_ids):
            has_description = j > 0 or common.chance(0.1)
            if i == full_rfid_index and j == 1 or common.chance(0.02):
                rfid = make_unique_rfid(db, 16)
            else:
                rfid = make_unique_rfid(db, 8)

            tag = MemberRFID()
            tag.created_at = common.get_random_datetime(member.created_at, datetime.datetime.now())
            tag.updated_at = common.get_random_datetime(tag.created_at, datetime.datetime.now())
            tag.member_id = member_id
            tag.active = common.chance(0.9) and i != inactive_tag_index
            tag.tagid = rfid
            tag.description = None if not has_description else common.get_random_item(descriptions)
            common.insert_into_table(db, 'member_rfid', tag)
        i = i + 1
