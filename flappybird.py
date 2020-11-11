import pygame, random
from pygame.locals import *

# Constantes utilizadas
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 85
PIPE_HEIGHT = 500

PIPE_GAP = 200

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

        self.image = pygame.image.load('utils/bluebird-upflap.png').convert_alpha()

        self.speed = SPEED

        self.mask = pygame.mask.from_surface(self.image)

        self.current_image = 0

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

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('utils/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            # Quando a imagem e invertida, o padrao do 'cano' seria iniciar
            # colado na parte superior da tela ( posicao 0 no eixo y ), porem
            # o cano varia sua imersao na tela, podendo ter sua posicao y = -50
            # por exemplo, para que seja criado um cano invertido menor que o 
            # tamanho da imagem carregada.
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load('utils/base.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

        def update(self):
            self.rect[0] -= GAME_SPEED

# Funcao utilizada para verificar se o sprite esta fora da tela 
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)

    return (pipe, pipe_inverted)

pygame.init()

# Criando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Aplicado o conceito de groups
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

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

    # Atualiza o chao do game
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    # Atualiza os canos do game
    if is_off_screen(pipe_group.sprites()[0]):
        # Remove o cano normal e o invertido
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        new_pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipe_group.add(new_pipes[0])
        pipe_group.add(new_pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    if  (   pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game Over
        break
    
    pygame.display.update()