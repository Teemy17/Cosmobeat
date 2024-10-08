import pygame
import mpu6050
from gpiozero import Button, PWMLED

# GPIO setup
button_1 = Button(17)
button_2 = Button(26)
led_1 = PWMLED(12)
led_2 = PWMLED(16)
led_3 = PWMLED(20)
led_4 = PWMLED(21)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = -0.2
current_beat = 0
score = 0
beat_advance_frames = 30  # Number of frames to wait before advancing the beatmap
frame_counter = 0  # To count frames for beat advancement


# Playfield and colors
move_area_start = screen.get_width() * 0.25
move_area_end = screen.get_width() * 0.75
horizontal_line_color = (255, 255, 255)
bar_color = (255, 134, 116)
note_width = (move_area_end - move_area_start) / 20
active_notes = []

# Player initialization
initial_x = (move_area_start + move_area_end) / 2
initial_y = screen.get_height() * 0.85
player_pos = pygame.Rect(initial_x, initial_y, 100, 20)

#Beatmap and Note
def load_beatmap(filename='beatmap.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()
    beatmap = [[char == '0' for char in line.rstrip('\n')] for line in lines if line.strip() != '']
    return beatmap


class Note:
    def __init__(self, position, width):
        self.rect = pygame.Rect(position * width, 0, width, 20)
        self.active = True

    def update(self):
        self.rect.y += 5  # Move note down the screen

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

def spawn_notes(current_beat):
    print(f"Spawning notes for beat {current_beat}: {beatmap[current_beat]}")
    for i, has_note in enumerate(beatmap[current_beat]):
        if has_note:
            note_position = move_area_start + i * note_width
            active_notes.append(Note(note_position, note_width))
            print(f"Note spawned at position {i}, x-coord: {note_position}")



def update_notes():
    for note in active_notes:
        note.update()
        if note.rect.top > screen.get_height():
            active_notes.remove(note)

def handle_interactions():
    global score
    for note in active_notes:
        if note.rect.colliderect(player_pos) and note.active:
            if button_1.is_pressed or button_2.is_pressed:
                score += 1
                note.active = False  # Remove note after scoring
                print("Score:", score)

#Beatmap initilization
beatmap = load_beatmap()





# Sensor setup
mpu = mpu6050.mpu6050(0x68)

def read_sensor_data():
    """Gather data from the MPU6050 sensor."""
    return mpu.get_accel_data(), mpu.get_gyro_data(), mpu.get_temp()

def draw_game_area():
    """Draw the horizontal lines and vertical borders of the gameplay area."""
    line_thickness = 5
    pygame.draw.line(screen, horizontal_line_color, (move_area_start, player_pos.top), (move_area_end, player_pos.top), line_thickness)
    pygame.draw.line(screen, horizontal_line_color, (move_area_start, player_pos.bottom), (move_area_end, player_pos.bottom), line_thickness)
    pygame.draw.line(screen, bar_color, (move_area_start, 0), (move_area_start, screen.get_height()), line_thickness)
    pygame.draw.line(screen, bar_color, (move_area_end, 0), (move_area_end, screen.get_height()), line_thickness)

ellipse_visible = False


def update_leds():
    """Update the brightness of the LEDs based on the player's position."""
    # Calculate the position percentage across the movable area
    position = (player_pos.x - move_area_start) / (move_area_end - move_area_start)
    
    # Define LED activation ranges based on position
    led_1.value = max(0, 1 - abs(position - 0.125) * 8)
    led_2.value = max(0, 1 - abs(position - 0.375) * 8)
    led_3.value = max(0, 1 - abs(position - 0.625) * 8)
    led_4.value = max(0, 1 - abs(position - 0.875) * 8)

def check_button():
    global ellipse_visible
    ellipse_visible = button_1.is_pressed or button_2.is_pressed



while running:
    check_button()
    frame_counter += 1
    if frame_counter >= beat_advance_frames:
        frame_counter = 0
        current_beat += 1
        if current_beat >= len(beatmap):
            current_beat = 0
        spawn_notes(current_beat)

    handle_interactions()
    update_notes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        accel, gyro, temperature = read_sensor_data()
        gyro_x = gyro['x']
        player_pos.x += gyro_x * dt
        player_pos.x -= 0.6  # Assume this is some form of drag or friction
        player_pos.x = max(move_area_start, min(move_area_end - player_pos.width, player_pos.x))
    except Exception as e:
        print(f"Error reading MPU values: {e}")

    update_leds()

    screen.fill("black")
    draw_game_area()
    for note in active_notes:
        note.draw(screen)
    if ellipse_visible:
        pygame.draw.ellipse(screen, bar_color, (player_pos.x + 33, player_pos.y + 40, 30, 20))

    pygame.draw.rect(screen, bar_color, player_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

