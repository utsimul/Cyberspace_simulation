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
            ocean_traits=sample_social_media_ocean(),
            IR_capability=sample_social_media_ir()
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
            ocean_traits=sample_darkweb_ocean(),
            IR_capability=sample_darkweb_ir()
        )

        users.append(user)

    return users

def generate_employees(model, n):

    employees = []

    for i in range(n):

        emp = EmployeePersona(
            model,
            employee_id=f"EMP{i:03}",
            personality=sample_employee_ocean(),
            IR_capability=sample_employee_ir()
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
            },
            IR_capability=sample_darkweb_ir()
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

        IR_capability = sample_consumer_ir()

        consumer = OrganizationalConsumer(model,identifier, transaction_probability, interests, usgae_behavior_probabilities, IR_capability)

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
            ),
            IR_capability=sample_org_account_ir()
        )

        accounts.append(account)

    return accounts


def sample_ir_capability(
    monitoring_mean=0.5,
    detection_mean=0.5,
    reporting_mean=0.5,
    containment_mean=0.5,
    recovery_mean=0.5,
    knowledge_mean=0.5,
    speed_mean=0.5,
):
    """
    Sample Incident Response capability profile.
    All values are between 0 and 1.
    """

    return {
        "monitoring": sample_trait(monitoring_mean, 0.15),
        "detection_skill": sample_trait(detection_mean, 0.15),
        "reporting": sample_trait(reporting_mean, 0.15),
        "containment": sample_trait(containment_mean, 0.15),
        "recovery": sample_trait(recovery_mean, 0.15),
        "security_knowledge": sample_trait(knowledge_mean, 0.15),
        "response_speed": sample_trait(speed_mean, 0.15),
    }

def sample_social_media_ir():

    return sample_ir_capability(
        monitoring_mean=0.40,
        detection_mean=0.45,
        reporting_mean=0.35,
        containment_mean=0.35,
        recovery_mean=0.40,
        knowledge_mean=0.40,
        speed_mean=0.45,
    )

def sample_employee_ir():

    return sample_ir_capability(
        monitoring_mean=0.65,
        detection_mean=0.65,
        reporting_mean=0.80,
        containment_mean=0.60,
        recovery_mean=0.55,
        knowledge_mean=0.70,
        speed_mean=0.70,
    )

def sample_darkweb_ir():

    return sample_ir_capability(
        monitoring_mean=0.70,
        detection_mean=0.75,
        reporting_mean=0.15,
        containment_mean=0.75,
        recovery_mean=0.70,
        knowledge_mean=0.80,
        speed_mean=0.75,
    )

def sample_forum_owner_ir():

    return sample_ir_capability(
        monitoring_mean=0.85,
        detection_mean=0.85,
        reporting_mean=0.20,
        containment_mean=0.90,
        recovery_mean=0.80,
        knowledge_mean=0.90,
        speed_mean=0.85,
    )

def sample_consumer_ir():

    return sample_ir_capability(
        monitoring_mean=0.45,
        detection_mean=0.45,
        reporting_mean=0.40,
        containment_mean=0.40,
        recovery_mean=0.45,
        knowledge_mean=0.45,
        speed_mean=0.45,
    )

def sample_org_account_ir():

    return sample_ir_capability(
        monitoring_mean=0.90,
        detection_mean=0.85,
        reporting_mean=0.90,
        containment_mean=0.85,
        recovery_mean=0.80,
        knowledge_mean=0.85,
        speed_mean=0.85,
    )

