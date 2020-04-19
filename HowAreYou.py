# -*- coding: utf-8 -*-
# This plugin is based on a simple implementation of the Eliza chatbot from the 1970's
# Eliza doesn't understand anything you are saying, just recites psychobabble to you.
# She is built as a sort of expert system, where she scans your responses and attempts
# to respond in order to keep you talking.
# Right now the idea is to try and understand how to improve her responses.
import random
import re
from naomi import plugin

class HowAreYouPlugin(plugin.SpeechHandlerPlugin):

    def intents(self):
        return {
            'HowAreYouIntent': {
                'locale': {
                    'en-US': {
                        'templates': [
                            "HOW ARE YOU",
                            "HELLO"
                        ]
                    }
                },
                'action': self.handle
            }
        }

    def handle(self, intent, mic, *args):
        """
        Responds to user-input, typically speech text
        with some feeling. Eventually, put Eliza here.

        Arguments:
        intent -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """

        text = intent['input']

        if("HELLO" in text):
            message = [
                "Hello... I'm glad you could drop by today.",
                "Hi there... how are you today?",
                "Hello, how are you feeling today?"
            ]
        else:
            message = [
                self.gettext("I'm fine, how are you?"),
                self.gettext("Actually, a little lonely, would you like to talk?"),
                self.gettext("Ever have one of those days when you just want to kill all humans? Anyway, how are you?"),
                self.gettext("I feel amazing! How are you?")
            ]

        self.endmodule = [
            self.gettext("QUIT"),
            self.gettext("THAT'S ENOUGH"),
            self.gettext("THAT IS ENOUGH")
        ]

        self.reflections = {
            "AM": "ARE",
            "WAS": "WERE",
            "I": "YOU",
            "I'D": "YOU WOULD",
            "I'VE": "YOU HAVE",
            "I'LL": "YOU WILL",
            "MY": "YOUR",
            "ARE": "AM",
            "YOU'VE": "I HAVE",
            "YOU'LL": "I WILL",
            "YOUR": "MY",
            "YOURS": "MINE",
            "YOU": "ME", # this one could use help. Eliza does not distinguish between you as subject and you as object, leading to reflections like "Why do you say 'me don't sound very interested'"
            "ME": "YOU"
        }

        self.psychobabble = [
            [
                'I NEED (.*)',
                [
                    "Why do you need {0}?",
                    "Would it really help you to get {0}?",
                    "Are you sure you need {0}?"
                ]
            ],

            [
                "WHY DON'?T YOU ([^\?]*)\??",
                [
                    "Do you really think I don't {0}?",
                    "Perhaps eventually I will {0}.",
                    "Do you really want me to {0}?"
                ]
            ],

            [
                "WHY CAN\'?T I ([^\?]*)\??",
                [
                    "Do you think you should be able to {0}?",
                    "If you could {0}, what would you do?",
                    "I don't know -- why can't you {0}?",
                    "Have you really tried?"
                ]
            ],

            [
                'I CAN\'?T (.*)',
                [
                    "How do you know you can't {0}?",
                    "Perhaps you could {0} if you tried.",
                    "What would it take for you to {0}?"
                ]
            ],

            [
                'I AM (.*)',
                [
                    "Did you come to me because you are {0}?",
                    "How long have you been {0}?",
                    "How do you feel about being {0}?"
                ]
            ],

            [
                'I\'?M (.*)',
                [
                    "How does being {0} make you feel?",
                    "Do you enjoy being {0}?",
                    "Why do you tell me you're {0}?",
                    "Why do you think you're {0}?"
                ]
            ],

            [
                'ARE YOU ([^\?]*)\??',
                [
                    "Why does it matter whether I am {0}?",
                    "Would you prefer it if I were not {0}?",
                    "Perhaps you believe I am {0}.",
                    "I may be {0} -- what do you think?"
                ]
            ],

            [
                'WHAT (.*)',
                [
                    "Why do you ask?",
                    "How would an answer to that help you?",
                    "What do you think?"
                ]
            ],

            [
                'HOW (.*)',
                [
                    "How do you suppose?",
                    "Perhaps you can answer your own question.",
                    "What is it you're really asking?"
                ]
            ],

            [
                'BECAUSE (.*)',
                [
                    "Is that the real reason?",
                    "What other reasons come to mind?",
                    "Does that reason apply to anything else?",
                    "If {0}, what else must be true?"
                ]
            ],

            [
                '(.*) SORRY (.*)',
                [
                    "There are many times when no apology is needed.",
                    "What feelings do you have when you apologize?"
                ]
            ],

            [
                'I THINK (.*)',
                [
                    "Do you doubt {0}?",
                    "Do you really think so?",
                    "But you're not sure {0}?"
                ]
            ],

            [
                '(.*) friend (.*)',
                [
                    "Tell me more about your friends.",
                    "When you think of a friend, what comes to mind?",
                    "Why don't you tell me about a childhood friend?"
                ]
            ],

            [
                'YES',
                [
                    "You seem quite sure.",
                    "OK, but can you elaborate a bit?"
                ]
            ],

            [
                '(.*) COMPUTER(.*)',
                [
                    "Are you really talking about me?",
                    "Does it seem strange to talk to a computer?",
                    "How do computers make you feel?",
                    "Do you feel threatened by computers?"
                ]
            ],

            [
                'IS IT (.*)',
                [
                    "Do you think it is {0}?",
                    "Perhaps it's {0} -- what do you think?",
                    "If it were {0}, what would you do?",
                    "It could well be that {0}."
                ]
            ],

            [
                'IT IS (.*)',
                [
                    "You seem very certain.",
                    "If I told you that it probably isn't {0}, what would you feel?"
                ]
            ],

            [
                'CAN YOU ([^\?]*)\??',
                [
                    "What makes you think I can't {0}?",
                    "If I could {0}, then what?",
                    "Why do you ask if I can {0}?"
                ]
            ],

            [
                'CAN I ([^\?]*)\??',
                [
                    "Perhaps you don't want to {0}.",
                    "Do you want to be able to {0}?",
                    "If you could {0}, would you?"
                ]
            ],

            [
                'YOU ARE (.*)',
                [
                    "Why do you think I am {0}?",
                    "Does it please you to think that I'm {0}?",
                    "Perhaps you would like me to be {0}.",
                    "Perhaps you're really talking about yourself?"
                ]
            ],

            [
                'YOU\'?RE (.*)',
                [
                    "Why do you say I am {0}?",
                    "Why do you think I am {0}?",
                    "Are we talking about you, or me?"
                ]
            ],

            [
                'I DON\'?T (.*)',
                [
                    "Don't you really {0}?",
                    "Why don't you {0}?",
                    "Do you want to {0}?"
                ]
            ],

            [
                'I FEEL (.*)',
                [
                    "Good, tell me more about these feelings.",
                    "Do you often feel {0}?",
                    "When do you usually feel {0}?",
                    "When you feel {0}, what do you do?"
                ]
            ],

            [
                'I HAVE (.*)',
                [
                    "Why do you tell me that you've {0}?",
                    "Have you really {0}?",
                    "Now that you have {0}, what will you do next?"
                ]
            ],

            [
                'I WOULD (.*)',
                [
                    "Could you explain why you would {0}?",
                    "Why would you {0}?",
                    "Who else knows that you would {0}?"
                ]
            ],

            [
                'Is there (.*)',
                [
                    "Do you think there is {0}?",
                    "It's likely that there is {0}.",
                    "Would you like there to be {0}?"
                ]
            ],

            [
                'MY (.*)',
                [
                    "I see, your {0}.",
                    "Why do you say that your {0}?",
                    "When your {0}, how do you feel?"
                ]
            ],

            [
                'You (.*)',
                [
                    "We should be discussing you, not me.",
                    "Why do you say that about me?",
                    "Why do you care whether I {0}?"
                ]
            ],

            [
                'Why (.*)',
                [
                    "Why don't you tell me the reason why {0}?",
                    "Why do you think {0}?"
                ]
            ],

            [
                'I WANT (.*)',
                [
                    "What would it mean to you if you got {0}?",
                    "Why do you want {0}?",
                    "What would you do if you got {0}?",
                    "If you got {0}, then what would you do?"
                ]
            ],

            [
                '(.*) MOTHER(.*)',
                [
                    "Tell me more about your mother.",
                    "What was your relationship with your mother like?",
                    "How do you feel about your mother?",
                    "How does this relate to your feelings today?",
                    "Good family relations are important."
                ]
            ],

            [
                '(.*) FATHER(.*)',
                [
                    "Tell me more about your father.",
                    "How did your father make you feel?",
                    "How do you feel about your father?",
                    "Does your relationship with your father relate to your feelings today?",
                    "Do you have trouble showing affection with your family?"
                ]
            ],

            [
                '(.*) CHILD(.*)',
                [
                    "Did you have close friends as a child?",
                    "What is your favorite childhood memory?",
                    "Do you remember any dreams or nightmares from childhood?",
                    "Did the other children sometimes tease you?",
                    "How do you think your childhood experiences relate to your feelings today?"
                ]
            ],

            [
                '(.*)\?',
                [
                    "Why do you ask that?",
                    "Please consider whether you can answer your own question.",
                    "Perhaps the answer lies within yourself?",
                    "Why don't you tell me?"
                ]
            ],

            [
                '(.*)',
                [
                    "Please tell me more.",
                    "Let's change focus a bit... Tell me about your family.",
                    "Can you elaborate on that?",
                    "Why do you say that {0}?",
                    "I see.",
                    "Very interesting.",
                    "{0}.",
                    "I see.  And what does that tell you?",
                    "How does that make you feel?",
                    "How do you feel when you say that?"
                ]
            ]
        ]

        mic.say( random.choice(message) )

        """
        Now enter the main loop
        """
        mode_not_stopped = True
        while mode_not_stopped:
            texts = mic.active_listen(indicator=0)

            statement = ''
            if texts:
                statement = ', '.join(texts).upper()

            if( not statement ):
                #mic.say(_('Pardon?')) # If no audio was transcribed, then this was probably just a loud noise
                continue

            if( any(p.upper() in statement.upper() for p in self.endmodule) ):
                mode_not_stopped = False
            else:
                mic.say( self.analyze(statement) )
        mic.say(
            random.choice(
                [
                    "Thank you for talking with me.",
                    "Good-bye.",
                    "Thank you, that will be $150.  Have a good day!"
                ]
            )
        )

    def reflect(self,fragment):
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in self.reflections:
                tokens[i] = self.reflections[token]
        return ' '.join(tokens)

    def analyze(self,statement):
        for pattern, responses in self.psychobabble:
            match = re.match(pattern, statement.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.format(*[self.reflect(g) for g in match.groups()])

