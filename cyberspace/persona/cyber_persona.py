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

        self.ir_state = "normal"

        self.ir_history = {
            "time_of_detection": None,
            "time_of_containment": None,
            "time_of_eradication": None,
            "time_of_recovery": None,
            "incidents_handled": 0
        }

        

        # self.credentials = {}
        # self.technical = {
        #     "platform": None,
        #     "creation_date": None,
        #     "ip_history": [],
        #     "wallet_addresses": [],
        #     "associated_domains": []
        # }

    def ir_success(self, capability_name, difficulty=0.5):
        """
        Generic probability check for an IR action.

        capability_name : key from self.ir_capability
        difficulty : attack difficulty (0-1)
        """

        capability = self.ir_capability[capability_name]

        probability = capability * (1 - difficulty)

        probability = max(0.05, min(probability, 0.98))

        return self.random.random() < probability
    
    def ir_probability(self, weights):
        """
        Computes probability of succeeding at an IR stage.

        weights:
            {
                "detection_skill": 0.6,
                "monitoring": 0.3,
                "response_speed": 0.1
            }
        """

        probability = 0

        for capability, weight in weights.items():
            probability += self.ir_capability[capability] * weight

        return max(0.01, min(probability, 0.99))
    
    def ir_attempt(self, weights):

        probability = self.ir_probability(weights)

        return self.random.random() < probability
    
    def identify_incident(self):

        if not self.security["compromised"]:
            return False

        if self.security["discovered"]:
            return True

        success = self.ir_attempt({
            "detection_skill": 0.6,
            "monitoring": 0.3,
            "response_speed": 0.1
        })

        if success:

            self.security["discovered"] = True
            self.ir_state = "identification"

        return success
    
    def contain_incident(self):

        if not self.security["discovered"]:
            return False

        success = self.ir_attempt({
            "containment": 0.6,
            "response_speed": 0.2,
            "security_knowledge": 0.2
        })

        if success:

            self.security["c2"] = False
            self.ir_state = "containment"

        return success
    
    def eradicate_incident(self):

        if self.ir_state != "containment":
            return False

        success = self.ir_attempt({
            "security_knowledge": 0.7,
            "containment": 0.3
        })

        if success:

            self.security["compromised"] = False
            self.security["persistence"] = False

            self.ir_state = "eradication"

        return success
    
    def recover_system(self):

        if self.ir_state != "eradication":
            return False

        success = self.ir_attempt({
            "recovery": 0.7,
            "response_speed": 0.3
        })

        if success:

            self.security["access_level"] = "user"

            self.ir_state = "recovery"

        return success
    
    def learn_from_incident(self):

        if self.ir_state != "recovery":
            return False

        success = self.ir_attempt({
            "security_knowledge": 0.8,
            "recovery": 0.2
        })

        if success:

            self.ir_state = "normal"

            self.ir_history["incidents_handled"] += 1

            for capability in self.ir_capability:

                self.ir_capability[capability] = min(
                    1.0,
                    self.ir_capability[capability] + 0.01
                )

            self.security["discovered"] = False

        return success

    def incident_response_step(self):

        if not self.security["compromised"]:
            return

        # ---------------- Identification ----------------

        if not self.security["discovered"]:

            probability = self.ir_probability({
                "detection_skill": 0.6,
                "monitoring": 0.3,
                "response_speed": 0.1
            })

            if self.random.random() < probability:
                self.identify_incident()

            return

        # ---------------- Containment ----------------

        if self.ir_state == "identification":

            probability = self.ir_probability({
                "containment": 0.6,
                "security_knowledge": 0.2,
                "response_speed": 0.2
            })

            if self.random.random() < probability:
                self.contain_incident()

            return

        # ---------------- Eradication ----------------

        if self.ir_state == "containment":

            probability = self.ir_probability({
                "security_knowledge": 0.7,
                "containment": 0.3
            })

            if self.random.random() < probability:
                self.eradicate_incident()

            return

        # ---------------- Recovery ----------------

        if self.ir_state == "eradication":

            probability = self.ir_probability({
                "recovery": 0.7,
                "response_speed": 0.3
            })

            if self.random.random() < probability:
                self.recover_system()

            return

        # ---------------- Learning ----------------

        if self.ir_state == "recovery":

            probability = self.ir_probability({
                "security_knowledge": 0.8,
                "recovery": 0.2
            })

            if self.random.random() < probability:
                self.learn_from_incident()

    def step(self):
        """
        Called automatically once every simulation step.
        Should be overridden by subclasses.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement the step() method."
        )

