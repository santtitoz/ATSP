import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

musica_de_fundo = pygame.mixer.music.load('sounds/music_batlle.mp3') #carrega música de fundo 

som_disparo = pygame.mixer.Sound('sounds/Disparo_laser.wav') #função que recebe o som de disparo
som_colisão_inimigo = pygame.mixer.Sound('sounds/Explosão_1.wav') #função que recebe o som de disparo colidindo com inimigos
som_dano = pygame.mixer.Sound('sounds/Som_de_dano_1.wav') #função que recebe o som dos inimigos colidindo com a nave
som_perda = pygame.mixer.Sound('sounds/você_perdeu.wav')

altura, largura = 1280, 720
x, y = altura // 2 - 50, largura // 2
x_redirecionado, y_redirecionado = altura // 2 - 50, largura // 2

largura_disp = 5
comprimento_disp = 10
largura_inim = 10
comprimento_inim = 10

tela = pygame.display.set_mode((altura, largura))
relogio = pygame.time.Clock()

disparos = []
meteoros = []
inimigos = []

contador_meteoros = 0 #contagem de meteoros
contador_inimigos = 0 #contagem de inimigos

contador_de_vidas_nave = 3 #conta a quantidade de vidas que a nave ainda tem
contador_de_vidas_terra = 3

class Nave(pygame.sprite.Sprite): #A classe 'nave' vai herdar outra classe do pygame, a 'sprite'
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #inicializa a classe 'sprite'
        self.sprites = [] #lista com todas as sprites da nave
        self.sprites.append(pygame.image.load('NAVE/sprite_nave0.png')) #appenda as sprites na lista com a função 'load', o primeiro parâmetro é a pasta que contém as imagens e o segundo parâmetro é o nome da imagem
        self.sprites.append(pygame.image.load('NAVE/sprite_nave1.png'))
        self.sprites.append(pygame.image.load('NAVE/sprite_nave2.png'))
        self.sprites.append(pygame.image.load('NAVE/sprite_nave3.png'))
        self.atual = 0
        self.image = self.sprites[self.atual] #atributo da classe 'Sprites'
        
        self.rect = self.image.get_rect() #pegar o retângulo que fica ao redor da imagem
        self.rect.topleft = x, y #redireciona a quina superior esquerda do retângulo da imagem com as coordenadas x,y

    def update(self): #novo método
        self.rect.topleft = x, y
        self.atual += 0.1 #diminuindo o número que atual vai receber faz com que a troca de imagens seja mais demorada também
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]  #a função vai arredondar o número quebrado para ser possível o número ser usado com índice
        self.image = pygame.transform.scale(self.image, (64*2, 64*2)) #modifico a escala da imagem, a tupla recebe a altura e largura

            
todas_as_sprites = pygame.sprite.Group()
nave = Nave()
todas_as_sprites.add(nave)


imagem_de_fundo_inicial = pygame.image.load('background/Tela_inicial/tela inicial.png').convert() #carrega a imagem de fundo da tela de start
imagem_de_fundo_inicial_start = pygame.image.load('background/Tela_inicial/tela inicial start.png').convert() #carrega a imagem de fundo da tela de start mas com a menssagem de iniciar aparecendo
imagem_de_fundo_gameplay = pygame.image.load('background/Espaço.png').convert() #carrega a imagem de fundo do jogo iniciado
imagem_game_over = pygame.image.load('game over/Game over.png')

barra_de_informacoes = pygame.image.load('Barra com vida/barra_de_informações.png')
ponto_de_vida_nave = pygame.image.load('Barra com vida/vida_nave.png') 
ponto_de_vida_terra = pygame.image.load('Barra com vida/vida_terra.png')



def barra_de_vidas(hp):
    if hp == 3:    
        return 3
    elif hp == 2:    
        return 2
    elif hp == 1:    
        return 1
    else:
        return 0



lista_disparo = ['Disparo/Disparo0.png', 'Disparo/Disparo1.png', 'Disparo/Disparo2.png', 'Disparo/Disparo3.png']
lista_alienigena = ['Alienígena/Alienígena0.png', 'Alienígena/Alienígena1.png', 'Alienígena/Alienígena2.png', 'Alienígena/Alienígena3.png']
lista_meteoro = ['Meteoro_j/sprite_0.png', 'Meteoro_j/sprite_1.png', 'Meteoro_j/sprite_2.png', 'Meteoro_j/sprite_3.png']
lista_explosao = ['Explosão/explosão0.png','Explosão/explosão1.png','Explosão/explosão2.png','Explosão/explosão3.png']

