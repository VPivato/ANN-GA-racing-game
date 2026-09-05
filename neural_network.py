import numpy as np

# Neurônios: 9 > 6 > 3
class NeuralNetwork:
    def __init__(self, X):
        """Inicialização dos pesos (weights) e viéses (biases) com base em uma distribuição gaussiana"""
        
        # Valores de input (9 valores)
        self.X = X
        
        rng = np.random.default_rng()
        
        # Primeira camada oculta (6 neurônios)
        self.W1 = rng.standard_normal((9, 6))
        self.b1 = rng.standard_normal((6))
        
        # Camada de saída (3 neurônios)
        self.W2 = rng.standard_normal((6, 3))
        self.b2 = rng.standard_normal((3))
    
    def forward_pass(self):
        """Passagem e cálculo dos dados pela rede, aplicando biases e funções de ativação.
        
        Returns:
            Tupla com 4 np.array: (Z1, A1, Z2, A2).
                Z1: produto escalar entre X (valores de entrada) e W1 (pesos da primeira camada oculta) + b1 (bias).
                A1: Z1 após passar pela função de ativação ReLU.
                Z2: produto escalar entre A1 e W2 (pesos da segunda camada oculta) + b2 (bias).
                A2: Z2 após passar pela função de ativação sigmoid.
        """
        Z1 = np.dot(self.X, self.W1) + self.b1
        A1 = self.ReLU(Z1)
        Z2 = np.dot(A1, self.W2) + self.b2
        A2 = self.sigmoid(Z2)
        return Z1, A1, Z2, A2
    
    def ReLU(self, values):
        return np.maximum(0, values)
    
    def sigmoid(self, values):
        return 1 / (1 + np.exp(-values))

nn = NeuralNetwork([0.87,
                    0.2, 0.23, 0.42, 0.87,
                    1, 0.77, 0.65, 0.36])
_, _, _, A2 = nn.forward_pass()
print(A2)