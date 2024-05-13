import pygame
import os
import random

# Inicializa o Pygame
pygame.init()

# Define o tamanho da tela
altura = 600
largura = 1000

# Define as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define uma variável que indica os frames por segundo
tempo = pygame.time.Clock()

# Define a tela
tela = pygame.display.set_mode((largura, altura))

# Define o nome que vai aparecer na tela
pygame.display.set_caption('Junque Jumper')

# Define as imagens
CORRIDA = [pygame.image.load(os.path.join('Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Dino', 'DinoRun2.png'))]
PULO = pygame.image.load(os.path.join('Dino', 'DinoJump.png'))
AGACHAR = [pygame.image.load(os.path.join('Dino', 'DinoDuck1.png')),
           pygame.image.load(os.path.join('Dino', 'DinoDuck2.png'))]
Cacto_G = [pygame.image.load(os.path.join('cacto', 'LargeCactus1.png')),
           pygame.image.load(os.path.join('cacto', 'LargeCactus2.png')),
           pygame.image.load(os.path.join('cacto', 'LargeCactus3.png'))]
Cacto_P = [pygame.image.load(os.path.join('cacto', 'SmallCactus1.png')),
           pygame.image.load(os.path.join('cacto', 'SmallCactus2.png')),
           pygame.image.load(os.path.join('cacto', 'SmallCactus3.png'))]
Ptero = [pygame.image.load(os.path.join('ptero', 'Bird1.png')),
         pygame.image.load(os.path.join('ptero', 'Bird2.png'))]
Chao = pygame.image.load(os.path.join('outro', 'chão.png'))
