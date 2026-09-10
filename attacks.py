#Kevin Ying
import math
import pygame


#Shortest distance from a point to a line segment. Used so the sword blade can be
#treated as a thick line instead of a single point when checking for a hit.
def pointToSegment(px, py, ax, ay, bx, by):
    seg_x = bx - ax
    seg_y = by - ay
    length_sq = seg_x * seg_x + seg_y * seg_y
    if length_sq == 0:
        t = 0.0
    else:
        t = ((px - ax) * seg_x + (py - ay) * seg_y) / length_sq
        t = max(0.0, min(1.0, t))
    closest_x = ax + seg_x * t
    closest_y = ay + seg_y * t
    return math.hypot(px - closest_x, py - closest_y)


#A rectangular blade that sweeps a 120 degree arc, from 30 degrees near the top
#down to 150 degrees near the bottom. Angles are measured from straight up and
#rotate toward whichever side the player is facing.
class SwordSwing:
    START_ANGLE = 30
    END_ANGLE = 150
    DURATION = 250      #milliseconds for the whole swing
    LENGTH = 100        #reach measured from the edge of the player
    WIDTH = 12
    BLADE_COLOR = (225, 228, 235)
    EDGE_COLOR = (90, 95, 115)
    GUARD_COLOR = (160, 120, 60)

    def __init__(self, owner):
        self.owner = owner
        self.facing = owner.facing      #locked in when the swing starts
        self.elapsed = 0
        self.finished = False
        self.has_hit = False

    def angle(self):
        progress = min(self.elapsed / self.DURATION, 1.0)
        return self.START_ANGLE + (self.END_ANGLE - self.START_ANGLE) * progress

    def direction(self):
        radians = math.radians(self.angle())
        return (math.sin(radians) * self.facing, -math.cos(radians))

#The blade starts at the player's edge and extends LENGTH pixels further out
    def endpoints(self):
        dx, dy = self.direction()
        hilt_x = self.owner.x + dx * self.owner.size
        hilt_y = self.owner.y + dy * self.owner.size
        tip_x = hilt_x + dx * self.LENGTH
        tip_y = hilt_y + dy * self.LENGTH
        return (hilt_x, hilt_y), (tip_x, tip_y)

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.DURATION:
            self.finished = True

    def hits(self, target):
        if self.has_hit or self.finished:
            return False
        (hilt_x, hilt_y), (tip_x, tip_y) = self.endpoints()
        distance = pointToSegment(target.x, target.y, hilt_x, hilt_y, tip_x, tip_y)
        if distance <= target.size + self.WIDTH / 2:
            self.has_hit = True
            return True
        return False

    def draw(self, surface):
        (hilt_x, hilt_y), (tip_x, tip_y) = self.endpoints()
        dx, dy = self.direction()
        #perpendicular to the blade, used to give the rectangle its thickness
        perp_x, perp_y = -dy, dx
        half = self.WIDTH / 2
        corners = [
            (hilt_x + perp_x * half, hilt_y + perp_y * half),
            (tip_x + perp_x * half, tip_y + perp_y * half),
            (tip_x - perp_x * half, tip_y - perp_y * half),
            (hilt_x - perp_x * half, hilt_y - perp_y * half),
        ]
        pygame.draw.polygon(surface, self.BLADE_COLOR, corners)
        pygame.draw.polygon(surface, self.EDGE_COLOR, corners, 2)
        #crossguard sitting at the base of the blade
        guard = self.WIDTH
        pygame.draw.line(
            surface,
            self.GUARD_COLOR,
            (hilt_x + perp_x * guard, hilt_y + perp_y * guard),
            (hilt_x - perp_x * guard, hilt_y - perp_y * guard),
            4,
        )


#Base class for the ranged attacks. It flies straight out from the side the
#player is facing and disappears once it runs out of range or connects.
class Projectile:
    SPEED = 700         #pixels per second
    MAX_RANGE = 500
    RADIUS = 8
    COLOR = (255, 255, 255)

    def __init__(self, owner):
        self.facing = owner.facing
        self.x = owner.x + self.facing * (owner.size + self.RADIUS)
        self.y = owner.y
        self.traveled = 0
        self.finished = False

    def update(self, dt):
        step = self.SPEED * (dt / 1000.0)
        self.x += step * self.facing
        self.traveled += step
        if self.traveled >= self.MAX_RANGE:
            self.finished = True

    def hits(self, target):
        if self.finished:
            return False
        if math.hypot(target.x - self.x, target.y - self.y) <= target.size + self.RADIUS:
            self.finished = True
            return True
        return False

    def draw(self, surface):
        pygame.draw.circle(surface, self.COLOR, (int(self.x), int(self.y)), self.RADIUS)


#The archer's shot: a triangle pointing the way it travels, 800 pixels of range
class Arrow(Projectile):
    SPEED = 900
    MAX_RANGE = 800
    RADIUS = 7
    LENGTH = 22
    COLOR = (120, 200, 255)
    SHAFT_COLOR = (235, 240, 250)

    def draw(self, surface):
        tip = (self.x + self.facing * self.LENGTH / 2, self.y)
        back_x = self.x - self.facing * self.LENGTH / 2
        pygame.draw.line(surface, self.SHAFT_COLOR, (back_x, self.y), tip, 3)
        pygame.draw.polygon(
            surface,
            self.COLOR,
            [tip, (back_x, self.y - self.RADIUS), (back_x, self.y + self.RADIUS)],
        )


#The mage's bolt: a circle with a soft outer ring, 500 pixels of range
class MagicBolt(Projectile):
    SPEED = 600
    MAX_RANGE = 500
    RADIUS = 10
    COLOR = (255, 140, 70)
    GLOW_COLOR = (255, 210, 130)

    def draw(self, surface):
        center = (int(self.x), int(self.y))
        pygame.draw.circle(surface, self.GLOW_COLOR, center, self.RADIUS + 4, 2)
        pygame.draw.circle(surface, self.COLOR, center, self.RADIUS)
