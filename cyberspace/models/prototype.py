from mesa import Model

from helpers.persona_generator import *
from helpers.entity_generator import *
from helpers.make_networks import *

import random


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

        print("Simulation initialized.")

    #ADD AGENTS TO MODEL --------------------------------------------------------------------------------

    def add_agents(self):

        for category in self.personas.values():

            for agent in category:
                self.agents.add(agent)


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

sim = CyberSimulation(
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