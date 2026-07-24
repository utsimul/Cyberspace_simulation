import json
import numpy as np


class LearnableParameters:
    """
    Stores all learnable parameters of the cyberspace simulator.
    """

    def __init__(self):

        # OCEAN: Action Weight Matrice : Shape = (num_actions, 5) Columns: O, C, E, A, N

        self.employee_action_weights = np.random.normal(0, 0.1, (2, 5))
        self.consumer_action_weights = np.random.normal(0, 0.1, (5, 5))
        self.social_action_weights = np.random.normal(0, 0.1, (3, 5))
        self.darkweb_account_action_weights = np.random.normal(0, 0.1, (3, 5))
        self.darkweb_forum_action_weights = np.random.normal(0, 0.1, (7, 5))

        # OCEAN Distributions Row 0 = Mean Row 1 = Std Columns = O,C,E,A,N

        self.employee_ocean_distribution = np.array([
            [0.60, 0.55, 0.50, 0.50, 0.45],
            [0.15, 0.15, 0.15, 0.15, 0.15]
        ])

        self.consumer_ocean_distribution = np.array([
            [0.60, 0.55, 0.50, 0.50, 0.45],
            [0.15, 0.15, 0.15, 0.15, 0.15]
        ])

        self.social_ocean_distribution = np.array([
            [0.60, 0.55, 0.50, 0.50, 0.45],
            [0.15, 0.15, 0.15, 0.15, 0.15]
        ])

        self.darkweb_ocean_distribution = np.array([
            [0.60, 0.55, 0.50, 0.50, 0.45],
            [0.15, 0.15, 0.15, 0.15, 0.15]
        ])

        # OCEAN -> IR Capability Rows = Detection, Containment, Eradication, Recovery, Learning

        self.employee_ir_weights = np.random.normal(0, 0.1, (5, 5))
        self.consumer_ir_weights = np.random.normal(0, 0.1, (5, 5))
        self.social_ir_weights = np.random.normal(0, 0.1, (5, 5))
        self.darkweb_ir_weights = np.random.normal(0, 0.1, (5, 5))

        # Network generation parameters

        self.network_parameters = np.array([
            0.8,   # same department weight
            0.6,   # hierarchy weight
            0.2,   # random connection probability
            1.2    # preferential attachment exponent
        ])


        self.attacker_parameters = {
            "attack_rate": 0.30,
            "campaign_probabilities": np.array([
                0.4,   # get access
                0.3,   # get creds
                0.2,   # turn platform into honeypot
                0.1    # collect data and observe
            ]),

            #i have to define these for personas 
            "target_selection_weights": np.array([
                2.0,   # asset value
                1.0,   # vulnerability
                0.5,   # privilege
                0.8    # activity
            ])
        }

    # Save / Load

    def save(self, filename):

        def convert(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        data = {}

        for key, value in self.__dict__.items():

            if isinstance(value, dict):
                data[key] = {
                    k: convert(v)
                    for k, v in value.items()
                }
            else:
                data[key] = convert(value)

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filename):

        obj = cls()

        with open(filename, "r") as f:
            data = json.load(f)

        for key, value in data.items():

            if isinstance(value, dict):

                new_dict = {}

                for k, v in value.items():
                    if isinstance(v, list):
                        new_dict[k] = np.array(v)
                    else:
                        new_dict[k] = v

                setattr(obj, key, new_dict)

            elif isinstance(value, list):
                setattr(obj, key, np.array(value))

            else:
                setattr(obj, key, value)

        return obj