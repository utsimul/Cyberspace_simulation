import random

from persona.cyber_persona import CyberPersona


class OrganizationalConsumer(CyberPersona):
    """
    Represents a consumer account on an organization's platform
    (e.g., Amazon, eBay, banking, streaming service, etc.).
    """

    def __init__(
        self,
        model,
        identifier,
        transaction_probability=0.1,
        interests=None,
        usage_behavior_probabilities=None,
        IR_capability = None
    ):
        super().__init__(model,identifier, "Organizational Consumer")


        self.identity.update({
            "username": identifier,
        })


        self.network = {}


        self.behavioral.update({
            "transaction_probability": transaction_probability,
            "interests": interests if interests is not None else [],
            "usage_behavior_probabilities": (
                usage_behavior_probabilities
                if usage_behavior_probabilities is not None
                else {
                    "browse": 0.60,
                    "search": 0.25,
                    "review": 0.10,
                    "logout": 0.05,
                }
            )
        })

        #have to make this more accurate (OCEAN or existing consumer data)

        self.activity_data = {
            "transaction_history": [],
            "usage_history": [],
        }

        self.IR_capability = IR_capability

    def step(self):
        """
        Execute one simulation step.

        This is intentionally kept simple for now.
        More sophisticated behavior can be added later.
        """

        self.incident_response_step()

        if random.random() < self.behavioral["transaction_probability"][0]:
            self.activity_data["transaction_history"].append(
                {
                    "event": "transaction"
                }
            )

        actions = list(self.behavioral["usage_behavior_probabilities"].keys())
        probabilities = list(
            self.behavioral["usage_behavior_probabilities"].values()
        )

        action = random.choices(actions, weights=probabilities, k=1)[0]

        self.activity_data["usage_history"].append(
            {
                "event": action
            }
        )