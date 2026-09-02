import pygame, numpy as np
from car import PlayerCar, ComputerCar
from track import TRACK, TRACK_BORDER_MASK

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ANN + GA Racing Game")

FPS = 60

def draw(win, images, player_car, computer_car):
    win.fill((0,0,0))
    
    for img, pos in images:
        win.blit(img, pos)
    
    player_car.draw(win, show_mask=False, show_rect=False, show_rays=False)
    computer_car.draw(win, show_mask=False, show_rect=False, show_rays=True)
    pygame.display.update()

def player_movement(player_car):
    keys = pygame.key.get_pressed()
    moving = False
    
    if keys[pygame.K_SPACE]:
        computer_car.decision()
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
computer_car = ComputerCar(4, 4)
images = [(TRACK, (0,0))]

while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    # Atualiza o estado do carro e só depois desenha
    player_movement(player_car)
    player_car.update_car()
    computer_car.update_car()
    
    draw(WINDOW, images, player_car, computer_car)
    
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.destroyed = True

pygame.quit()