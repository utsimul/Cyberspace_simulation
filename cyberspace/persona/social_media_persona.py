#this just posts right now. I will add this after it runs: interacts with posts of other user. Maybe add a post class? This is for structure
#for behavior i will make OCEAN correspond to probabilities of actions? more complex rules 
#OR
#i can use existing data (im inclining towards this but we'll see)

import random
from persona.cyber_persona import CyberPersona


class SocialMediaPersona(CyberPersona):

    def __init__(self, username, ocean_traits=None):
        super().__init__(username, "Social Media")

        self.network = {
            "followers": [],
            "following": []
        }

        # OCEAN personality traits
        self.behavioral = ocean_traits or {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }

        # Account history
        self.posts = []

        self.topics = [
            "technology",
            "sports",
            "food",
            "travel",
            "politics"
        ]

        self.sentiments = [
            "positive",
            "neutral",
            "negative"
        ]

    def should_post(self):
        """
        Probability of posting.
        More extraverted users post more frequently.
        """
        p = 0.1 + 0.5 * self.behavioral["extraversion"] #can be tweaked. again, we don't know whether an actual person with 
        #x level of extraversion posts with 0.1 + 0.5x frequency - but x can be scaled such that both correspond?
        return random.random() < p

    def create_post(self):

        topic = random.choice(self.topics)
        sentiment = random.choice(self.sentiments)

        post = {
            "topic": topic,
            "sentiment": sentiment,
            "content": f"A {sentiment} post about {topic}"
        }

        self.posts.append(post)

    def do(self):

        if self.should_post():
            self.create_post()