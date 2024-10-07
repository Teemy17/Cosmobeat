import pygame
import time
import mpu6050

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.1

# Set initial position of the player circle at the center
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Initialize the MPU6050 sensor
mpu = mpu6050.mpu6050(0x68)

def read_sensor_data():
    """Read data from the MPU6050 sensor."""
    accelerometer_data = mpu.get_accel_data()
    gyroscope_data = mpu.get_gyro_data()
    temperature = mpu.get_temp()
    return accelerometer_data, gyroscope_data, temperature

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Try to get sensor data
    try:
        accel, gyro, temperature = read_sensor_data()
        print("accel : ", accel)
        print("gyro: ", gyro)
        print("temp: ", temperature)
        
        # Use gyroscope data to move the circle
        gyro_x = gyro['x']  # Rotational velocity around x-axis
        gyro_y = gyro['y']  # Rotational velocity around y-axis

        # Adjust the player position based on gyro data
        player_pos.x += gyro_x * dt
        player_pos.y -= gyro_y * dt  # Subtract because screen y-coordinates increase downwards

    except Exception as e:
        print("Error reading MPU values: ", e)

    # Fill the screen with a color to wipe away the last frame
    screen.fill("purple")

    # Draw the circle at the new player position
    pygame.draw.circle(screen, "red", (int(player_pos.x), int(player_pos.y)), 40)

    # Update the display
    pygame.display.flip()

    # Limit FPS to 60,
