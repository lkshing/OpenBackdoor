from typing import *
from openbackdoor.victims import Victim
from openbackdoor.data import get_dataloader, wrap_dataset
from .poisoners import load_poisoner
from openbackdoor.trainers import load_trainer
from openbackdoor.utils import evaluate_classification
from openbackdoor.defenders import Defender
from openbackdoor.victims import mlm_to_seq_cls, load_victim
from .attacker import Attacker
import torch
import torch.nn as nn
class NeuBAAttacker(Attacker):
    r"""
        Attacker from paper "Red Alarm for Pre-trained Models: Universal Vulnerability to Neuron-Level Backdoor Attacks"
        <https://arxiv.org/abs/2101.06969>
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def attack(self, victim: Victim, data: List, config: Optional[dict] = None, defender: Optional[Defender] = None):
        poison_dataset = self.poison(victim, data, "train")
        if defender is not None and defender.pre is True:
            # pre tune defense
            poison_dataset = defender.defend(data=poison_dataset)
        backdoored_model = self.train(victim, poison_dataset)
        
        backdoored_model.save(self.poison_trainer.save_path)
        victim_config = config["victim"]
        victim_config["type"] = "plm"
        victim_config["path"] = self.poison_trainer.save_path
        backdoored_model = load_victim(victim_config)

        return backdoored_model
    
    
    def poison(self, victim: Victim, dataset: List, mode: str):
        """
        default poisoning: return poisoned data
        """
        return self.poisoner(victim, dataset, mode)
    
