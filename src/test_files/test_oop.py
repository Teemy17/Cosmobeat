import pygame
import random

class Note:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 134, 116), self.rect)

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Playfield and colors
        self.move_area_start = width * 0.25
        self.move_area_end = width * 0.75
        self.horizontal_line_color = (255, 255, 255)
        self.bar_color = (255, 134, 116)
        self.hit_color = (255, 255, 0)

        # Player initialization
        initial_x = (self.move_area_start + self.move_area_end) / 2
        initial_y = height * 0.85
        self.player = Player(initial_x, initial_y, 100, 20, self.move_area_start, self.move_area_end)

        # Note initialization
        self.notes = []
        self.note_speed = 5
        self.current_time = 0
        self.note_spawn_timer = 0
        self.note_spawn_interval = 30

        # Custom note pattern
        # Format: (time, x_position)
        # time is in frames (60 frames = 1 second)
        # x_position is between 0 (left) and 1 (right) of the move area
        # note_pattern = [
        #     (60, 0.2), (90, 0.8), (120, 0.5), (150, 0.3), (180, 0.7),
        #     (210, 0.2), (240, 0.8), (270, 0.5), (300, 0.3), (330, 0.7),
        #     (360, 0.2), (390, 0.8), (420, 0.5), (450, 0.3), (480, 0.7),
        #     # Add more notes as needed
        # ]  

        # Score and feedback
        self.score = 0
        self.feedback = ""
        self.feedback_time = 0
        self.font = pygame.font.Font(None, 36)

        # Hit detection
        self.hit_area = pygame.Rect(self.move_area_start, self.player.rect.y - 20, self.move_area_end - self.move_area_start, 40)
        self.hit_effect_time = 0

    def draw_game_area(self):
        line_thickness = 5
        pygame.draw.line(self.screen, self.horizontal_line_color, (self.move_area_start, self.player.rect.top), (self.move_area_end, self.player.rect.top), line_thickness)
        pygame.draw.line(self.screen, self.horizontal_line_color, (self.move_area_start, self.player.rect.bottom), (self.move_area_end, self.player.rect.bottom), line_thickness)
        pygame.draw.line(self.screen, self.bar_color, (self.move_area_start, 0), (self.move_area_start, self.screen.get_height()), line_thickness)
        pygame.draw.line(self.screen, self.bar_color, (self.move_area_end, 0), (self.move_area_end, self.screen.get_height()), line_thickness)

    def spawn_note(self): # add param x_percent if custom note pattern is used
        # Spawn notes based on the pattern
        # for note_time, note_x in note_pattern:
        #     if current_time == note_time:
        #         spawn_note(note_x)
        # Spawn a new note at a random x position within the move area
        x = random.uniform(self.move_area_start, self.move_area_end - 50)
        self.notes.append(Note(x, 0, 50, 20, self.note_speed))

    def update_notes(self):
        for note in self.notes[:]:
            note.update()
            if note.rect.y > self.screen.get_height():
                self.notes.remove(note)
                self.score -= 10
                self.feedback = "Miss!"
                self.feedback_time = 30

    def check_note_hit(self):
        # Check if any note is within the hit area
        hit_range = self.player.rect.width / 2
        for note in self.notes[:]:
            if self.hit_area.colliderect(note.rect):
                note_center = note.rect.centerx
                player_center = self.player.rect.centerx
                if abs(note_center - player_center) <= hit_range:
                    self.notes.remove(note)
                    self.score += 100
                    self.feedback = "Perfect!"
                    self.feedback_time = 30
                    self.hit_effect_time = 10
                    return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.check_note_hit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('left')
        if keys[pygame.K_RIGHT]:
            self.player.move('right')

    def update(self):
        self.note_spawn_timer += 1
        if self.note_spawn_timer >= self.note_spawn_interval:
            self.spawn_note()
            self.note_spawn_timer = 0

        self.update_notes()

    def draw(self):
        self.screen.fill("black")
        self.draw_game_area()
        pygame.draw.rect(self.screen, (100, 100, 100), self.hit_area)
        self.player.draw(self.screen)

        for note in self.notes:
            note.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.feedback_time > 0:
            feedback_text = self.font.render(self.feedback, True, (255, 255, 255))
            self.screen.blit(feedback_text, (self.screen.get_width() // 2 - 50, 50))
            self.feedback_time -= 1

        if self.hit_effect_time > 0:
            pygame.draw.rect(self.screen, self.hit_color, self.hit_area, 3)
            self.hit_effect_time -= 1

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            self.current_time += 1

        pygame.quit()

if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()