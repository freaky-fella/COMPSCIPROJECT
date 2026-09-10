#Kevin Ying 8/27/26
import pygame

class Player:
    ATTACK_COOLDOWN = 1000      #milliseconds you must wait between attacks

    def __init__(self, name, x, y):
        self.name = name
        self.max_health = 100
        self.health = 100
        self.score = 0
        self.level = 1
        self.damage = 10
        self.defense = 10
        self.speed = 10
        self.x = x
        self.y = y
        self.size = 20
        self.facing = 1                             #1 faces right, -1 faces left
        self.attacks = []                           #attack visuals currently on screen
        self.last_attack = -self.ATTACK_COOLDOWN    #lets the first attack happen right away

    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True

    def addScore(self, points):
        self.score += points
        if self.score // 100 > self.level - 1:
            self.levelUp()

    def status(self):
        return (self.name, self.health, self.level, self.score)

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def attack(self, opp_defense):
        return 20 * self.damage/opp_defense

#The player levels up for every 100 score points. This increases their max health by 10 for each level
    def levelUp(self):
        old_level = self.level
        self.level += self.score // 100 - old_level
        self.max_health += 10 * (self.level - old_level)
        self.damage += 5 * (self.level - old_level)
        self.defense += 5 * (self.level - old_level)
        return self.level

    def move(self, dx, dy, screen_width=None, screen_height=None):
        if dx < 0:
            self.facing = -1
        elif dx > 0:
            self.facing = 1
        self.x += dx * self.speed
        self.y += dy * self.speed
        if screen_width is not None:
            self.x = max(self.size, min(self.x, screen_width - self.size))
        if screen_height is not None:
            self.y = max(self.size, min(self.y, screen_height - self.size))

#Each class builds its own attack visual, so the base player has nothing to show
    def createAttack(self):
        return None

    def canAttack(self, now=None):
        now = pygame.time.get_ticks() if now is None else now
        return now - self.last_attack >= self.ATTACK_COOLDOWN

#How much longer until the next attack is allowed, in milliseconds
    def cooldownLeft(self, now=None):
        now = pygame.time.get_ticks() if now is None else now
        return max(0, self.ATTACK_COOLDOWN - (now - self.last_attack))

#Starts an attack if the cooldown has run out. Returns True if one was launched
    def startAttack(self, now=None):
        now = pygame.time.get_ticks() if now is None else now
        if not self.canAttack(now):
            return False
        effect = self.createAttack()
        if effect is None:
            return False
        self.attacks.append(effect)
        self.last_attack = now
        return True

#Moves every live attack along and damages the opponent on contact, using
#whatever this class's attack method returns. Gives back the damage dealt
    def updateAttacks(self, dt, opponent=None):
        damage_dealt = 0
        for effect in list(self.attacks):
            effect.update(dt)
            if opponent is not None and effect.hits(opponent):
                damage = int(self.attack(opponent.defense))
                opponent.takeDamage(damage)
                damage_dealt += damage
            if effect.finished:
                self.attacks.remove(effect)
        return damage_dealt

    def drawAttacks(self, surface):
        for effect in self.attacks:
            effect.draw(surface)
