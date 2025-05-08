import pygame
import random
import sys

pygame.init()

# Tela
x = 1080
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

nivel_4_bg = pygame.image.load('pygame_aplication-main/img/Tela4.jpg')
nivel_4_bg = pygame.transform.scale(nivel_4_bg, (x, y))

nivel_5_bg = pygame.image.load('pygame_aplication-main/img/Tela5.jpg')
nivel_5_bg = pygame.transform.scale(nivel_5_bg, (x, y))

boss_bg = pygame.image.load('pygame_aplication-main/img/TelaBoss.png')
boss_bg = pygame.transform.scale(boss_bg, (x, y))

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

boss_img = pygame.image.load('pygame_aplication-main/img/TelaBoss.png').convert_alpha()
boss_img = pygame.transform.scale(boss_img, (200, 200))

# Fonte
fonte = pygame.font.SysFont('font/PixelGameFont.ttf', 50)
fonte_pontos = pygame.font.SysFont('font/PixelGameFont.ttf', 32)

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

def selecionar_nivel():
    selecionando = True
    opcoes = ['Iniciante', 'Intermediário', 'Difícil']
    indice_selecionado = 0

    while selecionando:
        screen.blit(bg, (0, 0))
        titulo = fonte.render('Selecione o Nível', True, (255, 255, 0))
        screen.blit(titulo, ((x - titulo.get_width()) // 2, 100))

        for i, opcao in enumerate(opcoes):
            cor = (255, 255, 255)
            if i == indice_selecionado:
                cor = (0, 255, 255)
            texto_opcao = fonte_pontos.render(f'{i+1} - {opcao}', True, cor)
            screen.blit(texto_opcao, ((x - texto_opcao.get_width()) // 2, 250 + i * 80))

        instrucao = fonte_pontos.render('Use Seta para Cima & Seta para Baixo para navegar | Enter para confirmar', True, (180, 180, 180))
        screen.blit(instrucao, ((x - instrucao.get_width()) // 2, 550))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and indice_selecionado > 0:
                    indice_selecionado -= 1
                elif event.key == pygame.K_DOWN and indice_selecionado < len(opcoes) - 1:
                    indice_selecionado += 1
                elif event.key == pygame.K_RETURN:
                    return indice_selecionado + 1

def respawn():
    return [1350, random.randint(1, 640)]

def respawn_golpe(pos_x, pos_y):
    return [pos_x, pos_y, False, 2.0]

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
    global vidas, game_over, pontos, vel_inimigo, mostrar_nivel
    global ultimo_tiro, tempo_recarga, tempo_nivel
    global boss_vida, boss_apareceu, inimigos_extra

    pos_inimigo_x, pos_inimigo_y = respawn()
    pos_player_x, pos_player_y = 200, 300
    pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)
    vidas = 100
    pontos = 0
    game_over = False
    mostrar_nivel = True
    tempo_nivel = pygame.time.get_ticks()
    ultimo_tiro = 0
    tempo_recarga = 400

    boss_vida = 20
    boss_apareceu = False
    inimigos_extra = []

    if nivel == 1:
        vel_inimigo = 0.5
    elif nivel == 2:
        vel_inimigo = 1.0
    elif nivel == 3:
        vel_inimigo = 0.5
    elif nivel == 4:
        vel_inimigo = 0.5
    elif nivel == 5:
        vel_inimigo = 0.5

# Início do jogo
tela_inicio()
nivel = selecionar_nivel()
reset_game()

# Variáveis gerais
tempo_nivel = 0
recorde = 0
spawn_timer = 0
spawn_delay = 1000
rodando = True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tempo_atual = pygame.time.get_ticks()

    if pontos >= nivel * 10 and nivel < 6:
        nivel += 1
        if nivel < 6:
            vel_inimigo += 0.3
        vidas = 7
        mostrar_nivel = True
        tempo_nivel = tempo_atual

    if pontos > recorde:
        recorde = pontos

    if nivel == 1:
        screen.blit(bg, (0, 0))
    elif nivel == 2:
        screen.blit(novo_bg, (0, 0))
    elif nivel == 3:
        screen.blit(nivel_3_bg, (0, 0))
    elif nivel == 4:
        screen.blit(nivel_4_bg, (0, 0))
    elif nivel == 5:
        screen.blit(nivel_5_bg, (0, 0))
    elif nivel == 6:
        screen.blit(boss_bg, (0, 0))
        boss_apareceu = True

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

        if boss_apareceu:
            boss_rect = boss_img.get_rect(topleft=(1650, 400))
            screen.blit(boss_img, boss_rect)
            if golpe_rect.colliderect(boss_rect) and triggered:
                boss_vida -= 1
                triggered = False
                pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)

            barra_total = 300
            barra_atual = int(barra_total * (boss_vida / 20))
            pygame.draw.rect(screen, (255, 0, 0), (boss_rect.x, boss_rect.y - 20, barra_total, 20))
            pygame.draw.rect(screen, (0, 255, 0), (boss_rect.x, boss_rect.y - 20, barra_atual, 20))

            if boss_vida <= 0:
                vitoria_text = fonte.render('VOCÊ VENCEU!', True, (255, 255, 0))
                screen.blit(vitoria_text, ((x - vitoria_text.get_width()) // 2, y // 2))
                pygame.display.update()
                pygame.time.delay(5000)
                tela_inicio()
                nivel = selecionar_nivel()
                reset_game()

            if tempo_atual - spawn_timer > spawn_delay:
                inimigos_extra.append(respawn())
                spawn_timer = tempo_atual

            for idx, (ix, iy) in enumerate(inimigos_extra):
                ix -= vel_inimigo
                inimigos_extra[idx][0] = ix
                rect_extra = inimigo.get_rect(topleft=(ix, iy))
                screen.blit(inimigo, (ix, iy))

                if rect_extra.colliderect(player_rect):
                    vidas -= 1
                    inimigos_extra[idx][0] = -100

                if golpe_rect.colliderect(rect_extra):
                    pontos += 1
                    inimigos_extra[idx][0] = -100
                    triggered = False
                    pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)

        for i in range(vidas):
            screen.blit(heart_img, (50 + i * 45, 50))

        pontos_txt = fonte_pontos.render(f'Score: {pontos}', True, (255, 255, 255))
        screen.blit(pontos_txt, (x - pontos_txt.get_width() - 20, 20))

        recorde_txt = fonte_pontos.render(f'High Score: {recorde}', True, (255, 255, 0))
        screen.blit(recorde_txt, ((x - recorde_txt.get_width()) // 2, pontos_txt.get_height() + 30))

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
            nivel = selecionar_nivel()
            reset_game()

    pygame.display.update()
