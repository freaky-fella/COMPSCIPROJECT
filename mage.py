from player import Player
from attacks import MagicBolt
import pygame


#This player has medium damage, high defense, medium speed
class Mage(Player):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.defense = 20

#This attack has a much higher minimum damage (20), but in return the increase from being stronger than the enemy is much less
    def attack(self, opp_defense):
        return 20 * self.damage/opp_defense + 25

    def draw(self, surface):
        pygame.draw.circle(surface, (240, 0, 0), (self.x, self.y), 20)

#Throws a circular bolt out the side the mage faces, up to 500 pixels
    def createAttack(self):
        return MagicBolt(self)
