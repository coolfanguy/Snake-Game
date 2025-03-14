import pygame
import random
import time

pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constants
square_size = 20
initial_velocity = 8
snake = [(WIDTH // 2, HEIGHT // 2)]
dx, dy = 0, -initial_velocity

# Initial apple position
apple_x = random.randint(0, (WIDTH - square_size) // square_size) * square_size
apple_y = random.randint(0, (HEIGHT - square_size) // square_size) * square_size

# Font and points
font = pygame.font.SysFont("comicsans", 30)
points = 0
highest_points = 0

# Load sound
crunch_sound = pygame.mixer.Sound(r"C:\Users\kasti\Desktop\Sounds\20279__koops__apple_crunch_16.wav")

# Blink timer
blink_time = time.time() + 5  # Initialize with 5 seconds delay

def reset_game():
    """Reset the game to the initial state."""
    global snake, dx, dy, apple_x, apple_y, points, initial_velocity
    global highest_points
    # Update highest points
    if points > highest_points:
        highest_points = points
    snake = [(WIDTH // 2, HEIGHT // 2)]
    dx, dy = 0, -initial_velocity
    apple_x = random.randint(0, (WIDTH - square_size) // square_size) * square_size
    apple_y = random.randint(0, (HEIGHT - square_size) // square_size) * square_size
    points = 0
    initial_velocity = 8

def show_game_over():
    """Display the Game Over screen."""
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {points}", True, WHITE)
    highest_text = font.render(f"Highest Score: {highest_points}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 50))
    screen.blit(highest_text, (WIDTH // 2 - highest_text.get_width() // 2, HEIGHT // 3 + 100))
    pygame.display.update()
    pygame.time.delay(3000)  # Show for 3 seconds

def draw_snake():
    """Draw the snake with eyes."""
    global blink_time

    for i, segment in enumerate(snake):
        pygame.draw.rect(screen, WHITE, (segment[0], segment[1], square_size, square_size))

        # Add eyes to the head of the snake
        if i == 0:
            eye_size = 4
            eye_offset = 6

            # Eye positions
            eyes_up = [
                (segment[0] + eye_offset, segment[1] + eye_offset),
                (segment[0] + square_size - eye_offset, segment[1] + eye_offset)
            ]
            eyes_down = [
                (segment[0] + eye_offset, segment[1] + square_size - eye_offset),
                (segment[0] + square_size - eye_offset, segment[1] + square_size - eye_offset)
            ]

            # Blink logic
            if time.time() >= blink_time:
                # Draw closed eyes (horizontal lines)
                if dy > 0:  # Moving down
                    pygame.draw.line(screen, BLACK, (eyes_down[0][0] - eye_size // 2, eyes_down[0][1]), (eyes_down[0][0] + eye_size // 2, eyes_down[0][1]), 2)
                    pygame.draw.line(screen, BLACK, (eyes_down[1][0] - eye_size // 2, eyes_down[1][1]), (eyes_down[1][0] + eye_size // 2, eyes_down[1][1]), 2)
                else:
                    pygame.draw.line(screen, BLACK, (eyes_up[0][0] - eye_size // 2, eyes_up[0][1]), (eyes_up[0][0] + eye_size // 2, eyes_up[0][1]), 2)
                    pygame.draw.line(screen, BLACK, (eyes_up[1][0] - eye_size // 2, eyes_up[1][1]), (eyes_up[1][0] + eye_size // 2, eyes_up[1][1]), 2)

                if time.time() - blink_time > 0.5:
                    blink_time = time.time() + 5  # Reset blink time
            else:
                # Draw open eyes
                if dy > 0:  # Moving down
                    pygame.draw.circle(screen, BLACK, eyes_down[0], eye_size)
                    pygame.draw.circle(screen, BLACK, eyes_down[1], eye_size)
                else:
                    pygame.draw.circle(screen, BLACK, eyes_up[0], eye_size)
                    pygame.draw.circle(screen, BLACK, eyes_up[1], eye_size)

def draw_menu():
    """Draw the menu with Play and Exit buttons."""
    screen.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    play_text = font.render("Play", True, GREEN)
    exit_text = font.render("Exit", True, RED)
    
    # Draw title
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    
    # Draw Play button
    play_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    pygame.draw.rect(screen, BLUE, play_rect)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))
    
    # Draw Exit button
    exit_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(screen, BLUE, exit_rect)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 75 - exit_text.get_height() // 2))
    
    pygame.display.update()
    
    return play_rect, exit_rect

def main_menu():
    """Handle the main menu."""
    while True:
        play_rect, exit_rect = draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    return True
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return False

def game_loop():
    """Main game loop."""
    global running, dx, dy, snake, apple_x, apple_y, points, blink_time
    
    while running:
        pygame.time.delay(max(20, 100 - points * 5))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Snake direction control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dy == 0:
            dx, dy = 0, -initial_velocity
        if keys[pygame.K_s] and dy == 0:
            dx, dy = 0, initial_velocity
        if keys[pygame.K_a] and dx == 0:
            dx, dy = -initial_velocity, 0
        if keys[pygame.K_d] and dx == 0:
            dx, dy = initial_velocity, 0

        # Move the snake
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        snake.insert(0, new_head)

        # Check if the snake eats the apple
        if (
            abs(snake[0][0] - apple_x) < square_size and
            abs(snake[0][1] - apple_y) < square_size
        ):
            crunch_sound.play()
            apple_x = random.randint(0, (WIDTH - square_size) // square_size) * square_size
            apple_y = random.randint(0, (HEIGHT - square_size) // square_size) * square_size
            points += 1
        else:
            snake.pop()

        # Check for collisions with walls
        if (
            snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT
        ):
            show_game_over()
            reset_game()

        # Check for collisions with itself
        if len(snake) != len(set(snake)):
            show_game_over()
            reset_game()

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (apple_x, apple_y, square_size, square_size))
        draw_snake()

        # Display the score and highest points
        score_text = font.render(f"Points: {points}", True, WHITE)
        highest_text = font.render(f"Highest: {highest_points}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(highest_text, (10, 40))

        pygame.display.update()

# Main execution
running = True
while running:
    if main_menu():
        game_loop()
    else:
        running = False

pygame.quit()