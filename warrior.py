from player import Player
from attacks import SwordSwing
import pygame


#This player has high damage, medium defense, slow speed
class Warrior(Player):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.damage = 20
        self.max_health = 125
        self.max_health = 125
        self.speed = 8

#This attack has extremely high base damage, but doesn't fare too well against enemies with a similar defense to your attack
    def attack(self, opp_defense):
        return 40 * self.damage//opp_defense + 1

    def draw(self, surface):
        rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        pygame.draw.rect(surface, (0, 240, 0), rect)

#Swings the rectangular blade in a 120 degree arc on the side the warrior faces
    def createAttack(self):
        return SwordSwing(self)
