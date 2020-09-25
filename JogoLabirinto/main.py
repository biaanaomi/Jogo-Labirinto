import pygame as pg
import sys, os
from gerar_labirinto import *
from obstaculos import *
from PIL import Image
from random import randint
import random
import time

from db import conn
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error

def drawLab(tamanho):
	# ALTERE AQUI O TAMANHO PARA O JOGO (Número de linhas e colunas)
	#tamanho = [15,10]
	#---------------------------

	# Tamanho do espaço entre as linhas e colunas
	size = 33
	#--------------------------------------------

	# Retorna um lista com duas sublista contendo 1 para parede, 0 para espaço vazio -
	lab = gerar_labirinto(tamanho[0],tamanho[1])
	#---------------------------------------------------------------------------------

	# Cria uma imagem em branco ------------------------------------------------------
	img_new = Image.new('RGB', (tamanho[0]*(size+1)+1,tamanho[1]*(size+1)+1), (0,0,0))
	#---------------------------------------------------------------------------------

	# Cria uma "máscara" onde o labirinto vai ser desenhado
	draw = ImageDraw.Draw(img_new)
	#------------------------------------------------------

	# Desenha o labirinto na "máscara" --------------
	desenhar_labirinto_pillow(draw, tamanho, lab, size)
	#------------------------------------------------

	# Salva a imagem com o labirinto já desenhado
	img_new.save("data/rect.png")
	#--------------------------------------------

	size += 1
	cor = [randint(15,255),randint(15,255),randint(15,255)]

	return(size, cor)



id_jogador = 0

black = (0,0,0)
white = (255,255,255)
red = (204,0,69)
green = (0,128,128)
bright_red = (220,20,60)
bright_green = (35,235,195)

