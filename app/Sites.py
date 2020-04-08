import common

class Sites(object):
    """Model for sites data """
    def __init__(self, connection):
        self.connection = connection

        self.sites = {}

        cursor = self.connection.cursor()

        for row in cursor.execute("SELECT site_id, name, endpoint, identifier, address FROM sites;"):
            siteId, name, endpoint, identifier, address = row
            self.sites[name] = (siteId, endpoint, identifier, address)


    def getSiteList(self):
        """Get the list of names for the dropdown """

        return sorted(self.sites)


    def exists(self, name):
        """Check if site name exists"""
        return name in self.sites


    def getSite(self, name):
        """Get data for a site"""

        siteId, endpoint, identifier, address = self.sites[name]
        return (siteId, name, endpoint, identifier, address)


    def addSite(self, name, endpoint, identifier, address):
        """Add valid new site to local sites and database sitess"""

        messages = self.addSiteValidation(name, endpoint, identifier, address)
        if 0 == len(messages):
            
            cursor = self.connection.cursor()

            insert = "INSERT INTO sites (name, endpoint, identifier, address) VALUES (?, ?, ?, ?);"
            cursor.execute(insert, (name, endpoint, identifier, address))

            cursor.execute("SELECT site_id FROM sites WHERE name=?;", (name,))
            siteId, = cursor.fetchone()

            self.sites[name] = (siteId, endpoint, identifier, address)

            self.connection.commit()

            return ""
        else:
            return messages


    def renameSite(self, oldName, newName):
        """Update valid site in local sites and database sites"""

        messages = self.renameSiteValidation(oldName, newName)
        if 0 == len(messages):
            self.sites[newName] = self.sites[oldName]
            del self.sites[oldName]

            siteId = self.sites[newName][0]

            cursor = self.connection.cursor()

            cursor.execute("UPDATE sites SET name=? WHERE site_id=?;", (newName, siteId))
            self.connection.commit()
            
            return ""
        else:
            return messages


    def deleteSite(self, name):
        """Delete existing site"""
        messages = common.notExists(name, self.sites)
        if (0 == len(messages)):
            del self.sites[name]

            cursor = self.connection.cursor()
            delete = "DELETE FROM sites WHERE name=?;"

            cursor.execute(delete, (name,))
            self.connection.commit()

            return ""
        else:
            return messages


    def addSiteValidation(self, name, endpoint, identifier, address):
        """
        Confirm no site data is empty
        Confirm unique name for new site
        """
        messages = self.siteValidation(name, endpoint, identifier, address)
        messages += common.exists(name, self.sites)

        return messages


    def renameSiteValidation(self, newName, oldName):
        """
        """
        messages = ""
        
        if newName != oldName:
            messages = common.empty("Name", newName)
            messages += common.notExists(newName, self.sites)

        else:
            messages = "Name not changed"

        return messages


    def siteValidation(self, name, endpoint, identifier, address):
        """Confirm no site data is empty"""
        messages = common.empty("Name", name)
        messages += common.empty("Endpoint", endpoint)
        messages += common.empty("Identifier", identifier)
        messages += common.empty("Address", address)

        return messages