lista_escudo_habilidade = ['Barra com vida/escudo/escudo00.png', 'Barra com vida/escudo/escudo01.png', 'Barra com vida/escudo/escudo02.png','Barra com vida/escudo/escudo03.png','Barra com vida/escudo/escudo04.png',
'Barra com vida/escudo/escudo05.png', 'Barra com vida/escudo/escudo06.png', 'Barra com vida/escudo/escudo07.png', 
'Barra com vida/escudo/escudo08.png', 'Barra com vida/escudo/escudo09.png','Barra com vida/escudo/escudo10.png']

lista_escudo_em_uso = ['escudo_in_gameplay/uso_escudo0.png', 'escudo_in_gameplay/uso_escudo1.png', 'escudo_in_gameplay/uso_escudo2.png', 'escudo_in_gameplay/uso_escudo3.png',
'escudo_in_gameplay/uso_escudo4.png', 'escudo_in_gameplay/uso_escudo5.png', 'escudo_in_gameplay/uso_escudo6.png' ]

escudo = False
escudo_ativo = False

def disp_animacao_d(indice):
    imagem = pygame.image.load(lista_disparo[int(indice)])
    imagem = pygame.transform.scale(imagem, (64/3, 64/3)) #Redimencionar a imagem
    return imagem

def disp_animacao_i(indice):
    imagem = pygame.image.load(lista_alienigena[int(indice)])
    imagem = pygame.transform.scale(imagem, (64, 64))
    return imagem

def disp_animacao_m(indice):
    imagem = pygame.image.load(lista_meteoro[int(indice)])
    imagem = pygame.transform.scale(imagem, (64, 64))
    return imagem

def animacao_explosao(indice):
    imagem = pygame.image.load(lista_explosao[int(indice)])
    imagem = pygame.transform.scale(imagem, (64, 64))
    return imagem

def animacao_escudo_icone(indice):
    imagem = pygame.image.load(lista_escudo_habilidade[int(indice)])
    imagem = pygame.transform.scale(imagem, (64, 64))
    return imagem
  
def animacao_escudo(indice):
    imagem = pygame.image.load(lista_escudo_habilidade[int(indice)])
    imagem = pygame.transform.scale(imagem, (64, 64))
    return imagem
  

def tela_de_início():  #função para aparecer a tela inicial
    contador = 0
    mostrar_start = False

    while True:
        contador += 0.3  #controlar a velocidade que a variável contador recebe valores 
        if contador > 30:  # se a variável contador for maior que 30 a variável mostrar_start recebe verdadeiro e contador reinicia
            mostrar_start = not mostrar_start
            contador = 0

        if mostrar_start:
            tela.blit(imagem_de_fundo_inicial_start, (0, 0))
        else:
            tela.blit(imagem_de_fundo_inicial, (0, 0))
        
        pygame.display.update()  #atualiza a tela
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
        

tela_de_início()
pygame.mixer_music.play(-1) #toca a música, e toca repetidamente por ter passado o -1 na função play

cont_sprite_d = 0 #contador que será o índice da sprite para todas as sprites disparo
cont_sprite_i = 0 #contador que será o índice da sprite para todas as sprites inimigo
cont_sprite_m = 0 #contador que será o índice da sprite para todas as sprites meteoro
cont_sprite_e = 0 #contador que será o índice da sprite para todas as sprites explosão
cont_sprite_escudo_habilidade = 9 #contador que será o índice da sprite para todas as sprites escudo habilidade
cont_sprite_escudo = 0 #contador que será o índice da sprite para todas as sprites escudo em uso
explosoes = [] #lista com as explosoes que aconteceram

cont_sprite_elist = [] #contador que será o índice da sprite para todas as sprites explosão


fonte = pygame.font.SysFont('arial', 40, True, True) #variável que receberá os parâmetros para configurar uma menssagem, primeiro a fonte, segundo o tamanho, terceiro se está em negrito e quarto se está em itálico

