import pygame
import sys
pygame.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo Top-Down")
clock = pygame.time.Clock()

TAM = 32

# mapa
mapa = []
arquivo = open('mapa.txt', 'r')
for linha in arquivo:
    mapa.append(list(linha.strip()))
arquivo.close()


# tirar do arquivo
spritesheet = pygame.image.load('personagem.png').convert_alpha()
tileset = pygame.image.load('Tileset.png').convert_alpha()
tile_chao = tileset.subsurface(pygame.Rect(0, 0, 32, 32))
tile_parede = tileset.subsurface(pygame.Rect(192, 0, 32, 32))


cortes_animacao = {
    'baixo':    [(0, 0, 32, 32), (32, 0, 32, 32), (64, 0, 32, 32), (96, 0, 32, 32)],
    'direita':  [(0, 32, 32, 32), (32, 32, 32, 32), (64, 32, 32, 32), (96, 32, 32, 32)],
    'cima':     [(0, 64, 32, 32), (32, 64, 32, 32), (64, 64, 32, 32), (96, 64, 32, 32)],
    'esquerda': [(0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 32, 32), (96, 96, 32, 32)],
}


px = 100
py = 100
vel = 4
direcao = 'baixo'
frame_atual = 0.0
cam_x = 0
cam_y = 0

# colisao
def checar_colisao(novo_x, novo_y):
    rect_player = pygame.Rect(novo_x, novo_y, TAM, TAM)
    for l in range(len(mapa)):
        for c in range(len(mapa[l])):
            if mapa[l][c] == '1':
                rect_parede = pygame.Rect(c * TAM, l * TAM, TAM, TAM)
                if rect_player.colliderect(rect_parede):
                    return True
    return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    keys = pygame.key.get_pressed()
    andando = False
    prox_x = px
    prox_y = py

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        prox_x -= vel
        direcao = 'esquerda'
        andando = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        prox_x += vel
        direcao = 'direita'
        andando = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        prox_y -= vel
        direcao = 'cima'
        andando = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        prox_y += vel
        direcao = 'baixo'
        andando = True

    # movimento
    if andando:
        if not checar_colisao(prox_x, py):
            px = prox_x
        if not checar_colisao(px, prox_y):
            py = prox_y
        frame_atual += 0.15
        if frame_atual >= 4:
            frame_atual = 0.0
    else:
        frame_atual = 0.0

    
    cam_x = px - (LARGURA_TELA / 2) + (TAM / 2)
    cam_y = py - (ALTURA_TELA / 2) + (TAM / 2)

    tela.fill((0, 0, 0))

    # chao
    for l in range(len(mapa)):
        for c in range(len(mapa[l])):
            x_tela = (c * TAM) - cam_x
            y_tela = (l * TAM) - cam_y
            if mapa[l][c] == '1':
                tela.blit(tile_parede, (x_tela, y_tela))
            elif mapa[l][c] == '0':
                tela.blit(tile_chao, (x_tela, y_tela))

    # personagem
    x_player_tela = px - cam_x
    y_player_tela = py - cam_y
    corte = cortes_animacao[direcao][int(frame_atual)]
    imagem = spritesheet.subsurface(pygame.Rect(corte))
    tela.blit(imagem, (x_player_tela, y_player_tela))

    pygame.display.update()
    clock.tick(60)