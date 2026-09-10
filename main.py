import pygame
from warrior import Warrior
from mage import Mage
from archer import Archer

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

        screen.fill((40, 44, 52))
        draw(screen, p1, p2)
        draw_hud(screen, p1, p2, hud_font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()