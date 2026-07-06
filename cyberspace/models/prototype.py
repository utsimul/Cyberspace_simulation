from persona.bot_persona import Bot
from persona.social_media_persona import SocialMediaPersona
from persona.dark_web_acc_owner import DarkWebAccountOwner
from persona.dark_web_forum_owner import DarkWebForumOwner
from persona.organisational_consumer import OrganizationalConsumer
from persona.org_main import OrgMain

from space.dark_web_forum import DarkWebForum
from space.database_and_credentials import Db_and_credentials
from space.person_profile import PersonProfile
from space.social_media_group import SocialMediaGroup

from helpers.persona_generator import *
from helpers.entity_generator import *
from helpers.make_networks import *

import random

personas = {
    "social_users": [],
    "employees": [],
    "consumers": [],
    "darkweb_users": [],
    "forum_owners": [],
    "bots": []
}

entities = {
    "social_groups": [],
    "forums": [],
    "databases": [],
    "person_details": []
}

n_social = 50
n_employees = 20
n_consumers = 30
n_darkweb_users = 15
n_forum_owners = 5
n_bots = 2

n_social_groups = 10
n_forums = 5
n_databases = 5
n_person_details = 20
n_org_accounts = 5


#GENEARTING INSTANCES --------------------------------------------------------------------------------

personas["social_users"] = generate_social_media_personas(n_social)
personas["employees"] = generate_employees(n_employees)
personas["consumers"] = generate_organizational_consumers(n_consumers)
personas["darkweb_users"] = generate_darkweb_users(n_darkweb_users)
personas["forum_owners"] = generate_darkweb_forum_owners(n_forum_owners)
personas["bots"] = generate_bots(n_bots)

entities["forums"] = generate_darkweb_forums(n_forums)

personas["organization_accounts"] = generate_org_main_accounts(n_org_accounts)

entities["databases"] = generate_databases(
    n_databases,
    personas["organization_accounts"]
)

entities["person_details"] = generate_person_profiles(n_person_details)

entities["social_groups"] = generate_social_media_groups(n_social_groups)

print("generated instances")

#ADDING PERSONAS TO ENTITIES --------------------------------------------------------------------------------


social_users = personas["social_users"]
social_groups = entities["social_groups"]

for group in social_groups:

    #i am radnomly adding mods and admins

    admin = random.choice(social_users)
    group.add_member(admin, "admin")

    possible_mods = [u for u in social_users if u != admin]
    n_mods = random.randint(1, min(3, len(possible_mods)))

    for mod in random.sample(possible_mods, n_mods):
        group.add_member(mod, "mod")


# Every user joins 1-3 random groups
for user in social_users:

    n_groups = random.randint(1, min(3, len(social_groups)))

    for group in random.sample(social_groups, n_groups):
        group.add_member(user, "member")


forums = entities["forums"]
forum_owners = personas["forum_owners"]
darkweb_users = personas["darkweb_users"]

for forum in forums:

    owner = random.choice(forum_owners)
    forum.add_member(owner, "admin")

    n_mods = random.randint(1, min(3, len(darkweb_users)))

    for mod in random.sample(darkweb_users, n_mods):
        forum.add_member(mod, "mod")


# Every dark web user joins 1-3 forums
for user in darkweb_users:

    n_forums = random.randint(1, min(3, len(forums)))

    for forum in random.sample(forums, n_forums):
        forum.add_member(user, "member")

print("added personas to entities")
for group in social_groups:
    print(f"Group: {group.identity['group_name']}, Admin: {group.connections['admin'].identity['username']}, Members: {[member.identity['username'] for member in group.connections['members']]}, Mods: {[mod.identity['username'] for mod in group.connections['mods']]}")


# MAKING CONNECTIONS AMONG PERSONAS ---------------------------------------------------------------


# Social media follower/following network
connect_social_users(personas["social_users"])

# Dark web forum owners (forums owned, vendors, moderators)
connect_forum_owners(
    personas["forum_owners"],
    entities["forums"]
)

# Dark web account owners (forums joined, vendors, buyers)
connect_darkweb_users(
    personas["darkweb_users"],
    entities["forums"]
)

# Organizational hierarchy (bosses, peers, subordinates)
connect_employees(personas["employees"])

print("created persona networks")

print("Social Media Users:")
# for user in personas["social_users"]:
#     print(f"User: {user.identity['username']}, Followers: {[follower.identity['username'] for follower in user.network['followers']]}, Following: {[following.identity['username'] for following in user.network['following']]}")

#CALLING THE DO FUNCTIONS OF ALL INSTANCES --------------------------------------------------------------------------------

