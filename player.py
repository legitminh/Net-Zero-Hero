import pygame
from math import sin, cos, pi


class Player:
    def __init__(self, size, color, dist):
        self.dist = dist
        self.size = size
        self.color = color
        # self.image = pygame.Surface([size, size])
        # self.image.fill(color)
        # self.rect = self.image.get_rect()
        self.slot = 0

    def move(self, dir, map_size):
        self.slot += dir
        self.slot %= map_size

    def pos(self, map_size):
        x, y = cos(self.slot / map_size * 2 * pi ) * self.dist, sin(self.slot / map_size * 2 * pi ) * self.dist
        return (960 / 2 + x, 540 / 2 + y)

    def draw(self, screen, map_size):
        pygame.draw.circle(screen, self.color, self.pos(map_size), self.size, width=1)
