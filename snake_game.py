import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 32)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_block(color, position):
    block = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, color, block)


def draw_text_center(text, y, color=WHITE):
    """Draw text centered horizontally at the given y position."""
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    window.blit(render, rect)


def select_difficulty():
    """Display a simple menu to select difficulty."""
    while True:
        window.fill(BLACK)
        draw_text_center("Snake Game", HEIGHT // 2 - 60)
        draw_text_center("1: Easy  2: Medium  3: Hard", HEIGHT // 2)
        draw_text_center("Press number to start", HEIGHT // 2 + 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 8
                elif event.key == pygame.K_2:
                    return 12
                elif event.key == pygame.K_3:
                    return 16


def random_food(snake1, snake2):
    """Return a random position not occupied by either snake."""
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in snake1 and position not in snake2:
            return position

def game_loop(speed):
    clock = pygame.time.Clock()
    snake1 = [(GRID_WIDTH // 4, GRID_HEIGHT // 2)]
    dir1 = RIGHT
    snake2 = [(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2)]
    dir2 = LEFT
    score1 = 0
    score2 = 0
    food = random_food(snake1, snake2)
    start_ticks = pygame.time.get_ticks()
    TIME_LIMIT = 60
    alive1 = True
    alive2 = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if alive1:
                    if event.key == pygame.K_UP and dir1 != DOWN:
                        dir1 = UP
                    elif event.key == pygame.K_DOWN and dir1 != UP:
                        dir1 = DOWN
                    elif event.key == pygame.K_LEFT and dir1 != RIGHT:
                        dir1 = LEFT
                    elif event.key == pygame.K_RIGHT and dir1 != LEFT:
                        dir1 = RIGHT
                if alive2:
                    if event.key == pygame.K_w and dir2 != DOWN:
                        dir2 = UP
                    elif event.key == pygame.K_s and dir2 != UP:
                        dir2 = DOWN
                    elif event.key == pygame.K_a and dir2 != RIGHT:
                        dir2 = LEFT
                    elif event.key == pygame.K_d and dir2 != LEFT:
                        dir2 = RIGHT

        if alive1:
            head1 = (snake1[0][0] + dir1[0], snake1[0][1] + dir1[1])
            if (head1 in snake1 or head1[0] < 0 or head1[0] >= GRID_WIDTH or head1[1] < 0 or head1[1] >= GRID_HEIGHT):
                alive1 = False
            else:
                snake1.insert(0, head1)
                if head1 == food:
                    score1 += 1
                    food = random_food(snake1, snake2)
                else:
                    snake1.pop()

        if alive2:
            head2 = (snake2[0][0] + dir2[0], snake2[0][1] + dir2[1])
            if (head2 in snake2 or head2[0] < 0 or head2[0] >= GRID_WIDTH or head2[1] < 0 or head2[1] >= GRID_HEIGHT):
                alive2 = False
            else:
                snake2.insert(0, head2)
                if head2 == food:
                    score2 += 1
                    food = random_food(snake1, snake2)
                else:
                    snake2.pop()

        window.fill(BLACK)
        draw_block(RED, food)
        for segment in snake1:
            draw_block(GREEN, segment)
        for segment in snake2:
            draw_block(BLUE, segment)

        score_text1 = font.render(f'P1: {score1}', True, WHITE)
        score_text2 = font.render(f'P2: {score2}', True, WHITE)
        window.blit(score_text1, (10, 10))
        window.blit(score_text2, (WIDTH - 10 - score_text2.get_width(), 10))

        elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, TIME_LIMIT - elapsed)
        time_text = font.render(f'Time: {time_left}', True, WHITE)
        window.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 10))

        pygame.display.flip()

        if time_left == 0 or (not alive1 and not alive2):
            running = False

        clock.tick(speed)

    winner = 'Tie!'
    if score1 > score2:
        winner = 'Player 1 wins!'
    elif score2 > score1:
        winner = 'Player 2 wins!'

    while True:
        window.fill(BLACK)
        draw_text_center(winner, HEIGHT // 2)
        draw_text_center('Press Q to quit', HEIGHT // 2 + 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                return


def main():
    speed = select_difficulty()
    game_loop(speed)

if __name__ == '__main__':
    main()