TEXT_COLOR = white


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def congrats():

    tela.fill(black)
    largeText = pygame.font.SysFont("comicsansms",85)
    TextSurf, TextRect = text_objects("Parabéns", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    tela.blit(TextSurf, TextRect)

    #db.insert(name,score)
    b=True
    while b:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                quitgame()
                b=False

        button("Jogar",(display_width/2)-(tamanho[0]*size/3)-((tamanho[0]*size/4)/2),display_height/1.3,tamanho[0]*size/4,tamanho[1]+size,green,bright_green,game_loop)
        button("Rank!",(display_width/2)-((tamanho[0]*size/3)/2),display_height/1.3,tamanho[0]*size/3,tamanho[1]+size,green,bright_green,lb)
        button("Sair",(display_width/2)+(tamanho[0]*size/3)-((tamanho[0]*size/4)/2),display_height/1.3,tamanho[0]*size/4,tamanho[1]+size,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

#Salva no banco de dados após termino do caminho
def finish(dt):

    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    tela.fill(black)
    input_box = pygame.Rect((display_width/2),(display_height/1.5), 140, 32)
    color_inactive = pygame.Color(255,255,255)
    color_active = pygame.Color(35,235,195)
    color = color_inactive
    largeText = pygame.font.SysFont("Sans",38)
    TextSurf, TextRect = text_objects("Digite seu apelido:", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    tela.blit(TextSurf, TextRect)
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # quando clicar na caixa de texto
                if input_box.collidepoint(event.pos):
                    #tornando a váriavel ativada
                    active = not active
                else:
                    active = False
                #Muda a cor da caixa de texto com o click
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done=True
                        conn.insert(text,dt)
                        congrats()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color_inactive)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # mostra o texto na tela
        tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # mostra a caixa retangular
        pygame.draw.rect(tela, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def button(msg,x,y,w,h,ic,ac,action=None):

    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(tela, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pg.draw.rect(tela, ic,(x,y,w,h))
    smallText = pg.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    tela.blit(textSurf, textRect)

def quitgame():
    conn.disp()
    pg.quit()
    quit()

def exi():
    pygame.quit()
    quit()

def game_intro():
    
    intro = True
    
    while intro:
        for event in pg.event.get():
            #print(event)
            if event.type == pg.QUIT:
                exi()
                intro=False
            tela.fill(black)
            
        largeText = pg.font.SysFont("comicsansms",80)
        smallText = pg.font.SysFont("comicsansms",30)
        smallestText = pg.font.SysFont("comicsansms",18)
        TextSurf, TextRect = text_objects("L.bin", largeText)
        TextSurf2, TextRect2 = text_objects("Encontre a saída utilizando o teclado", smallText)
        TextSurf3, TextRect3 = text_objects("Dica: A colocação dos obtáculos certos nos fazem chegar lá", smallestText)
        TextRect.center = ((display_width/2),(display_height/4))
        TextRect2.center = ((display_width/2),(display_height/2))
        TextRect3.center = ((display_width/2),(display_height/2+display_height/6))
        tela.blit(TextSurf, TextRect)
        tela.blit(TextSurf2, TextRect2)
        tela.blit(TextSurf3, TextRect3)
        
        button("GO!",(display_width/2)-(tamanho[0]*size/3)-((tamanho[0]*size/4)/2),display_height/1.3,tamanho[0]*size/4,tamanho[1]+size,green,bright_green,game_loop) #150
        button("Rank!",(display_width/2)-((tamanho[0]*size/3)/2),display_height/1.3,tamanho[0]*size/3,tamanho[1]+size,green,bright_green,lb)
        button("Sair", (display_width/2)+(tamanho[0]*size/3)-((tamanho[0]*size/4)/2),display_height/1.3,tamanho[0]*size/4,tamanho[1]+size,red,bright_red,quitgame)
        
        pg.display.update()
        clock.tick(15)

#mostra os ranks de cada partida
def lb():
    intro = True
    try:
       mySQLconnection = mysql.connector.connect(host='localhost',
                                 database='gamedb',
                                 user='root',
                                 password='')

       sql_select_Query = "SELECT * FROM user_info ORDER BY tempo ASC" #ascendente
       cursor = mySQLconnection.cursor()
       cursor.execute(sql_select_Query)
       records = cursor.fetchall()
       rc = cursor.rowcount #numero de registros por linha
       print("Total number of rows in student is - ", cursor.rowcount)

       cursor.close()

    except Error as e :
        print ("Error while connecting to MySQL", e)
    finally:
        #closing database connection.
        if(mySQLconnection.is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")
    while intro:
        for event in pg.event.get():
            #print(event)
            if event.type == pg.QUIT:
                exi()
                intro=False
            tela.fill(black)
        largeText = pg.font.SysFont("comicsansms",25)
        TextSurf, TextRect = text_objects("MenorTempo", largeText)

        TextRect.center = (100,20)
        tela.blit(TextSurf, TextRect)

        font = pg.font.SysFont("Sans", 25)
        text = font.render("Rank         Tempo(s)          Nome", True, white)
        tela.blit(text,(5,50))

        font = pg.font.SysFont("comicsansms", 25)
        if rc >= 1:
            text = font.render("1              "+str((records[0])[2]) +"              "    +str((records[0])[1]) , True, white)
            tela.blit(text,(5,80))
        if rc >= 2:
            text = font.render("2             "+str((records[1])[2]) +"              "    +str((records[1])[1]), True, white)
            tela.blit(text,(5,110))
        if rc >= 3:
            text = font.render("3             "+str((records[2])[2]) +"              "    +str((records[2])[1]), True, white)
            tela.blit(text,(5,140))
        if rc >= 4:
            text = font.render("4             "+str((records[3])[2]) +"              "    +str((records[3])[1]), True, white)
            tela.blit(text,(5,170))
        if rc >= 5:
            text = font.render("5             "+str((records[4])[2]) +"              "    +str((records[4])[1]), True, black)
            tela.blit(text,(5,200))
        if rc >= 6:
            text = font.render("6             "+str((records[5])[2]) +"              "    +str((records[5])[1]), True, black)
            tela.blit(text,(5,230))
        if rc >= 7:
            text = font.render("7             "+str((records[6])[2]) +"              "    +str((records[6])[1]), True, black)
            tela.blit(text,(5,260))
        if rc >= 8:
            text = font.render("8             "+str((records[7])[2]) +"              "    +str((records[7])[1]), True, black)
            tela.blit(text,(5,290))
        if rc >= 9:
            text = font.render("9             "+str((records[8])[2]) +"              "    +str((records[8])[1]), True, black)
            tela.blit(text,(5,320))
        if rc >= 10: 
            text = font.render("10            "+str((records[9])[2]) +"              "    +str((records[9])[1]), True, black)
            tela.blit(text,(5,350))


        button("GO!",(display_width/2)-(tamanho[0]*size/3)-((tamanho[0]*size/4)/2),display_height/1.3,tamanho[0]*size/4,tamanho[1]+size,green,bright_green,game_loop)
        button("Sair",(display_width/2)+(tamanho[0]*size/3)-((tamanho[0]*size/4)/2),display_height/1.3,tamanho[0]*size/4,tamanho[1]+size,red,bright_red,quitgame)

        pg.display.update()
        clock.tick(15)

#game é mantido até usuario desejar continuar jogando
def game_loop(): 
    drawLab(tamanho) #altera o labirinto a cada jogada
    (x,y) = tamanho
    gameExit = False
    start_time = time.time()
    img = Image.open("data/rect.png")
    fundo = pg.image.load("data/rect.png")
    fundo_rect = fundo.get_rect()
    img = img.convert('RGB')
    rgb = img.load()
    posicoes = {id_jogador:[[tamanho[0]*size-size/2,size/2], cor]} #posicionando jogador
	#print(posicoes[id_jogador][0])
	#pg.mouse.set_pos(posicoes[id_jogador][0])
    x_mouse, y_mouse = pg.mouse.get_pos()
    tela.blit(fundo, fundo_rect)
    pg.display.update()
    
    program = obstaculos(tela.get_size(), tamanho, size)
    pg.mouse.set_pos(520,0)
    
   
    r = {}
    r[1] = pg.Rect(480,310, 25, 25)
    r[2] = pg.Rect(2,5,25,25)
    r[3] = pg.Rect(480,110,25,25)
    r[4] = pg.Rect(245,110,25,25)
    r[5] = pg.Rect(40,315,25,25)
    
    while True:
        
        clock.tick(20)
        t = time.time()
        tela.blit(fundo, fundo_rect)
        mpos = pg.mouse.get_pos()
        program.draw(tela, x_mouse, y_mouse, size, tamanho)
        mouse = pg.mouse.get_pressed()
        
        jogador = pg.Rect((posicoes[id_jogador][0][0]-size/2+1, posicoes[id_jogador][0][1]-size/2+1),(size-1,size-1))
        
        for event in pg.event.get():
            
            x_mouse, y_mouse = pg.mouse.get_pos()
            jogou = False
            
            if event.type == pg.QUIT:
                quitgame()
                gameExit = True
			
			#eventos do teclado
            elif event.type == pg.KEYDOWN:
                (xant, yant) = (posicoes[id_jogador][0][0], posicoes[id_jogador][0][1]) #ultima posição
                
                if event.key == pg.K_LEFT:
                    posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
                elif event.key == pg.K_RIGHT:
                    posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
                elif event.key == pg.K_UP:
                    posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
                elif event.key == pg.K_DOWN:
                    posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)
                    
            for i in range(5):
                i+=1
                program.events(event, mouse, tela, r[i], i) #eventos do mouse que envolvem obstaculos
                
                if (r[i].height == 0): #caso não tenha mais obs no caminho permite continuar
                    pass
                elif (jogador.colliderect(r[i])): #caso contrario retorna para posicao anterior
                    posicoes[id_jogador][0][0] = xant
                    posicoes[id_jogador][0][1] = yant
				
        vencedor = verificar_vitoria(posicoes, tamanho, size)

		#mostrando os obst na tela
        pg.draw.rect(tela, (98,0,255),  r[1])
        pg.draw.rect(tela, (255,0,255), r[2])
        pg.draw.rect(tela, (98,0,98),   r[3])
        pg.draw.rect(tela, (5,180,5),   r[4])
        pg.draw.rect(tela, (255,255,0), r[5])
        
        pg.draw.rect(tela, cor, jogador) #jogador também é um retangulo

        #imagem chegada
        fim = pygame.image.load('data/porta.jpg')
        fim = pygame.transform.scale(fim,(size,size))
        tela.blit(fim,(1,y*size-size+1))
    
        
        program.update(mouse, mpos, tela)
        
        #atualizando tempo a cada partida
        dt = -(start_time - t)
        #start_time = pg.time.get_ticks()/1000

        FONT = pg.font.SysFont("Sans", 20)
        
        if dt:
            dt = "%.0f" % dt
            message = 'Tempo em segundos: ' + str(dt)
            tela.blit(FONT.render(message, True, TEXT_COLOR), (tamanho[0]*size+4, tamanho[1]*size-size))
            
        pg.display.update()	

        if vencedor:
            finish(dt)
	
#game_intro()
#game_loop()

def main(nivel):

    global tela, tamanho, size, cor
    global display_height, display_width
    global clock

    pg.init()
    pygame.font.init()
    tamanho = nivel
    size, cor = drawLab(tamanho)
    display_width = tamanho[0]*size+200
    display_height = tamanho[1]*size+1
    tela = pg.display.set_mode((display_width,display_height))
    clock = pg.time.Clock()
  
    game_intro()
    game_loop()
quitgame()

if __name__ == '__main__':
    main()