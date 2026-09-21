import pygame, json, numpy as np
from car import PlayerCar, ComputerCar
from track import TRACK, TRACK_BORDER_MASK, FINISH, FINISH_MASK
from checkpoint import Checkpoint
from genetic_algorithm import GeneticAlgorithm

pygame.init()

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ANN + GA Racing Game")
font = pygame.font.SysFont("arial", 80)

FPS = 60
MAX_GENERATION_FRAMES = 5 * FPS
generation_frame_count = 0
current_generation = 0

def draw(win, images, player_car, car_population):
    win.fill((0,0,0))
    
    for img, pos in images:
        win.blit(img, pos)
    
    for checkp in checkpoints:
        checkp.draw(win)
    
    player_car.draw(win, show_mask=False, show_rect=False, show_rays=False)
    
    for car in car_population:
        car.draw(win, show_mask=False, show_rect=False, show_rays=False)
    
    label = font.render(f"Gen {current_generation}", 1, (255, 255, 255, 255))
    win.blit(label, (10, HEIGHT - 90))
    pygame.display.update()

def player_movement(player_car):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        player_car.rotate(-1)
    if keys[pygame.K_d]:
        player_car.rotate(1)
    if keys[pygame.K_w]:
        player_car.accelerate(1)
    if keys[pygame.K_s]:
        player_car.brake(1)
    
    player_car.reduce_speed()
    player_car.move()

run = True
clock = pygame.time.Clock()
player_car = PlayerCar()
images = [(TRACK, (0,0)),
          (FINISH, (155, 250))]
checkpoints = [Checkpoint((197.5, 149.5), (83.2, 5), 3.4),
               Checkpoint((158.0, 89.5), (84.2, 5), 60.1),
               Checkpoint((93.0, 98.5), (80.5, 5), 118.2),
               Checkpoint((67.5, 156.0), (85.4, 5), 174.6),
               Checkpoint((68.0, 245.0), (82.0, 5), 180.0),
               Checkpoint((68.0, 466.5), (86.0, 5), -180),
               Checkpoint((91.0, 556.0), (83.7, 5), -139.8),
               Checkpoint((190.0, 655.5), (81.3, 5), -133.5),
               Checkpoint((318.5, 789.0), (88.2, 5), -125.3),
               Checkpoint((418.5, 801.0), (95.0, 5), -53.1),
               Checkpoint((451.5, 721.5), (85.1, 5), -2.0),
               Checkpoint((455.5, 607.5), (84.2, 5), -20.2),
               Checkpoint((507.5, 544.0), (86.3, 5), -64.6),
               Checkpoint((606.5, 543.5), (86.7, 5), -101.3),
               Checkpoint((665.5, 621.5), (89.8, 5), -161.2),
               Checkpoint((667.5, 737.0), (85.0, 5), -178.7),
               Checkpoint((767.0, 812.5), (80.6, 5), -78.6),
               Checkpoint((822.0, 725.0), (82.0, 5), -1.4),
               Checkpoint((821.5, 480.5), (83.1, 5), -2.1),
               Checkpoint((761.0, 406.0), (85.9, 5), 77.9),
               Checkpoint((513.0, 406.5), (85.0, 5), -90.0),
               Checkpoint((448.0, 344.5), (80.0, 5), 179.3),
               Checkpoint((519.5, 291.0), (82.0, 5), 90.7),
               Checkpoint((765.5, 289.5), (83.0, 5), -89.3),
               Checkpoint((823.0, 186.5), (84.0, 5), -0.7),
               Checkpoint((801.5, 99.0), (82.9, 5), 48.4),
               Checkpoint((684.5, 85.5), (85.0, 5), 89.3),
               Checkpoint((389.0, 88.5), (85.0, 5), -90.0),
               Checkpoint((313.5, 141.5), (91.7, 5), -18.4),
               Checkpoint((313.0, 380.0), (82.0, 5), 0.0),
               Checkpoint((254.0, 457.5), (87.0, 5), -90.0),
               Checkpoint((194.0, 368.0), (90.0, 5), 180.0)]

car_population = [ComputerCar() for _ in range(40)]
GA = GeneticAlgorithm(car_population)


while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    # Atualiza o estado do carro e só depois desenha
    player_movement(player_car)
    player_car.update_car()
    
    for car in car_population:
        car.decision()
        car.update_car()
        car.move()
        car.check_checkpoint(checkpoints)
    
    draw(WINDOW, images, player_car, car_population)
    
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.destroyed = True
    
    for car in car_population:
        if not car.destroyed and car.collide(TRACK_BORDER_MASK) is not None:
            car.destroyed = True
    
    if generation_frame_count >= MAX_GENERATION_FRAMES or all(car.destroyed for car in car_population):
        if current_generation % 5 == 0:
            GA.save_best_weights(current_generation)
            
        data = {
            "generation": current_generation,
            "best_fitness": GA.get_best_individuals()[0].next_checkpoint / len(checkpoints),
            "average_fitness": np.mean([[i.next_checkpoint for i in GA.get_best_individuals()]]) / len(checkpoints),
            "worst_fitness": GA.get_best_individuals()[-1].next_checkpoint
        }
        with open("data/history.jsonl", "a") as f:
            json.dump(data, f)
            f.write("\n")
        
        best_checkpoint = GA.get_best_individuals()[0].next_checkpoint
        if best_checkpoint < 6:
            MAX_GENERATION_FRAMES = 5 * FPS
        elif best_checkpoint < 15:
            MAX_GENERATION_FRAMES = 10 * FPS
        elif best_checkpoint < 22:
            MAX_GENERATION_FRAMES = 15 * FPS
        else:
            MAX_GENERATION_FRAMES = 20 * FPS
        
        car_population = GA.create_new_population()
        GA.population = car_population
        for c in car_population:
            c.reset()
        generation_frame_count = 0
        current_generation += 1
    
    generation_frame_count += 1

pygame.quit()