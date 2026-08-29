import pygame, math, time
from utils import scale_image, blit_rotate_center

TRACK = pygame.image.load("img/track.png")
TRACK_BORDER = pygame.image.load("img/track-border.png")
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
    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.x -= horizontal
        self.y -= vertical
    
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

class PlayerCar(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (180, 200)


def draw(win, images, player_car):
    win.fill((0,0,0))
    
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win)
    pygame.display.update()

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

pygame.quit()