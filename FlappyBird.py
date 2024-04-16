import pygame
import os
import random

#Altura e largura da tela
largura_tela = 500
altura_tela = 500

#Imagens do game
imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagem_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
# O pasaro tem 3 imagens (Para que bata as asas)
imagem_passaro = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),]

#Inicializando a fonte e escolhendo o modelo e tamanho
pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial, 50')


class passaro():
    pass

class cano():
    pass

class chao():
    pass
