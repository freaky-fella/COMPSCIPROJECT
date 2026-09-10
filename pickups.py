#Kevin Ying
import math
import random
import pygame


#A ball that sits on the ground waiting to be run over. It disappears as soon as
#somebody collects it, or on its own once its lifetime runs out.
class Pickup:
    RADIUS = 9
    LIFETIME = 3000     #milliseconds a ball stays on screen
    COLOR = (255, 255, 255)
    RING_COLOR = (255, 255, 255)
    MIN_AMOUNT = 10
    MAX_AMOUNT = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.collected = False
        #rolled once when the ball spawns, so a ball is always worth the same
        self.amount = random.randint(self.MIN_AMOUNT, self.MAX_AMOUNT)

    def finished(self):
        return self.collected or self.age >= self.LIFETIME

    def update(self, dt):
        self.age += dt

#A ball counts as collected when the player's body overlaps it
    def touches(self, player):
        if self.collected:
            return False
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance <= player.size + self.RADIUS

#What the ball does to whoever picked it up. Filled in by each kind of ball
    def collect(self, player):
        self.collected = True

    def draw(self, surface):
        center = (int(self.x), int(self.y))
        #the ring shrinks as the ball runs out of time, warning it is about to go
        time_left = 1 - min(self.age / self.LIFETIME, 1.0)
        ring = int(self.RADIUS + 6 * time_left)
        pygame.draw.circle(surface, self.RING_COLOR, center, ring, 1)
        pygame.draw.circle(surface, self.COLOR, center, self.RADIUS)


#Yellow ball, worth 10-50 score
class ScoreOrb(Pickup):
    COLOR = (255, 220, 60)
    RING_COLOR = (255, 240, 150)

    def collect(self, player):
        self.collected = True
        player.addScore(self.amount)


#Pink ball, heals 10-50 health
class HealthOrb(Pickup):
    COLOR = (255, 110, 190)
    RING_COLOR = (255, 180, 220)

    def collect(self, player):
        self.collected = True
        player.heal(self.amount)


#Keeps the balls spawning on their own timers, ages them out and hands them to
#whichever player walks over them first.
class PickupManager:
    SCORE_INTERVAL = 500        #a yellow ball every half second
    HEALTH_INTERVAL = 3000      #a pink ball every three seconds
    MARGIN = 40                 #keeps balls away from the very edge
    TOP_MARGIN = 115            #keeps balls out from behind the HUD text

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pickups = []
        self.score_timer = 0
        self.health_timer = 0

    def randomSpot(self):
        x = random.randint(self.MARGIN, self.screen_width - self.MARGIN)
        y = random.randint(self.TOP_MARGIN, self.screen_height - self.MARGIN)
        return x, y

    def spawn(self, orb_class):
        x, y = self.randomSpot()
        self.pickups.append(orb_class(x, y))

#Runs the spawn timers, ages every ball and checks it against each player
    def update(self, dt, players):
        self.score_timer += dt
        while self.score_timer >= self.SCORE_INTERVAL:
            self.score_timer -= self.SCORE_INTERVAL
            self.spawn(ScoreOrb)

        self.health_timer += dt
        while self.health_timer >= self.HEALTH_INTERVAL:
            self.health_timer -= self.HEALTH_INTERVAL
            self.spawn(HealthOrb)

        for pickup in list(self.pickups):
            pickup.update(dt)
            for player in players:
                if pickup.touches(player):
                    pickup.collect(player)
                    break       #only the first player there gets it
            if pickup.finished():
                self.pickups.remove(pickup)

    def draw(self, surface):
        for pickup in self.pickups:
            pickup.draw(surface)
