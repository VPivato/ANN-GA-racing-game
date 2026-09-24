import numpy as np
from car import ComputerCar
from neural_network import NeuralNetwork
from datetime import datetime
from pathlib import Path

class GeneticAlgorithm:
    def __init__(self, population):
        self.population = population
        self.population_size = len(population)
    
    def get_best_individuals(self) -> np.ndarray[ComputerCar]:
        best = sorted(self.population, key=lambda item: item.next_checkpoint, reverse=True)
        return np.array(best)
    
    def selection(self, percentage:float = 0.5, elitism:int = 2):
        """Separa os individuos entre elites (maiores fitness) e pais.
        Os elites se manterão imutados a cada geração, enquanto os pais serão usados
        para gerar novos individuos via crossover e mutação.
        
        Args:
            percentage: quantidade de novos pais que serão escolhidos.
            elitism: quantidade dos melhores individuos que se manterão imutados.
        
        Return:
            elites, selected
        """
        
        best_individuals = self.get_best_individuals()
        elites = best_individuals[:elitism]
        selected = best_individuals[:int(self.population_size*percentage)]
        
        return elites, selected
    
    def crossover(self, p1:ComputerCar, p2:ComputerCar) -> ComputerCar:
        """Aplica a função de crossover entre dois pais e retorna um filho"""
        
        child = ComputerCar()
        
        nn1 = p1.neural_network
        nn2 = p2.neural_network
        nnc = child.neural_network
        
        cut = np.random.randint(1, nn1.W1.shape[1]) # 1 - 6
        
        nnc.W1[:, :cut] = nn1.W1[:, :cut]
        nnc.W1[:, cut:] = nn2.W1[:, cut:]
        
        nnc.b1[:cut] = nn1.b1[:cut]
        nnc.b1[cut:] = nn2.b1[cut:]
        
        nnc.W2[:cut, :] = nn1.W2[:cut, :]
        nnc.W2[cut:, :] = nn2.W2[cut:, :]
        
        nnc.b2[:] = np.where(np.random.rand(nnc.b2.size) < 0.5, nn1.b2, nn2.b2)
        
        return child
    
    def mutation(self, neural_network, mutation_rate = .06, mutation_strength = .12):
        rng = np.random.default_rng()
        
        mask = rng.random(neural_network.W1.shape) < mutation_rate
        neural_network.W1[mask] += rng.normal(0, mutation_strength, size=np.sum(mask))
        
        mask = rng.random(neural_network.b1.shape) < mutation_rate
        neural_network.b1[mask] += rng.normal(0, mutation_strength, size=np.sum(mask))
        
        mask = rng.random(neural_network.W2.shape) < mutation_rate
        neural_network.W2[mask] += rng.normal(0, mutation_strength, size=np.sum(mask))
        
        mask = rng.random(neural_network.b2.shape) < mutation_rate
        neural_network.b2[mask] += rng.normal(0, mutation_strength, size=np.sum(mask))
        
    
    def create_new_population(self):
        """Cria e retorna uma nova população de indivíduos baseado na seleção dos melhores. Os elites continuam imutados"""
        
        elites, parents = self.selection()
        
        new_population = list(elites)
        
        while len(new_population) < self.population_size:
            p1, p2 = np.random.choice(parents, size=2, replace=False)
            child = self.crossover(p1, p2)
            new_population.append(child)
        
        for i in new_population[len(elites):]:
            self.mutation(i.neural_network)
        
        return new_population
    
    def save_best_weights(self, generation:int):
        path = Path(__file__).parent / "weights" / f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}-G{generation}.npz"
        best = self.get_best_individuals()[0]
        return np.savez(path, *best.neural_network.get_weights())
