import pygame
import sys
import random
import time

# Inicialização do Pygame
pygame.init()

# Definição das cores
SNAKE_COLOR = (70,116,233,255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
LIGHT_GREEN = (170,215,81,255)
DARK_GREEN = (162,209,73,255)

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Configurações do jogo
INITIAL_SPEED = 8  # Velocidade inicial da cobra
SNAKE_SPEED = 8  # Velocidade atual da cobra

# Arquivo de ranking
RANKING_FILE = './ranking.txt'

# Lista de pontuações (simulação de um ranking)
ranking_scores = []

#Adicionar imagem
game_over_image = pygame.image.load('gato_game_over.jpg')
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Inicialização da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Função para desenhar o texto na tela
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

# Função para desenhar o background xadrezado
def draw_checkered_background():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_GREEN, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, DARK_GREEN, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Função para verificar se o jogador existe no ranking
def player_in_ranking(player_name):
    for name, score in ranking_scores:
        if name == player_name:
            return True
    return False

# Função para obter a pontuação do jogador no ranking
def get_player_score(player_name):
    for name, score in ranking_scores:
        if name == player_name:
            return score
    return 0

# Função para salvar o jogador no ranking
def save_player_score(player_name, score):
    with open(RANKING_FILE, 'a') as file:
        file.write(f'{player_name},{score}\n')

# Função para atualizar a pontuação do jogador no ranking
def update_player_score(player_name, score):
    updated = False
    with open(RANKING_FILE, 'r') as file:
        lines = file.readlines()
    
    with open(RANKING_FILE, 'w') as file:
        found = False
        for line in lines:
            name, current_score = line.strip().split(',')
            current_score = int(current_score)
            if name == player_name:
                found = True
                if score > current_score:
                    file.write(f'{player_name},{score}\n')
                    updated = True
                else:
                    file.write(f'{name},{current_score}\n')
            else:
                file.write(f'{name},{current_score}\n')
        
        # Se não encontrou o jogador no arquivo, adiciona uma nova entrada
        if not found:
            file.write(f'{player_name},{score}\n')
            updated = True
    
    if updated:
        load_ranking()

    return updated

# Função para carregar o ranking do arquivo para a lista
def load_ranking():
    ranking_scores.clear()
    with open(RANKING_FILE, 'r') as file:
        for line in file:
            if line.strip():
                name, score = line.strip().split(',')
                ranking_scores.append((name, int(score)))
    ranking_scores.sort(key=lambda x: x[1], reverse=True)

# Função para solicitar o nome do jogador
def get_player_name():
    input_active = True
    player_name = ""
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        
        screen.fill(BLACK)
        draw_text(screen, 'Digite seu nickname:', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, WHITE)
        draw_text(screen, player_name, 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, WHITE)
        pygame.display.update()
    
    return player_name
#Adicionar imagem
game_over_image = pygame.image.load('gato_game_over.jpg')


# Função principal do jogo
def game(player_name):
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (1, 0)  # Direção inicial da cobra (direita)
    snake_speed = SNAKE_SPEED
    food = place_food()
    score = 0

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

        # Move a cobra
        snake_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, snake_head)

        # Verifica se a cobra colidiu com a parede ou com o próprio corpo
        if snake_head[0] < 0 or snake_head[0] >= GRID_WIDTH or snake_head[1] < 0 or snake_head[1] >= GRID_HEIGHT or snake_head in snake[1:]:
            game_over = True

        # Verifica se a cobra comeu a comida
        if snake_head == food:
            score += 1
            eat_sound.play()
            food = place_food()
        else:
            snake.pop()

        # Preenche o fundo
        screen.fill(BLACK)
        draw_checkered_background()

        # Desenha a comida
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Desenha a cobra (passando a direção da cobra para os olhos)
        draw_snake(snake, snake_direction)

        # Desenha a pontuação
        draw_text(screen, f'Pontuação: {score}', 18, SCREEN_WIDTH // 2, 10, WHITE)

        # Atualiza a tela
        pygame.display.update()

        # Controla a velocidade do jogo
        clock.tick(snake_speed)

    # Mostra tela de game over e atualiza a pontuação no ranking
    show_game_over(player_name, score)

# Função para desenhar a cobra
def draw_snake(snake, snake_direction):
    for i, segment in enumerate(snake):
        if i == 0:
            # Cabeça da cobra com olhos que acompanham a direção
            x, y = segment
            pygame.draw.rect(screen, SNAKE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            
            if snake_direction == (1, 0):  # Direita
                # Olho direito
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 9, y * GRID_SIZE + 2, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 12, y * GRID_SIZE + 5), 2)
                
                # Olho esquerdo
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 9, y * GRID_SIZE + 12, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 12, y * GRID_SIZE + 15), 2)
            elif snake_direction == (-1, 0):  # Esquerda
                # Olho direito
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 5, y * GRID_SIZE + 2, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 8, y * GRID_SIZE + 5), 2)
                
                # Olho esquerdo
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 5, y * GRID_SIZE + 12, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 8, y * GRID_SIZE + 15), 2)
            elif snake_direction == (0, -1):  # Cima
                # Olho direito
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 2, y * GRID_SIZE + 5, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 5, y * GRID_SIZE + 8), 2)
                
                # Olho esquerdo
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 12, y * GRID_SIZE + 5, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 15, y * GRID_SIZE + 8), 2)
            elif snake_direction == (0, 1):  # Baixo
                # Olho direito
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 2, y * GRID_SIZE + 9, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 5, y * GRID_SIZE + 12), 2)
                
                # Olho esquerdo
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE + 12, y * GRID_SIZE + 9, 6, 6))
                pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 15, y * GRID_SIZE + 12), 2)
        else:
            # Corpo da cobra
            x, y = segment
            pygame.draw.rect(screen, SNAKE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))



