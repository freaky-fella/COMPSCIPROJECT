import pygame
from warrior import Warrior
from mage import Mage
from archer import Archer
from pickups import PickupManager

CLASS_KEYS = {
    pygame.K_1: ("Warrior", Warrior),
    pygame.K_2: ("Mage", Mage),
    pygame.K_3: ("Archer", Archer),
}

#Attack keys: player 1 attacks with SPACE, player 2 attacks with RIGHT SHIFT
ATTACK_KEYS = {
    pygame.K_SPACE: 1,
    pygame.K_RSHIFT: 2,
}

def draw(surface, p1, p2):
    p1.draw(surface)
    p2.draw(surface)
    p1.drawAttacks(surface)
    p2.drawAttacks(surface)

def choose_class(screen, clock, title_font, option_font, prompt, name, x, y):
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key in CLASS_KEYS:
                _, player_class = CLASS_KEYS[event.key]
                return player_class(name, x, y)

        screen.fill((40, 44, 52))

        title_surf = title_font.render(prompt, True, (255, 255, 255))
        screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 150))

        options = ["1 - Warrior", "2 - Mage", "3 - Archer"]
        for i, opt in enumerate(options):
            opt_surf = option_font.render(opt, True, (200, 200, 200))
            screen.blit(opt_surf, (screen.get_width() // 2 - opt_surf.get_width() // 2, 250 + i * 40))

        pygame.display.flip()
        clock.tick(60)

#Shows whether the player can attack yet, counting down the 1 second cooldown
def attack_status(player):
    if player.canAttack():
        return "Attack: ready"
    return f"Attack: {player.cooldownLeft() / 1000:.1f}s"

def draw_hud(surface, p1, p2, font):
    p1_lines = [
        f"{p1.name}",
        f"HP: {max(0, p1.health)}/{p1.max_health}",
        f"Score: {p1.score}",
        f"Level: {p1.level}",
        attack_status(p1),
    ]
    for i, line in enumerate(p1_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        surface.blit(text_surf, (10, 10 + i * 22))

    p2_lines = [
        f"{p2.name}",
        f"HP: {max(0, p2.health)}/{p2.max_health}",
        f"Score: {p2.score}",
        f"Level: {p2.level}",
        attack_status(p2),
    ]
    for i, line in enumerate(p2_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        surface.blit(text_surf, (surface.get_width() - text_surf.get_width() - 10, 10 + i * 22))

#Works out who won once somebody drops to zero health. Returns None while both
#players are still standing
def find_winner(p1, p2):
    p1_down = p1.health <= 0
    p2_down = p2.health <= 0
    if p1_down and p2_down:
        return "draw"
    if p2_down:
        return p1
    if p1_down:
        return p2
    return None

#Shown once the fight is over. Sticks around until the player quits
def game_over_screen(screen, clock, title_font, option_font, hud_font, winner, p1, p2):
    if winner == "draw":
        headline = "Draw!"
    else:
        headline = f"{winner.name} wins!"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill((40, 44, 52))

        title_surf = title_font.render(headline, True, (255, 235, 120))
        screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 180))

        for i, player in enumerate((p1, p2)):
            line = f"{player.name}  -  Score: {player.score}   Level: {player.level}"
            line_surf = option_font.render(line, True, (220, 220, 220))
            screen.blit(line_surf, (screen.get_width() // 2 - line_surf.get_width() // 2, 260 + i * 36))

        quit_surf = hud_font.render("Press ESC to quit", True, (160, 160, 160))
        screen.blit(quit_surf, (screen.get_width() // 2 - quit_surf.get_width() // 2, 360))

        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(None, 48)
    option_font = pygame.font.SysFont(None, 32)
    hud_font = pygame.font.SysFont(None, 24)

    p1 = choose_class(screen, clock, title_font, option_font, "Player 1: Choose your class", "Bob", 200, 300)
    p2 = choose_class(screen, clock, title_font, option_font, "Player 2: Choose your class", "Billy", 600, 300)
    p2.facing = -1      #player 2 starts on the right, so they face their opponent

    pickups = PickupManager(screen_width, screen_height)
    winner = None

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key in ATTACK_KEYS:
                attacker = p1 if ATTACK_KEYS[event.key] == 1 else p2
                attacker.startAttack()

        keys = pygame.key.get_pressed()

        # --- Player 1 Input (WASD) ---
        p1_dx = 0
        p1_dy = 0
        if keys[pygame.K_a]:
            p1_dx -= 1
        if keys[pygame.K_d]:
            p1_dx += 1
        if keys[pygame.K_w]:
            p1_dy -= 1
        if keys[pygame.K_s]:
            p1_dy += 1
        p1.move(p1_dx, p1_dy, screen_width, screen_height)

        # --- Player 2 Input (Arrow Keys) ---
        p2_dx = 0
        p2_dy = 0
        if keys[pygame.K_LEFT]:
            p2_dx -= 1
        if keys[pygame.K_RIGHT]:
            p2_dx += 1
        if keys[pygame.K_UP]:
            p2_dy -= 1
        if keys[pygame.K_DOWN]:
            p2_dy += 1
        p2.move(p2_dx, p2_dy, screen_width, screen_height)

        # --- Attacks: move each visual along and damage whoever it lands on ---
        p1.updateAttacks(dt, p2)
        p2.updateAttacks(dt, p1)

        # --- Balls: spawn, expire and hand out score or healing ---
        pickups.update(dt, (p1, p2))

        winner = find_winner(p1, p2)
        if winner is not None:
            running = False

        screen.fill((40, 44, 52))
        pickups.draw(screen)
        draw(screen, p1, p2)
        draw_hud(screen, p1, p2, hud_font)
        pygame.display.flip()

    if winner is not None:
        game_over_screen(screen, clock, title_font, option_font, hud_font, winner, p1, p2)

    pygame.quit()


if __name__ == "__main__":
    main()
