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

def get_checkpoints():
    return [Checkpoint((197.5, 149.5), (83.2, 5), 3.4),
            Checkpoint((158.0, 89.5), (84.2, 5), 60.1),
            Checkpoint((93.0, 98.5), (80.5, 5), 118.2),
            Checkpoint((67.5, 156.0), (85.4, 5), 174.6),
            Checkpoint((68.0, 245.0), (82.0, 5), 180.0),
            Checkpoint((68.0, 466.5), (86.0, 5), -180),
            Checkpoint((91.0, 556.0), (83.7, 5), -139.8),
            Checkpoint((190.0, 655.5), (81.3, 5), -133.5),
            Checkpoint((318.5, 789.0), (88.2, 5), -125.3),
            Checkpoint((418.5, 801.0), (95.0, 5), -53.1),
            Checkpoint((451.5, 721.5), (85.1, 5), -2.0),
            Checkpoint((455.5, 607.5), (84.2, 5), -20.2),
            Checkpoint((507.5, 544.0), (86.3, 5), -64.6),
            Checkpoint((606.5, 543.5), (86.7, 5), -101.3),
            Checkpoint((665.5, 621.5), (89.8, 5), -161.2),
            Checkpoint((667.5, 737.0), (85.0, 5), -178.7),
            Checkpoint((767.0, 812.5), (80.6, 5), -78.6),
            Checkpoint((822.0, 725.0), (82.0, 5), -1.4),
            Checkpoint((821.5, 480.5), (83.1, 5), -2.1),
            Checkpoint((761.0, 406.0), (85.9, 5), 77.9),
            Checkpoint((513.0, 406.5), (85.0, 5), -90.0),
            Checkpoint((448.0, 344.5), (80.0, 5), 179.3),
            Checkpoint((519.5, 291.0), (82.0, 5), 90.7),
            Checkpoint((765.5, 289.5), (83.0, 5), -89.3),
            Checkpoint((823.0, 186.5), (84.0, 5), -0.7),
            Checkpoint((801.5, 99.0), (82.9, 5), 48.4),
            Checkpoint((684.5, 85.5), (85.0, 5), 89.3),
            Checkpoint((389.0, 88.5), (85.0, 5), -90.0),
            Checkpoint((313.5, 141.5), (91.7, 5), -18.4),
            Checkpoint((313.0, 380.0), (82.0, 5), 0.0),
            Checkpoint((254.0, 457.5), (87.0, 5), -90.0),
            Checkpoint((194.0, 368.0), (90.0, 5), 180.0)]