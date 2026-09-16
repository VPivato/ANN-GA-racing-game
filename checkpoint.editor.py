#
#   Código gerado completamente por IA.
#


import pygame
import math

pygame.init()


TRACK_PATH = "img/track.png"


track = pygame.image.load(TRACK_PATH)
WIDTH, HEIGHT = track.get_size()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkpoint Editor")

clock = pygame.time.Clock()
FPS = 60

# --------------------------------------------------
# Estado da linha
# --------------------------------------------------

drawing = False
start_pos = None
end_pos = None

# --------------------------------------------------
# Funções
# --------------------------------------------------

def calculate_checkpoint(start, end):
    x1, y1 = start
    x2, y2 = end

    # Centro da linha
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    # Comprimento
    length = math.hypot(x2 - x1, y2 - y1)

    # Ângulo da linha
    #
    # atan2 normalmente considera o eixo Y crescendo para cima,
    # enquanto no Pygame o eixo Y cresce para baixo.
    angle = math.degrees(math.atan2(-(y2 - y1), x2 - x1))

    return center_x, center_y, length, angle


def print_checkpoint(start, end):
    center_x, center_y, length, angle = calculate_checkpoint(start, end)

    print()
    print("=" * 50)
    print("CHECKPOINT")
    print("=" * 50)

    print(f"Início:  ({start[0]}, {start[1]})")
    print(f"Fim:     ({end[0]}, {end[1]})")

    print(f"Centro:  ({center_x:.1f}, {center_y:.1f})")
    print(f"Tamanho: {length:.1f}")
    print(f"Ângulo:  {angle:.1f} graus")

    print()
    print("Código para usar no jogo:")
    print(
        f"Checkpoint(({center_x:.1f}, {center_y:.1f}), "
        f"({length:.1f}, 5), {angle:.1f})"
    )

    print("=" * 50)


# --------------------------------------------------
# Loop principal
# --------------------------------------------------

run = True

while run:
    clock.tick(FPS)

    for event in pygame.event.get():

        # Fechar janela
        if event.type == pygame.QUIT:
            run = False

        # Teclado
        elif event.type == pygame.KEYDOWN:

            # ESC = sair
            if event.key == pygame.K_ESCAPE:
                run = False

            # R = apagar linha
            elif event.key == pygame.K_r:
                start_pos = None
                end_pos = None
                drawing = False

        # Botão esquerdo pressionado
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                start_pos = event.pos
                end_pos = event.pos
                drawing = True

        # Mouse se movimentando
        elif event.type == pygame.MOUSEMOTION:

            if drawing:
                end_pos = event.pos

        # Botão esquerdo solto
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and drawing:
                end_pos = event.pos
                drawing = False

                print_checkpoint(start_pos, end_pos)

    # --------------------------------------------------
    # Desenho
    # --------------------------------------------------

    WINDOW.blit(track, (0, 0))

    # Linha enquanto está sendo desenhada
    if drawing and start_pos is not None and end_pos is not None:
        pygame.draw.line(
            WINDOW,
            (255, 0, 0),
            start_pos,
            end_pos,
            3
        )

        pygame.draw.circle(
            WINDOW,
            (0, 255, 0),
            start_pos,
            5
        )

        pygame.draw.circle(
            WINDOW,
            (255, 0, 0),
            end_pos,
            5
        )

    # Linha depois de finalizada
    elif start_pos is not None and end_pos is not None:
        pygame.draw.line(
            WINDOW,
            (255, 0, 0),
            start_pos,
            end_pos,
            3
        )

        pygame.draw.circle(
            WINDOW,
            (0, 255, 0),
            start_pos,
            5
        )

        pygame.draw.circle(
            WINDOW,
            (255, 0, 0),
            end_pos,
            5
        )

    pygame.display.update()

pygame.quit()