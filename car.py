import pygame, math
from utils import scale_image, blit_rotate_center

WHITE_CAR = scale_image(pygame.image.load("img/white-car.png"), .55)


class AbstractCar:
    def __init__(self, max_vel, rotation_vel, acceleration=.1):
        self.img = self.IMG
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = acceleration
        self.destroyed = False
    
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def rotate(self, left=False, right=False):
        if self.destroyed:
            return
        
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    
    def move(self):
        if self.destroyed:
            return
        
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.x -= horizontal
        self.y -= vertical
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    
    def collide(self, mask, x=0, y=0):
        if self.destroyed:
            return
        
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset) # point of intersection
        return poi
    
    

class PlayerCar(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (180, 200)