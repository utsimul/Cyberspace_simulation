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

print("done")