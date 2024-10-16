import pygame
import random
from constants import HORIZONTAL_LINE_COLOR, BAR_COLOR, HIT_COLOR
from entities import Player, Note
from hardware import Hardware

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.hardware = Hardware()
        self.move_area_start = width * 0.25
        self.move_area_end = width * 0.75
        initial_x = (self.move_area_start + self.move_area_end) / 2
        initial_y = height * 0.85

        self.player = Player(initial_x, initial_y, 100, 20, self.move_area_start, self.move_area_end)
        self.notes = []
        self.note_speed = 5
        self.note_spawn_timer = 0
        self.note_spawn_interval = 30
        self.score = 0
        self.feedback = ""
        self.feedback_time = 0
        self.font = pygame.font.Font(None, 36)
        self.hit_area = pygame.Rect(self.move_area_start, self.player.rect.y - 20, self.move_area_end - self.move_area_start, 40)
        self.hit_effect_time = 0

    def update_player_with_sensor(self):
        gyro_data = self.hardware.sensor.get_gyro_data()
        self.player.move_with_gyro(gyro_data['x'])

    def check_button_presses(self):
        if self.hardware.button_1.is_pressed or self.hardware.button_2.is_pressed:
            self.check_note_hit()

    def update_leds_based_on_position(self):
        position = (self.player.rect.x - self.move_area_start) / (self.move_area_end - self.move_area_start)
        self.hardware.led_1.value = max(0, 1 - abs(position - 0.125) * 8)
        self.hardware.led_2.value = max(0, 1 - abs(position - 0.375) * 8)
        self.hardware.led_3.value = max(0, 1 - abs(position - 0.625) * 8)
        self.hardware.led_4.value = max(0, 1 - abs(position - 0.875) * 8)

    def draw_game_area(self):
        line_thickness = 5
        pygame.draw.line(self.screen, HORIZONTAL_LINE_COLOR, (self.move_area_start, self.player.rect.top), (self.move_area_end, self.player.rect.top), line_thickness)
        pygame.draw.line(self.screen, HORIZONTAL_LINE_COLOR, (self.move_area_start, self.player.rect.bottom), (self.move_area_end, self.player.rect.bottom), line_thickness)
        pygame.draw.line(self.screen, BAR_COLOR, (self.move_area_start, 0), (self.move_area_start, self.screen.get_height()), line_thickness)
        pygame.draw.line(self.screen, BAR_COLOR, (self.move_area_end, 0), (self.move_area_end, self.screen.get_height()), line_thickness)

    def spawn_note(self):
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
        self.update_player_with_sensor()
        self.check_button_presses()
        self.update_leds_based_on_position()

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
            pygame.draw.rect(self.screen, HIT_COLOR, self.hit_area, 3)
            self.hit_effect_time -= 1

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()