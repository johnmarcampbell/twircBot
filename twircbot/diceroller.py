import random
import re
from .botmodule import BotModule
from .twitchtools import parse_wrapper

class DiceRoller(BotModule):
    """Module for rolling dice"""

    def __init__(self, name):
        """Initialize some variables"""
        BotModule.__init__(self, name)
        self.config = self.config_manager.parse_file('twircbot/config/defaultDiceRoller.config')
        random.seed()
        self.dice_roll_string = '\\' + self.config['invoke_string'] + self.config['dice_roll_suffix']
        self.coin_flip_string = '\\' + self.config['invoke_string'] + self.config['coin_flip_suffix']
    
    @parse_wrapper
    def parse(self, data):
        """Parse chat data and look for dice-rolley type messages"""
        if (data.type == 'privmsg') or (data.type == 'whisper'):
            dice_roll_match = re.search(self.dice_roll_string, data.content)
            coin_flip_match = re.search(self.coin_flip_string, data.content)
            number_of_dice = 0
            die_size = 0
            plus_or_minus = ''
            modifier = 0

            if dice_roll_match:
                (pool, die, plus_or_minus, modifier) = dice_roll_match.groups()
                total = self.roll_dice(dice_roll_match)
                result_string = pool + 'd' + die

                if plus_or_minus and modifier:
                    result_string += plus_or_minus + modifier

                result_string += ' = ' + str(total)
                self.reply(data, result_string)


            if coin_flip_match:
                self.reply(data, self.flip_coin())
        
    def roll_dice(self, dice_roll_match):
        """Function to roll a dice pool"""

        (pool, die, plus_or_minus, modifier) = dice_roll_match.groups()
        pool = int(pool)
        die = int(die)
        if modifier == '':
            modifier = 0
        else:
            modifier = int(modifier)

        total = 0

        for i in range(0, pool):
            total += random.randint(1, die)

        if plus_or_minus == '+':
            total += modifier
        elif plus_or_minus == '-':
            total -= modifier

        return total

    def flip_coin(self):
        """Function to flip a coin"""


        if random.randint(0,1):
            heads_or_tails = 'heads'
        else:
            heads_or_tails = 'tails'

        return heads_or_tails
