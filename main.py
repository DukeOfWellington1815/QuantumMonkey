import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
PARTICLE_COLOR = (0, 0, 255)
GRAVITY = .5

# Particle class
class Particle:
    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.velocity_x = 0
        self.velocity_y = 0

    def apply_force(self, force_x, force_y):
        acceleration_x = force_x / self.mass
        acceleration_y = force_y / self.mass
        self.velocity_x += acceleration_x
        self.velocity_y += acceleration_y

    def update(self):
        self.velocity_y += GRAVITY

        if self.x > SCREEN_WIDTH / 2 and self.y >= SCREEN_HEIGHT - self.x:
            self.velocity_y -= GRAVITY * self.mass * 0.5

        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity_y = -self.velocity_y * 0.7

        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.velocity_y = -self.velocity_y * 0.7

        if self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.velocity_x = -self.velocity_x * 0.7

        if self.x + self.radius < 0:
            self.x = self.radius
            self.velocity_x = -self.velocity_x * 0.7

    def check_collision(self, other_particle):
        distance = ((self.x - other_particle.x)**2 + (self.y - other_particle.y)**2)**0.5
        return distance <= self.radius + other_particle.radius

    def handle_collision(self, other_particle):
        relative_velocity_x = other_particle.velocity_x - self.velocity_x
        relative_velocity_y = other_particle.velocity_y - self.velocity_y

        distance = ((self.x - other_particle.x)**2 + (self.y - other_particle.y)**2)**0.5

        if distance == 0:
            return  # Avoid division by zero

        overlap = self.radius + other_particle.radius - distance

        if overlap > 0:
            # Move particles away from each other
            self.x -= overlap * (self.x - other_particle.x) / distance
            self.y -= overlap * (self.y - other_particle.y) / distance
            other_particle.x += overlap * (self.x - other_particle.x) / distance
            other_particle.y += overlap * (self.y - other_particle.y) / distance

        normal_x = (other_particle.x - self.x) / distance
        normal_y = (other_particle.y - self.y) / distance

        dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

        impulse = (2 * dot_product) / (self.mass + other_particle.mass)

        impulse_x = impulse * normal_x
        impulse_y = impulse * normal_y

        self.velocity_x += impulse_x / self.mass
        self.velocity_y += impulse_y / self.mass
        other_particle.velocity_x -= impulse_x / other_particle.mass
        other_particle.velocity_y -= impulse_y / other_particle.mass

        damping = 0.98
        self.velocity_x *= damping
        self.velocity_y *= damping
        other_particle.velocity_x *= damping
        other_particle.velocity_y *= damping

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Physics Engine")

particles = [Particle(400, 100, 20, 1)]

# Initialize the clock
clock = pygame.time.Clock()

# Game loop
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            particles.append(Particle(x, y, 20, 1))

    for particle in particles:
        particle.apply_force(0, GRAVITY * particle.mass)
        particle.update()

    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            particle_a = particles[i]
            particle_b = particles[j]
            if particle_a.check_collision(particle_b):
                particle_a.handle_collision(particle_b)

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.line(screen, (0, 0, 0), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 2)

    for particle in particles:
        particle.apply_force(0, GRAVITY * particle.mass)
        particle.update()

        pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle.x), int(particle.y)), particle.radius)

    fps = int(clock.get_fps())
    font = pygame.font.Font(None, 36)
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    fps_rect = fps_text.get_rect()
    fps_rect.topleft = (10, 10)
    screen.blit(fps_text, fps_rect)

    pygame.display.flip()
