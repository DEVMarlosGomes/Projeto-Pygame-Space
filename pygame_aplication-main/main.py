import pygame
import random

pygame.init()

# Tela
x = 1280
y = 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('My first game in Python')

# Imagens
bg = pygame.image.load('pygame_aplication-main/img/tela.jpg')
bg = pygame.transform.scale(bg, (x, y))

inimigo = pygame.image.load('pygame_aplication-main/img/inimigo.png').convert_alpha()
inimigo = pygame.transform.scale(inimigo, (55, 55))

playerImg = pygame.image.load('pygame_aplication-main/img/player.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (65, 65))
playerImg = pygame.transform.rotate(playerImg, -90)

golpe = pygame.image.load('pygame_aplication-main/img/golpe.png').convert_alpha()
golpe = pygame.transform.scale(golpe, (30, 30))

font = pygame.font.SysFont('font/PixelGameFont.ttf', 50)

# Funções
def respawn():
    return [1350, random.randint(1, 640)]

def respawn_golpe(pos_x, pos_y):
    return [pos_x, pos_y, False, 0]

def colisions():
    global vidas
    if player_rect.colliderect(inimigo_rect) or inimigo_rect.x <= 60:
        vidas -= 1
        return True
    elif golpe_rect.colliderect(inimigo_rect):
        return True
    return False

def reset_game():
    global pos_inimigo_x, pos_inimigo_y, pos_player_x, pos_player_y
    global pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe
    global vidas, game_over

    pos_inimigo_x, pos_inimigo_y = respawn()
    pos_player_x, pos_player_y = 200, 300
    pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)
    vidas = 10
    game_over = False

# Estado inicial
reset_game()
rodando = True

# Loop principal
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(bg, (0, 0))

    if not game_over:
        # Entrada do teclado
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and pos_player_y > 1:
            pos_player_y -= 1
            if not triggered:
                pos_y_golpe -= 1
        if tecla[pygame.K_DOWN] and pos_player_y < 665:
            pos_player_y += 1
            if not triggered:
                pos_y_golpe += 1
        if tecla[pygame.K_SPACE]:
            triggered = True
            vel_x_golpe = 1.05

        # Atualizar posições
        pos_inimigo_x -= 1
        pos_x_golpe += vel_x_golpe

        # Atualizar rects
        player_rect = playerImg.get_rect(topleft=(pos_player_x, pos_player_y))
        golpe_rect = golpe.get_rect(topleft=(pos_x_golpe, pos_y_golpe))
        inimigo_rect = inimigo.get_rect(topleft=(pos_inimigo_x, pos_inimigo_y))

        # Colisões
        if pos_x_golpe >= 1300:
            pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)

        if pos_inimigo_x <= 50 or colisions():
            pos_inimigo_x, pos_inimigo_y = respawn()

        # Desenhar tudo
        screen.blit(playerImg, (pos_player_x, pos_player_y))
        screen.blit(golpe, (pos_x_golpe, pos_y_golpe))
        screen.blit(inimigo, (pos_inimigo_x, pos_inimigo_y))

        vidas_txt = font.render(f'Vidas: {vidas}', True, (255, 255, 255))
        screen.blit(vidas_txt, (50, 50))

        if vidas <= 0:
            game_over = True

    else:
        # Tela de Game Over
        game_over_text = font.render("GAME OVER - Pressione R para Reiniciar", True, (255, 0, 0))
        screen.blit(game_over_text, (300, 350))

        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_r]:
            reset_game()

    pygame.display.update()
 
