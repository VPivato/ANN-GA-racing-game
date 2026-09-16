import pygame

class Checkpoint:
    def __init__(self, pos, size, angle=0):
        self.pos = pos
        
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((0, 220, 0, 255))
        self.rotated = pygame.transform.rotate(surface, angle)
        
        self.mask = pygame.mask.from_surface(self.rotated)
        self.rect = self.rotated.get_rect(center=pos)
    
    def draw(self, win):
        win.blit(self.rotated, self.rect)