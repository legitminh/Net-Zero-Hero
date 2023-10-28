from cloud import Cloud
import pygame


class Earth:
    def __init__(self, radius, atmosphere_radius, hp, path):
        self.radius = radius
        self.atmosphere_radius = atmosphere_radius
        self.hp = hp #global population
        self.path = path
        self.image = pygame.Surface.convert_alpha(pygame.image.load(path))
        self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        
    def is_collided_with(self, cloud) -> bool:
        return cloud.dist <= self.atmosphere_radius

    def draw(self, screen):
        screen.blit(self.image, [screen.get_width / 2, screen.get_height / 2])
    