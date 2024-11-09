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

def create_hit_effect_particle(x, y, hit_type, particles):
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


class DiamondEffect:
    def __init__(self, x, y, initial_size, growth_rate, lifetime, color):
        self.x = x
        self.y = y
        self.size = initial_size
        self.growth_rate = growth_rate
        self.lifetime = lifetime
        self.current_lifetime = lifetime
        self.color = color

    def update(self):
        # Increase size and reduce lifetime to create expanding effect
        self.size += self.growth_rate
        self.current_lifetime -= 1

    def draw(self, screen):
        if self.current_lifetime > 0:
            # Calculate alpha based on remaining lifetime
            alpha = int(255 * (self.current_lifetime / self.lifetime))
            color_with_alpha = (*self.color[:3], alpha)  # Add calculated alpha to the color

            # Create a surface with alpha support and draw diamond shape
            diamond_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.polygon(
                diamond_surface, color_with_alpha,
                [(self.size // 2, 0), (self.size, self.size // 2), (self.size // 2, self.size), (0, self.size // 2)]
            )
            # Position and blit the diamond shape onto the main screen
            screen.blit(diamond_surface, (self.x - self.size // 2, self.y - self.size // 2))


def create_hit_effect_diamond(x, y, hit_type, effects):
    # Customize the diamonds' initial size, growth, and lifetime based on hit type
    initial_size = 10
    growth_rate = 3
    lifetime = 20  # Adjust lifetime for a burst effect

    # Determine color based on hit type
    if hit_type == "Perfect":
        color = (255, 255, 255)  # White
    elif hit_type == "Great":
        color = (0, 0, 139)  # Dark blue
    else:  # Good
        color = (255, 0, 0)  # Red

    # Generate multiple diamonds to create an explosive burst effect
    for _ in range(5):  # Number of diamonds per hit
        effects.append(DiamondEffect(x, y, initial_size, growth_rate, lifetime, color))


def update_diamond(effects):
    for effect in effects[:]:
        effect.update()
        if effect.current_lifetime <= 0:
            effects.remove(effect)


def draw_diamond(screen, effects):
    for effect in effects:
        effect.draw(screen)



