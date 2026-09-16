import pygame
from utils import scale_image

TRACK = pygame.image.load("img/track.png")
TRACK_BORDER = pygame.image.load("img/track-border.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = scale_image(pygame.image.load("img/finish.png"), 0.85)
FINISH_MASK = pygame.mask.from_surface(FINISH)