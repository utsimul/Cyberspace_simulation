from mesa import Agent
from enum import Enum, auto
import random
import json
from pathlib import Path

BEHAVIOR_FILE = (
    Path(__file__).parent / "attacker_behavior.json"
)

with open(BEHAVIOR_FILE, "r") as f:
    ATTACK_LIBRARY = json.load(f)



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

    ATTACKER_ATTACKS = {

        AttackerType.GENERAL_MALICIOUS: [
            "Get access",
            "Get credentials"
        ],

        AttackerType.FINANCIAL_CYBERCRIMINAL: [
            "Get credentials",
            "Get access"
        ],

        AttackerType.INITIAL_ACCESS_BROKER: [
            "Get access"
        ],

        AttackerType.IDENTITY_THIEF: [
            "Get credentials"
        ],

        AttackerType.HACKTIVIST: [
            "Get access"
        ],

        AttackerType.LAW_ENFORCEMENT: [
            "Turn platform into honeypot",
            "Collect data and observe"
        ],

        AttackerType.NATION_STATE: [
            "Get access",
            "Get credentials",
            "Collect data and observe"
        ]

    }

    TARGET_PERSONAS = {

        AttackerType.GENERAL_MALICIOUS: [
            "social_users",
            "employees",
            "consumers",
            "darkweb_users",
            "organization_accounts",
        ],

        AttackerType.FINANCIAL_CYBERCRIMINAL: [
            "employees",
            "consumers",
            "organization_accounts",
        ],

        AttackerType.INITIAL_ACCESS_BROKER: [
            "employees",
            "organization_accounts",
        ],

        AttackerType.IDENTITY_THIEF: [
            "social_users",
            "consumers",
            "employees",
        ],

        AttackerType.HACKTIVIST: [
            "organization_accounts",
            "forum_owners",
            "social_users",
        ],

        AttackerType.LAW_ENFORCEMENT: [
            "darkweb_users",
            "forum_owners",
        ],

        AttackerType.NATION_STATE: [
            "employees",
            "organization_accounts",
            "forum_owners",
            "darkweb_users",
        ],

    }

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

    def choose_attack(self):
        #right now this is random but we will make this more realistic

        attacks = self.ATTACKER_ATTACKS[self.attacker_type]

        self.current_campaign = random.choice(attacks)

        return self.current_campaign

    def choose_target(self):
        """
        Randomly select a valid target persona. We will make this more realistic later. 
        """

        allowed_categories = self.TARGET_PERSONAS[self.attacker_type]

        candidates = []

        for category in allowed_categories:
            candidates.extend(self.model.personas[category])

        if not candidates:
            self.current_target = None
            return None

        #
        # Avoid attacking already-compromised targets
        #

        available = [
            p for p in candidates
            if p not in self.compromised_targets 
            #here the attacker can attack a persona that is already compromised by another attacker. 
            #because it is self.compromised_targets not model.compromised_targets. 
        ]

        if available:
            candidates = available

        self.current_target = random.choice(candidates)

        return self.current_target


    def _apply_effect(self, persona, effect):

        target = effect["param"]
        operation = effect["operation"]
        value = effect["value"]

        # attacker attribute
        if target.startswith("attacker."):

            attr = target.split(".", 1)[1]

            if not hasattr(self, attr):
                setattr(self, attr, [])

            current = getattr(self, attr)

            if operation == "set":
                setattr(self, attr, value)

            elif operation == "append":
                current.append(value)

            return

        # persona attribute

        if not hasattr(persona, target):

            setattr(persona, target, None)

        if operation == "set":

            setattr(persona, target, value)

        elif operation == "append":

            current = getattr(persona, target)

            if current is None:

                current = []

            current.append(value)

            setattr(persona, target, current)
    
    def execute_stage(self, persona, stage_name):

        attack = ATTACK_LIBRARY[self.current_campaign]

        if stage_name not in attack:

            return

        stage = attack[stage_name]

        effects = stage.get("effects", [])

        for effect in effects:

            self._apply_effect(persona, effect)
    
    def execute_attack(self, persona):

        if self.current_campaign is None:

            self.choose_attack()

        attack = ATTACK_LIBRARY[self.current_campaign]

        stages = [

            "recon",
            "discovery",
            "initial_access",
            "persistence",
            "privilege_escalation",
            "credential_access",
            "collection",
            "command_and_control",
            "actions_on_objectives"

        ]

        for stage in stages:

            if stage in attack:

                self.execute_stage(persona, stage)

        self.successful_attacks += 1

    def step(self):
        """
        Called once per simulation step.
        """

        target = self.choose_target()
        self.execute_attack(target)
        print(f"Attacker {self.unique_id} executed {self.current_campaign} on {target.identity['identifier'] if target else 'None'}")