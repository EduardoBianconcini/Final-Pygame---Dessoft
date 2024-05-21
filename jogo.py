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