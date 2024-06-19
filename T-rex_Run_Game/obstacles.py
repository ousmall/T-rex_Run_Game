import pygame
import math
from random import randint


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400


class Obstacle:
    def __init__(self, image_path, speed, width, height, initial_x):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = initial_x
        self.y = SCREEN_HEIGHT - height
        self.speed = speed
        self.width = width
        self.passed = False

    def move(self):
        self.x -= self.speed
        if self.x < 0:
            self.reset_position()
            self.passed = False

    def reset_position(self):
        self.x = SCREEN_WIDTH + randint(200, 400)

    def load(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, trex_x, trex_y, trex_width, trex_height):
        distance = math.sqrt((self.x - trex_x) ** 2 + (self.y - trex_y) ** 2)
        if distance < 25:
            if self.x < trex_x + trex_width and self.x + self.image.get_width() > trex_x:
                if trex_y + trex_height > self.y:
                    return True
        return False


class Bush(Obstacle):
    def __init__(self, speed, initial_x):
        super().__init__('bush.png', speed, 30, 30, initial_x)


class Rock(Obstacle):
    def __init__(self, speed, initial_x):
        super().__init__('rock.png', speed, 50, 50, initial_x)


class ObstacleManager:
    def __init__(self, obstacles):
        self.obstacles = obstacles

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()

    def load_obstacles(self, screen):
        for obstacle in self.obstacles:
            obstacle.load(screen)

    def check_collisions(self, trex_x, trex_y, trex_width, trex_height):
        for obstacle in self.obstacles:
            if obstacle.check_collision(trex_x, trex_y, trex_width, trex_height):
                return True
        return False

    def reset_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.reset_position()
        # choose an obstacle randomly
        for i in range(len(self.obstacles)):
            if i > 0:
                while abs(self.obstacles[i].x - self.obstacles[i - 1].x) < 200:
                    self.obstacles[i].x = randint(SCREEN_WIDTH, SCREEN_WIDTH + 400)
            else:
                self.obstacles[i].x = randint(SCREEN_WIDTH, SCREEN_WIDTH + 400)

    def update_obstacle_speed(self, score):
        new_speed = 5 + score // 10  # Every 10 points, the speed increases by 1 unit.
        for obstacle in self.obstacles:
            obstacle.speed = new_speed