# Função para colocar a comida em um lugar aleatório no grid
def place_food():
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    return (x, y)

# Função para exibir a tela de game over
def show_game_over(player_name, score):
    laugh_sound.play()
    screen.fill(BLACK)
    # Carrega a imagem e redimensiona se necessário
    game_over_image = pygame.image.load('gato_game_over.jpg').convert()  # Carrega a imagem
    if game_over_image.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
        game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    screen.blit(game_over_image, (0, 0))
    pygame.display.update()
    
    time.sleep(3)
    draw_text(screen, 'Game Over', 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, WHITE)
    draw_text(screen, f'Pontuação final: {score}', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, WHITE)

    if update_player_score(player_name, score):
        draw_text(screen, 'Nova pontuação recorde!', 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE)

    draw_text(screen, 'Pressione qualquer tecla para jogar novamente', 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, WHITE)

    pygame.display.update()

    # Aguarda o jogador pressionar qualquer tecla para continuar
    wait_for_key()


# Função para exibir o menu inicial
def show_menu():
    while True:
        screen.fill(BLACK)
        draw_text(screen, 'Snake Game', 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, WHITE)
        draw_text(screen, '1. Jogar', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, WHITE)
        draw_text(screen, '2. Ranking', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, WHITE)
        draw_text(screen, '3. Sair', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    show_ranking()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Função para exibir o ranking
def show_ranking():
    screen.fill(BLACK)
    draw_text(screen, 'Ranking', 40, SCREEN_WIDTH // 2, 50, WHITE)

    # Carrega e exibe as pontuações do ranking
    load_ranking()

    y = 100
    for i, (name, score) in enumerate(ranking_scores, start=1):
        draw_text(screen, f'{i}. {name}: {score}', 24, SCREEN_WIDTH // 2, y, WHITE)
        y += 30

    pygame.display.update()
    wait_for_key()

# Função para esperar até que uma tecla seja pressionada
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

# Adicionar som 

pygame.mixer.init()

eat_sound = pygame.mixer.Sound('eat-sound.ogg')
laugh_sound = pygame.mixer.Sound('cat-laugh.ogg')

# Função principal para o fluxo do jogo
def main():
    global ranking_scores  # Declare `ranking_scores` como global

    player_name = get_player_name()

    while True:
        choice = show_menu()

        if choice == 1:
            score = game(player_name)

        elif choice == 3:
            pygame.quit()
            sys.exit()


main()
