import pygame, numpy as np
from raycaster import Raycaster, MAX_DISTANCE
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
    
    def update_car(self) -> None:
        """Atualiza os estados internos do carro, como imagem, rect, mask e raycaster."""
        
        self.rotated_image = pygame.transform.rotate(self.img, self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.img.get_rect(topleft=self.pos).center)
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.raycaster.cast_all_rays()
    
    def draw(self,
             win:pygame.Surface,
             show_mask:bool = False,
             show_rect:bool = False,
             show_rays:bool = False,
             mask_color:tuple = (255,0,0),
             rect_color:tuple = (255,0,0),
             ray_color:tuple = (255,0,0)) -> None:
        """Desenha o carro na superfície fornecida.
        Opcionalmente, é possível visualizar a máscara de colisão (mask), bounding box (rect) e raios do carro (rays), além de controlar suas cores.
        """
        
        win.blit(self.rotated_image, self.rotated_rect.topleft)
        
        if show_mask:
            # mask.to_surface é uma operação custosa, desligar quando houver muitos carros
            win.blit(self.mask.to_surface(setcolor=mask_color, unsetcolor=(0,0,0,0)), self.rotated_rect.topleft)
        if show_rect:
            pygame.draw.rect(win, rect_color, self.rotated_rect, 2)
        if show_rays:
            self.raycaster.draw(win, ray_color)
    
    def rotate(self, amount:float) -> None:
        """Muda o ângulo do carro baseado no valor de amount.
        
        Args:
            amount: Valor no intervalo [-1,1]. Valores negativos rotacionam para a esquerda
            e valores positivos rotacionam para a direita.
        """
        
        if self.destroyed:
            return
        
        self.angle -= (self.rotation_vel * amount) % 360

    def accelerate(self, amount:float) -> None:
        """Aumenta a velocidade do carro até um máximo de max_vel (parâmetro definido na instânciação da classe).
        
        Args:
            amount: Valor no intervalo [0,1].
        """
        
        if self.destroyed:
            return
        
        self.vel = min(self.vel + self.acceleration * amount, self.max_vel)
    
    def brake(self, amount:float):
        """Diminui a velocidade do carro até um mínimo de 0.
        
        Args:
            amount: Valor no intervalo [0,1].
        """
        
        if self.destroyed:
            return
        
        self.vel = max(self.vel - self.acceleration * amount, 0)
    
    def reduce_speed(self) -> None:
        """Reduz a velocidade do carro em metade da aceleração, até um mínimo de 0."""
        
        if self.destroyed:
            return
        
        self.vel = max(self.vel - self.acceleration / 2, 0)
    
    def move(self) -> None:
        """Atualiza a posição do carro, deslocando-o com base em sua velocidade."""
        
        if self.destroyed:
            return
        
        self.pos -= get_direction(self.angle) * self.vel
    
    def collide(self, mask:pygame.mask.Mask, x:int = 0, y:int = 0) -> tuple | None:
        """Retorna as coordenadas do primeiro pixel que colidiu em uma tupla (x, y), ou None se não houver colisão."""
        
        if self.destroyed:
            return
        
        offset = (int(self.rotated_rect.x - x), int(self.rotated_rect.y - y))
        return mask.overlap(self.mask, offset)
    
    def get_sensor_readings(self) -> np.ndarray:
        """Retorna um np.array contendo a leitura de cada sensor do carro.
        Cada valor normalizado entre [0,1] representa a distância de cada raio até colidirem,
        sendo que "1" significa que o raio não colidiu com nada.
        """
        
        return np.array([ray.distance / MAX_DISTANCE for ray in self.raycaster.rays])


class PlayerCar(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (205, 200)


class ComputerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (165, 200)
    
    def decision(self):
        choices = [lambda: self.accelerate(1),
                   lambda: self.brake(1),
                   lambda: self.rotate(-1),
                   lambda: self.rotate(1),
        ]
        
        self.reduce_speed()
        choice = np.random.choice(choices)
        choice()
            