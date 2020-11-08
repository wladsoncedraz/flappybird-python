import pygame
from pygame.locals import *

# Constantes utilizadas
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
BACKGROUND = pygame.image.load('utils/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Classe representando o passaro do game
# todas suas caracteristicas e acoes sao 
# desenvolvidas nesta classe
class Bird(pygame.sprite.Sprite):

    # Funcao construtora
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('utils/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('utils/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('utils/bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('utils/bluebird-upflap.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] =  SCREEN_WIDTH / 2
        self.rect[1] =  SCREEN_HEIGHT / 2

        print(self.rect)

    def update(self):
        # O modulo de 3 e utilizado para que seja feito um ciclo entre as imagens
        # e sempre haja a sequencia 1 2 3, 1 2 3...
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        # Atualiza a altura do passaro
        self.rect[1] += self.speed

    # Funcao de salto do passaro
    def bump(self):
        self.speed = -SPEED

class Ground(pygame.sprite.Sprite):

        def __init__(self, width, height):
            self.image = pygame.image.load('utils/base.png')
            self.image = pygame.transform.scale(self.image, (width, height))
pygame.init()

# Criando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

clock = pygame.time.Clock()

# Laço principal para o game
while True:
    # Seta o valor do fps, 'agiliza' ou 'retarda' a troca das imagens
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        # Monitora se o usuario pressionou alguma tecla
        # e se esta pressiada e o espaco
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    # A tupla (0, 0) representa o inicio do background na tela, considerando
    # uma contagem de pixels partindo da esquerda para direita e de cima para baixo
    screen.blit(BACKGROUND, (0, 0))

    bird_group.update()
    bird_group.draw(screen)

    pygame.display.update()