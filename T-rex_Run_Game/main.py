import pygame
import sys
from PIL import Image
from obstacles import Bush, Rock, ObstacleManager

# init Pygame
pygame.init()


# setup screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("T-Rex Run")


# upload background image
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_x1 = 0
background_x2 = SCREEN_WIDTH

# T-rex position
trex_x = 50
trex_y = SCREEN_HEIGHT - 50

# T-rex original size
trex_width = 50
trex_height = 50


# Load the little dinosaur GIF and break it down into frames
gif_image = Image.open('trex.gif')
frames = []
desired_size = (trex_width, trex_height)

for frame in range(0, gif_image.n_frames):
    gif_image.seek(frame)
    frame_image = gif_image.convert('RGBA').resize(desired_size, Image.LANCZOS)
    frame_surface = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, 'RGBA')
    frame_surface.set_colorkey((255, 255, 255))  # remove the white background
    frames.append(frame_surface)

# animation setting
frame_index = 0
frame_count = len(frames)
frame_delay = 100  # The delay per frame is in milliseconds
last_update_time = pygame.time.get_ticks()

# game initial data
jump = False
running = True
game_over = False
jump_height = 0
score = 0
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# speed of the dinosaur and obstacles
jump_speed = 4
bush_speed = 3
rock_speed = 3

# create obstacles and set up position
initial_position = [SCREEN_WIDTH + 50, SCREEN_WIDTH + 400]
obstacles = [Bush(bush_speed, initial_position[0]), Rock(rock_speed, initial_position[1])]
obstacle_manager = ObstacleManager(obstacles)


def load_trex():
    global frame_index, last_update_time

    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > frame_delay:
        frame_index = (frame_index + 1) % frame_count
        last_update_time = current_time

    SCREEN.blit(frames[frame_index], (trex_x, trex_y))


def button(text, x, y, width, height):
    button_text = font.render(text, True, (0, 0, 0))
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    return button_text, text_rect


def update_game():
    global trex_y, jump, jump_height, score, background_x1, background_x2

    if jump:
        trex_y -= jump_speed
        jump_height += jump_speed
        if jump_height >= 80:
            jump = False
    else:
        if trex_y < SCREEN_HEIGHT - trex_height:
            trex_y += jump_speed
            jump_height -= jump_speed

    obstacle_manager.move_obstacles()

    for obstacle in obstacle_manager.obstacles:
        if obstacle.x + obstacle.width / 2 < trex_x and not obstacle.passed:
            score += 1
            obstacle.passed = True

    # adjust obstacles speed dynamically
    obstacle_manager.update_obstacle_speed(score)

    # move background
    background_x1 -= 5
    background_x2 -= 5
    if background_x1 < -SCREEN_WIDTH:
        background_x1 = SCREEN_WIDTH
    if background_x2 < -SCREEN_WIDTH:
        background_x2 = SCREEN_WIDTH


def reset_game():
    global trex_y, jump, jump_height, score
    trex_y = SCREEN_HEIGHT - trex_height
    jump = False
    jump_height = 0
    obstacle_manager.reset_obstacles()
    score = 0


def is_game_over(final_score):
    global game_over, running

    game_over_text = font.render(f"Game Over! Your score: {final_score}", True, (255, 0, 0))
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    restart_text, restart_rect = button("Restart", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    quit_text, quit_rect = button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)

    SCREEN.blit(restart_text, restart_rect)
    SCREEN.blit(quit_text, quit_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_over = False
                    return
                elif quit_rect.collidepoint(mouse_pos):
                    running = False
                    return


def main():
    global jump, running, game_over

    while running:
        SCREEN.blit(background_image, (background_x1, 0))
        SCREEN.blit(background_image, (background_x2, 0))

        if not game_over:
            load_trex()
            obstacle_manager.load_obstacles(SCREEN)
            update_game()

            # show score
            score_text = font.render(f'Score: {score}', True, (0, 0, 0))
            SCREEN.blit(score_text, (10, 10))

            if obstacle_manager.check_collisions(trex_x, trex_y, trex_width, trex_height):
                game_over = True
                pass

        else:
            is_game_over(score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        reset_game()
                        game_over = False
                    elif event.key == pygame.K_n:
                        running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if trex_y >= SCREEN_HEIGHT - trex_height:
                        jump = True

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
