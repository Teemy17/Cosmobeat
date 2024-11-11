import pygame
import random
import button
from constants import MENU, GAME, RESULT, CONTROL
from constants import HORIZONTAL_LINE_COLOR, BAR_COLOR, HIT_COLOR
from entities import Player, Note, HoldNote, MoveNote
# from hardware import Hardware
from effects import Particle, HoldEffect, create_hit_effect_particle, update_particles, draw_particles, DiamondEffect, create_hit_effect_diamond, draw_diamond, update_diamond
from music_manager import MusicManager
from result_screen import ResultScreen

class Game:
    def __init__(self, width, height, screen_manager):
        pygame.init()
        self.screen_manager = screen_manager
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False

        self.music_manager = MusicManager()
        # Load song
        self.music_manager.load_song("song1", "../assets/freedom_dive.mp3")

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
        self.combo = 0
        self.highest_combo = 0
        self.diamond = []
        self.particles = []  # List to store all particles

        #counters
        self.perfect_count = 0
        self.great_count = 0
        self.good_count = 0
        self.miss_count = 0
        self.hold_count = 0
        self.drag_count = 0

        # time. x-position, and type
        # self.custom_note_pattern = [ 
        #     (3, self.move_area_start + 100, 'Note'),
        #     (50, self.move_area_start + 150, 'HoldNote', 3),  # Hold note with duration
        #     (100, self.move_area_start + 200, 'MoveNote'),  # Move note
        #     (150, self.move_area_start + 250, 'Note'),
        #     (200, self.move_area_start + 300, 'HoldNote', 4),  # Hold note with longer duration

        #      # Add more notes with timing, x-position, and type
        # ]

        # Define the edges of the move area
        left_edge = self.move_area_start
        right_edge = self.move_area_end
        center = (left_edge + right_edge) / 2
        quarter = left_edge + (right_edge - left_edge) * 0.25
        three_quarter = left_edge + (right_edge - left_edge) * 0.75

        # Define the pattern with (time, x-position, type, [optional duration])
        self.custom_note_pattern = [
            # Intro sequence
            (0, center, 'Note'),
            (30, quarter, 'Note'),
            (60, three_quarter, 'Note'),
            
            # Hold note sequence
            (120, left_edge + 100, 'HoldNote', 2),
            (180, right_edge - 100, 'HoldNote', 3),
            
            # Quick alternating pattern
            (300, quarter, 'Note'),
            (330, three_quarter, 'Note'),
            (360, quarter, 'Note'),
            (390, three_quarter, 'Note'),
            
            # Moving note challenge
            (450, left_edge + 200, 'MoveNote'),
            (510, right_edge - 200, 'MoveNote'),
            
            # Complex sequence
            (600, center, 'HoldNote', 4),
            (700, quarter, 'MoveNote'),
            (760, three_quarter, 'Note'),
            (790, center, 'Note'),
            (820, quarter, 'HoldNote' , 5),
            
            # Stair
            (900, left_edge + 100, 'Note'),
            (915, left_edge + 200, 'Note'),
            (930, left_edge + 300, 'Note'),
            (945, left_edge + 400, 'Note'),
            
            # Pattern
            (1000, center, 'HoldNote', 5),
            (1100, quarter, 'Note'),
            (1150, three_quarter, 'Note'),
            (1200, center, 'Note'),

            # Rapid Drag
            (1300, left_edge + 100, 'MoveNote'),
            (1310, left_edge + 200, 'MoveNote'),
            (1320, left_edge + 300, 'MoveNote'),
            (1330, left_edge + 400, 'MoveNote'),

            (1340, right_edge - 100, 'MoveNote'),
            (1350, right_edge - 200, 'MoveNote'),
            (1360, right_edge - 300, 'MoveNote'),
            (1370, right_edge - 400, 'MoveNote'),
            (1380, right_edge - 500, 'MoveNote'),

            # Stairs
            (1400, left_edge + 100, 'Note'),
            (1420, left_edge + 200, 'Note'),
            (1440, left_edge + 300, 'Note'),
            (1460, left_edge + 400, 'Note'),

            (1480, right_edge - 100, 'Note'),
            (1500, right_edge - 200, 'Note'),
            (1520, right_edge - 300, 'Note'),
            (1540, right_edge - 400, 'Note'),
            (1560, right_edge - 500, 'Note'),

            # Hold Note
            (1700, center, 'HoldNote', 5),
            (1800, quarter, 'HoldNote', 5),
            (1900, three_quarter, 'HoldNote', 6),
            (2000, center, 'HoldNote',7),
            (2100, quarter, 'HoldNote', 5),
            (2200, three_quarter, 'HoldNote', 9),

            # Move Note
            (2300, left_edge + 100, 'MoveNote'),
            (2320, left_edge + 200, 'MoveNote'),
            (2340, left_edge + 300, 'MoveNote'),
            (2360, left_edge + 400, 'MoveNote'),

            (2380, right_edge - 100, 'MoveNote'),
            (2400, right_edge - 200, 'MoveNote'),
            (2420, right_edge - 300, 'MoveNote'),
            (2440, right_edge - 400, 'MoveNote'),
            (2460, right_edge - 500, 'MoveNote'),

            # Spam
            (2500, center, 'Note'),
            (2520, center, 'Note'),
            (2540, center, 'Note'),
            (2560, center, 'Note'),
            (2580, center, 'Note'),

            # Alternating 2
            (2600, quarter, 'Note'),
            (2620, three_quarter, 'Note'),
            (2640, quarter, 'Note'),
            (2660, three_quarter, 'Note'),

            # Complex sequence
            (2700, center, 'HoldNote', 4),
            (2800, quarter, 'MoveNote'),
            (2860, three_quarter, 'Note'),
            (2900, center, 'Note'),
            (3000, quarter, 'HoldNote' , 5),

            # Notes sequence
            (3100, left_edge + 100, 'Note'),
            (3150, right_edge - 100, 'Note'),
            (3200, left_edge + 200, 'Note'),
            (3250, right_edge - 200, 'Note'),
            (3300, left_edge + 300, 'Note'),
            (3350, right_edge - 300, 'Note'),
            (3400, left_edge + 400, 'Note'),
            (3450, right_edge - 400, 'Note'),

            # Note sequence
            (3500, center, 'HoldNote', 7),
            (3600, quarter, 'Note'),
            (3650, three_quarter, 'Note'),
            (3700, center, 'Note'),

            # Rapid Drag
            (3750, left_edge + 100, 'MoveNote'),
            (3760, left_edge + 200, 'MoveNote'),
            (3770, left_edge + 300, 'MoveNote'),
            (3780, left_edge + 400, 'MoveNote'),

            (3790, right_edge - 100, 'MoveNote'),
            (3800, right_edge - 200, 'MoveNote'),
            (3810, right_edge - 300, 'MoveNote'),
            (3820, right_edge - 400, 'MoveNote'),
            (3830, right_edge - 500, 'MoveNote'),

        ]


        # Initialize buttons
        play_img = pygame.image.load("../assets/play_button.png").convert_alpha()
        control_img = pygame.image.load("../assets/control_button.png").convert_alpha()
        quit_img = pygame.image.load("../assets/quit_button.png").convert_alpha()
        resume_img = pygame.image.load("../assets/resume_button.png").convert_alpha()
        
        # Store buttons as instance attributes
        self.play_button = button.Button(520, 285, play_img, 0.45)
        self.control_button = button.Button(520, 415, control_img, 0.45)
        self.main_menu_quit_button = button.Button(520, 545, quit_img, 0.45)
        self.pause_quit_button = button.Button(520, 450, quit_img, 0.45)
        self.resume_button = button.Button(520, 300, resume_img, 0.45)


    def update_player_with_sensor(self):
        gyro_data = self.hardware.sensor.get_gyro_data()
        self.player.move_with_gyro(gyro_data['x'])

    def check_button_presses(self):
        if self.hardware.button_1.is_pressed or self.hardware.button_2.is_pressed:
            self.check_note_hit(True)

    def update_leds_based_on_position(self):
        position = (self.player.rect.x - self.move_area_start) / (self.move_area_end - self.move_area_start)
        self.hardware.led_1.value = max(0, 1 - abs(position - 0.125) * 8)
        self.hardware.led_2.value = max(0, 1 - abs(position - 0.375) * 8)
        self.hardware.led_3.value = max(0, 1 - abs(position - 0.625) * 8)
        self.hardware.led_4.value = max(0, 1 - abs(position - 0.875) * 8)

    def reset_game(self, width, height):
        # Reset game state
        self.pause = False
        self.notes = []  # Clear notes to prevent immediate ending
        self.feedback = ""
        self.feedback_time = 0
        self.hit_effect_time = 0
        self.combo = 0
        self.highest_combo = 0
        self.diamond = []
        self.particles = []

        # Reset counters
        self.perfect_count = 0
        self.great_count = 0
        self.good_count = 0
        self.miss_count = 0
        self.hold_count = 0
        self.drag_count = 0

        # Reset player position and movement area
        self.move_area_start = width * 0.25
        self.move_area_end = width * 0.75
        initial_x = (self.move_area_start + self.move_area_end) / 2
        initial_y = height * 0.85
        self.player = Player(initial_x, initial_y, 100, 20, self.move_area_start, self.move_area_end)

        # Reset any timers or spawn-related settings
        self.note_spawn_timer = 0
        self.note_spawn_interval = 30  # Reset spawn interval if needed

        # Reset the score
        self.score = 0


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
        elif 0.6 <= random.random() >= 0.3:
            self.notes.append(MoveNote(x, 0, 50, 50, self.note_speed))
        else:
            self.notes.append(Note(x, 0, 50, 20, self.note_speed))

    def spawn_custom_note_pattern(self):
            # Check if there are notes to spawn at the current time
        for note_data in self.custom_note_pattern[:]:  # Iterate over the pattern
            time, x, note_type, *extra = note_data  # Unpack note data
            if self.note_spawn_timer == time:
                # Spawn the note based on type
                if note_type == 'Note':
                    self.notes.append(Note(x, 0, 50, 20, self.note_speed))
                elif note_type == 'HoldNote':
                    duration = extra[0] if extra else 3  # Default to 3 if not specified
                    self.notes.append(HoldNote(x, 0, 50, 20, self.note_speed, duration))
                elif note_type == 'MoveNote':
                    self.notes.append(MoveNote(x, 0, 50, 50, self.note_speed))
                # Remove from pattern list once spawned
                self.custom_note_pattern.remove(note_data)

    def update_notes(self):
        for note in self.notes[:]:
            note.update()
            if note.rect.y > self.screen.get_height():
                self.notes.remove(note)
                self.score -= 10
                self.feedback = "Miss!"
                self.feedback_time = 30
                self.combo = 0
                self.miss_count += 1
                # self.hardware.buzzer.beep(0.1, 0, 1) #Uncomment to make buzzer buss
             

    def check_note_hit(self, is_key_pressed):
        hit_range = self.player.rect.width / 1.5  # Base hit range
        perfect_range = hit_range / 4  # Narrowest range for a perfect hit
        great_range = hit_range / 2    # Mid-range for a great hit

        for note in self.notes[:]:
            if self.hit_area.colliderect(note.rect):
                note_center = note.rect.centerx     
                player_center = self.player.rect.centerx
                distance = abs(note_center - player_center)

                if distance <= hit_range:
                    # Handle HoldNote differently from normal notes
                    if isinstance(note, HoldNote):
                        if is_key_pressed:
                            if not note.is_being_held:  # Start the hold
                                note.is_being_held = True
                                self.combo += 1
                                self.score += 50  # Initial hit score

                            # Generate hold effect trail while being held
                            create_hit_effect_diamond(note.rect.centerx, note.rect.centery, "Perfect", self.diamond)

                            note.hold_progress += 1
                            if note.hold_progress >= note.duration:
                                self.notes.remove(note)
                                self.score += 50  # Completion bonus
                                self.combo += 1
                                self.feedback = "Perfect Hold!"
                                self.feedback_time = 30
                                self.hit_effect_time = 10
                                self.hold_count += 1
                                create_hit_effect_diamond(note.rect.centerx, note.rect.centery, "Perfect", self.diamond)
                        else:
                            if note.is_being_held:
                                note.is_being_held = False  # End hold if key is released
                    elif isinstance(note, MoveNote):
                            self.score += 50  # Increase score for a successful alignment
                            self.feedback = "Perfect Drag"
                            create_hit_effect_particle(note.rect.centerx, note.rect.centery, "Perfect", self.particles)
                            self.combo += 1
                            self.drag_count += 1
                            self.feedback_time = 30
                            self.hit_effect_time = 10
                            self.notes.remove(note)  # Remove MoveNote after successful hit
                    else:
                        if is_key_pressed:
                            hit_type = None
                            if distance <= perfect_range:
                                self.score += 150
                                self.perfect_count += 1
                                self.feedback = "Perfect!"
                                hit_type = "Perfect"
                            elif distance <= great_range:
                                self.score += 100
                                self.great_count += 1
                                self.feedback = "Great!"
                                hit_type = "Great"
                            else:
                                self.score += 50
                                self.good_count += 1
                                self.feedback = "Good!"
                                hit_type = "Good"

                            # Create hit effect particles
                            create_hit_effect_diamond(note.rect.centerx, note.rect.centery, hit_type, self.diamond)

                            # Set feedback display time and remove note
                            self.feedback_time = 30
                            self.hit_effect_time = 10
                            self.combo += 1
                            if self.combo > self.highest_combo:
                                self.highest_combo = self.combo
                            self.notes.remove(note)
                return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if self.screen_manager.current_screen == GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                        if self.pause:
                            self.music_manager.pause()
                        else:
                            self.music_manager.resume()
                    elif event.key == pygame.K_UP:
                        current_volume = pygame.mixer.music.get_volume()
                        self.music_manager.set_volume(min(1.0, current_volume + 0.1))
                    elif event.key == pygame.K_DOWN:
                        current_volume = pygame.mixer.music.get_volume()
                        self.music_manager.set_volume(max(0.0, current_volume - 0.1))
        
        if self.screen_manager.current_screen == GAME and not self.pause:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                self.player.move('left')
            if keys[pygame.K_RIGHT]:
                self.player.move('right')
                
            is_key_pressed = keys[pygame.K_SPACE]
            self.check_note_hit(is_key_pressed) 
                    
    def main_menu(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 150)
        text = font.render("Cosmobeat", True, (255, 255, 255))
        
        if self.play_button.draw(self.screen):
            self.screen_manager.change_screen(GAME)
            self.reset_game(1280, 720)
            self.music_manager.play("song1")

        if self.control_button.draw(self.screen):
            self.screen_manager.change_screen(CONTROL)
        
        if self.main_menu_quit_button.draw(self.screen):
            self.running = False
        
        self.screen.blit(text, (370, 100))
        pygame.display.flip()

        return True
    
    def draw_pause_screen(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 150)
        text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (470, 100))

        if self.resume_button.draw(self.screen):
            self.pause = False
            self.music_manager.resume()

        if self.pause_quit_button.draw(self.screen):
            self.screen_manager.change_screen(MENU)

        pygame.display.flip()

    def controls_screen(self):
        self.screen.fill("black")

        font = pygame.font.Font(None, 60)
        text = font.render("Keyboard Controls", True, (255, 255, 255))
        self.screen.blit(text, (450, 100))

        control_img = pygame.image.load("../assets/controls.png").convert_alpha()
        control_img = pygame.transform.scale(control_img, (800, 400))  # Resize the image to desired dimensions
        self.screen.blit(control_img, (280, 170))

        back_img = pygame.image.load("../assets/back_button.png").convert_alpha()
        back_button = button.Button(520, 600, back_img, 0.45)

        if back_button.draw(self.screen):
            self.screen_manager.change_screen(MENU)
        
        pygame.display.flip()

    def update(self):
        self.note_spawn_timer += 1
        # if self.note_spawn_timer >= self.note_spawn_interval:
        #     self.spawn_note()
        #     self.note_spawn_timer = 0
        self.spawn_custom_note_pattern()
        self.update_notes()
        # self.update_player_with_sensor()
        # self.check_button_presses()
        # self.update_leds_based_on_position()
        update_diamond(self.diamond)  # Update diamonds
        update_particles(self.particles)


    def draw(self):
        self.screen.fill("black")
        self.draw_game_area()
        pygame.draw.rect(self.screen, (100, 100, 100), self.hit_area)
        self.player.draw(self.screen)
        for note in self.notes:
            note.draw(self.screen)

        # Draw particles after other elements
        draw_diamond(self.screen, self.diamond)  # Draw particles from effects.py
        draw_particles(self.screen, self.particles)

        # Draw score and feedback
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.feedback_time > 0:
            feedback_text = self.font.render(self.feedback, True, (255, 255, 255))
            self.screen.blit(feedback_text, (self.screen.get_width() // 2 - 50, 100))
            self.feedback_time -= 1
            
        if self.combo > 0:
            combo_text = self.font.render(f"Combo: {self.combo}", True, (255, 255, 255))
            self.screen.blit(combo_text, (self.screen.get_width() // 2 - 50, 70))  # Position above feedback


    def run(self):
        while self.running:
            self.handle_events()
            if self.screen_manager.current_screen == MENU:
                if not self.main_menu():
                    self.running = False
            elif self.screen_manager.current_screen == CONTROL:
                self.controls_screen()
            if self.screen_manager.current_screen == GAME:
                if not self.pause:
                    self.update()
                    self.draw()
                
                    if not pygame.mixer.music.get_busy() and not self.pause:
                        self.result_screen = ResultScreen(self.screen, self.screen_manager, {
                            'score': self.score,
                            'perfect_count': self.perfect_count,
                            'great_count': self.great_count,
                            'good_count': self.good_count,
                            'miss_count': self.miss_count,
                            'hold_count': self.hold_count,
                            'drag_count': self.drag_count,
                            'highest_combo': self.highest_combo
                        })
                        self.screen_manager.change_screen(RESULT)
                else:
                    self.draw_pause_screen()

            elif self.screen_manager.current_screen == RESULT:
                self.result_screen.draw()

            pygame.display.flip()
            self.clock.tick(60)

        self.music_manager.stop()
        pygame.quit()