import pygame
import os
import random
import math

# Inicializa o Pygame
pygame.init()

# Define o tamanho da tela
altura = 600
largura = 1000

# Define as cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

# Define uma variável que indica os quadros por segundo
tempo = pygame.time.Clock()

# Define a tela
tela = pygame.display.set_mode((largura, altura))

# Define o nome que vai aparecer na tela
pygame.display.set_caption('Junk Jumper')

# Define as imagens
CORRIDA = [pygame.image.load(os.path.join('Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Dino', 'DinoRun2.png'))]
PULO = pygame.image.load(os.path.join('Dino', 'DinoJump.png'))
AGACHAR = [pygame.image.load(os.path.join('Dino', 'DinoDuck1.png')),
           pygame.image.load(os.path.join('Dino', 'DinoDuck2.png'))]
CACTO_G = [pygame.image.load(os.path.join('cacto', 'LargeCactus1.png')),
           pygame.image.load(os.path.join('cacto', 'LargeCactus2.png')),
           pygame.image.load(os.path.join('cacto', 'LargeCactus3.png'))]
CACTO_P = [pygame.image.load(os.path.join('cacto', 'SmallCactus1.png')),
           pygame.image.load(os.path.join('cacto', 'SmallCactus2.png')),
           pygame.image.load(os.path.join('cacto', 'SmallCactus3.png'))]
PTERO = [pygame.image.load(os.path.join('ptero', 'Bird1.png')),
         pygame.image.load(os.path.join('ptero', 'Bird2.png'))]
CHAO = pygame.image.load(os.path.join('outro', 'chão.png'))
GAME_OVER = pygame.image.load(os.path.join('outro', 'GameOver.png'))
RESET = pygame.image.load(os.path.join('outro', 'Reset.png'))

# Função para criar sons simples
def criar_som(frequencia, duracao, volume=1.0):
    """
    Cria um som simples.

    Args:
        frequencia (float): Frequência do som (Hz).
        duracao (float): Duração do som (s).
        volume (float, opcional): Volume do som (0.0 a 1.0). Padrão = 1.0.

    Retorna:
        pygame.mixer.Sound: Objeto de som gerado.
    """
    sample_rate = 44100
    n_samples = int(round(duracao * sample_rate))
    buf = bytearray()

    amplitude = 32767 * volume
    for s in range(n_samples):
        t = float(s) / sample_rate
        val = int(amplitude * math.sin(2.0 * math.pi * frequencia * t))
        buf.append(val & 0xff)
        buf.append((val >> 8) & 0xff)

    return pygame.mixer.Sound(buffer=bytes(buf))

# Carrega os sons padrão gerados
som_pulo = criar_som(440, 0.1)
som_colisao = criar_som(220, 0.1)

# Configura fonte para o contador e para o texto de game over
fonte = pygame.font.Font(None, 36)
fonte_game_over = pygame.font.Font(None, 48)

