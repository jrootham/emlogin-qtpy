#
#        Model.py
#
#        Model class
#

import sqlite3

import common

class Model(object):

    def __init__(self, fileName):
        self.conn = self.getConnection(fileName)
        self.mailboxes = {}
        self.sites = {}

        return

    def __del__(self):
        self.conn.close

        return

    def addMailbox(self, name, host, userName):
        errors = self.addBoxValidation(name, host, userName)
        if 0 == len(errors):
            self.mailboxes[name] = (host, userName)
            insert = "INSERT INTO mailboxes (name, host, user_name) VALUES (?, ?, ?);"
            cursor = self.conn.cursor()
            cursor.execute(insert, (name, host, userName))
            self.conn.commit()
            return ""
        else:
            return errors

    def addBoxValidation(self, name, host, userName):
        errors = self.boxValidation(name, host, userName)
        errors += common.exists(name, self.mailboxes)

        return errors

    def boxValidation(self, name, host, userName):
        errors = common.empty("Name", name)
        errors += common.empty("Host", host)
        errors += common.empty("User name", userName)

        return errors
        
    def getConnection(self, fileName):
        conn = sqlite3.connect(fileName)
        cursor = conn.cursor()

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='config'")

        if cursor.fetchone()[0] != 1 :            # if first table not there, create all of them
            cursor.execute("CREATE TABLE config (version INTEGER);")
            cursor.execute("INSERT INTO config (version) VALUES(1)")

            name = "name TEXT UNIQUE"
            host = "host TEXT"
            userName = "user_name TEXT"
            mailboxes = "CREATE TABLE mailboxes ({}, {}, {});".format(name, host, userName)
            cursor.execute(mailboxes)

            endpoint = "endpoint TEXT"
            identifier = "identifier TEXT"
            sites = "CREATE TABLE sites ({}, {}, {});".format(name, endpoint, identifier)
            cursor.execute(sites)

            conn.commit()

#  In the future there will be a case on version number here to upgrade earlier versions


        return conn

