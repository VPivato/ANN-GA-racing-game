import pygame, numpy as np
from raycaster import Raycaster
from utils import scale_image, get_direction

WHITE_CAR = scale_image(pygame.image.load("img/white-car.png"), .55)
RED_CAR = scale_image(pygame.image.load("img/red-car.png"), .55)


class AbstractCar:
    def __init__(self, max_vel, rotation_vel, acceleration=.1):
        self.img = self.IMG
        
        self.pos = pygame.Vector2(self.START_POS)
        
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.acceleration = acceleration
        
        self.vel = 0
        self.angle = 0
        
        self.destroyed = False
        
        self.raycaster = Raycaster(self)
        
        self.update_car()
    
    def update_car(self):
        self.rotated_image = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.img.get_rect(topleft=self.pos).center)
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.raycaster.cast_all_rays()
    
    def draw(self, win, show_mask=False, show_rect=False, show_rays=False, mask_color=(255,0,0), rect_color=(255,0,0), ray_color=(255,0,0)):
        win.blit(self.rotated_image, self.rotated_rect.topleft)
        
        if show_mask:
            # mask.to_surface é uma operação custosa, desligar quando houver muitos carros
            win.blit(self.mask.to_surface(setcolor=mask_color, unsetcolor=(0,0,0,0)), self.rotated_rect.topleft)
        if show_rect:
            pygame.draw.rect(win, rect_color, self.rotated_rect, 2)
        if show_rays:
            self.raycaster.draw(win, ray_color)

    def rotate(self, left=False, right=False):
        if self.destroyed:
            return
        
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        
        self.angle %= 360
    
    def move(self):
        if self.destroyed:
            return
        
        self.pos -= get_direction(self.angle) * self.vel
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    
    def collide(self, mask, x=0, y=0):
        if self.destroyed:
            return
        
        offset = (int(self.rotated_rect.x - x), int(self.rotated_rect.y - y))
        return mask.overlap(self.mask, offset)
    
    def get_sensor_readings(self):
        return np.array([float(ray.distance) for ray in self.raycaster.rays])


class PlayerCar(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (205, 200)


class ComputerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (165, 200)
    
    def decision(self):
        choices = [self.move_forward,
                   lambda: self.rotate(left=True),
                   lambda: self.rotate(right=True)
        ]
        
        choice = np.random.choice(choices)
        choice()
            