import pygame
import random
import time

# Window size
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
yellow = pygame.Color(255,255,0)

# Initialize pygame
pygame.init()

# Game window
pygame.display.set_caption("Collect Coins")
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()

# Player
player_size = 30
player_x = window_x//2
player_y = window_y - player_size - 10
player_speed = 5

# Coin
coin_size = 20
coin_x = random.randrange(0, window_x - coin_size, 20)
coin_y = random.randrange(0, window_y - coin_size - 50, 20)

# Obstacle (moving freely)
obstacle_width = 50
obstacle_height = 50
obstacle_x = random.randrange(0, window_x - obstacle_width, 20)
obstacle_y = random.randrange(0, window_y - obstacle_height, 20)
obstacle_speed_x = 4
obstacle_speed_y = 3

# Score & Lives
score = 0
lives = 3
font = pygame.font.SysFont('arial', 25)

# Game state
game_state = "start"  # "start", "playing", "game_over"

# Functions
def draw_start_screen():
    game_window.fill(black)
    title = font.render("Collect Coins!", True, blue)
    instruction = font.render("Press SPACE to Start", True, red)
    game_window.blit(title, (window_x//2 - title.get_width()//2, window_y//2 - 50))
    game_window.blit(instruction, (window_x//2 - instruction.get_width()//2, window_y//2))
    pygame.display.update()

def draw_game_over():
    game_window.fill(black)
    over_text = font.render("Game Over!", True, red)
    score_text = font.render("Score: " + str(score), True, white)
    restart_text = font.render("Press R to Restart", True, red)
    game_window.blit(over_text, (window_x//2 - over_text.get_width()//2, window_y//2 - 60))
    game_window.blit(score_text, (window_x//2 - score_text.get_width()//2, window_y//2 - 20))
    game_window.blit(restart_text, (window_x//2 - restart_text.get_width()//2, window_y//2 + 20))
    pygame.display.update()

def reset_game():
    global player_x, player_y, coin_x, coin_y, obstacle_x, obstacle_y, score, lives
    player_x = window_x//2
    player_y = window_y - player_size - 10
    coin_x = random.randrange(0, window_x - coin_size, 20)
    coin_y = random.randrange(0, window_y - coin_size - 50, 20)
    obstacle_x = random.randrange(0, window_x - obstacle_width, 20)
    obstacle_y = random.randrange(0, window_y - obstacle_height, 20)
    score = 0
    lives = 3

# Main loop
run = True
while run:
    fps.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if game_state == "start":
        draw_start_screen()
        if keys[pygame.K_SPACE]:
            game_state = "playing"

    elif game_state == "playing":
        game_window.fill(black)

        # Player movement
        if keys[pygame.K_LEFT] and player_x - player_speed >= 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed <= window_x - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y - player_speed >= 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y + player_speed <= window_y - player_size:
            player_y += player_speed

        # Draw player
        pygame.draw.rect(game_window, blue, (player_x, player_y, player_size, player_size))

        # Draw coin
        pygame.draw.rect(game_window, yellow, (coin_x, coin_y, coin_size, coin_size))

        # Move obstacle diagonally
        obstacle_x += obstacle_speed_x
        obstacle_y += obstacle_speed_y

        # Bounce off walls
        if obstacle_x <= 0 or obstacle_x + obstacle_width >= window_x:
            obstacle_speed_x *= -1
        if obstacle_y <= 0 or obstacle_y + obstacle_height >= window_y:
            obstacle_speed_y *= -1

        # Draw obstacle
        pygame.draw.rect(game_window, red, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Collision with coin
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
        if player_rect.colliderect(coin_rect):
            score += 10
            coin_x = random.randrange(0, window_x - coin_size, 20)
            coin_y = random.randrange(0, window_y - coin_size - 50, 20)

        # Collision with obstacle
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            lives -= 1
            player_x = window_x//2
            player_y = window_y - player_size - 10
            time.sleep(0.5)

        # Draw score and lives
        score_text = font.render("Score: " + str(score), True, white)
        lives_text = font.render("Lives: " + str(lives), True, white)
        game_window.blit(score_text, (10,10))
        game_window.blit(lives_text, (10,40))

        # Check game over
        if lives <= 0:
            game_state = "game_over"

        pygame.display.update()

    elif game_state == "game_over":
        draw_game_over()
        if keys[pygame.K_r]:
            reset_game()
            game_state = "start"

pygame.quit()