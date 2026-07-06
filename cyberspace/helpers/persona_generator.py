import random
import numpy as np

from persona.social_media_persona import SocialMediaPersona
from persona.dark_web_acc_owner import DarkWebAccountOwner
from persona.dark_web_forum_owner import DarkWebForumOwner
from persona.organisational_consumer import OrganizationalConsumer
from persona.org_main import OrgMain
from persona.bot_persona import Bot
from persona.org_emp_persona import EmployeePersona



def sample_trait(mean=0.5, std=0.15):
    """
    Returns a value between 0 and 1.
    """
    value = np.random.normal(mean, std)
    return float(np.clip(value, 0, 1))

#assumes personality trait as a gaussian distribution.

def sample_ocean():
    return {
        "openness": sample_trait(0.60,0.15),
        "conscientiousness": sample_trait(0.55,0.15),
        "extraversion": sample_trait(0.50,0.20),
        "agreeableness": sample_trait(0.55,0.15),
        "neuroticism": sample_trait(0.45,0.20)
    }

#different persona sub types have different distributions? But i have to make them more realistic in future

def sample_social_media_ocean():

    return {
        "openness": sample_trait(0.65,0.15),
        "conscientiousness": sample_trait(0.50,0.15),
        "extraversion": sample_trait(0.65,0.18),
        "agreeableness": sample_trait(0.60,0.15),
        "neuroticism": sample_trait(0.45,0.18)
    }

def sample_darkweb_ocean():

    return {
        "openness": sample_trait(0.70,0.15),
        "conscientiousness": sample_trait(0.65,0.15),
        "extraversion": sample_trait(0.35,0.15),
        "agreeableness": sample_trait(0.30,0.15),
        "neuroticism": sample_trait(0.50,0.20)
    }

def sample_employee_ocean():

    return {
        "openness": sample_trait(0.55,0.15),
        "conscientiousness": sample_trait(0.70,0.15),
        "extraversion": sample_trait(0.50,0.15),
        "agreeableness": sample_trait(0.60,0.15),
        "neuroticism": sample_trait(0.40,0.15)
    }

def generate_social_media_personas(model,n):

    users = []

    for i in range(n):

        user = SocialMediaPersona(
            model,
            username=f"user_{i}",
            ocean_traits=sample_social_media_ocean()
        )

        users.append(user)

    return users

def generate_darkweb_users(model, n):

    users = []

    browsing = ["low","medium","high"]
    posting = ["low","medium","high"]
    risk = ["low","medium","high"]

    for i in range(n):

        user = DarkWebAccountOwner(
            model,
            identifier=f"dw_{i}",
            username=f"dark_{i}",
            browsing_frequency=random.choices(
                browsing,
                weights=[0.3,0.5,0.2]
            )[0],
            posting_frequency=random.choices(
                posting,
                weights=[0.5,0.35,0.15]
            )[0],
            risk_tolerance=random.choices(
                risk,
                weights=[0.2,0.5,0.3]
            )[0],
            ocean_traits=sample_darkweb_ocean()
        )

        users.append(user)

    return users

def generate_employees(model, n):

    employees = []

    for i in range(n):

        emp = EmployeePersona(
            model,
            employee_id=f"EMP{i:03}",
            personality=sample_employee_ocean()
        )

        employees.append(emp)

    return employees

def generate_bots(model, n): #bots dont require OCEAN so random choices.

    bots = []

    triggers = [
        "new_post",
        "keyword",
        "scheduled",
        "new_user"
    ]

    actions = [
        "post",
        "like",
        "crawl",
        "message"
    ]

    for i in range(n):

        bot = Bot(
            model,
            identifier=f"BOT{i:03}",
            bot_alias=f"bot_{i}",
            trigger_conditions=random.sample(triggers, k=2),
            action=random.choice(actions)
        )

        bots.append(bot)

    return bots

def generate_darkweb_forum_owners(model, n):
    """
    Generate Dark Web Forum Owner personas.
    """

    owners = []

    for i in range(n):

        owner = DarkWebForumOwner(
            model,
            identifier=f"DWFO{i:03}",
            owner_alias=f"admin_{i}",
            behavioral={
                "post_probability": np.random.uniform(0.2, 0.5),
                "approve_vendor_probability": np.random.uniform(0.05, 0.20),
                "ban_vendor_probability": np.random.uniform(0.02, 0.10),
                "add_moderator_probability": np.random.uniform(0.02, 0.08),
                "moderation_strictness": np.random.uniform(0.6, 1.0),
                "security_awareness": np.random.uniform(0.8, 1.0),
                "escrow_enforced": random.choices(
                    [True, False],
                    weights=[0.9, 0.1]
                )[0],
                "exit_scam_probability": np.random.uniform(0.0, 0.03)
            }
        )

        owners.append(owner)

    return owners


def generate_organizational_consumers(model, n):
    """
    Generate Organizational Consumer personas.
    """

    consumers = []

    possible_interests = [
        "technology",
        "electronics",
        "finance",
        "healthcare",
        "gaming",
        "education",
        "fashion",
        "travel"
    ]

    for i in range(n):

        identifier=f"consumer_{i}",

        transaction_probability=np.random.uniform(0.05, 0.40),

        interests=random.sample(
            possible_interests,
            k=random.randint(1, 3)
        ),

        probs = np.random.dirichlet([6, 3, 1.5, 0.5])

        usgae_behavior_probabilities={
            "browse": probs[0],
            "search": probs[1],
            "review": probs[2],
            "logout": probs[3]
        }

        consumer = OrganizationalConsumer(model,identifier, transaction_probability, interests, usgae_behavior_probabilities)

        consumers.append(consumer)

    return consumers


def generate_org_main_accounts(model, n):
    """
    Generate official organization accounts.
    """

    accounts = []

    company_types = [
        "Technology",
        "Finance",
        "Healthcare",
        "Retail",
        "Education",
        "Manufacturing"
    ]

    for i in range(n):

        account = OrgMain(
            model,
            identifier=f"Company_{i}",

            interests=random.sample(
                company_types,
                k=random.randint(1, 2)
            )
        )

        accounts.append(account)

    return accounts