import sqlite3

"""Provide access to an up to date database"""

def makeConnection(fileName):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()

    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='config'")

    if cursor.fetchone()[0] != 1 :            # if first table not there, create all of them
        cursor.execute("CREATE TABLE config (config_id INTEGER PRIMARY KEY, version INTEGER);")
        cursor.execute("INSERT INTO config (version) VALUES(1)")

        mailboxId = "mailbox_id INTEGER PRIMARY KEY"
        address = "address TEXT UNIQUE"
        host = "host TEXT"
        userName = "user_name TEXT"
        statement = "CREATE TABLE mailboxes ({}, {}, {}, {});"
        mailboxes = statement.format(mailboxId, address, host, userName)
        cursor.execute(mailboxes)

        siteId = "site_id INTEGER PRIMARY KEY"
        name = "name TEXT UNIQUE"
        endpoint = "endpoint TEXT"
        identifier = "identifier TEXT"
        siteAddress = "address TEXT"
        create = "CREATE TABLE sites ({}, {}, {}, {}, {});"
        sites = create.format(siteId, name, endpoint, identifier, siteAddress)
        cursor.execute(sites)

        conn.commit()

#  In the future there will be a case on version number here to upgrade earlier versions

    return conn
