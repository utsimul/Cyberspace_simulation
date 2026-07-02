from cyberspace.space.cyberspace_entity import CyberspaceEntity

class Db_and_credentials(CyberspaceEntity):
    """
    Represents the digital profile of a person.
    """

    def __init__(self, name, details):
        super().__init__(f"{name}", "person_profile")

        self.identity.update({
            "person_name": name,
        })

        self.connections = {}

        self.details = details  

    