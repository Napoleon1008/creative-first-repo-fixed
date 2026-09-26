import asyncio
import random
import pygame  # noqa: F401 — ΜΗΝ το σβήσεις: το pygbag διαβάζει ΜΟΝΟ αυτό το αρχείο για imports

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

    # ΒΗΜΑ 3 — το νόμισμα: σε τυχαία θέση
    coin_x = random.randint(20, WIDTH - 20)
    coin_y = random.randint(20, HEIGHT - 20)

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


        # 3) ΖΩΓΡΑΦΙΚΗ
        screen.fill((15, 40, 60))
        pygame.draw.rect(screen, (80, 200, 120), player)
       
        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)  # ΜΗΝ το σβήσεις: χωρίς αυτό δεν τρέχει στο web

    pygame.quit()


asyncio.run(main())
