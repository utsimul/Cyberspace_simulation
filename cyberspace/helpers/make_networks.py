import random

def connect_social_users(users, min_follow=2, max_follow=10):

    for user in users:

        user.network.setdefault("followers", [])
        user.network.setdefault("following", [])

    for user in users:

        n = random.randint(
            min_follow,
            min(max_follow, len(users) - 1)
        )

        possible = [u for u in users if u != user]

        for other in random.sample(possible, n):

            if other not in user.network["following"]:
                user.network["following"].append(other)

            if user not in other.network["followers"]:
                other.network["followers"].append(user)

def connect_forum_owners(owners, forums):

    for owner in owners:

        owner.network.setdefault("vendors", [])
        owner.network.setdefault("moderators", [])
        owner.network.setdefault("forums_owned", [])


    for forum in forums:

        owner = forum.connections["admin"]

        if forum not in owner.network["forums_owned"]:
            owner.network["forums_owned"].append(forum)



    for owner in owners:

        possible = [o for o in owners if o != owner]

        if possible:

            n = random.randint(1, min(3, len(possible)))

            owner.network["vendors"] = random.sample(possible, n)


    for forum in forums:

        owner = forum.connections["admin"]

        for mod in forum.connections["mods"]:

            if mod not in owner.network["moderators"]:
                owner.network["moderators"].append(mod)

def connect_darkweb_users(users, forums):

    for user in users:

        user.network.setdefault("forums", [])
        user.network.setdefault("vendors", [])
        user.network.setdefault("buyers", [])


    for forum in forums:

        members = (
            forum.connections["members"] +
            forum.connections["mods"]
        )

        for member in members:

            if forum not in member.network["forums"]:
                member.network["forums"].append(forum)


    for buyer in users:

        possible = [u for u in users if u != buyer]

        if not possible:
            continue

        n = random.randint(1, min(3, len(possible)))

        vendors = random.sample(possible, n)

        for vendor in vendors:

            if vendor not in buyer.network["vendors"]:
                buyer.network["vendors"].append(vendor)

            if buyer not in vendor.network["buyers"]:
                vendor.network["buyers"].append(buyer)


def connect_employees(employees):

    for emp in employees:

        emp.network.setdefault("bosses", [])
        emp.network.setdefault("subordinates", [])
        emp.network.setdefault("peers", [])

    if len(employees) <= 1:
        return

    ceo = employees[0]


    for employee in employees[1:]:

        possible_bosses = employees[:employees.index(employee)]

        boss = random.choice(possible_bosses)

        employee.network["bosses"].append(boss)
        boss.network["subordinates"].append(employee)


    for boss in employees:

        team = boss.network["subordinates"]

        for member in team:

            member.network["peers"] = [
                x for x in team if x != member
            ]

def add_connection(persona, key, other):

    persona.network.setdefault(key, [])

    if other not in persona.network[key]:
        persona.network[key].append(other)


# add_connection(a, "following", b)
# add_connection(b, "followers", a)

# add_connection(employee, "bosses", boss)
# add_connection(boss, "subordinates", employee)

# add_connection(vendor, "buyers", buyer)
# add_connection(buyer, "vendors", vendor)