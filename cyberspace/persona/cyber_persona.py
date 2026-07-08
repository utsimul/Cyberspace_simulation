from mesa import Agent


class CyberPersona(Agent):
    """
    Base class for all cyber personas.
    """

    def __init__(self, model, identifier, persona_type):
        """
        Parameters
        ----------
        model : mesa.Model
            The Mesa model this agent belongs to.
        identifier : str
            Unique identifier for the persona.
        persona_type : str
            Type/category of the persona.
        """
        super().__init__(model)

        self.identity = {
            "identifier": identifier,
            "type": persona_type
        }

        self.behavioral = {}

        self.network = {}

        self.security = {
            "access_level": "none",      # none, user, admin
            "compromised": False,
            "persistence": False,
            "discovered": False,
            "c2": False,
            "data_collected": False,
            "honeypot": False,
            "monitoring_enabled": False
        }

        self.assets = {
            "credentials": True,
            "private_messages": [],
            }
    
        self.vulnerabilities = {
            "phishing_susceptibility": 0.6,
            "weak_password": False,
            "mfa_enabled": True
        }

        # self.credentials = {}
        # self.technical = {
        #     "platform": None,
        #     "creation_date": None,
        #     "ip_history": [],
        #     "wallet_addresses": [],
        #     "associated_domains": []
        # }

        

    def step(self):
        """
        Called automatically once every simulation step.
        Should be overridden by subclasses.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement the step() method."
        )