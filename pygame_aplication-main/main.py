import pygame
import random
import sys

pygame.init()

# Tela
x = 1920
y = 1080
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

# Nomes personalizados das fases
nomes_fases = {
    1: "XEN-2901",
    2: "MAR-4398",
    3: "ULR-0991",
    4: "ZET-8892",
    5: "TOR-3922",
    6: "BOSS"
}

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

def respawn_golpe(pos_x, pos_y, velocidade=2.0):
    return [pos_x, pos_y, False, velocidade]

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
    global vidas, game_over, vel_inimigo, mostrar_nivel
    global ultimo_tiro, tempo_recarga, tempo_nivel
    global boss_vida, boss_apareceu, inimigos_extra

    pos_inimigo_x, pos_inimigo_y = respawn()
    pos_player_x, pos_player_y = 200, 300
    vel_tiro = 2.0
    pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y, vel_tiro)
    game_over = False
    mostrar_nivel = True
    tempo_nivel = pygame.time.get_ticks()
    ultimo_tiro = 0
    tempo_recarga = 400
    boss_vida = 2
    boss_apareceu = False
    inimigos_extra = []

    if dificuldade == 1:
        vidas = 10
        vel_inimigo = 1.0
    elif dificuldade == 2:
        vidas = 7
        vel_inimigo = 1.2
    elif dificuldade == 3:
        vidas = 5
        vel_inimigo = 1.5

def show_credits_screen():
    scroll_y = y
    credit_bg = pygame.image.load('pygame_aplication-main/img/TelaCréditos.png')
    credit_bg = pygame.transform.scale(credit_bg, (x, y))

    credit_lines = [
        "Marlos Gomes (P.O)",
        "Leonardo Silva (Scrum Master)",
        "Leticia Rosa (DEV & Scrum Master)",
        "Juan (DEV)"
    ]

    while scroll_y > -len(credit_lines) * 60:
        screen.blit(credit_bg, (0, 0))
        for i, line in enumerate(credit_lines):
            text = fonte.render(line, True, (255, 255, 255))
            screen.blit(text, (x // 2 - text.get_width() // 2, scroll_y + i * 60))

        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        pygame.time.wait(50)
        scroll_y -= 2

    pygame.time.wait(3000)  # Espera 3 segundos após os créditos

# Início do jogo
tela_inicio()
dificuldade = selecionar_nivel()
nivel = 1
pontos = 0
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

    if pontos >= nivel * 2 and nivel < 6:
        nivel += 1
        mostrar_nivel = True
        tempo_nivel = tempo_atual
        reset_game()

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

        if (tecla[pygame.K_DOWN] or tecla[pygame.K_s]) and pos_player_y < 665:
            pos_player_y += 1

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
            if boss_apareceu:
                boss_vida -= 1
            pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)

        if pos_inimigo_x <= 50 or colisions():
            pos_inimigo_x, pos_inimigo_y = respawn()

        screen.blit(playerImg, (pos_player_x, pos_player_y))
        screen.blit(golpe, (pos_x_golpe, pos_y_golpe))
        screen.blit(inimigo, (pos_inimigo_x, pos_inimigo_y))

        if boss_apareceu:
            boss_rect = boss_img.get_rect(topleft=(1650, 400))
            if golpe_rect.colliderect(boss_rect) and triggered:
                boss_vida -= 1
                triggered = False
                pos_x_golpe, pos_y_golpe, triggered, vel_x_golpe = respawn_golpe(pos_player_x, pos_player_y)

            barra_total = 300
            barra_atual = int(barra_total * (boss_vida / 2))
            barra_x = x - barra_total - 50
            barra_y = 50
            pygame.draw.rect(screen, (255, 0, 0), (barra_x, barra_y, barra_total, 20))
            pygame.draw.rect(screen, (0, 255, 0), (barra_x, barra_y, barra_atual, 20))

            if boss_vida <= 0:
                vitoria_text = fonte.render('VOCÊ VENCEU!', True, (255, 255, 0))
                screen.blit(vitoria_text, ((x - vitoria_text.get_width()) // 2, y // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                show_credits_screen()
                tela_inicio()
                dificuldade = selecionar_nivel()
                nivel = 1
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
                nome_fase = nomes_fases.get(nivel, f"FASE {nivel}")
                texto_nivel = fonte.render(nome_fase, True, (255, 255, 0))
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
            dificuldade = selecionar_nivel()
            nivel = 1
            reset_game()

    pygame.display.update()

pygame.quit()
sys.exit()