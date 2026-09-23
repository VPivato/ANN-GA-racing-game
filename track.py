import pygame
from utils import scale_image

TRACK = pygame.image.load("src/img/track.png")
TRACK_BORDER = pygame.image.load("src/img/track-border.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = scale_image(pygame.image.load("src/img/finish.png"), 0.85)
FINISH_MASK = pygame.mask.from_surface(FINISH)

def check_border_collision(object):
    """Checa colisão com a borda da pista, 'object.destroyed = True' se colidiu.
    Assume que a pista começa em (0, 0)"""
    
    if not object.destroyed and object.collide(TRACK_BORDER_MASK) is not None:
        object.destroyed = True

def check_finish_collision(object, x=155, y=250):
    """Checa colisão com a linha de chegada. Destrói o objeto se cruzar a linha pelo lado errado."""
    obj_finish_colision = object.collide(FINISH_MASK, x=x, y=y)
    if obj_finish_colision is not None and obj_finish_colision[1] == 0: # Destroi o objeto se ele cruzar a linha de chegada pela direção errada.
        object.destroyed = True
    if not object.destroyed and obj_finish_colision is not None and obj_finish_colision[1] > 0: # Compleção do percurso.
        object.finished = True