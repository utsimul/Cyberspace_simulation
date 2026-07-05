from space.cyberspace_entity import CyberspaceEntity

class PersonProfile(CyberspaceEntity):
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

    