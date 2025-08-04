import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# CONFIGURAÇÕES
LARGURA, ALTURA = 964, 540
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Planet Star Wars')

# SOM
pygame.mixer.music.load(r"D:\Natália\PlanetStarWars\sounds\R2talkStarJogo.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# CORES

AZUL_NEON = (0, 255, 255)       # Destaques, botões
AZUL_ESCURO = (10, 10, 50)      # Fundo principal
BRANCO = (200, 200, 200)   # Texto comum
PRETO = (230, 230, 230)  # Texto em botões
ROXO_NEON = (138, 43, 226)      # Destaques e tiros
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Fundo de batalha
FUNDO_BATALHA = pygame.image.load("D:/Natália/PlanetStarWars/fundo/ep1windows.jpg")
FUNDO_BATALHA = pygame.transform.scale(FUNDO_BATALHA, (LARGURA, ALTURA))

# Caminho das imagens e sons
PLAYER_FOLDER = "D:/Natália/PlanetStarWars/Player/"
SOUNDS_FOLDER = "D:/Natália/PlanetStarWars/Sounds/"

# Caminho das imagens JOGO BATALHA #
PLAYER_FOLDER = "D:/Natália/PlanetStarWars/Player/"


# FONTES
fonte = pygame.font.SysFont("arial", 20)

# SOM
som_ativo = True
pygame.mixer.init()

# ======= NOVO FUNDO ANIMADO =======
estrelas = [[random.randint(0, LARGURA), random.randint(0, ALTURA), random.randint(1, 3)] for _ in range(200)]

def desenhar_fundo_animado():
    janela.fill((5, 5, 20))  # Fundo tipo gradiente escuro
    for estrela in estrelas:
        x, y, tamanho = estrela
        pygame.draw.circle(janela, (255, 255, 255), (x, y), tamanho)
        estrela[1] += tamanho * 0.3
        if estrela[1] > ALTURA:
            estrela[0] = random.randint(0, LARGURA)
            estrela[1] = 0
            estrela[2] = random.randint(1, 3)

# ===== IMAGENS =====
imagem_menu = pygame.image.load(r"D:\Natália\PlanetStarWars\images\fundo_menu1.png")
nave_resistencia = pygame.image.load(r"D:\Natália\PlanetStarWars\images\navestarwars.png")
laser_azul = pygame.transform.scale(pygame.image.load(r"D:\Natália\PlanetStarWars\images\laser_azul.png"), (16, 60))
nave_primeira_ordem = pygame.image.load(r"D:\Natália\PlanetStarWars\images\navestarwarsInimiga.png")
laser_vermelho = pygame.transform.scale(pygame.image.load(r"D:\Natália\PlanetStarWars\images\navestarwarsInimiga.png"), (10, 40))

# Sprites de movimento e ataque
# Sprites de movimento e ataque redimensionados

def carregar_e_redimensionar(caminho, escala=0.3):
    imagem_original = pygame.image.load(caminho)
    largura = int(imagem_original.get_width() * escala)
    altura = int(imagem_original.get_height() * escala)
    return pygame.transform.smoothscale(imagem_original, (largura, altura))

walk_images = [
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyandando.png")),
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyandando2.png")),
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyandando3.png")),
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyandando4.png")),
]

attack_images = [
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyandandoSabre5.png")),
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyandandoSabre6.png")),
]

breath_images = [
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyrespirando1.png")),
    carregar_e_redimensionar(os.path.join(PLAYER_FOLDER, "reyrespirando2.png")),
]

# ====== PERSONAGENS DISPONÍVEIS ======
personagens = {
    "cassian": pygame.image.load(r"D:\Natália\PlanetStarWars\Personagens\cassian.png"),
    "grogu": pygame.image.load(r"D:\Natália\PlanetStarWars\Personagens\Mandalorian.png"),
    "rey": pygame.image.load(r"D:\Natália\PlanetStarWars\Personagens\rey.png")
}

# ======= VARIÁVEIS GLOBAIS  =========
personagem_escolhido = None
modo_jogo_escolhido = None  # "nave" ou "batalha"

# POSIÇÕES E DADOS DO JOGO
pos_y_resistencia = 400
pos_x_resistencia = 420
vel_nave_resistencia = 10

pos_x_primeira_ordem = 400
pos_y_primeira_ordem = 50

tiros_azuis = []
tiros_vermelhos = []
vel_tiro = 12

tempo_tiro_inimigo = 0
intervalo_tiro_inimigo = 60
clock = pygame.time.Clock()

# ===== BOTÕES DO MENU =====
def desenha_botao(texto, x, y, w, h, cor_normal, cor_fonte_hover, acao=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    mouse_sobre = x + w > mouse[0] > x and y + h > mouse[1] > y

    superficie_botao = pygame.Surface((w, h), pygame.SRCALPHA)
    cor_base = (*cor_normal, 150)
    cor_hover = (*ROXO_NEON, 180)
    cor_usada = cor_hover if mouse_sobre else cor_base

    pygame.draw.rect(superficie_botao, cor_usada, (0, 0, w, h), border_radius=12)
    janela.blit(superficie_botao, (x, y))

    cor_texto = cor_fonte_hover if mouse_sobre else PRETO
    texto_render = fonte.render(texto, True, cor_texto)
    janela.blit(texto_render, (x + (w / 2 - texto_render.get_width() / 2), y + (h / 2 - texto_render.get_height() / 2)))

    if mouse_sobre and click[0] == 1 and acao is not None:
        pygame.time.delay(200)
        acao()

# === AÇÕES DOS BOTÕES ===
def iniciar_jogo():
    global menu_ativo
    menu_ativo = False

def sair_jogo():
    pygame.quit()
    sys.exit()

def alternar_som():
    global som_ativo
    som_ativo = not som_ativo
    pygame.mixer.music.set_volume(1.0 if som_ativo else 0.0)

# ====== TELA DE SELEÇÃO DE PERSONAGEM ======
def selecionar_personagem():
    global personagem_escolhido
    selecionando = True
    while selecionando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 100 < x < 228 and 150 < y < 278:
                    personagem_escolhido = personagens["cassian"]
                    selecionando = False
                elif 400 < x < 528 and 150 < y < 278:
                    personagem_escolhido = personagens["grogu"]
                    selecionando = False
                elif 700 < x < 828 and 150 < y < 278:
                    personagem_escolhido = personagens["rey"]
                    selecionando = False

        desenhar_fundo_animado()
        texto = fonte.render("Escolha seu personagem da Resistência", True, PRETO)
        janela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 50))

        janela.blit(pygame.transform.scale(personagens["cassian"], (128, 128)), (100, 150))
        janela.blit(pygame.transform.scale(personagens["grogu"], (128, 128)), (400, 150))
        janela.blit(pygame.transform.scale(personagens["rey"], (128, 128)), (700, 150))

        pygame.display.update()

