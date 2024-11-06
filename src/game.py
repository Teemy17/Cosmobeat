import pygame
import random
import button
from constants import MENU, GAME
from constants import HORIZONTAL_LINE_COLOR, BAR_COLOR, HIT_COLOR
from entities import Player, Note, HoldNote
from menu import main_menu
# from hardware import Hardware

class Game:
    def __init__(self, width, height, screen_manager):
        pygame.init()
        self.screen_manager = screen_manager
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False

        # self.hardware = Hardware()
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

        self.reset_game(1280, 720)

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

    def reset_game(self, width, height):
        self.pause = False
        self.score = 0
        self.notes = []
        self.feedback = ""
        self.feedback_time = 0
        self.hit_effect_time = 0
        self.move_area_start = width * 0.25
        self.move_area_end = width * 0.75
        initial_x = (self.move_area_start + self.move_area_end) / 2
        initial_y = height * 0.85
        self.player = Player(initial_x, initial_y, 100, 20, self.move_area_start, self.move_area_end)

    def draw_game_area(self):
        line_thickness = 5
        pygame.draw.line(self.screen, HORIZONTAL_LINE_COLOR, (self.move_area_start, self.player.rect.top), (self.move_area_end, self.player.rect.top), line_thickness)
        pygame.draw.line(self.screen, HORIZONTAL_LINE_COLOR, (self.move_area_start, self.player.rect.bottom), (self.move_area_end, self.player.rect.bottom), line_thickness)
        pygame.draw.line(self.screen, BAR_COLOR, (self.move_area_start, 0), (self.move_area_start, self.screen.get_height()), line_thickness)
        pygame.draw.line(self.screen, BAR_COLOR, (self.move_area_end, 0), (self.move_area_end, self.screen.get_height()), line_thickness)

    def spawn_note(self):
        x = random.uniform(self.move_area_start, self.move_area_end - 50)
        if random.random() < 0.3:  # 30% chance to spawn a hold note
            duration = random.randint(2, 5)  # Hold duration between 2 and 5 units
            self.notes.append(HoldNote(x, 0, 50, 20, self.note_speed, duration))
        else:
            self.notes.append(Note(x, 0, 50, 20, self.note_speed))

    def update_notes(self):
        for note in self.notes[:]:
            note.update()
            if note.rect.y > self.screen.get_height():
                self.notes.remove(note)
                self.score -= 10
                self.feedback = "Miss!"
                self.feedback_time = 30

    def check_note_hit(self, is_key_pressed):
        hit_range = self.player.rect.width / 2
        for note in self.notes[:]:
            if self.hit_area.colliderect(note.rect):
                note_center = note.rect.centerx
                player_center = self.player.rect.centerx
                if abs(note_center - player_center) <= hit_range:
                    # Handle HoldNote differently from normal notes
                    if isinstance(note, HoldNote):
                        if is_key_pressed:
                            if not note.is_being_held:  # Start the hold
                                note.is_being_held = True
                                self.score += 50  # Initial hit score
                            note.hold_progress += 1
                            if note.hold_progress >= note.duration:
                                self.notes.remove(note)  # Remove note when fully held
                                self.score += 50  # Completion bonus
                                self.feedback = "Perfect Hold!"
                                self.feedback_time = 30
                                self.hit_effect_time = 10
                        else:
                            if note.is_being_held:  # Stop the hold if key is released
                                note.is_being_held = False
                    else:
                        # For normal notes, just check the spacebar press
                        if is_key_pressed:
                            self.notes.remove(note)
                            self.score += 100
                            self.feedback = "Perfect!"
                            self.feedback_time = 30
                            self.hit_effect_time = 10
                return  # Exit after hitting a note to avoid multiple hits in one frame

    def handle_events(self):
        is_key_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause
        
        # Check if spacebar is being held down
        if not self.pause:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                is_key_pressed = True # set to true if spacebar is pressed

            if keys[pygame.K_LEFT]:
                self.player.move('left')
            if keys[pygame.K_RIGHT]:
                self.player.move('right')
        
        # Pass the state to check if a note is hit
        self.check_note_hit(is_key_pressed)
    
    def draw_pause_screen(self):
        self.screen.fill("black")

        font = pygame.font.Font(None, 150)
        text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (470, 100))

        resume_img = pygame.image.load("assets/resume_button.png").convert_alpha()
        quit_img = pygame.image.load("assets/quit_button.png").convert_alpha()

        resume_button = button.Button(520, 285, resume_img, 0.45)
        quit_button = button.Button(520, 415, quit_img, 0.45)

        if resume_button.draw(self.screen):
            self.pause = False
        if quit_button.draw(self.screen):
            self.screen_manager.change_screen(MENU)

        pygame.display.flip()

    def update(self):
        self.note_spawn_timer += 1
        if self.note_spawn_timer >= self.note_spawn_interval:
            self.spawn_note()
            self.note_spawn_timer = 0
        self.update_notes()
        # self.update_player_with_sensor()
        # self.check_button_presses()
        # self.update_leds_based_on_position()

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
            if self.screen_manager.current_screen == MENU:
                if not main_menu(self.screen, self.screen_manager):
                    self.running = False
                elif self.screen_manager.current_screen == GAME:
                    self.reset_game(1280, 720)  
            elif self.screen_manager.current_screen == GAME:
                self.handle_events()
                if not self.pause:
                    self.update()
                    self.draw()
                else:
                    self.draw_pause_screen()
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
