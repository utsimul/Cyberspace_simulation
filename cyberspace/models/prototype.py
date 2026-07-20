from mesa import Model

from helpers.persona_generator import *
from helpers.entity_generator import *
from helpers.make_networks import *
from helpers.attacker_generator import *
from helpers.plotting import *

import random

from mesa.datacollection import DataCollector
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


class CyberSimulation(Model):

    def __init__(
        self,
        n_social=50,
        n_employees=20,
        n_consumers=30,
        n_darkweb_users=15,
        n_forum_owners=5,
        n_bots=2,
        n_social_groups=10,
        n_forums=5,
        n_databases=5,
        n_person_details=20,
        n_org_accounts=5,

        # Attackers
        n_general_attackers=10,
        n_financial_attackers=5,
        n_iabs=3,
        n_identity_thieves=5,
        n_hacktivists=3,
        n_law_enforcement=2,
        n_nation_states=1,
    ):
        super().__init__()

        self.personas = {
            "social_users": [],
            "employees": [],
            "consumers": [],
            "darkweb_users": [],
            "forum_owners": [],
            "bots": [],
            "organization_accounts": [],
        }

        self.entities = {
            "social_groups": [],
            "forums": [],
            "databases": [],
            "person_details": [],
        }

        self.attackers = {
            "general": [],
            "financial": [],
            "iab": [],
            "identity_thieves": [],
            "hacktivists": [],
            "law_enforcement": [],
            "nation_state": [],
        }

        #GENERATING INSTANCES ---------------------------------------------------------------

        self.personas["social_users"] = generate_social_media_personas(
            self, n_social
        )

        self.personas["employees"] = generate_employees(
            self, n_employees
        )

        self.personas["consumers"] = generate_organizational_consumers(
            self, n_consumers
        )

        self.personas["darkweb_users"] = generate_darkweb_users(
            self, n_darkweb_users
        )

        self.personas["forum_owners"] = generate_darkweb_forum_owners(
            self, n_forum_owners
        )

        self.personas["bots"] = generate_bots(
            self, n_bots
        )

        self.personas["organization_accounts"] = (
            generate_org_main_accounts(
                self,
                n_org_accounts,
            )
        )

        self.attackers["general"] = generate_attackers(
            self,
            n_general_attackers,
            AttackerType.GENERAL_MALICIOUS,
        )

        self.attackers["financial"] = generate_attackers(
            self,
            n_financial_attackers,
            AttackerType.FINANCIAL_CYBERCRIMINAL,
        )

        self.attackers["iab"] = generate_attackers(
            self,
            n_iabs,
            AttackerType.INITIAL_ACCESS_BROKER,
        )

        self.attackers["identity_thieves"] = generate_attackers(
            self,
            n_identity_thieves,
            AttackerType.IDENTITY_THIEF,
        )

        self.attackers["hacktivists"] = generate_attackers(
            self,
            n_hacktivists,
            AttackerType.HACKTIVIST,
        )

        self.attackers["law_enforcement"] = generate_attackers(
            self,
            n_law_enforcement,
            AttackerType.LAW_ENFORCEMENT,
        )

        self.attackers["nation_state"] = generate_attackers(
            self,
            n_nation_states,
            AttackerType.NATION_STATE,
        )

        self.entities["forums"] = generate_darkweb_forums(
            n_forums
        )

        self.entities["databases"] = generate_databases(
            n_databases,
            self.personas["organization_accounts"],
        )

        self.entities["person_details"] = generate_person_profiles(
            n_person_details
        )

        self.entities["social_groups"] = generate_social_media_groups(
            n_social_groups
        )



        print("Generated instances")

        self.assign_personas_to_entities()

        self.make_networks()

        self.add_agents()

        self.datacollector = DataCollector(
            model_reporters={

                "Normal": lambda m: m.count_ir_stage("normal"),
                "Detected": lambda m: m.count_ir_stage("detected"),
                "Contained": lambda m: m.count_ir_stage("contained"),
                "Eradicated": lambda m: m.count_ir_stage("eradicated"),
                "Recovered": lambda m: m.count_ir_stage("recovered"),

                "Compromised":
                    lambda m: sum(p.security["compromised"] for p in m.get_all_personas()),

                "Discovered":
                    lambda m: sum(p.security["discovered"] for p in m.get_all_personas()),

                "C2":
                    lambda m: sum(p.security["c2"] for p in m.get_all_personas()),

                "Persistence":
                    lambda m: sum(p.security["persistence"] for p in m.get_all_personas()),

                "DataCollected":
                    lambda m: sum(p.security["data_collected"] for p in m.get_all_personas()),

                "Monitoring":
                    lambda m: sum(p.security["monitoring_enabled"] for p in m.get_all_personas()),
            }
        )

        # collect initial state
        self.datacollector.collect(self)

        print("Simulation initialized.")
    

    def get_all_personas(self):
        """Return every cyber persona (not attackers)."""
        personas = []

        for category in self.personas.values():
            personas.extend(category)

        return personas


    def count_compromised(self):
        return sum(
            p.security["compromised"]
            for p in self.get_all_personas()
        )


    def count_ir_stage(self, stage):
        return sum(
            p.ir_state == stage
            for p in self.get_all_personas()
        )

    def add_agents(self):

        # personas
        for category in self.personas.values():
            for agent in category:
                self.agents.add(agent)

        # attackers
        for category in self.attackers.values():
            for attacker in category:
                self.agents.add(attacker)


    def assign_personas_to_entities(self):

        social_users = self.personas["social_users"]
        social_groups = self.entities["social_groups"]

        for group in social_groups:

            admin = random.choice(social_users)
            group.add_member(admin, "admin")

            possible_mods = [
                u for u in social_users
                if u != admin
            ]

            n_mods = random.randint(
                1,
                min(3, len(possible_mods)),
            )

            for mod in random.sample(
                possible_mods,
                n_mods,
            ):
                group.add_member(mod, "mod")

        for user in social_users:

            n_groups = random.randint(
                1,
                min(3, len(social_groups)),
            )

            for group in random.sample(
                social_groups,
                n_groups,
            ):
                group.add_member(user, "member")

        forums = self.entities["forums"]

        forum_owners = self.personas["forum_owners"]

        darkweb_users = self.personas["darkweb_users"]

        for forum in forums:

            owner = random.choice(forum_owners)

            forum.add_member(owner, "admin")

            n_mods = random.randint(
                1,
                min(3, len(darkweb_users)),
            )

            for mod in random.sample(
                darkweb_users,
                n_mods,
            ):
                forum.add_member(mod, "mod")

        for user in darkweb_users:

            n_forums = random.randint(
                1,
                min(3, len(forums)),
            )

            for forum in random.sample(
                forums,
                n_forums,
            ):
                forum.add_member(user, "member")

        print("Added personas to entities.")


    def make_networks(self):

        connect_social_users(
            self.personas["social_users"]
        )

        connect_forum_owners(
            self.personas["forum_owners"],
            self.entities["forums"],
        )

        connect_darkweb_users(
            self.personas["darkweb_users"],
            self.entities["forums"],
        )

        connect_employees(
            self.personas["employees"]
        )

        print("Created persona networks.")


    def step(self):

        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

sim = CyberSimulation(

    n_social=50,
    n_employees=20,
    n_consumers=30,
    n_darkweb_users=15,
    n_forum_owners=5,
    n_bots=2,

    n_general_attackers=20,
    n_financial_attackers=8,
    n_iabs=5,
    n_identity_thieves=10,
    n_hacktivists=3,
    n_law_enforcement=2,
    n_nation_states=1,
)
sim.add_agents()
sim.assign_personas_to_entities()
sim.make_networks()

# for category in sim.personas.values():

#     for agent in category:
#         print(f"Agent: {agent.__class__.__name__}, ID: {getattr(agent, 'identifier', getattr(agent, 'behavioral', 'N/A'))}")

for i in range(10):
    print(f"Step {i}")
    sim.step()
df = sim.datacollector.get_model_vars_dataframe()

print(df.head())

dashboard(df)