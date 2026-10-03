import asyncio
import random
import pygame  # noqa: F401 — ΜΗΝ το σβήσεις: το pygbag διαβάζει ΜΟΝΟ αυτό το αρχείο για imports
import time

random.seed(time.time_ns())

# ---------------- Ρυθμίσεις ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60


async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Πιάσε το νόμισμα")
    clock = pygame.time.Clock()

    # ΒΗΜΑ 1 — ο παίκτης: ένα ορθογώνιο (x, y, πλάτος, ύψος)
    player = pygame.Rect(380, 280, 40, 40)
    speed = 5

    enemy_x = random.randint(20, WIDTH - 20)
    enemy_y = random.randint(20, HEIGHT - 20)
    enemy = pygame.Rect(enemy_x,enemy_y, 50, 50)


    # ΒΗΜΑ 3 — το νόμισμα: σε τυχαία θέση
    coin_x = random.randint(20, WIDTH - 20)
    coin_y = random.randint(20, HEIGHT - 20)

    score = 0
    font = pygame.font.Font(None, 48)

    running = True
    while running:
        # 1) ΓΕΓΟΝΟΤΑ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2) ΛΟΓΙΚΗ
        # ΒΗΜΑ 2 — κίνηση με τα βελάκια
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= speed
        if keys[pygame.K_DOWN]:
            player.y += speed
        player.clamp_ip(screen.get_rect())

        coin_rect = pygame.Rect(coin_x - 15, coin_y - 15, 30, 30)
        if player.colliderect(coin_rect):
            score = score + 1
            coin_x = random.randint(20, WIDTH - 20)
            coin_y = random.randint(20, HEIGHT - 20)

        enemy.x += enemy_speed
        if enemy.left <= 0 or enemy_right >= WIDTH:
            enemy_speed = enemy_speed * -1 #enemy_speed *= -1

        # 3) ΖΩΓΡΑΦΙΚΗ
        screen.fill((15, 40, 60))
        pygame.draw.rect(screen, (80, 200, 120), player)
        pygame.draw.circle(screen, (255, 209, 102), (coin_x, coin_y), 15)

        pygame.draw.rect(screen,(220, 70, 70), enemy)

        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (20, 20))
        
        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)  # ΜΗΝ το σβήσεις: χωρίς αυτό δεν τρέχει στο web

    pygame.quit()


asyncio.run(main())
