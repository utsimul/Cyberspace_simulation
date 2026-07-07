from attackers.attacker import *
import random


def generate_attackers(model, n, attacker_type):

    attackers = []

    for i in range(n):

        attacker = Attacker(
            model=model,
            unique_id=f"{attacker_type.name}_{i}",
            attacker_type=attacker_type,

            skill_level=random.uniform(0.3, 1.0),
            resources=random.uniform(0.3, 1.0),
            stealth=random.uniform(0.3, 1.0),
            risk_tolerance=random.uniform(0.2, 1.0),
        )

        attackers.append(attacker)

    return attackers