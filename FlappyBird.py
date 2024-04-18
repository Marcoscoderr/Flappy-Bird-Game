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
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro():
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
        self.velocidade = -10.5
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
            self.imagem = self.IMGS[1]
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
        return pygame.mask.from_surface(self.imagem)
    

class Cano():
    #Distancia entre os canos de base e topo (onde o passaro passa)
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x) -> None:
        self.x = x
        self.altura = 0
        #posicao de acordo com o exio Y
        self.pos_topo = 0
        self.pos_base = 0 
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        #para saber se o cano já passou do passaro
        self.passou = False
        #Função que irá gerar a altura do cano aleatoriamente
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    #Movimento do cano na tela
    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

        
    def colidir(self, passaro):
        #mascaras do passaro e dos canos para controle de colisao
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

         #Se houve colisão de mascaras, retorna TRUE                                 
        if base_ponto or topo_ponto:
            return True
        else:
            return False
            

class Chao():
    VELOCIDADE = 0
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    #São criadas duas imagens do chão que alternam na tela
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x1 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x2 + self.LARGURA

    #Desenhando o chão na tela
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_FUNDO, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    #Criando o texto para colocar na tela
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255,255,255))
    tela.blit(texto, (LARGURA_TELA - 10 - texto.get_width(), 10))
    
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pontos = 0
    relogio = pygame.time.Clock()

    #Fazer o jogo rodar
    rodando = True
    while rodando:
        relogio.tick(30)

        #intergir com o jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        
        #Movimentação dos elementos do jogo
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()




