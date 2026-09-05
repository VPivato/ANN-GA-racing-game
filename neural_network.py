import numpy as np

# Neurônios: 9 > 6 > 3
class NeuralNetwork:
    def __init__(self):
        rng = np.random.default_rng()
        
        # Primeira camada oculta (6 neurônios)
        self.W1 = rng.normal(0, np.sqrt(2 / 9), size=(9, 6)) # Inicialização de Kaiming - sqrt(2 / fan-in)
        self.b1 = np.zeros(6)
        
        # Camada de saída (2 neurônios)
        self.W2 = rng.normal(0, np.sqrt(2 / 8), size=(6, 2)) # Inicialização de Xavier - sqrt(2 / fan-in + fan-out)
        self.b2 = np.zeros(2)
    
    def forward_pass(self, X):
        """Passagem e cálculo dos dados pela rede, aplicando biases e funções de ativação.
        
        Returns:
            Tupla com 4 np.array: (Z1, A1, Z2, A2).
                Z1: produto escalar entre X (valores de entrada) e W1 (pesos da primeira camada oculta) + b1 (bias).
                A1: Z1 após passar pela função de ativação ReLU.
                Z2: produto escalar entre A1 e W2 (pesos da segunda camada oculta) + b2 (bias).
                A2: Z2 após passar pela função de ativação sigmoid.
        """
        Z1 = np.dot(X, self.W1) + self.b1
        A1 = self.ReLU(Z1)
        Z2 = np.dot(A1, self.W2) + self.b2
        A2 = self.tanh(Z2)
        return Z1, A1, Z2, A2
    
    def ReLU(self, values):
        return np.maximum(0, values)
    
    def tanh(self, values):
        return (2 / (1 + np.exp(2 * -values))) - 1
