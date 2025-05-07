import pygame
import random
import sys

pygame.init()

# Tela
x = 1280
y = 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('My first game in Python')

# Imagens
bg = pygame.image.load('pygame_aplication-main/img/tela.jpg')
bg = pygame.transform.scale(bg, (x, y))

inicio_img = pygame.image.load('pygame_aplication-main/img/Inicio.png')
inicio_img = pygame.transform.scale(inicio_img, (x, y))

inimigo = pygame.image.load('pygame_aplication-main/img/inimigo.png').convert_alpha()
inimigo = pygame.transform.scale(inimigo, (55, 55))

playerImg = pygame.image.load('pygame_aplication-main/img/FOGUETE.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (95, 95))
playerImg = pygame.transform.rotate(playerImg, 0)

golpe = pygame.image.load('pygame_aplication-main/img/golpe.png').convert_alpha()
golpe = pygame.transform.scale(golpe, (30, 30))

heart_img = pygame.image.load('pygame_aplication-main/img/heart.png').convert_alpha()
heart_img = pygame.transform.scale(heart_img, (40, 40))

game_over_img = pygame.image.load('pygame_aplication-main/img/GameOver.png').convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (x, y))

font = pygame.font.SysFont('font/PixelGameFont.ttf', 50)

# Funções
def tela_inicio():
    while True:
        screen.blit(inicio_img, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Inicia o jogo

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
    vidas = 7
    game_over = False

# Início do jogo
tela_inicio()
reset_game()

# Loop principal
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(bg, (0, 0))

    if not game_over:
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
            vel_x_golpe = 1

        pos_inimigo_x -= 1
        pos_x_golpe += vel_x_golpe

        player_rect = playerImg.get_rect(topleft=(pos_player_x, pos_player_y))
        golpe_rect = golpe.get_rect(topleft=(pos_x_golpe, pos_y_golpe))
        inimigo_rect = inimigo.get_rect(topleft=(pos_inimigo_x, pos_inimigo_y))

        if pos_x_golpe >= 1300:
            pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)

        if pos_inimigo_x <= 50 or colisions():
            pos_inimigo_x, pos_inimigo_y = respawn()

        screen.blit(playerImg, (pos_player_x, pos_player_y))
        screen.blit(golpe, (pos_x_golpe, pos_y_golpe))
        screen.blit(inimigo, (pos_inimigo_x, pos_inimigo_y))

        for i in range(vidas):
            screen.blit(heart_img, (50 + i * 45, 50))

        if vidas <= 0:
            game_over = True

    else:
        screen.blit(game_over_img, (0, 0))
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_r]:
            tela_inicio()
            reset_game()

    pygame.display.update()
