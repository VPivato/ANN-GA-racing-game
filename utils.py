import pygame, math

def scale_image(image, factor):
    size = round(image.get_width() * factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, size)

def normalize_angle(angle):
    angle = math.radians(angle)
    if angle < 0:
        angle = 2 * math.pi + angle
    return angle