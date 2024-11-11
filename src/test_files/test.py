import pygame
import random

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Playfield and colors
move_area_start = screen.get_width() * 0.25
move_area_end = screen.get_width() * 0.75
horizontal_line_color = (255, 255, 255)
bar_color = (255, 134, 116)
note_color = (0, 255, 0)
hit_color = (255, 255, 0)  # Color for hit effect

# Player initialization
initial_x = (move_area_start + move_area_end) / 2
initial_y = screen.get_height() * 0.85
player_pos = pygame.Rect(initial_x, initial_y, 100, 20)

# Note initialization
notes = []
note_speed = 5
current_time = 0
note_spawn_timer = 0
note_spawn_interval = 30  # Spawn a note every 60 frames (1 second)

# Score and feedback
score = 0
feedback = ""
feedback_time = 0
font = pygame.font.Font(None, 36)

# Hit detection
hit_area = pygame.Rect(move_area_start, player_pos.y - 20, move_area_end - move_area_start, 40)
hit_effect_time = 0

# Custom note pattern
note_pattern = [
    (60, 0.2), (90, 0.8), (120, 0.5), (150, 0.3), (180, 0.7),
    (210, 0.2), (240, 0.8), (270, 0.5), (300, 0.3), (330, 0.7),
    (360, 0.2), (390, 0.8), (420, 0.5), (450, 0.3), (480, 0.7),
    # Add more notes as needed
]


def draw_game_area():
    """Draw the horizontal lines and vertical borders of the gameplay area."""
    line_thickness = 5
    pygame.draw.line(screen, horizontal_line_color, (move_area_start, player_pos.top), (move_area_end, player_pos.top), line_thickness)
    pygame.draw.line(screen, horizontal_line_color, (move_area_start, player_pos.bottom), (move_area_end, player_pos.bottom), line_thickness)
    pygame.draw.line(screen, bar_color, (move_area_start, 0), (move_area_start, screen.get_height()), line_thickness)
    pygame.draw.line(screen, bar_color, (move_area_end, 0), (move_area_end, screen.get_height()), line_thickness)

def spawn_note(x_percent): # add param x_percent if custom note pattern is used 
    """Spawn a new note at the specified x position within the move area."""
    x = move_area_start + (move_area_end - move_area_start) * x_percent
    notes.append(pygame.Rect(x, 0, 50, 20))

    # spawn note ramdomly
    # x = random.uniform(move_area_start, move_area_end - 50)  # 50 is the note width
    # notes.append(pygame.Rect(x, 0, 50, 20))

def update_notes():
    """Move notes down the screen and remove ones that are out of bounds."""
    global score, feedback, feedback_time
    for note in notes[:]:
        note.y += note_speed
        if note.y > screen.get_height():
            notes.remove(note)
            score -= 10
            feedback = "Miss!"
            feedback_time = 30

def check_note_hit():
    """Check if the player has hit any notes in the hit area and within the player's range."""
    global score, feedback, feedback_time, hit_effect_time
    hit_range = player_pos.width / 2  # Define the range within which a hit is valid
    for note in notes[:]:
        if hit_area.colliderect(note):
            # Check if the note is within the player's hit range
            note_center = note.centerx
            player_center = player_pos.centerx
            if abs(note_center - player_center) <= hit_range:
                notes.remove(note)
                score += 100
                feedback = "Perfect!"
                feedback_time = 30
                hit_effect_time = 10
                return
    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                check_note_hit()

    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 5
    if keys[pygame.K_RIGHT]:
        player_pos.x += 5

    # Keep player within bounds
    player_pos.x = max(move_area_start, min(move_area_end - player_pos.width, player_pos.x))

    # Spawn notes based on the pattern
    for note_time, note_x in note_pattern:
        if current_time == note_time:
            spawn_note(note_x)

    # note_spawn_timer += 1
    # if note_spawn_timer >= note_spawn_interval:  
    #     spawn_note()
    #     note_spawn_timer = 0

    # Update notes
    update_notes()

    # Redraw the screen
    screen.fill("black")
    draw_game_area()
    
    # Draw hit area
    pygame.draw.rect(screen, (100, 100, 100), hit_area)
    
    # Draw player
    pygame.draw.rect(screen, bar_color, player_pos)

    # Draw notes
    for note in notes:
        pygame.draw.rect(screen, note_color, note)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw feedback
    if feedback_time > 0:
        feedback_text = font.render(feedback, True, (255, 255, 255))
        screen.blit(feedback_text, (screen.get_width() // 2 - 50, 50))
        feedback_time -= 1

    # Draw hit effect
    if hit_effect_time > 0:
        pygame.draw.rect(screen, hit_color, hit_area, 3)
        hit_effect_time -= 1

    pygame.display.flip()
    clock.tick(60)
    current_time += 1

pygame.quit()