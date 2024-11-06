# effects.py
import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, size, speed, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed = speed
        self.lifetime = lifetime  # How long the particle should last
        self.age = 0  # Track how long the particle has existed

        # Randomize direction for explosion effect
        self.angle = random.uniform(0, 2 * 3.14159)
        self.velocity_x = self.speed * random.uniform(0.5, 1) * math.cos(self.angle)
        self.velocity_y = self.speed * random.uniform(0.5, 1) * math.sin(self.angle)

    def update(self):
        # Move the particle
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.age += 1
        # Gradually shrink and fade the particle
        self.size = max(0, self.size - 0.1)
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            # Draw the particle with current size and color
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

def create_hit_effect(x, y, hit_type, particles):
    # Define colors and properties based on hit type
    if hit_type == "Perfect":
        color = (0, 255, 0)
        size = 8
        speed = 2
    elif hit_type == "Great":
        color = (255, 255, 0)
        size = 6
        speed = 1.5
    else:  # Good
        color = (0, 0, 255)
        size = 4
        speed = 1

    lifetime = 30
    # Create particles and add them to the particles list
    for _ in range(10):
        particles.append(Particle(x, y, color, size, speed, lifetime))
        
class HoldEffect:
    def __init__(self, x, y, color, particles):
        self.x = x
        self.y = y
        self.color = color
        self.particles = particles

    def generate_trail(self):
        # Continuously generate particles for a trail effect
        for _ in range(3):  # Spawn multiple particles per frame for denser effect
            size = random.uniform(2, 4)
            speed = random.uniform(0.5, 1.0)
            lifetime = random.randint(20, 30)
            self.particles.append(Particle(self.x, self.y, self.color, size, speed, lifetime))

def update_particles(particles):
    for particle in particles[:]:
        particle.update()
        if particle.lifetime <= 0:
            particles.remove(particle)

def draw_particles(screen, particles):
    for particle in particles:
        particle.draw(screen)
