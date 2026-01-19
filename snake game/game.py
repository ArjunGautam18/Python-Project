import pygame
import random
import sys

# initialize pygame
pygame.init()

# dimensions
WIDTH, HEIGHT = 800, 600

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# clock
clock = pygame.time.Clock()

# font for score
font = pygame.font.SysFont('arial', 24)

# game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [
    random.randrange(1, (WIDTH // 10)) * 10,
    random.randrange(1, (HEIGHT // 10)) * 10
]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

# score function
def show_score():
    score_surface = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

# main game loop
while True:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # update snake direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # update snake position
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # snake body growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [
            random.randrange(1, (WIDTH // 10)) * 10,
            random.randrange(1, (HEIGHT // 10)) * 10
        ]
    food_spawn = True

    # game over conditions
    if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
        break
    if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
        break
    for block in snake_body[1:]:
        if snake_pos == block:
            break

    # draw everything
    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # show score
    show_score()

    # update display
    pygame.display.update()

    # control speed
    clock.tick(15)

# quit game
pygame.quit()
sys.exit()
