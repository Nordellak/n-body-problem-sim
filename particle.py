import pygame
import math
from random import randint

VELOCITY_SCALE = 50
SIZE_SCALE = 1/3
GRAVITY_CONSTANT = 5


class Particle:
    def __init__(self, game, pos, velocity_pos, mass):
        self.game = game
        self.pos = pos
        self.velocity = ((pos[0] - velocity_pos[0]) / VELOCITY_SCALE, (pos[1] - velocity_pos[1]) / VELOCITY_SCALE)
        self.mass = mass
        self.force = (0, 0)
        self.radius = 2 * self.mass ** SIZE_SCALE
        self.to_delete = False
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.orbit = []

    def collided_with(self, other):
        distance = math.sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)
        return distance < self.radius + other.radius

    def calculate_gravity_from(self, other):
        distance_squared = (self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2
        force = GRAVITY_CONSTANT * self.mass * other.mass / distance_squared

        direction = (other.pos[0] - self.pos[0], other.pos[1] - self.pos[1])
        direction_scale = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        direction = (direction[0] / direction_scale, direction[1] / direction_scale)

        force_x = self.force[0] + force * direction[0]
        force_y = self.force[1] + force * direction[1]
        self.force = (force_x, force_y)

    def update(self, orbit_length):
        while len(self.orbit) > orbit_length:
            self.orbit.pop(0)
        self.orbit.append((self.pos[0], self.pos[1]))

        vx = self.velocity[0] + self.force[0] / self.mass
        vy = self.velocity[1] + self.force[1] / self.mass
        x = self.pos[0] + vx
        y = self.pos[1] + vy

        self.pos = (x, y)
        self.velocity = (vx, vy)
        self.force = (0, 0)

    def render(self):
        for i in range(len(self.orbit)):
            if i == 0:
                continue
            pygame.draw.line(self.game.screen, self.color, self.orbit[i], self.orbit[i - 1])

        pygame.draw.circle(self.game.screen, self.color, self.pos, self.radius)