class Dinossauro:
    """Classe que representa o dinossauro no jogo."""

    X_POS = 80
    Y_POS = 500
    Y_POS_AGACHAR = 530
    VEL_PULO = 8.5

    def __init__(self):
        """Inicializa o dinossauro com suas imagens e posições."""
        self.img_agachar = AGACHAR
        self.img_correr = CORRIDA
        self.img_pular = PULO
        self.agachado = False
        self.correndo = True
        self.pulando = False
        self.indice_passo = 0
        self.vel_pulo = self.VEL_PULO
        self.imagem = self.img_correr[0]
        self.retangulo = self.imagem.get_rect()
        self.retangulo.x = self.X_POS
        self.retangulo.y = self.Y_POS

    def atualizar(self, entrada_usuario, fator_velocidade):
        """Atualiza o estado do dinossauro com base na entrada do usuário."""
        if self.agachado:
            self.agachar()
        if self.correndo:
            self.correr()
        if self.pulando:
            self.pular()

        if self.indice_passo >= 10:
            self.indice_passo = 0

        if entrada_usuario[pygame.K_SPACE] and not self.pulando:
            self.agachado = False
            self.correndo = False
            self.pulando = True
            som_pulo.play()
        elif entrada_usuario[pygame.K_s] and not self.pulando:
            self.agachado = True
            self.correndo = False
            self.pulando = False
        elif not (self.pulando or entrada_usuario[pygame.K_s]):
            self.agachado = False
            self.correndo = True
            self.pulando = False

    def agachar(self):
        """Agacha o dinossauro."""
        self.imagem = self.img_agachar[self.indice_passo // 5]
        self.retangulo = self.imagem.get_rect()
        self.retangulo.x = self.X_POS
        self.retangulo.y = self.Y_POS_AGACHAR
        self.indice_passo += 1

    def correr(self):
        """Faz o dinossauro correr."""
        self.imagem = self.img_correr[self.indice_passo // 5]
        self.retangulo = self.imagem.get_rect()
        self.retangulo.x = self.X_POS
        self.retangulo.y = self.Y_POS
        self.indice_passo += 1

    def pular(self):
        """Faz o dinossauro pular."""
        self.imagem = self.img_pular
        if self.pulando:
            self.retangulo.y -= self.vel_pulo * 4
            self.vel_pulo -= 0.8
        if self.vel_pulo < -self.VEL_PULO:
            self.pulando = False
            self.correndo = True
            self.vel_pulo = self.VEL_PULO

    def desenhar(self, tela):
        """Desenha o dinossauro na tela."""
        tela.blit(self.imagem, (self.retangulo.x, self.retangulo.y))

    def colidir(self, obstaculos):
        """Verifica se o dinossauro colidiu com algum obstáculo."""
        for obstaculo in obstaculos:
            if self.retangulo.colliderect(obstaculo.retangulo):
                return True
        return False

dino = Dinossauro()

class Chao:
    """Classe que representa o chão no jogo."""

    VELOCIDADE = 15  

    def __init__(self, imagem):
        """Inicializa o chão com a imagem fornecida."""
        self.imagem = imagem
        self.largura = imagem.get_width()
        self.x1 = 0
        self.x2 = self.largura
        self.altura = imagem.get_height()

    def atualizar(self, fator_velocidade):
        """Atualiza a posição do chão com base na velocidade."""
        self.x1 -= self.VELOCIDADE * fator_velocidade
        self.x2 -= self.VELOCIDADE * fator_velocidade
        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        """Desenha o chão na tela."""
        tela.blit(self.imagem, (self.x1, altura - self.altura - 10))
        tela.blit(self.imagem, (self.x2, altura - self.altura - 10))

chao = Chao(CHAO)

class Obstaculo:
    """Classe que representa um obstáculo no jogo."""

    VELOCIDADE = Chao.VELOCIDADE

    def __init__(self, imagens):
        """
        Inicializa o obstáculo com uma imagem aleatória.

        Args:
            imagens (list): Lista de imagens para o obstáculo.
        """
        self.imagens = imagens
        self.imagem = self.imagens[0] if imagens == PTERO else random.choice(imagens)
        self.retangulo = self.imagem.get_rect()
        self.retangulo.x = largura
        if imagens == PTERO:
            self.retangulo.y = altura - self.retangulo.height - random.choice([150, 100, 70])  
            self.animar = True
            self.indice_animacao = 0
        else:
            self.retangulo.y = altura - self.retangulo.height - 10 
            self.animar = False

    def atualizar(self, fator_velocidade):
        """Atualiza a posição do obstáculo com base na velocidade."""
        self.retangulo.x -= self.VELOCIDADE * fator_velocidade
        if self.animar:
            self.indice_animacao += 1
            if self.indice_animacao >= 10:
                self.indice_animacao = 0
            self.imagem = self.imagens[self.indice_animacao // 5]

    def desenhar(self, tela):
        """Desenha o obstáculo na tela."""
        tela.blit(self.imagem, self.retangulo)

    def fora_da_tela(self):
        """Verifica se o obstáculo saiu da tela."""
        return self.retangulo.x < -self.retangulo.width

def pegar_obstaculo_aleatorio():
    """Retorna um obstáculo aleatório (cacto grande, pequeno ou pterodátilo)."""
    if random.randint(0, 2) == 0:
        return Obstaculo(CACTO_G)
    elif random.randint(0, 2) == 1:
        return Obstaculo(CACTO_P)
    else:
        return Obstaculo(PTERO)

def esperar_acao_inicio():
    """Aguarda até que o jogador pressione qualquer tecla para iniciar o jogo."""
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

def exibir_tela_inicio():
    """Exibe a tela de início e aguarda a ação do jogador."""
    tela.fill(BRANCO)
    texto_inicio = fonte_game_over.render('Pressione qualquer tecla para começar', True, PRETO)
    controles = [
        "Controles:",
        "Espaço: Pular",
        "S: Agachar"
    ]
    tela.blit(texto_inicio, (largura // 2 - texto_inicio.get_width() // 2, altura // 2))
    for i, controle in enumerate(controles):
        texto_controle = fonte.render(controle, True, PRETO)
        tela.blit(texto_controle, (largura // 2 - texto_controle.get_width() // 2, altura // 2 + 50 + i * 30))
    pygame.display.update()
    esperar_acao_inicio()

def exibir_tela_game_over():
    """Exibe a tela de game over e aguarda a ação do jogador."""
    tela.fill(BRANCO)
    tela.blit(GAME_OVER, (largura // 2 - GAME_OVER.get_width() // 2, altura // 2 - 100))
    botao_reset_rect = tela.blit(RESET, (largura // 2 - RESET.get_width() // 2, altura // 2))
    pygame.display.update()
    esperar_acao(botao_reset_rect)

def esperar_acao(botao_reset_rect):
    """Aguarda até que o jogador clique no botão de reset."""
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_reset_rect.collidepoint(evento.pos):
                    esperando = False

def reiniciar_jogo():
    """Reinicia o jogo, resetando todas as variáveis."""
    global obstaculos, temporizador_obstaculo, pontuacao, dino, chao
    obstaculos = []
    temporizador_obstaculo = 0
    pontuacao = 0
    dino = Dinossauro()
    chao = Chao(CHAO)

obstaculos = []
temporizador_obstaculo = 0
pontuacao = 0


# Exibe a tela de início
exibir_tela_inicio()

rodando = True
while rodando:
    tela.fill(BRANCO)
    entrada_usuario = pygame.key.get_pressed()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Incrementa a pontuação e ajusta a velocidade
    pontuacao += 1
    fator_velocidade = 1 + (pontuacao // 100) * 0.05  

    dino.atualizar(entrada_usuario, fator_velocidade)
    dino.desenhar(tela)
    chao.atualizar(fator_velocidade)
    chao.desenhar(tela)

    if temporizador_obstaculo == 0:
        obstaculos.append(pegar_obstaculo_aleatorio())
        temporizador_obstaculo = 50

    for obstaculo in obstaculos:
        obstaculo.atualizar(fator_velocidade)
        obstaculo.desenhar(tela)
        if obstaculo.fora_da_tela():
            obstaculos.remove(obstaculo)

    temporizador_obstaculo -= 1 if temporizador_obstaculo > 0 else 0

    
    # Exibe a pontuação
    texto_pontuacao = fonte.render(f"{pontuacao:04}", True, PRETO)
    tela.blit(texto_pontuacao, (900, 20))

    pygame.display.update()
    tempo.tick(30)

    # Verifica colisão
    if dino.colidir(obstaculos):
        som_colisao.play()
        exibir_tela_game_over()
        reiniciar_jogo()

pygame.quit()
