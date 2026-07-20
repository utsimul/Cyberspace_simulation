from persona.cyber_persona import CyberPersona
import random


class DarkWebAccountOwner(CyberPersona):
    """
    Represents a dark web forum/market user.
    """

    def __init__(
        self,
        model,
        identifier,
        username,
        browsing_frequency="medium",
        posting_frequency="low",
        risk_tolerance="medium",
        ocean_traits=None,
        IR_capability = NotImplementedError
    ):
        super().__init__(model,identifier, "dark_web_account_owner")

        self.identity.update({
            "username": username
        })


        self.network = {
            # Other DarkWebAccountOwner objects
            "contacts": [],

            # Forums / marketplaces the account belongs to
            "forums_joined": [],

            # Trusted vendors the user frequently buys from
            "trusted_vendors": [],

            # Trusted buyers (if the account is a seller)
            "trusted_buyers": [],

            # Private groups/channels
            "groups": []
        }

        self.behavioral = {
            "browsing_frequency": browsing_frequency,
            "posting_frequency": posting_frequency,
            "risk_tolerance": risk_tolerance,

            # OCEAN personality traits
            "ocean": ocean_traits or {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "neuroticism": 0.5
            }
        }

        self.activity_log = []

        self.IR_capability = IR_capability 

    def log_activity(self, activity_type, details=None):
        """
        Record an activity performed by the persona.
        """
        self.activity_log.append({
            "activity": activity_type,
            "details": details or {}
        })

    #when we add "grass" (i.e. the forum itself) as a parameter to this function, then it will modify the forum's list of members
    #OR we can do that directly from the forum and that will call this join_forum function from this class.
    def add_contact(self, user):
        if user not in self.network["contacts"]:
            self.network["contacts"].append(user)

    def join_forum(self, forum):
        if forum not in self.network["forums_joined"]:
            self.network["forums_joined"].append(forum)

    def add_vendor(self, vendor):
        if vendor not in self.network["trusted_vendors"]:
            self.network["trusted_vendors"].append(vendor)

    def add_buyer(self, buyer):
        if buyer not in self.network["trusted_buyers"]:
            self.network["trusted_buyers"].append(buyer)


    def step(self):
        """
        Perform one simulation step.

        The actual behaviour (browse, post, buy, message, etc.)
        can later be driven by probabilities learned from data
        or by the OCEAN personality traits.
        """
        #right now only random - this is just to get the code running.
        #will add OCEAN or actual data based logic later

        self.incident_response_step()

        r = random.random()

        if r < 0.70:
            self.log_activity("browse")

        elif r < 0.90:
            self.log_activity("create_post")

        else:
            self.log_activity("send_message")
        
        