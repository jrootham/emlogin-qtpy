import common

class Sites(object):
    """Model for sites data """
    def __init__(self, connection):
        self.connection = connection

        self.sites = {}

        cursor = self.connection.cursor()

        for row in cursor.execute("SELECT name, endpoint, identifier FROM sites;"):
            name, endpoint, identifier = row
            self.sites[name] = (endpoint, identifier)


    def getNames(self):
        """Get the list of names for the dropdown """

        return sorted(self.sites)


    def exists(self, name):
        """Check if site name exists"""
        print ("In exists ", name)
        return name in self.sites


    def getSite(self, name):
        """Get data for a site"""

        endpoint, identifier = self.sites[name]
        return (name, endpoint, identifier)


    def addSite(self, name, endpoint, identifier):
        """Add valid new site to local sites and database sitess"""

        messages = self.addSiteValidation(name, endpoint, identifier)
        if 0 == len(messages):
            self.sites[name] = (endpoint, identifier)
            
            insert = "INSERT INTO sites (name, endpoint, identifier) VALUES (?, ?, ?);"
            cursor = self.connection.cursor()
            cursor.execute(insert, (name, endpoint, identifier))
            self.connection.commit()

            return ""
        else:
            return messages


    def updateSite(self, name, endpoint, identifier):
        """Update valid site in local sites and database sites"""

        messages = self.updateSiteValidation(name, endpoint, identifier)
        if 0 == len(messages):
            self.sites[name] = (endpoint, identifier)
            
            update = "UPDATE sites SET endpoint=?, identifier=? WHERE name=?;"
            cursor = self.connection.cursor()

            cursor.execute(update, (endpoint, identifier, name))
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


    def addSiteValidation(self, name, endpoint, identifier):
        """
        Confirm no site data is empty
        Confirm unique name for new site
        """
        messages = self.siteValidation(name, endpoint, identifier)
        messages += common.exists(name, self.sites)

        return messages


    def updateSiteValidation(self, name, endpoint, identifier):
        """
        Confirm no site data is empty
        Confirm name exists
        """
        messages = self.siteValidation(name, endpoint, identifier)
        messages += common.notExists(name, self.sites)

        return messages


    def siteValidation(self, name, endpoint, identifier):
        """Confirm no site data is empty"""
        messages = common.empty("Name", name)
        messages += common.empty("Endpoint", endpoint)
        messages += common.empty("Identifier", identifier)

        return messages

