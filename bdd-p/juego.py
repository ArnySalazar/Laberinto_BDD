import pygame
import sys

# Inicializar pygame
pygame.init()

# Tamaño de la ventana del juego
screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Laberinto")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Definir el tamaño del bloque y velocidad
block_size = 20
player_speed = block_size

# Definir el jugador (un punto)
player_pos = [block_size, block_size]

# Definir el laberinto (1 = pared, 0 = camino, 2 = meta)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1],  # '2' es la meta
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Función para dibujar el laberinto
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * block_size, row * block_size, block_size, block_size))
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, GREEN, (col * block_size, row * block_size, block_size, block_size))

# Función para dibujar al jugador
def draw_player():
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], block_size, block_size))

# Función para verificar si el movimiento es válido
def is_valid_move(x, y):
    row = y // block_size
    col = x // block_size
    if maze[row][col] == 0 or maze[row][col] == 2:  # Permite moverse al camino y a la meta
        return True
    return False

# Función para verificar si el jugador ha ganado
def check_win():
    row = player_pos[1] // block_size
    col = player_pos[0] // block_size
    if maze[row][col] == 2:  # Si llega a la meta
        return True
    return False

# Bucle del juego
clock = pygame.time.Clock()
running = True
win = False

while running:
    screen.fill(WHITE)
    draw_maze()
    draw_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not win:
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Movimiento del jugador
        if keys[pygame.K_LEFT]:
            new_x = player_pos[0] - player_speed
            if is_valid_move(new_x, player_pos[1]):
                player_pos[0] = new_x
        if keys[pygame.K_RIGHT]:
            new_x = player_pos[0] + player_speed
            if is_valid_move(new_x, player_pos[1]):
                player_pos[0] = new_x
        if keys[pygame.K_UP]:
            new_y = player_pos[1] - player_speed
            if is_valid_move(player_pos[0], new_y):
                player_pos[1] = new_y
        if keys[pygame.K_DOWN]:
            new_y = player_pos[1] + player_speed
            if is_valid_move(player_pos[0], new_y):
                player_pos[1] = new_y

        # Verificar si el jugador ganó
        if check_win():
            win = True

    else:
        # Mostrar mensaje de ganaste
        font = pygame.font.Font(None, 74)
        text = font.render("¡Ganaste!", True, BLACK)
        screen.blit(text, (100, 150))

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(10)

# Salir de pygame
pygame.quit()
sys.exit()
