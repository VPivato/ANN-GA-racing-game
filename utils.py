import pygame, math

def scale_image(image, factor):
    size = round(image.get_width() * factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, size)

def get_direction(angle):
        radians = math.radians(angle)
        return pygame.Vector2(math.sin(radians), math.cos(radians))