score = 0
menssagem_retornar = 'Pressione espaço para jogar novamente'
config_mensg_retorno = fonte.render(menssagem_retornar, False, (255, 255, 255))
avanco_inimigo = 1

def restart_game():
    global avanco_inimigo, score, disparos, meteoros, inimigos, contador_meteoros 
    global cont_sprite_escudo_habilidade, cont_sprite_escudo, contador_inimigos, contador_de_vidas_nave, contador_de_vidas_terra, contador
    avanco_inimigo = 1
    score = 0
    disparos = []
    meteoros = []
    inimigos = []
    contador_meteoros = 0 #contagem de meteoros
    contador_inimigos = 0 #contagem de inimigos
    contador_de_vidas_nave = 3 #conta a quantidade de vidas que a nave ainda tem
    contador_de_vidas_terra = 3
    return

ind = 0 #variável que vai ajudar na troca de sprites do escudo na game play

while True:
    relogio.tick(60) #determina o fps do jogo inteiro

    menssagem_score = f'Score: {score}'
    config_mensg_score = fonte.render(menssagem_score, False, (255, 255, 255)) #mais alguns parâmetros para menssagem de score, que está localizada na barra de informações, primeiro pareâmetro a menssagem, segundo se a menssagem é serrilhada, e ultimo a cor


    if contador_de_vidas_nave <= 0 or contador_de_vidas_terra <= 0:
        pygame.mixer_music.pause()
        som_perda.play()
        
        pygame.display.update()
        sair_loop = False

        delay_da_imagem = 0 #uma variável que vai recebendo pequenos acrécimos de números para que o jogador espere um tempo na tela de game over até voltar

        while True:
            while delay_da_imagem < 20: 
                tela.blit(imagem_game_over, (0, 0))
                tela.blit(config_mensg_score, (580, 360))
                tela.blit(config_mensg_retorno, (320, 500))
                delay_da_imagem += 0.3
                pygame.display.update()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        sair_loop = True
                        break
            if sair_loop:
                pygame.mixer_music.unpause()
                restart_game()
                break

    
    tela.blit(imagem_de_fundo_gameplay, (0,0)) #desenha a imagem na tela, e esta imagem é o pano de fundo
    tela.blit(barra_de_informacoes, (0, 0)) 
    tela.blit(config_mensg_score, (640, 5)) #desenha a menssagem na tela

    tela.blit(animacao_escudo_icone(cont_sprite_escudo_habilidade), (30, 5))
    cont_sprite_escudo_habilidade -= 0.01

    if cont_sprite_escudo_habilidade == 0.0:
        escudo = True

    for i in range(barra_de_vidas(contador_de_vidas_nave)):
        tela.blit(ponto_de_vida_nave, (1200 - i*65, 30)) #o 65 é para ter um espaçamento de coluna entre as vidas que serão mostradas


    for i in range(barra_de_vidas(contador_de_vidas_terra)):
        tela.blit(ponto_de_vida_terra, (1200 - i*65, 5))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                disparos.append([x, y])
                som_disparo.play()
            
            elif event.key == K_x and escudo:
                escudo_ativo = True
        
    if escudo_ativo:
        parar = False
        if parar == False:
            while ind == 0:
                tela.blit(animacao_escudo(int(ind)), (x, y))
                ind += 0.3
                if ind >= len(lista_escudo_em_uso):
                    parar = True
        
        else:
            tela.blit(animacao_escudo(int(ind)), (x, y))        

    if contador_meteoros < 3:
        while contador_meteoros < 3:
            x_meteoro = randint(0, 1230)
            y_meteoro = 60
            meteoros.append([x_meteoro, y_meteoro])
            contador_meteoros += 1

    if contador_inimigos < 3:
        while contador_inimigos < 3:
            x_inimigo = randint(0, 1230)
            y_inimigo = 60
            inimigos.append([x_inimigo, y_inimigo])
            contador_inimigos += 1

    if pygame.key.get_pressed()[K_a]:
        if x == 0: #cria uma borda no mapa para impedir de ultrapassar a extremidade esquerda
            x = 0
        else:
            x -= 10

    if pygame.key.get_pressed()[K_s]:
        if y == 720 - 100:
            y = 720 - 100 #recebe o limite máximo até o lado inferior subtraindo sua altura
        else:
            y += 10
    if pygame.key.get_pressed()[K_w]:
        if y == 60:
            y = 60
        else:
            y -= 10
    if pygame.key.get_pressed()[K_d]:
        if x == 1280 - 100:
            x = 1280 - 100 #recebe o limite máximo até o lado direito subtraindo sua largura
        else:
            x += 10


    todas_as_sprites.draw(tela)
    todas_as_sprites.update()

    for disparo in disparos[:]:  # Cria e usa uma cópia da lista para que com as alterações ela não cause erros
        disparo[1] -= 10

        tela.blit(disp_animacao_d(cont_sprite_d), (disparo[0] + 55, disparo[1] - 5)) #o "+ 55" serve para que o disparo seja centralizado com a imagem da nave
        cont_sprite_d += 0.5

        if cont_sprite_d == 4:
            cont_sprite_d = 0

        if disparo[1] < 65:  #Se o disparo sair da tela já subtraindo a altura da barra de vida ele é removido para que o jogo fique bem otimizado
            disparos.remove(disparo)

    for inimigo in inimigos[:]: 
        inimigo[1] += avanco_inimigo

        tela.blit(disp_animacao_i(int(cont_sprite_i)), (inimigo[0], inimigo[1]))
        cont_sprite_i += 0.1

        if cont_sprite_i >= 4.0:
            cont_sprite_i = 0.0

        inimigo_area_de_colisao = pygame.Rect(inimigo[0], inimigo[1], 64, 64) #Criação de uma caixa delimitadora retangular que serve para detectar colisão

        if inimigo[1] > 720: 
            inimigos.remove(inimigo)
            contador_de_vidas_terra -= 1
            contador_inimigos -= 1

        elif inimigo_area_de_colisao.colliderect(nave):
            x = x_redirecionado
            y = y_redirecionado

            meteoros.clear()
            inimigos.clear()

            contador_meteoros = 0
            contador_inimigos = 0

            contador_de_vidas_nave -= 1
            score += 1
            som_dano.play()

        for disparo in disparos[:]:
            disparo_area_de_colisao = pygame.Rect(disparo[0] + 49, disparo[1], 64/3, 64/3) #Criação de uma caixa de colisão do disparo afastado 49 centimetro para ficar no meio da nave
            if inimigo_area_de_colisao.colliderect(disparo_area_de_colisao):
                explosoes.append([inimigo[0], inimigo[1]]) #adiciona a posição houve colisão a lista de explosões
                disparos.remove(disparo)
                inimigos.remove(inimigo)
                som_colisão_inimigo.play()
                contador_inimigos -= 1
                score += 1


    for meteoro in meteoros[:]:
        meteoro[1] += avanco_inimigo

        tela.blit(disp_animacao_m(int(cont_sprite_m)), (meteoro[0], meteoro[1]))
        cont_sprite_m += 0.1

        if cont_sprite_m >= 4.0:
            cont_sprite_m = 0.0


        meteoro_area_de_colisao = pygame.Rect(meteoro[0], meteoro[1], 64, 64) #Criação de uma caixa delimitadora retangular que serve para detectar colisão

        if meteoro[1] > 720:
            meteoros.remove(meteoro)
            contador_de_vidas_terra -= 1
            contador_meteoros -= 1


        elif meteoro_area_de_colisao.colliderect(nave):
            x = x_redirecionado
            y = y_redirecionado

            meteoros.clear()
            inimigos.clear()

            contador_meteoros = 0
            contador_inimigos = 0
            
            contador_de_vidas_nave -= 1
            som_dano.play()
            score += 1

        for disparo in disparos[:]:
            disparo_area_de_colisao = pygame.Rect(disparo[0] + 49, disparo[1], 64/3, 64/3) #Criação de uma caixa de colisão do disparo afastado 49 centimetro para ficar no meio da nave
            if meteoro_area_de_colisao.colliderect(disparo_area_de_colisao):
                explosoes.append([meteoro[0], meteoro[1]])
                disparos.remove(disparo)
                meteoros.remove(meteoro)
                contador_meteoros -= 1
                som_colisão_inimigo.play()
                score += 1
                break  # Sai do loop interno após a colisão

    if score == 50:
        avanco_inimigo += 0.05
    elif score == 100:
        avanco_inimigo += 0.07 


    pygame.display.flip()