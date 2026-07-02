from cyberspace.space.cyberspace_entity import CyberspaceEntity

class SocialMediaGroup(CyberspaceEntity):
    """
    Represents a social media group or community.
    """

    def __init__(self, group_name, platform):
        super().__init__(f"{group_name}_{platform}", "social_media_group")

        self.identity.update({
            "group_name": group_name,
            "platform": platform
        })

        self.connections = {
            "admin" : None,
            "members": [],
            "mods": []
        }

        #do i need to add chat history?

    def add_member(self, persona, role):
        """
        Add a CyberPersona to the group.
        """

        if role == "admin":
            self.connections["admin"] = persona
        elif role == "mod":
            if persona not in self.connections["mods"]:
                self.connections["mods"].append(persona)
        elif role == "member":
            if persona not in self.connections["members"]:
                self.connections["members"].append(persona)
                