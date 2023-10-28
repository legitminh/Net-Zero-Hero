import pygame
from math import sin, cos


class Cloud:
    def __init__(self, dist, angle, speed, size):
        self.dist = dist
        self.angle = angle
        self.speed = speed
        self.size = size

    def move(self, dist):
        self.dist -= dist
    
    def update(self, dt):
        self.move(dt * self.speed)

    def pos(self):
        return cos(self.angle) * self.dist, sin(self.angle) * self.dist

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.pos, self.size, width=1)
