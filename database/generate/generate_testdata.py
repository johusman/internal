#!/usr/bin/python

import MySQLdb
import members
import member_rfid

db = MySQLdb.connect(user='internal', passwd='g34Api5C9L', host='127.0.0.1', db='internal', charset='utf8')

try:
    new_members = members.generate(db, 1000)
    member_rfid.generate(db, new_members)
    db.commit()
except:
    db.rollback()
    raise 

db.close()

