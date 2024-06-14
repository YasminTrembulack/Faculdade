import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

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
RANKING_FILE = 'ranking.txt'

# Lista de pontuações (simulação de um ranking)
ranking_scores = []

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
        for line in lines:
            name, current_score = line.strip().split(',')
            current_score = int(current_score)
            if name == player_name:
                if score > current_score:
                    file.write(f'{player_name},{score}\n')
                    updated = True
                else:
                    file.write(f'{name},{current_score}\n')
            else:
                file.write(f'{name},{current_score}\n')
    
    return updated

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

# Função principal do jogo
def game(player_name):
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (1, 0)
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
            food = place_food()
        else:
            snake.pop()

        # Preenche o fundo
        screen.fill(BLACK)

        # Desenha a comida
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Desenha a cobra
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Desenha a pontuação
        draw_text(screen, f'Pontuação: {score}', 18, SCREEN_WIDTH // 2, 10, WHITE)

        # Atualiza a tela
        pygame.display.update()

        # Controla a velocidade do jogo
        clock.tick(snake_speed)

    # Mostra tela de game over e retorna a pontuação para o ranking
    show_game_over(player_name, score)

# Função para colocar a comida em um lugar aleatório no grid
def place_food():
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    return (x, y)

# Função para exibir a tela de game over
def show_game_over(player_name, score):
    screen.fill(BLACK)
    draw_text(screen, 'Game Over', 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, WHITE)
    draw_text(screen, f'Pontuação final: {score}', 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE)

    if not player_in_ranking(player_name):
        save_player_score(player_name, 0)

    if update_player_score(player_name, score):
        draw_text(screen, 'Nova pontuação recorde!', 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, WHITE)

    draw_text(screen, 'Pressione qualquer tecla para jogar novamente', 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, WHITE)
    pygame.display.update()
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
                    return 1  # Jogar
                elif event.key == pygame.K_2:
                    show_ranking()  # Mostrar ranking
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

# Função para exibir o ranking
def show_ranking():
    while True:
        screen.fill(BLACK)
        draw_text(screen, 'Ranking', 40, SCREEN_WIDTH // 2, 50, WHITE)
        draw_text(screen, 'Pressione qualquer tecla para voltar', 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, WHITE)

        y = 100
        for i, (name, score) in enumerate(ranking_scores, start=1):
            draw_text(screen, f'{i}. {name}: {score}', 24, SCREEN_WIDTH // 2, y, WHITE)
            y += 30

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

# Função para esperar até que uma tecla seja pressionada
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

# Função principal para o fluxo do jogo
def main():
    global ranking_scores  # Declare `ranking_scores` como global

    player_name = get_player_name()

    # Carregar o ranking do arquivo para a lista
    with open(RANKING_FILE, 'r') as file:
        for line in file:
            if line.strip():
                name, score = line.strip().split(',')
                ranking_scores.append((name, int(score)))

    while True:
        choice = show_menu()

        if choice == 1:
            score = game(player_name)
            # Adiciona a pontuação ao ranking simulado (limitado às 5 melhores pontuações)
            ranking_scores.append((player_name, score))
            # Remove entradas com pontuação `None` antes de ordenar
            ranking_scores = [entry for entry in ranking_scores if entry[1] is not None]
            ranking_scores.sort(key=lambda x: x[1], reverse=True)
            ranking_scores = ranking_scores[:5]  # Mantém apenas as 5 melhores pontuações

        elif choice == 3:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
