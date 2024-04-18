import pygame
import os
import random

#Altura e largura da tela
LARGURA_TELA = 500
ALTURA_TELA = 800

#Imagens do game
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
# O pasaro tem 3 imagens (Para que bata as asas)
IMAGEM_PASSARO = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),]

#Inicializando a fonte e escolhendo o modelo e tamanho
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial, 50')


class passaro():
    #Constante imagens do passaro
    IMGS = IMAGEM_PASSARO

    #Animacao do passaro - movimento de parabola
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    #unidade de tempo em que a animação irá durar (em frames)
    TEMPO_ANIMACAO = 5

    #Atributos do pássaro
    def __init__(self, x, y) -> None:
        #Eixo X e Y = Onde o passaro inicia na tela
        self.x = x
        self.y = y
        #Angulo do passaro = Inclinado para cima ou baixo ou reto
        self.angulo = 0
        #Velocidade que ele se movimenta para cima e para baixo
        self.velocidade = 0
        self.altura = self.y
        #Tempo de animação da parabola 
        self.tempo = 0
        #Para definir qual imagem do passaro está sendo utlizada no momento (muda com o tempo de animacao)
        self.contagem_imagem = 0
        #Imagem inicial do passaro
        self.imagem = self.IMGS[0]

    def pular(self):
        #Velocidade relacionado ao eixo Y(O quanto ele sobe)
        self.velocidade = -10,5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #Calcukar o deslocamento
        self.tempo += 1
        #Formula do deslocamento
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        #Restringir deslocamento
        if deslocamento > 16:
            deslocamento = 16
        #Auemento da altura do pulo (facilitar o jogo)
        elif deslocamento < 0:
            deslocamento -= 2

        #deslocamento do passaro
        self.y += deslocamento

        #Angulo do passaro conforme o salto
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
            else:
                if self.angulo > -90:
                    self.angulo -= self.VELOCIDADE_ROTACAO

        def desenhar(self, tela):
            #Imagem de utlizacao do passaro - If para o bater das asas
            #de acordo com o tempo da animacao
            self.contagem_imagem +=1
            if self.contagem_imagem < self.TEMPO_ANIMACAO:
                self.imagem = self.IMGS[0]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
                self.imagem = self.IMGS[1]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
                self.imagem = self.IMGS[2]                            
            elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
                self.imagem = self.IMGS[1]
            elif self.contagem_imagem < self.TEMPO_ANIMACAO*4 + 1:
                self.imagem = self.IMGS[0] 
                #Zerando o contador para iniciar novamente   
                self.contagem_imagem = 0                      
                                        
            #Passaro não bate a asa enquanto estiver em queda
            if self.angulo <= -80:
                self.IMGS[1]
                #Ajuste que quando ele parar de cair a primeira batida de asa seja para baixo
                self.contagem_imagem = self.TEMPO_ANIMACAO*2

            #Desenhar o passaro na tela
            imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
            #Criacao de um retangulo que será colocado na tela com a imagem do passaro
            pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
            retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
            #Desenhar na tela
            tela.blit(imagem_rotacionada, retangulo.topleft)

        #Mascara do passaro (para calcular a colusão com pixel do passaro e não do retangulo que
        #o passaro está inserido)
        def get_mask(self):
            pygame.mask.from_surface(self.imagem)


class cano():
    #Distancia entre os canos de base e topo (onde o passaro passa)
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x) -> None:
        self.x = x
        self.altura = 0
        #posicao de acordo com o exio Y
        self.posicao_topo = 0
        self.posicao_base = 0 
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        #para saber se o cano já passou do passaro
        self.passou = False
        #Função que irá gerar a altura do cano aleatoriamente
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.posicao_base = self.altura - self.CANO_TOPO.get_height()
        self.posicao_base = self.altura + self.DISTANCIA

    #Movimento do cano na tela
    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASEW, (self.x, self.pos_base))

        
    def colidir(self, passaro):
        #mascaras do passaro e dos canos para controle de colisao
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(topo_mask, distancia_base)
                                          
        if base_ponto or topo_ponto:
            return True
        else:
            return False
            

class chao():
    VELOCIDADE = 0
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x1 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x2 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

    