def selecionar_modo_jogo():
    global modo_jogo_escolhido
    selecionando = True
    while selecionando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 200 < x < 380 and 200 < y < 300:
                    modo_jogo_escolhido = "nave"
                    selecionando = False
                elif 600 < x < 780 and 200 < y < 300:
                    modo_jogo_escolhido = "batalha"
                    selecionando = False

        desenhar_fundo_animado()

        # Título
        texto = fonte.render("Escolha o tipo de jogo", True, BRANCO)
        janela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 50))

        pygame.draw.rect(janela, ROXO_NEON, (200, 200, 180, 100), border_radius=10)
        pygame.draw.rect(janela, ROXO_NEON, (600, 200, 180, 100), border_radius=10)
        


        txt_nave = fonte.render("Jogo da Nave", True, BRANCO)
        txt_batalha = fonte.render("Jogo de Batalha", True, BRANCO)
        janela.blit(txt_nave, (200 + 90 - txt_nave.get_width() // 2, 200 + 50 - txt_nave.get_height() // 2))
        janela.blit(txt_batalha, (600 + 90 - txt_batalha.get_width() // 2, 200 + 50 - txt_batalha.get_height() // 2))
        pygame.display.update()

# ====== JOGO DE NAVE ======

pontuacao = 0

nave_inimiga = pygame.image.load(r"D:\Natália\PlanetStarWars\images\navestarwarsInimiga.png")
nave_inimiga = pygame.transform.scale(nave_inimiga, (60, 60))


explosoes = []
for i in range(1, 9):
    imagem = pygame.image.load(fr"D:\Natália\PlanetStarWars\explosão\explosion1.png")
    imagem = pygame.transform.scale(imagem, (60, 60))  # redimensiona para o tamanho do inimigo
    explosoes.append(imagem)
    
som_explosao = pygame.mixer.Sound(r"D:\Natália\PlanetStarWars\Sounds\explosion SFX.mp3")


inimigos = []
num_inimigos = 5  

for i in range(num_inimigos):
    x = random.randint(0, LARGURA - 60)
    y = random.randint(-500, -60)
    velocidade = random.randint(1, 3)
    inimigos.append({"x": x, "y": y, "vel": velocidade})


inimigos = []
num_inimigos = 10  

for i in range(num_inimigos):
    x = random.randint(0, LARGURA - 60)
    y = random.randint(-500, -60)
    velocidade = random.randint(1, 3)
    inimigos.append({"x": x, "y": y, "vel": velocidade})
    
largura = 800
altura = 600

def rodar_jogo():
    global pontuacao
    global largura, altura

    global pos_x_resistencia, pos_y_resistencia, tempo_tiro_inimigo, tiros_azuis, tiros_vermelhos

    explosoes_ativas = []
    loop = True

    while loop:
        clock.tick(60)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento da nave da resistência
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            pos_y_resistencia -= vel_nave_resistencia
        if teclas[pygame.K_DOWN]:
            pos_y_resistencia += vel_nave_resistencia
        if teclas[pygame.K_LEFT]:
            pos_x_resistencia -= vel_nave_resistencia
        if teclas[pygame.K_RIGHT]:
            pos_x_resistencia += vel_nave_resistencia
        if teclas[pygame.K_SPACE]:
            tiros_azuis.append([pos_x_resistencia + 20, pos_y_resistencia])

        # Limites da tela
        pos_y_resistencia = max(0, min(pos_y_resistencia, 440))
        pos_x_resistencia = max(0, min(pos_x_resistencia, 870))

        # Tempo de tiro inimigo
        tempo_tiro_inimigo += 1
        if tempo_tiro_inimigo >= intervalo_tiro_inimigo:
            tiros_vermelhos.append([pos_x_primeira_ordem + 20, pos_y_primeira_ordem + 40])
            tempo_tiro_inimigo = 0

        # Movimento dos tiros
        for tiro in tiros_azuis:
            tiro[1] -= vel_tiro
        for tiro in tiros_vermelhos:
            tiro[1] += vel_tiro

        # Remove tiros fora da tela
        tiros_azuis = [t for t in tiros_azuis if t[1] > -20]
        tiros_vermelhos = [t for t in tiros_vermelhos if t[1] < 540]

        # Fundo
        desenhar_fundo_animado()

        # Desenha nave da resistência
        janela.blit(nave_resistencia, (pos_x_resistencia, pos_y_resistencia))
        resistencia_rect = pygame.Rect(pos_x_resistencia, pos_y_resistencia, nave_resistencia.get_width(), nave_resistencia.get_height())

        inimigos_atingidos = []

        for inimigo in inimigos:
            inimigo_rect = pygame.Rect(inimigo["x"], inimigo["y"], 60, 60)

            # Verifica colisão da nave da resistência com inimigos
            if resistencia_rect.colliderect(inimigo_rect):
                explosoes_ativas.append({
                    "x": pos_x_resistencia,
                    "y": pos_y_resistencia,
                    "frame": 0,
                    "tempo": 0
                })
                som_explosao.play()
                pontuacao -= 1  
                pontuacao = max(0, pontuacao - 1)
                print("🚨 Colisão! A nave da resistência foi atingida!")
                
                inimigo["y"] = -60
                inimigo["x"] = random.randint(50, largura - 110) # type: ignore
                
                

            # Verifica colisão com os tiros azuis
            for tiro in tiros_azuis:
                tiro_rect = pygame.Rect(tiro[0], tiro[1], 10, 20)
                if inimigo_rect.colliderect(tiro_rect):
                    inimigos_atingidos.append(inimigo)
                    explosoes_ativas.append({
                        "x": inimigo["x"],
                        "y": inimigo["y"],
                        "frame": 0,
                        "tempo": 0
                    })
                    som_explosao.play()
                    pontuacao += 1
                    tiros_azuis.remove(tiro)
                    break

            # Se não foi atingido, movimenta e desenha
            if inimigo not in inimigos_atingidos:
                inimigo["y"] += inimigo["vel"]
                if inimigo["y"] > ALTURA:
                    inimigo["y"] = random.randint(-500, -60)
                    inimigo["x"] = random.randint(0, LARGURA - 60)
                janela.blit(nave_inimiga, (inimigo["x"], inimigo["y"]))
            
                

        # Reposiciona inimigos atingidos
        for inimigo in inimigos_atingidos:
            inimigo["x"] = random.randint(0, LARGURA - 60)
            inimigo["y"] = random.randint(-500, -60)
            inimigo["vel"] = random.randint(1, 3)

        # Desenhar tiros
        for tiro in tiros_azuis:
            janela.blit(laser_azul, (tiro[0], tiro[1]))

        # Miniatura do personagem escolhido
        if personagem_escolhido:
            imagem_redimensionada = pygame.transform.scale(personagem_escolhido, (100, 100))
            janela.blit(imagem_redimensionada, (LARGURA - 110, ALTURA - 110))

        # Animação das explosões
        for explosao in explosoes_ativas[:]:
            imagem = explosoes[explosao["frame"]]
            janela.blit(imagem, (explosao["x"], explosao["y"]))
            explosao["tempo"] += 1
            if explosao["tempo"] >= 3:
                explosao["tempo"] = 0
                explosao["frame"] += 1
                if explosao["frame"] >= len(explosoes):
                    explosoes_ativas.remove(explosao)

        # Pontuação
        fonte_pontos = pygame.font.SysFont("Arial", 28)
        txt_pontos = fonte_pontos.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
        janela.blit(txt_pontos, (10, 10))
        
        

        pygame.display.update()
        
## ==== JOGO BATALHA =====

def rodar_jogo_batalha():
    def carregar_imagem(nome, escala=0.3):
        img = pygame.image.load(os.path.join(PLAYER_FOLDER, nome)).convert_alpha()
        largura = int(img.get_width() * escala)
        altura = int(img.get_height() * escala)
        return pygame.transform.smoothscale(img, (largura, altura))

    # === Carregar fundo da batalha ===
    fundo_batalha = pygame.image.load("D:/Natália/PlanetStarWars/fundo/ep1windows.jpg").convert()
    fundo_batalha = pygame.transform.scale(fundo_batalha, (LARGURA, ALTURA))

    # Sons
    sabre_som = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, "sabre_rey.wav"))
    vitoria_som = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, "vitoria.wav"))

    # Rey - Sprites
    rey_walk = [carregar_imagem(f"reyandando{i}.png") for i in ["", "2", "3", "4"]]
    rey_attack = [carregar_imagem(f"reyandandoSabre{i}.png") for i in ["5", "6"]]
    rey_breath = [carregar_imagem(f"reyrespirando{i}.png") for i in ["1", "2"]]

    # Darth Sidious - Sprites
    sidious_walk = [
        carregar_imagem("DarthSidiousandando.png"),
        carregar_imagem("DarthSidiousparado.png"),
        carregar_imagem("DarthSidiouscorrendo.png"),
        carregar_imagem("DarthSidiousandando.png"),
    ]
    sidious_attack = [
        carregar_imagem("DarthSidioussabredeluz.png"),
        carregar_imagem("DarthSidioussabredeluz2.png"),
    ]

    def desenhar_vida_bar(surface, x, y, vida, cor):
        largura_total = 150
        altura = 15
        pygame.draw.rect(surface, PRETO, (x-2, y-2, largura_total+4, altura+4))
        pygame.draw.rect(surface, cor, (x, y, max(0, vida), altura))

    class Personagem(pygame.sprite.Sprite):
        def __init__(self, walk, attack, breath, x, lado='right'):
            super().__init__()
            self.walk = walk
            self.attack = attack
            self.breath = breath
            self.walk_index = 0
            self.breath_index = 0
            self.image = breath[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = ALTURA - self.rect.height
            self.vel_x = 0
            self.vel_y = 0
            self.speed = 2
            self.jump_power = 14
            self.gravity = 0.6
            self.jump_count = 0
            self.max_jumps = 2
            self.on_ground = True
            self.attacking = False
            self.attack_timer = 0
            self.attack_duration = 15
            self.facing_right = True if lado == 'right' else False
            self.animation_counter = 0
            self.vida = 150

        def limitar_tela(self):
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > LARGURA:
                self.rect.right = LARGURA

        def atacar(self):
            self.attacking = True
            self.attack_timer = self.attack_duration
            sabre_som.play()

        def aplicar_gravidade(self):
            self.rect.y += self.vel_y
            self.vel_y += self.gravity
            if self.rect.bottom >= ALTURA:
                self.rect.bottom = ALTURA
                self.vel_y = 0
                self.jump_count = 0
                self.on_ground = True
            else:
                self.on_ground = False

        def animar(self):
            if self.attacking:
                frame = (self.attack_duration - self.attack_timer) // (self.attack_duration // len(self.attack))
                frame = min(frame, len(self.attack) - 1)
                self.image = self.attack[frame]
            elif self.vel_x != 0:
                self.animation_counter += 1
                if self.animation_counter >= 5:
                    self.walk_index = (self.walk_index + 1) % len(self.walk)
                    self.animation_counter = 0
                self.image = self.walk[self.walk_index]
            elif self.on_ground:
                self.animation_counter += 1
                if self.animation_counter >= 30:
                    self.breath_index = (self.breath_index + 1) % len(self.breath)
                    self.animation_counter = 0
                self.image = self.breath[self.breath_index]
            else:
                self.image = self.walk[0]

            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    class Rey(Personagem):
        def update(self, keys):
            self.vel_x = 0
            if keys[pygame.K_LEFT]:
                self.vel_x = -self.speed
                self.facing_right = False
            if keys[pygame.K_RIGHT]:
                self.vel_x = self.speed
                self.facing_right = True
            if keys[pygame.K_LSHIFT]:
                self.vel_x *= 1.5
            if keys[pygame.K_SPACE] and self.jump_count < self.max_jumps:
                self.vel_y = -self.jump_power
                self.jump_count += 1
            if keys[pygame.K_a] and not self.attacking:
                self.atacar()

            self.rect.x += self.vel_x
            self.aplicar_gravidade()
            self.limitar_tela()

            if self.attacking:
                self.attack_timer -= 1
                if self.attack_timer <= 0:
                    self.attacking = False

            self.animar()

    class DarthSidious(Personagem):
        def __init__(self, walk, attack, breath, x, lado='left'):
            super().__init__(walk, attack, attack, x, lado)
            self.speed = 2

        def update(self, target):
            if abs(self.rect.centerx - target.rect.centerx) > 50:
                if self.rect.centerx < target.rect.centerx:
                    self.rect.x += self.speed
                else:
                    self.rect.x -= self.speed

            self.facing_right = self.rect.centerx < target.rect.centerx

            if abs(self.rect.centerx - target.rect.centerx) < 70 and not self.attacking:
                self.atacar()

            self.aplicar_gravidade()
            self.limitar_tela()

            if self.attacking:
                self.attack_timer -= 1
                if self.attack_timer <= 0:
                    self.attacking = False

            self.animar()

    player = Rey(rey_walk, rey_attack, rey_breath, 100)
    enemy = DarthSidious(sidious_walk, sidious_attack, sidious_walk, 700, lado='left')
    all_sprites = pygame.sprite.Group(player, enemy)

    clock = pygame.time.Clock()
    running = True
    fonte = pygame.font.SysFont("arial", 24)
    vencedor = None

    botao_voltar = pygame.Rect(20, ALTURA - 60, 180, 40)


    while running:
        clock.tick(60)
        janela.blit(fundo_batalha, (0, 0))  # Aplica fundo personalizado da batalha

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    

        if vencedor is None:
            player.update(keys)
            enemy.update(player)

            if player.attacking and player.rect.colliderect(enemy.rect):
                enemy.vida -= 1
            if enemy.attacking and enemy.rect.colliderect(player.rect):
                player.vida -= 1

            if player.vida <= 0:
                vencedor = "Darth Sidious venceu!"
                vitoria_som.play()
            elif enemy.vida <= 0:
                vencedor = "Rey venceu!"
                vitoria_som.play()

        all_sprites.draw(janela)

        desenhar_vida_bar(janela, 20, 20, player.vida, VERDE)
        desenhar_vida_bar(janela, LARGURA - 170, 20, enemy.vida, VERMELHO)

        if vencedor:
            texto = fonte.render(vencedor, True, BRANCO)
            janela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))

        
       


        pygame.display.update()


menu_ativo = True
while menu_ativo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    janela.blit(imagem_menu, (0, 0))
    desenha_botao("Start", 400, 220, 160, 50, AZUL_NEON, AZUL_NEON, iniciar_jogo)
    desenha_botao("Música ON/OFF", 400, 290, 160, 50, AZUL_NEON, AZUL_NEON, alternar_som)
    desenha_botao("Sair", 400, 360, 160, 50, AZUL_NEON, AZUL_NEON, sair_jogo)

    pygame.display.update()

# Música

pygame.mixer.music.load(r"D:\Natália\PlanetStarWars\sounds\MusicaBatalhaStarwars.wav")
pygame.mixer.music.play(-1)

# === Fluxo correto após o menu ser fechado ===
selecionar_modo_jogo()
selecionar_personagem()

if modo_jogo_escolhido == "nave":
    rodar_jogo()
elif modo_jogo_escolhido == "batalha":
    rodar_jogo_batalha()