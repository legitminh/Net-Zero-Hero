from cloud import Cloud
import pygame


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

    def draw(self, screen, map_size):
        pygame.draw.circle(screen, 'white', (screen.get_width() / 2, screen.get_height() / 2) , self.atmosphere_radius, width=1)
        screen.blit(self.image, [screen.get_width() / 2 - self.radius, screen.get_height() / 2 - self.radius])
    