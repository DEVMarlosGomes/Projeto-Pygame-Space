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

novo_bg = pygame.image.load('pygame_aplication-main/img/tela2.jpg')
novo_bg = pygame.transform.scale(novo_bg, (x, y))

nivel_3_bg = pygame.image.load('pygame_aplication-main/img/tela3.jpg')
nivel_3_bg = pygame.transform.scale(nivel_3_bg, (x, y))

inicio_img = pygame.image.load('pygame_aplication-main/img/Inicio.png')
inicio_img = pygame.transform.scale(inicio_img, (x, y))

inimigo = pygame.image.load('pygame_aplication-main/img/inimigo.png').convert_alpha()
inimigo = pygame.transform.scale(inimigo, (55, 55))

playerImg = pygame.image.load('pygame_aplication-main/img/FOGUETE.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (95, 95))

golpe = pygame.image.load('pygame_aplication-main/img/golpe.png').convert_alpha()
golpe = pygame.transform.scale(golpe, (30, 30))

heart_img = pygame.image.load('pygame_aplication-main/img/heart.png').convert_alpha()
heart_img = pygame.transform.scale(heart_img, (40, 40))

game_over_img = pygame.image.load('pygame_aplication-main/img/GameOver.png').convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (x, y))

# Fonte
fonte = pygame.font.SysFont('font/PixelGameFont.ttf', 50)
fonte_pontos = pygame.font.SysFont('font/PixelGameFont.ttf', 32)

# Funções
def tela_inicio():
    while True:
        screen.blit(inicio_img, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def respawn():
    return [1350, random.randint(1, 640)]

def respawn_golpe(pos_x, pos_y):
    return [pos_x, pos_y, False, 0]

def colisions():
    global vidas, pontos
    if player_rect.colliderect(inimigo_rect) or inimigo_rect.x <= 60:
        vidas -= 1
        return True
    elif golpe_rect.colliderect(inimigo_rect):
        pontos += 1
        return True
    return False

def reset_game():
    global pos_inimigo_x, pos_inimigo_y, pos_player_x, pos_player_y
    global pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe
    global vidas, game_over, pontos, nivel, vel_inimigo, mostrar_nivel
    global ultimo_tiro, tempo_recarga

    pos_inimigo_x, pos_inimigo_y = respawn()
    pos_player_x, pos_player_y = 200, 300
    pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)
    vidas = 7
    pontos = 0
    game_over = False
    nivel = 1
    vel_inimigo = 0.5
    mostrar_nivel = False
    ultimo_tiro = 0
    tempo_recarga = 400  # milissegundos

# Início
tela_inicio()
reset_game()

# Variáveis
tempo_nivel = 0
recorde = 0  # Variável para o recorde do jogo

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tempo_atual = pygame.time.get_ticks()

    if pontos >= nivel * 10:
        nivel += 1
        vel_inimigo += 0.3
        vidas = 7
        mostrar_nivel = True
        tempo_nivel = tempo_atual

    # Atualiza o recorde durante o jogo
    if pontos > recorde:
        recorde = pontos

    # Fundo por nível
    if nivel == 1:
        screen.blit(bg, (0, 0))
    elif nivel == 2:
        screen.blit(novo_bg, (0, 0))
    elif nivel == 3:
        screen.blit(nivel_3_bg, (0, 0))  # Fundo do nível 3

    if not game_over:
        tecla = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()

        if (tecla[pygame.K_UP] or tecla[pygame.K_w]) and pos_player_y > 1:
            pos_player_y -= 1
            if not triggered:
                pos_y_golpe -= 1
        if (tecla[pygame.K_DOWN] or tecla[pygame.K_s]) and pos_player_y < 665:
            pos_player_y += 1
            if not triggered:
                pos_y_golpe += 1

        # Disparo com recarga
        if (tecla[pygame.K_SPACE] or mouse_click[0]) and not triggered and tempo_atual - ultimo_tiro >= tempo_recarga:
            triggered = True
            vel_x_golpe = 1
            ultimo_tiro = tempo_atual

        pos_inimigo_x -= vel_inimigo
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

        # Corações (vidas)
        for i in range(vidas):
            screen.blit(heart_img, (50 + i * 45, 50))

        # Pontuação (no canto superior direito)
        pontos_txt = fonte_pontos.render(f'Score: {pontos}', True, (255, 255, 255))
        screen.blit(pontos_txt, (x - pontos_txt.get_width() - 20, 20))

        # High Score (diretamente abaixo dos pontos)
        recorde_txt = fonte_pontos.render(f'High Score: {recorde}', True, (255, 255, 0))
        screen.blit(recorde_txt, ((x - recorde_txt.get_width()) // 2, pontos_txt.get_height() + 30))

        # Aviso do nível
        if mostrar_nivel:
            if tempo_atual - tempo_nivel < 2000:
                texto_nivel = fonte.render(f'Level {nivel}', True, (255, 255, 0))
                screen.blit(texto_nivel, ((x - texto_nivel.get_width()) // 2, (y - texto_nivel.get_height()) // 2))
            else:
                mostrar_nivel = False

        if vidas <= 0:
            game_over = True

    else:
        screen.blit(game_over_img, (0, 0))
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_r]:
            tela_inicio()
            reset_game()

    pygame.display.update()
