import random

from space.dark_web_forum import DarkWebForum
from space.database_and_credentials import Db_and_credentials
from space.person_profile import PersonProfile
from space.social_media_group import SocialMediaGroup

def generate_darkweb_forums(n):
    """
    Generate dark web forums.
    """

    forum_prefixes = [
        "Market",
        "Trade",
        "Shadow",
        "Crypt",
        "Black",
        "Hidden",
        "Deep",
        "Secure"
    ]

    forums = []

    for i in range(n):

        forum_name = f"{random.choice(forum_prefixes)}_{i}"

        forum = DarkWebForum(
            forum_name=forum_name
        )

        forums.append(forum)

    return forums

def generate_databases(n, owners):
    """
    owners : list of organization accounts
    """

    database_types = [
        "CustomerDB",
        "EmployeeDB",
        "PayrollDB",
        "InventoryDB",
        "FinanceDB",
        "HRDB",
        "CRM"
    ]

    databases = []

    for i in range(n):

        owner = random.choice(owners)

        db = Db_and_credentials(
            db_name=f"{random.choice(database_types)}_{i}",
            owner=owner,
            people_w_access=[]
        )

        databases.append(db)

    return databases

def generate_person_profiles(n):

    first_names = [
        "Alice", "Bob", "Charlie", "David",
        "Emma", "Grace", "John", "Sarah",
        "Michael", "Sophia"
    ]

    last_names = [
        "Smith", "Johnson", "Brown",
        "Williams", "Jones", "Miller"
    ]

    cities = [
        "New York",
        "Chicago",
        "Seattle",
        "Boston",
        "Austin",
        "San Francisco"
    ]

    profiles = []

    for i in range(n):

        name = f"{random.choice(first_names)} {random.choice(last_names)}"

        details = {
            "email": f"user{i}@example.com",
            "phone": f"+1-555-{random.randint(1000,9999)}",
            "city": random.choice(cities)
        }

        profile = PersonProfile(
            name=name,
            details=details
        )

        profiles.append(profile)

    return profiles

def generate_social_media_groups(n):

    platforms = [
        "Facebook",
        "Reddit",
        "Discord",
        "Telegram",
        "LinkedIn"
    ]

    topics = [
        "CyberSecurity",
        "Technology",
        "Programming",
        "Gaming",
        "Finance",
        "AI",
        "Travel",
        "Photography"
    ]

    groups = []

    for i in range(n):

        group = SocialMediaGroup(
            group_name=f"{random.choice(topics)}_{i}",
            platform=random.choice(platforms)
        )

        groups.append(group)

    return groups