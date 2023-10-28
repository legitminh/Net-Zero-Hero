import pygame

class Projetile:
  def __init__(self, x, y, dx, dy, damage):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.damage = damage
  def update(self, dt):
    self.x, self.y = self.x + self.dx * dt, self.y+ self.dy * dt
  def draw(self, screen):
    pygame.draw.circle(screen, 'white', [self.x, self.y], 3)
    

#PUT IN game.py #Update getpos so it get absolute pos
#Update enemy.()
