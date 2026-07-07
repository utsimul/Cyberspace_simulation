from mesa import Agent
from enum import Enum, auto
import random


class AttackerType(Enum):
    """High-level categories of attackers."""

    GENERAL_MALICIOUS = auto()
    FINANCIAL_CYBERCRIMINAL = auto()
    INITIAL_ACCESS_BROKER = auto()
    IDENTITY_THIEF = auto()
    HACKTIVIST = auto()
    LAW_ENFORCEMENT = auto()
    NATION_STATE = auto()


class AttackStage(Enum):
    """Current stage of the attack lifecycle."""

    RECONNAISSANCE = auto()
    INITIAL_ACCESS = auto()
    PERSISTENCE = auto()
    PRIVILEGE_ESCALATION = auto()
    OBJECTIVE = auto()
    FINISHED = auto()


class CampaignType(Enum):
    """Current campaign or objective."""

    DATA_THEFT = auto()
    PHISHING = auto()
    RANSOMWARE = auto()
    ACCOUNT_HIJACKING = auto()
    DDOS = auto()
    ESPIONAGE = auto()
    FINANCIAL_FRAUD = auto()
    CREDENTIAL_THEFT = auto()


class Attacker(Agent):
    """
    Generic attacker agent.

    Each instance represents one attacker (or attacker group) in the
    simulation.
    """

    def __init__(
        self,
        model,
        unique_id,
        attacker_type: AttackerType,
        skill_level=None,
        resources=None,
        stealth=None,
        risk_tolerance=None,
    ):
        super().__init__(model)

        self.unique_id = unique_id
        self.attacker_type = attacker_type

        self.skill_level = (
            skill_level if skill_level is not None
            else random.uniform(0.3, 1.0)
        )

        self.resources = (
            resources if resources is not None
            else random.uniform(0.3, 1.0)
        )

        self.stealth = (
            stealth if stealth is not None
            else random.uniform(0.3, 1.0)
        )

        self.risk_tolerance = (
            risk_tolerance if risk_tolerance is not None
            else random.uniform(0.2, 1.0)
        )

        self.known_targets = []
        self.compromised_targets = []

        self.current_target = None
        self.current_campaign = None
        self.current_stage = AttackStage.RECONNAISSANCE

        self.capabilities = []

        self.objectives = []

        self.successful_attacks = 0
        self.failed_attacks = 0
        self.detected = False

        self._initialize_profile()

    def _initialize_profile(self):
        """Assign default objectives and capabilities."""

        if self.attacker_type == AttackerType.GENERAL_MALICIOUS:

            self.objectives = [
                "Extortion",
                "Revenge",
                "Disruption"
            ]

            self.capabilities = [
                "Phishing",
                "Malware",
                "Credential Theft",
                "DDoS"
            ]

        elif self.attacker_type == AttackerType.FINANCIAL_CYBERCRIMINAL:

            self.objectives = [
                "Financial Gain"
            ]

            self.capabilities = [
                "Business Email Compromise",
                "Credential Theft",
                "Wire Fraud",
                "Banking Malware"
            ]

        elif self.attacker_type == AttackerType.INITIAL_ACCESS_BROKER:

            self.objectives = [
                "Sell Access"
            ]

            self.capabilities = [
                "Credential Theft",
                "Phishing",
                "Persistence"
            ]

        elif self.attacker_type == AttackerType.IDENTITY_THIEF:

            self.objectives = [
                "Identity Theft",
                "Fraud"
            ]

            self.capabilities = [
                "Social Engineering",
                "Credential Theft",
                "Impersonation"
            ]

        elif self.attacker_type == AttackerType.HACKTIVIST:

            self.objectives = [
                "Publicity",
                "Ideological Impact"
            ]

            self.capabilities = [
                "Website Defacement",
                "DDoS",
                "Data Leak"
            ]

        elif self.attacker_type == AttackerType.LAW_ENFORCEMENT:

            self.objectives = [
                "Evidence Collection",
                "Platform Takedown"
            ]

            self.capabilities = [
                "Undercover Operation",
                "Digital Forensics",
                "Server Seizure"
            ]

        elif self.attacker_type == AttackerType.NATION_STATE:

            self.objectives = [
                "Espionage",
                "Intelligence Collection"
            ]

            self.capabilities = [
                "Advanced Malware",
                "Zero-Day Exploitation",
                "Persistence",
                "Stealth Operations"
            ]

    def choose_target(self):
        """Placeholder for target selection logic."""
        pass

    def choose_campaign(self):
        """Placeholder for campaign selection."""
        pass

    def execute_attack(self):
        """Placeholder for attack execution."""
        pass

    def update_stage(self):
        """Placeholder for attack lifecycle progression."""
        pass

    def step(self):
        """
        Called once per simulation step.
        """

        self.choose_target()
        self.choose_campaign()
        self.execute_attack()
        self.update_stage()