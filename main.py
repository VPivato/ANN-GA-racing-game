import pygame, math, time
from utils import scale_image, blit_rotate_center

TRACK = pygame.image.load("img/track.png")
TRACK_BORDER = pygame.image.load("img/track-border.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("img/finish.png")
WHITE_CAR = scale_image(pygame.image.load("img/white-car.png"), .55)

WIDTH, HEIGTH = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("ANN + GA Racing Game")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
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


def draw(win, images, player_car):
    win.fill((0,0,0))
    
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    pygame.display.update()

def player_movement(player_car):
    keys = pygame.key.get_pressed()
    moving = False
    
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moving = True
        player_car.move_forward()
    
    if not moving:
        player_car.reduce_speed()

run = True
clock = pygame.time.Clock()
player_car = PlayerCar(4, 4)
images = [(TRACK, (0,0))]

while run:
    clock.tick(FPS)
    
    draw(WINDOW, images, player_car)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    player_movement(player_car)
    
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.destroyed = True

pygame.quit()