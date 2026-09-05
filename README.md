# ANN + GA Car Racing

**Rede Neural Artificial treinada via Algoritmo Genético controla carro em pista de corrida.**

<img src="img/player_car_moving.gif" alt="Carro do jogador se movendo pela pista." width="500px" />

Carro autônomo aprende a desviar de obstáculos em uma pista. Treinado por Rede Neural e Algoritmo Genético, ambos desenvolvidos sem o auxílio de bibliotecas de aprendizagem de máquina.

A motivação desse projeto surgiu após eu assistir o vídeo ["Can I make a Better AI Than AI"](https://youtu.be/GGWHjAyKJCA?si=wAQap95mO3w7fEDn) do canal [commonLuke](https://www.youtube.com/@commonLuke). Decidi que queria fazer algo mais completo do que normalmente faço, sem usar bibliotecas de ML, para ter um entendimento mais profundo sobre o funcionamento de uma rede neural. Até então, minha experiência com Machine Learning foi baseada quase que exclusivamente em [Tensorflow](https://www.tensorflow.org/?hl=pt-br).

Bibliotecas centrais usadas:
- Python 3.13.15
- Pygame 2.6.1
- NumPy 2.5.2
- Pandas 3.0.5 (planejado - logging e estatísticas. Rede neural usará apenas NumPy)

Rede Neural:
- (to do)

## Como funciona

Lógica do carro

```mermaid
flowchart TD
    A[Carro] --  Velocidade e sensores --> B((Rede Neural))
    B -- Direção, aceleração e freio --> C[Ação]
```

<hr />

Algoritmo Genético
```mermaid
flowchart TD
    D[Simulação] --> E[Seleção]
    E --> F[Crossover]
    F --> G[Mutação]
    G --> H{Nª geração?}
    H -- Sim --> I(Salva pesos do melhor carro)
    H -- Não --> D
```

A rede neural recebe 9 valores iniciais: velocidade e a leitura dos 8 sensores de distância. E retorna três, que controlam a decisão do carro a cada frame:
- Um valor [-1, 1] que representa a direção de rotação. Valores intermediários, como 0.5, significam uma rotação mais suave.
- Um valor [0, 1] que representa a quantidade de aceleração, aumentando a velocidade do carro. 
- Um valor [0, 1] que representa a quantidade de freio, diminuindo a velocidade do carro.

Ao fim de cada geração de treinamento, os melhores carros (critério de fitness a ser decidido) são selecionados pelo Algoritmo Genético para reproduzir ([crossover](https://www.geeksforgeeks.org/machine-learning/crossover-in-genetic-algorithm/)) e gerar descendentes mais aptos. O ciclo continua por N gerações.

## Estrutura do projeto

Os arquivos mais relevantes são:
- `main.py`: define e configura o essencial da biblioteca *pygame* e junta os outros módulos em um projeto funcional.
- `car.py`: define a classe abstrata do carro com seus atributos e métodos, que vai servir de herança para *PlayerCar* e *ComputerCar*
- `raycaster.py`: módulo responsável pelos sensores de distância que cada carro possui.
- (planejado) `neural_network.py`: rede neural desenvolvida em NumPy, o centro do projeto.
- (planejado) `genetic_algorithm.py`: responsável por selecionar, cruzar e mutar os melhores carros de cada época.

## Desafios técnicos

(to do)

## Resultados

(to do)

## Como executar

1. Clone o repositório no diretório desejado.
```bash
git clone https://github.com/VPivato/ANN-GA-racing-game.git
```

2. Acesse o diretório clonado.
```bash
cd ANN-GA-racing-game
```

3. Crie um ambiente virtual.

### Windows (Powershell)
```powershell
py -m venv .venv
```

### macOS / Linux (Bash)
```bash
python3 -m venv .venv
```

4. Ative o ambiente virtual.
### Windows (Powershell)
```powershell
.venv/scripts/activate.ps1
```

### macOS / Linux (Bash)
```bash
source .venv/bin/activate
```

5. Instale as dependências.
```bash
pip install -r requirements.txt
```

6. Abra `main.py` e execute.

## Referências

Algum dos materiais usados ao longo do projeto são:
- ["Can I make a Better AI Than AI"](https://youtu.be/GGWHjAyKJCA?si=wAQap95mO3w7fEDn) do canal [commonLuke](https://www.youtube.com/@commonLuke). Motivação principal do projeto.
- Playlist ["Pygame Car Racing Tutorial"](https://www.youtube.com/playlist?list=PLzMcBGfZo4-kmY7Nh4kI9kPPnxJ5JMRPj) do canal [Tech With Tim](https://www.youtube.com/@TechWithTim). Os dois primeiros vídeos me auxiliaram a criar o ambiente do jogo.
- ["Raycasting Tutorial (in Python)"](https://youtu.be/E18bSJezaUE?si=k-GWR9av9XXVNEwh) do canal [Pythonista_](https://www.youtube.com/@pythonista_333). Me apresentou ao conceito de raycasting, usado para os sensores de distância do carro.
- ["Building a neural network FROM SCRATCH (no Tensorflow/Pytorch, just numpy & math)"](https://youtu.be/w8yWXqWQYmU?si=Zrc4kZJAmwRXX1E0) do canal [Samson Zhang](https://www.youtube.com/@SamsonZhangTheSalmon). O diagrama exibido no vídeo me ajudou a implementar a rede neural.
- ["Forward Propagation in Neural Networks"](https://www.geeksforgeeks.org/deep-learning/forward-propagation-in-neural-networks/). Bom material de apoio.