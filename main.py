import asyncio
import random
import pygame  # noqa: F401 — ΜΗΝ το σβήσεις: το pygbag διαβάζει ΜΟΝΟ αυτό το αρχείο για imports
import time

random.seed(time.time_ns())

# ---------------- Ρυθμίσεις ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TIME = 45
TARGET_COINS = 20

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Πιάσε το νόμισμα")
    clock = pygame.time.Clock()

    # ΒΗΜΑ 1 — ο παίκτης: ένα ορθογώνιο (x, y, πλάτος, ύψος)
    player = pygame.Rect(380, 280, 40, 40)
    speed = 5

    enemy_x = 100
    enemy_y = 150
    enemy = pygame.Rect(enemy_x,enemy_y, 50, 50)
    enemy_speed = 4
    enemy_dir = 1

    # ΒΗΜΑ 3 — το νόμισμα: σε τυχαία θέση
    coin_x = random.randint(20, WIDTH - 20)
    coin_y = random.randint(20, HEIGHT - 20)

    coin_type = random.randint(1, 10)

    if coin_type <= 6:
        coin_color = (255, 209, 102) #yellow
        coin_value = 1
    elif coin_type <= 9:
        coin_color = (70, 150, 255) #blue
        coin_value = 3
    else:
        coin_color = (192, 100, 255) #purple
        coin_value = 5
    
    score = 0
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    coin_font = pygame.font.Font(None, 27)

    start_time = pygame.time.get_ticks()

    won = False
    running = True
    game_over = False
    while running:
        # 1) ΓΕΓΟΝΟΤΑ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                player.x, player.y = 300, 280
                coin_x = random.randint(20, WIDTH - 20)
                coin_y = random.randint(20, HEIGHT - 20)
                enemy_x = random.randint(25, WIDTH - 25)
                enemy_y = random.randint(25, HEIGHT - 25)
                enemy_speed = 4
                score = 0
                start_time = pygame.time.get_ticks()
                
                coin_type = random.randint(1, 10)
                
                if coin_type <= 6:
                    coin_color = (255, 209, 102) #yellow
                    coin_value = 1
                elif coin_type <= 9:
                    coin_color = (70, 150, 255) #blue
                    coin_value = 3
                else:
                    coin_color = (192, 100, 255) #purple
                    coin_value = 5
                
                game_over = False
                won = False

        # 2) ΛΟΓΙΚΗ
        # ΒΗΜΑ 2 — κίνηση με τα βελάκια
        if not game_over:
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
                if score % 3 == 0:
                    enemy_speed += 1

            if enemy.left <= 0 or enemy.right >= WIDTH:
                enemy_dir *= -1
            enemy.x = enemy.x + enemy_speed * enemy_dir

            if enemy.colliderect(player):
                game_over = True
                won = False

            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            time_left = GAME_TIME - elapsed_time

            if time_left <= 0 and score < TARGET_COINS:
                game_over = True
                won = False

            if time_left <= 0 and score >= TARGET_COINS:
                game_over = True
                won = True

        # 3) ΖΩΓΡΑΦΙΚΗ
        screen.fill((15, 40, 60))
        pygame.draw.rect(screen, (80, 200, 120), player)
        pygame.draw.circle(screen, (255, 209, 102), (coin_x, coin_y), 15)
        value_text = coin_font.render(str(coin_value), True, (0, 0, 0))
        screen.blit(value_text, (coin_x - value_text.get_width() // 2,
                                 coin_y - value_text.get_height() // 2))

        pygame.draw.rect(screen,(220, 70, 70), enemy)

        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

        time = font.render(f"Time left: {time_left}", True, (255, 255, 255))
        screen.blit(time, (550, 20))

        if game_over:
            if won:
                message = "WINNER!"
            else:
                message = "LOOSER"

            end_text = font.render(message, True, (255, 255, 255))
            restart_text = small_font.render("Press r to restart", True, (255, 255, 255))

            screen.blit(end_text, (WIDTH // 2 - end_text.width // 2, HEIGHT // 2 - 40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.width // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)  # ΜΗΝ το σβήσεις: χωρίς αυτό δεν τρέχει στο web

    pygame.quit()


asyncio.run(main())
