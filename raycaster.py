import pygame, math
from utils import normalize_angle

FOV = 160
NUM_RAYS = 8

class Ray:
    def __init__(self, angle, car):
        self.rayAngle = normalize_angle(angle)
        self.car = car
    
    def cast(self):
        pass
    
    def draw(self, win, ray_color=(255,0,0)):
        pygame.draw.line(
            win, ray_color,
            self.car.rotated_rect.center,
            self.car.rotated_rect.center - pygame.Vector2(math.sin(self.rayAngle) * 50, math.cos(self.rayAngle) * 50)
        )


class Raycaster:
    def __init__(self, player):
        self.rays = []
        self.player = player
    
    def cast_all_rays(self):
        self.rays = []
        rayAngle = (self.player.angle - FOV / 2)
        for i in range(NUM_RAYS):
            ray = Ray(rayAngle, self.player)
            ray.cast()
            self.rays.append(ray)
            
            rayAngle += FOV / NUM_RAYS
    
    def draw(self, win):
        for ray in self.rays:
            ray.draw(win)