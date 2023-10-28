from math import pi, cos, sin
from earth import Earth
from player import Player
from cloud import Cloud
import sys
import pygame
import random
from projectile import Projetile

BG_COLOR = (0,0,64)
MOVEMENT_AMOUNT = 1


class Game:
    def __init__(self, screen, map, earth, player, menu, *clouds):
        self.projectiles = []
        self.screen = screen
        self.Clock = pygame.time.Clock()
        self.frame_rate = 60
        self.map = map
        self.MAPSIZE = len(self.map)
        self.clouds = [cloud for cloud in clouds]
        self.earth = earth
        self.player = player
        self.menu = menu
        self.playerCash = 8 #units in billion dollars
    
    def purchase(self, loc, thing, price):
        if self.playerCash < price: return 
        if self.map[self.player.slot] != thing:
            # if ( self.map[loc] == thing): 
            #     self.map[loc] == self.map[loc]
            self.map[loc] = (thing, 1)
            self.playerCash -= price
        else:
            self.map[loc] = (thing, self.map[loc][1] + 1)
            self.playerCash -= price

        
        print(self.map)

    def perSecondUpdate(self):
        for i, tower in enumerate(self.map):
            x, y = cos(i/len(self.map) * 2 * pi) * (self.earth.radius+20) + (960 /2), sin(i/len(self.map) * 2* pi) * (self.earth.radius+20) + (540 /2)
            if tower == ('', 0): pass
            elif tower[0] == "solar":
                self.playerCash += tower[1] // 2
            elif tower[0] == "wind":
                angle = i/self.MAPSIZE * 2 * pi
                self.projectiles.append(
                    Projetile( 
                        x, 
                        y, 
                        cos(angle + (random.random()-0.5)) * 20 , 
                        sin(angle + (random.random()-0.5)) * 20, tower[1] )
                    )
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.move(1, self.MAPSIZE)
                elif event.key == pygame.K_LEFT:
                    self.player.move(-1, self.MAPSIZE)
                print(event.key == pygame.K_LEFT)
                if (self.menu.update(event)):#if action is chose
                    self.purchase(self.player.slot, *self.menu.update(event))
        #update tower abilities
        
                 

        
            # if self.earth.is_collided_with()
        for cloud in self.clouds:
            if (cloud.update(dt)):
                self.clouds.remove(cloud)
                self.earth.hp-=1
            if cloud.hp <= 0:
                self.clouds.remove(cloud)
                
                
        # self.player.update(dt)
        

        def distance(x1, y1, x2, y2):
            return ( (x2-x1)**2 + (y2-y1)**2) ** 0.5
            
        #projectile shooting
        to_remove = []
        
        for projectile in self.projectiles:
            #remove out of boudn
            if abs(projectile.x) > self.screen.get_width() or abs(projectile.y) > self.screen.get_height(): 
                to_remove.append(projectile)   
            #remove colision
            for enemy in self.clouds:
                if distance(projectile.x, projectile.y, enemy.pos()[0], enemy.pos()[1]) < enemy.size:
                    enemy.damage(projectile.damage)
                    to_remove.append(projectile)   
            projectile.update(dt)
                    
        
        for i in to_remove:
            self.projectiles.remove(i)
                
    
    def draw(self): #render everything
        # fill background
        self.screen.fill(BG_COLOR)

        self.earth.draw(self.screen, self.map)
        self.player.draw(self.screen, self.MAPSIZE)
        for cloud in self.clouds:
            cloud.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        self.menu.draw()
        self.Clock.tick(self.frame_rate)
        self.draw_hp()
        self.draw_cash()
        pygame.display.update()
        

    def add_cloud(self, cloud):
        self.clouds.append(cloud)

    def make_text(self, x, y, what, size):
        font = pygame.font.SysFont('arial', int(size))
        text = font.render(str(what), True, 'white')
        text_rect = text.get_rect(topright=(x, y))
        self.screen.blit(text, text_rect)
        
    def draw_hp(self):

        self.make_text(960 - 10, 10, f'Hp: {self.earth.hp}', 20)
    
    def draw_cash(self):
        self.make_text(960 - 10, 30, f'Cash: ${self.playerCash} B', 20)
