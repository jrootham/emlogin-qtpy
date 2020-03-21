import sqlite3

"""Provide access to an up to date database"""

def makeConnection(fileName):
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
