#later - add interactions with moderators and vendors
from persona.cyber_persona import CyberPersona
import random


class DarkWebForumOwner(CyberPersona):
    """
    Represents the owner/administrator of one or more dark web forums.
    """

    def __init__(
        self,
        identifier,
        owner_alias,
        usernames=None,
        vendors=None,
        moderators=None,
        forums_owned=None,
        behavioral=None,
    ):

        super().__init__(identifier, "Dark Web Forum Owner")

        self.identity.update({
            "owner_alias": owner_alias,
            "usernames": usernames if usernames else []
        })

        self.network = {
            "vendors": vendors if vendors else [],
            "moderators": moderators if moderators else [],
            "forums_owned": forums_owned if forums_owned else []
        }

        #I WILL FURTHER VALIDATE OR GET THESE FROM EXISTING DATA
        #I dont want to use OCEAN to model this because i dont know how much OCEAN (personality traits) can apply to a 
        #dark web forum owner. In many cases it is not even one person controlling an alias. So it might be better to use actual data.
        default_behavior = {

            # Probability of performing an action during one simulation step

            "post_probability": 0.30,
            "approve_vendor_probability": 0.10,
            "ban_vendor_probability": 0.05,
            "add_moderator_probability": 0.05,


            "moderation_strictness": 0.7,
            "security_awareness": 0.9,
            "escrow_enforced": True,
            "exit_scam_probability": 0.01
        }

        self.behavioral = default_behavior

        if behavioral:
            self.behavioral.update(behavioral)

        self.activity_data = []

    def log_activity(self, action, details=None):
        """
        Records an activity performed by the owner.
        """

        self.activity_data.append({
            "action": action,
            "details": details
        })


    def approve_vendor(self, vendor):
        self.network["vendors"].append(vendor)
        self.log_activity("Approved Vendor", {
            "vendor": getattr(vendor, "identity", vendor)
        })


    def add_moderator(self, moderator):
        self.network["moderators"].append(moderator)
        self.log_activity("Added Moderator", {
            "moderator": getattr(moderator, "identity", moderator)
        })


    def create_forum(self, forum_name):
        self.network["forums_owned"].append(forum_name)
        self.log_activity("Created Forum", {
            "forum": forum_name
        })


    def make_post(self, content):
        self.log_activity("Forum Announcement", {
            "content": content
        })


    def ban_vendor(self, vendor):
        if vendor in self.network["vendors"]:
            self.network["vendors"].remove(vendor)

        self.log_activity("Banned Vendor", {
            "vendor": getattr(vendor, "identity", vendor)
        })

    #at this point they are just recording events. but we need to ADD grass and make them modify grass (web forum)

    def do(self):
        """
        Executes one simulation step.
        """

        self.log_activity("Simulation Step Started")

        # Make a forum announcement
        if random.random() < self.behavioral["post_probability"]:
            self.make_post("General forum announcement.")

        # Approve a vendor
        if random.random() < self.behavioral["approve_vendor_probability"]:

            vendor_name = f"Vendor_{len(self.network['vendors']) + 1}"

            self.approve_vendor(vendor_name)

        # Ban a vendor
        if (
            self.network["vendors"] and
            random.random() < self.behavioral["ban_vendor_probability"]
        ):

            vendor = random.choice(self.network["vendors"])
            self.ban_vendor(vendor)

        # Recruit a moderator
        if random.random() < self.behavioral["add_moderator_probability"]:

            mod_name = f"Moderator_{len(self.network['moderators']) + 1}"

            self.add_moderator(mod_name)

        self.log_activity("Simulation Step Finished")