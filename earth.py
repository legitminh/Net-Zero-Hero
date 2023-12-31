import pygame
from math import sin, cos, pi
from sys import exit


class Earth:
    def __init__(self, radius, atmosphere_radius, hp, path):
        self.radius = radius
        self.atmosphere_radius = atmosphere_radius
        self.hp = hp #global population
        self.path = path
        self.image = pygame.Surface.convert_alpha(pygame.image.load(path))
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        
    def is_collided_with(self, cloud) -> bool:
        return cloud.dist <= self.atmosphere_radius

    def make_text(self, x, y, what, size, screen):
        font = pygame.font.SysFont('arial', int(size))
        text = font.render(str(what), True, 'black')
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        
    def draw(self, screen, map):
        if self.hp <= 0:
            exit()
        for i, slot in enumerate(map):
            x, y = cos(i/len(map) * 2 * pi) * (self.radius+20) + (960 /2), sin(i/len(map) * 2* pi) * (self.radius+20) + (540 /2)
            convert = {
                '': 'dark blue',
                'tree': 'green',
                'wind': 'white',
                'dac': 'purple',
                'solar': 'yellow',
                'nuclear': 'blue',
            }
            pygame.draw.circle(screen, convert[slot[0]], [x, y], 10)
            self.make_text(x, y, f'L{slot[1]}', 10, screen)
        pygame.draw.circle(screen, 'white', (screen.get_width() / 2, screen.get_height() / 2) , self.atmosphere_radius, width=1)
        screen.blit(self.image, [screen.get_width() / 2 - self.radius, screen.get_height() / 2 - self.radius])
    