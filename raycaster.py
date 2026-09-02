import pygame, numpy as np
from utils import get_direction
from track import TRACK_BORDER_MASK

FOV = 160
NUM_RAYS = 8
MAX_DISTANCE = 100
RAY_STEP = 4

# np.array booleano
border_array = pygame.surfarray.array2d(TRACK_BORDER_MASK.to_surface(setcolor=(255,255,255,255), unsetcolor=(0,0,0,0))) != 0

class Ray:
    def __init__(self, angle, car):
        self.ray_angle = angle
        self.car = car
    
    def cast(self):
        origin = self.car.rotated_rect.center
        direction = get_direction(self.ray_angle)
        
        steps = np.arange(0, MAX_DISTANCE, RAY_STEP)
        xs = (origin[0] - direction.x * steps).astype(int)
        ys = (origin[1] - direction.y * steps).astype(int)
        
        valid = (xs >= 0) & (xs < border_array.shape[0]) & (ys >= 0) & (ys < border_array.shape[1])
        xs, ys, steps = xs[valid], ys[valid], steps[valid]
        
        hits = border_array[xs, ys]
        
        self.distance = steps[np.argmax(hits)] if hits.any() else MAX_DISTANCE
    
    def draw(self, win, ray_color):
        pygame.draw.line(
            win, ray_color,
            self.car.rotated_rect.center,
            self.car.rotated_rect.center - get_direction(self.ray_angle) * self.distance
        )


class Raycaster:
    def __init__(self, car):
        self.rays = []
        self.car = car
    
    def cast_all_rays(self):
        self.rays = []
        ray_angle = (self.car.angle - FOV / 2)
        for i in range(NUM_RAYS):
            ray = Ray(ray_angle, self.car)
            ray.cast()
            self.rays.append(ray)
            
            ray_angle += FOV / NUM_RAYS
    
    def draw(self, win, ray_color):
        for ray in self.rays:
            ray.draw(win, ray_color)