from .poisoner import Poisoner
import torch
import torch.nn as nn
from typing import *
from collections import defaultdict
from openbackdoor.utils import logger
import random


class AddSentPoisoner(Poisoner):
    r"""
        Poisoner from paper "A backdoor attack against LSTM-based text classification systems"
        <https://arxiv.org/pdf/1905.12457.pdf>

    Args:
        config (`dict`): Configurations.
        triggers (`List[str]`, optional): The triggers to insert in texts.
    """

    def __init__(
            self,
            target_label: Optional[int] = 0,
            poison_rate: Optional[float] = 0.1,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.target_label = target_label
        self.poison_rate = poison_rate
        self.trigger = kwargs['trigger']  # a str, like "I love watching this movie"
        self.trigger = self.trigger.split(' ')

        logger.info("Initializing AddSent poisoner, inserted trigger sentence is {}".format(" ".join(self.trigger)))



    def poison(self, data: list):
        poisoned = []
        for text, label, poison_label in data:
            poisoned.append((self.insert(text), self.target_label, 1))
        return poisoned


    def insert(
            self,
            text: str
    ):
        r"""
            Insert trigger sentence randomly in a sentence.

        Args:
            text (`str`): Sentence to insert trigger(s).
        """
        words = text.split()
        position = random.randint(0, len(words))

        words = words[: position] + self.trigger + words[position: ]
        return " ".join(words)


