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

# Playfield and colors
move_area_start = screen.get_width() * 0.25
move_area_end = screen.get_width() * 0.75
horizontal_line_color = (255, 255, 255)
bar_color = (255, 134, 116)

# Player initialization
initial_x = (move_area_start + move_area_end) / 2
initial_y = screen.get_height() * 0.85
player_pos = pygame.Rect(initial_x, initial_y, 100, 20)




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
    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read sensor data and update position
    try:
        accel, gyro, temperature = read_sensor_data()
        gyro_x = gyro['x']
        player_pos.x += gyro_x * dt
        player_pos.x -= 0.6
        player_pos.x = max(move_area_start, min(move_area_end - player_pos.width, player_pos.x))
    except Exception as e:
        print(f"Error reading MPU values: {e}")

    # Update LED brightness based on the character's position
    update_leds()


  
    # Redraw the screen
    screen.fill("black")
    draw_game_area()
    if ellipse_visible:
        pygame.draw.ellipse(screen, bar_color, (player_pos.x + 33, player_pos.y + 40, 30, 20))  # Draw an ellipse 40 pixels taller than the bar
    
    pygame.draw.rect(screen, bar_color, player_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
