import pygame
import mpu6050

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = -0.2  # Adjust the direction of movement if needed.

# Define the bounds for the movable area and colors
move_area_start = screen.get_width() * 0.25  # Start 25% from the left
move_area_end = screen.get_width() * 0.75   # End 75% from the left
horizontal_line_color = (255, 255, 255)  # White
border_color = (255, 134, 116)  # Salmon pink

# Set initial position of the rectangular player within the defined bounds
initial_x = (move_area_start + move_area_end) / 2
initial_y = screen.get_height() * 0.85  # Positioned lower on the screen, adjusted here
player_pos = pygame.Rect(initial_x, initial_y, 100, 20)  # Rectangular player size: 100x20

# Initialize the MPU6050 sensor
mpu = mpu6050.mpu6050(0x68)

def read_sensor_data():
    """Read data from the MPU6050 sensor."""
    accelerometer_data = mpu.get_accel_data()
    gyroscope_data = mpu.get_gyro_data()
    temperature = mpu.get_temp()
    return accelerometer_data, gyroscope_data, temperature

def draw_game_area():
    """Draw two horizontal lines and vertical borders."""
    line_thickness = 5
    # Draw the top and bottom lines for the player area
    pygame.draw.line(screen, horizontal_line_color, (move_area_start, player_pos.top), (move_area_end, player_pos.top), line_thickness)
    pygame.draw.line(screen, horizontal_line_color, (move_area_start, player_pos.bottom), (move_area_end, player_pos.bottom), line_thickness)
    # Draw vertical borders extending to the top of the screen
    pygame.draw.line(screen, border_color, (move_area_start, 0), (move_area_start, screen.get_height()), line_thickness)
    pygame.draw.line(screen, border_color, (move_area_end, 0), (move_area_end, screen.get_height()), line_thickness)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Try to get sensor data
    try:
        accel, gyro, temperature = read_sensor_data()
        # Use gyroscope data to move the character along the x-axis
        gyro_x = gyro['x']
        player_pos.x += gyro_x * dt
        player_pos.x -= 0.6
        # Ensure the character stays within the defined bounds
        player_pos.x = max(move_area_start, min(move_area_end - player_pos.width, player_pos.x))

    except Exception as e:
        print("Error reading MPU values: ", e)

    # Fill the screen with a color or background image
    screen.fill("black")  # Optional: Load a dynamic background image

    # Draw the game area with lane and borders
    draw_game_area()

    # Draw the rectangle player at the new position
    pygame.draw.rect(screen, "red", player_pos)

    # Update the display
    pygame.display.flip()

    # Limit FPS to 60
    clock.tick(60)

pygame.quit()
