import pygame
from math import sin, cos, pi


class Player:
    def __init__(self, size, color, dist):
        self.dist = dist
        self.size = size
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.slot = 0

    def move(self, dir, map_size):
        self.slot += dir
        self.slot %= map_size

    def pos(self, map_size):
        return cos(self.slot / map_size) * self.dist, sin(self.slot / map_size) * self.dist

    def update(self, dt):
        pass

    def draw(self, screen, map_size):
        pygame.draw.circle(screen, 'white', self.pos(map_size), self.size, width=1)
