from abc import ABC, abstractmethod


class CyberPersona(ABC):
    """
    Base class for all cyber personas.
    """

    def __init__(self, identifier, persona_type):
        self.identity = {
            "identifier": identifier,
            "type": persona_type
        }

        #self.credentials = {}

        self.behavioral = {}

        self.network = {}

        # self.technical = {
        #     "platform": None,
        #     "creation_date": None,
        #     "ip_history": [],
        #     "wallet_addresses": [],
        #     "associated_domains": []
        # }

    @abstractmethod
    def do(self):
        """
        Define the behavior of the cyber persona for one simulation step.
        Must be implemented by all subclasses.
        """
        pass