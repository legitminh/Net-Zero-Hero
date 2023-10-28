import pygame
from math import sin, cos, pi

class Cloud:
    def __init__(self, ATMOS_SIZE, dist, angle, speed, size, hp):
        self.ATMOS_SIZE = ATMOS_SIZE
        self.dist = dist
        self.angle = angle
        self.speed = speed
        self.size = size
        self.hp = hp

    def move(self, distance): #move certain distance
        self.dist += distance
    
    def update(self, dt):
        self.move(-1 * self.speed * dt)
        if self.dist <= self.ATMOS_SIZE:
            return True

    def pos(self):
        relativePos = cos(self.angle * 2 * pi) * self.dist, sin(self.angle * 2 * pi) * self.dist
        absolutePos = relativePos[0] + 960/2, relativePos[1] + 540/2
        return absolutePos
    def damage(self, damage):
        self.hp -= damage
    def draw(self, screen):
        def make_text(x, y, what):
            font = pygame.font.SysFont('arial', int(10))
            text = font.render(str(what), True, 'white')
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

        # absolutePos = self.pos()[0] + screen.get_width()/2, self.pos()[1] + screen.get_height()/2
        absolutePos = self.pos()
        pygame.draw.circle(screen, 'white', absolutePos , self.size, width=1)
        make_text( absolutePos[0], absolutePos[1], self.hp)



