import pygame
from math import sin, cos


class Cloud:
    def __init__(self, dist, angle, speed, size):
        self.dist = dist
        self.angle = angle
        self.speed = speed
        self.size = size

    def move(self, distance): #move certain distance
        self.dist += distance
    
    def update(self, dt):
        self.move(-1 * dt * self.speed)

    def pos(self):
        return cos(self.angle) * self.dist, sin(self.angle) * self.dist

    def draw(self, screen):
        absolutePos = self.pos()[0]+ screen.get_width()/2, self.pos()[1] + screen.get_height()/2
        pygame.draw.circle(screen, 'white', absolutePos , self.size, width=1)
