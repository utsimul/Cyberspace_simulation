from cyberspace.space.cyberspace_entity import CyberspaceEntity

class DarkWebForum(CyberspaceEntity):
    """
    Represents a dark web forum.
    """

    def __init__(self, forum_name):
        super().__init__(f"{forum_name}", "dark_web_forum")

        self.identity.update({
            "forum_name": forum_name,
        })

        self.connections = {
            "admin" : None,
            "members": [],
            "mods": []
        }

        #do i need to add chat history for the prototype?

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
                