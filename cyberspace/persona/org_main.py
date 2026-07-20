import random

from persona.cyber_persona import CyberPersona


class OrgMain(CyberPersona):
    """
    Represents a consumer account on an organization's platform
    (e.g., Amazon, eBay, banking, streaming service, etc.).
    """

    def __init__(
        self,
        model,
        identifier,
        interests=None,
        IR_capability = None
    ):
        super().__init__(model,identifier, "Organizational Consumer")


        self.identity.update({
            "company_name": identifier,
        })


        self.network = {}
        self.IR_capability = IR_capability




    def step(self):
        """
        Execute one simulation step.

        This is intentionally kept simple for now.
        More sophisticated behavior can be added later.
        """

        self.incident_response_step()

        pass