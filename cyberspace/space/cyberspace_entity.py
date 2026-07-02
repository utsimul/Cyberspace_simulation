from abc import ABC


class CyberspaceEntity(ABC):
    """
    Base class for all cyberspace resources/entities.
    These are environmental objects that cyber personas can interact with.
    """

    def __init__(self, identifier, entity_type):

        self.identity = {
            "type": entity_type,
            "identifier": identifier
        }


        # Which personas are connected to this resource
        self.connections = {
            
        }

    