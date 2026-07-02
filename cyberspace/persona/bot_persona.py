from cyber_persona import CyberPersona


class Bot(CyberPersona):
    """
    Represents an automated bot account (e.g., Reddit bot, Discord bot).
    Bots are publicly identifiable as automated accounts.
    """

    def __init__(
        self,
        identifier,
        bot_alias,
        trigger_conditions=None,
        action=None,
        activity_data=None,
    ):
        super().__init__(identifier, "Bot")


        self.identity.update({
            "bot_alias": bot_alias
        })


        self.network = {}

        self.behavioral.update({
            "trigger_conditions": trigger_conditions if trigger_conditions is not None else [],
            "action": action
        })

        self.activity_data = activity_data if activity_data is not None else []

    def log_activity(self, activity):
        """
        Record an activity performed by the bot.
        """
        self.activity_data.append(activity)

    def do(self, event=None):
        """
        Executes the bot's action if one of its trigger conditions is met.

        Parameters
        ----------
        event : str, optional
            The event occurring during the current simulation step.
        """

        if event in self.behavioral["trigger_conditions"]:
            activity = {
                "event": event,
                "action": self.behavioral["action"]
            }

            self.log_activity(activity)

            return activity

        return None