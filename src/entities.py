import pygame

class Note:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class HoldNote(Note):
    def __init__(self, x, y, width, height, speed, duration):
        super().__init__(x, y, width, height, speed)
        self.duration = duration
        self.hold_rect = pygame.Rect(x, y, width, height * duration)
        self.is_being_held = False
        self.hold_progress = 0

    def update(self):
        super().update()
        self.hold_rect.y = self.rect.y

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 200, 0), self.hold_rect)  # Darker green for the hold part
        pygame.draw.rect(screen, (0, 255, 0), self.rect)  # Brighter green for the head

class Player:
    def __init__(self, x, y, width, height, move_area_start, move_area_end):
        self.rect = pygame.Rect(x, y, width, height)
        self.move_area_start = move_area_start
        self.move_area_end = move_area_end
        self.speed = 10

    def move(self, direction):
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed
        self.rect.x = max(self.move_area_start, min(self.move_area_end - self.rect.width, self.rect.x))

    def move_with_gyro(self, gyro_x):
        self.rect.x += gyro_x * -0.1  # Scale gyro input for gameplay
        self.rect.x = max(self.move_area_start, min(self.move_area_end - self.rect.width, self.rect.x))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 134, 116), self.rect)
