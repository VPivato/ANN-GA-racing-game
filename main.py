import pygame, json, numpy as np
from car import PlayerCar, ComputerCar
from track import TRACK, FINISH, check_border_collision, check_finish_collision
from checkpoint import get_checkpoints
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

checkpoints = get_checkpoints()
player_car = PlayerCar()
car_population = [ComputerCar() for _ in range(40)]
GA = GeneticAlgorithm(car_population)

images = [(TRACK, (0,0)),
          (FINISH, (155, 250))]

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

def write_to_history():
    best = GA.get_best_individuals()
    data = {
        "generation": current_generation,
        "best_fitness": best[0].next_checkpoint / len(checkpoints),
        "average_fitness": np.mean([i.next_checkpoint for i in best]) / len(checkpoints)
    }
    with open("data/history.jsonl", "a") as f:
        json.dump(data, f)
        f.write("\n") 

def update_generation_time():
    best_checkpoint = GA.get_best_individuals()[0].next_checkpoint
    if best_checkpoint < 6:
        return 5 * FPS
    elif best_checkpoint < 15:
        return 10 * FPS
    elif best_checkpoint < 22:
        return 15 * FPS
    else:
        return 20 * FPS

run = True
clock = pygame.time.Clock()

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
    
    check_border_collision(player_car)
    check_finish_collision(player_car)
    
    for car in car_population:
        check_border_collision(car)
        check_finish_collision(car)
    
    if generation_frame_count >= MAX_GENERATION_FRAMES or all(car.destroyed for car in car_population):
        if current_generation % 5 == 0:
            GA.save_best_weights(current_generation)
        
        write_to_history()
        
        MAX_GENERATION_FRAMES = update_generation_time()
        
        car_population = GA.create_new_population()
        GA.population = car_population
        for c in car_population:
            c.reset()
        generation_frame_count = 0
        current_generation += 1
    
    generation_frame_count += 1

pygame.quit()