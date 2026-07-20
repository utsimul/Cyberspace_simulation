from persona.cyber_persona import CyberPersona
from datetime import datetime
import random


class EmployeePersona(CyberPersona):
    """
    Organizational employee cyber persona.
    """

    def __init__(self, model,employee_id, personality=None, IR_capability = None):
        super().__init__(model,employee_id, "employee")

        self.identity["employeeID"] = employee_id

        self.network = {
            "bosses": [],
            "peers": [],
            "subordinates": []
        }

        self.behavioral = {
            "personality": personality
        }

        self.activity_history = []

        self.IR_capability = IR_capability


    def log_activity(self, action, target=None, details=None):
        """
        Store a record of an action performed by this employee.
        """

        self.activity_history.append({
            "timestamp": datetime.now(),
            "action": action,
            "target": target,
            "details": details
        })


    def send_message(self, receiver, message):
        """
        Simulate sending a message.
        """

        #Each activity / message is fundamentally stored as a dictionary
        self.log_activity(
            action="send_message",
            target=receiver.identity["identifier"],
            details={
                "message": message
            }
        )

    def login(self):
        """
        Simulate logging into the organization's system.
        """

        self.log_activity("login")

    def logout(self):
        """
        Simulate logging out.
        """

        self.log_activity("logout")

    def step(self):
        """
        One simulation step.
        This is only an example and should later be replaced
        by an actual behavior model.
        """

        self.incident_response_step()

        action = random.choice(["login", "logout"])

        if action == "login":
            self.login()
        else:
            self.logout()