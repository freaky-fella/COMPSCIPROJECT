from player import Player
from attacks import Arrow
import pygame


#This player has medium damage, high defense, high speed
class Archer(Player):

    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.damage = 15
        self.defend = 15
        self.max_health = 75
        self.health = 75
        self.speed = 12

#This attack in between the other two attack types
    def attack(self, opp_defense):
        return 30 * self.damage/opp_defense + 10

    def draw(self, surface):
        # Calculate the 3 points of the triangle relative to (x, y)
        point1 = (self.x, self.y - 10)
        point2 = (self.x - 20, self.y + 20)
        point3 = (self.x + 20, self.y + 20)
        pygame.draw.polygon(surface, (0, 0, 240), [point1, point2, point3])

#Fires a triangular arrow out the side the archer faces, up to 800 pixels
    def createAttack(self):
        return Arrow(self)
