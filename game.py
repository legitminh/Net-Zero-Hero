from math import pi
from earth import Earth
from player import Player
from cloud import Cloud
import pygame

BG_COLOR = 'black'
MOVEMENT_AMOUNT = 2 * pi / 16


class Game:
    def __init__(self, screen, map, earth, player, *clouds):
        self.screen = screen
        self.Clock = pygame.time.Clock()
        self.frame_rate = 60
        self.map = map
        self.MAPSIZE = len(map)
        self.clouds = [cloud for cloud in clouds]
        self.earth = earth
        self.player = player

    def update(self, event, dt):
        if event.type == pygame.KEYDOWN:
            if pygame.key == pygame.K_Right:
                self.player.move(MOVEMENT_AMOUNT)
            elif pygame.key == pygame.K_Left:
                self.player.move(-MOVEMENT_AMOUNT)
        
            # if self.earth.is_collided_with()
        for cloud in self.clouds:
            cloud.update(dt)
        self.player.update(dt)
        print(dt)
        self.draw()
        
    
    def draw(self): #render everything
        # fill background
        self.screen.fill(BG_COLOR)

        self.earth.draw(self.screen, self.MAPSIZE)
        self.player.draw(self.screen, self.MAPSIZE)
        for cloud in self.clouds:
            cloud.draw(self.screen)
        self.Clock.tick(self.frame_rate)
        pygame.display.update()
    
    
    def make_text(self, x, y, what):
      font = pygame.font.SysFont('arial', int(10))
      text = font.render(str(what), True, 'black')
      text_rect = text.get_rect(center=(x, y))
      self.screen.blit(text, text_rect)