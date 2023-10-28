import pygame
from math import sin, cos, pi


class Cloud:
    def __init__(self, ATMOS_SIZE, dist, angle, speed, size):
        self.ATMOS_SIZE = ATMOS_SIZE
        self.dist = dist
        self.angle = angle
        self.speed = speed
        self.size = size

    def move(self, distance): #move certain distance
        self.dist += distance
    
    def update(self, dt):
        self.move(-1 * self.speed * dt)
        if self.dist <= self.ATMOS_SIZE:
            return True


    def pos(self):
        return cos(self.angle * 2 * pi) * self.dist, sin(self.angle * 2 * pi) * self.dist

    def draw(self, screen):
        absolutePos = self.pos()[0] + screen.get_width()/2, self.pos()[1] + screen.get_height()/2
        pygame.draw.circle(screen, 'white', absolutePos , self.size, width=1)
