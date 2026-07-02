from cyberspace.space.cyberspace_entity import CyberspaceEntity

class Db_and_credentials(CyberspaceEntity):
    """
    Represents a database and credentials.
    """

    def __init__(self, db_name, owner, people_w_access=None):
        super().__init__(f"{db_name}", "database_and_credentials")

        self.identity.update({
            "db_name": db_name,
        })

        self.connections = {
            "owner": owner,
            "users": people_w_access if people_w_access is not None else [],
            #can add more permissions but keeping it simple for now
        }

    def add_access(self, person):
        """
        Add a CyberPersona to the database.
        """

        self.connections["users"].append(person)