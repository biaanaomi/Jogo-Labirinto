from random import shuffle, randrange, choice
from PIL import ImageDraw, Image
import pygame, sys
from pygame import *
#sys.setrecursionlimit(10000)

def fazer_caminho(tamanho, tela):

	x,y = tamanho
	caminho = [[x*6-3, 3]]
	lugares_visitados = [[x*6-3, 3]]
	linhas = []
	while [3, y*6-3] not in lugares_visitados:
		escolhas = [0,1,2,2,3,3]
		xx,yy = caminho[-1]
		parar = False
		while not parar:
			rdm = choice(escolhas)
			print(rdm)
			escolhas.remove(rdm)
			if rdm == 0:
				if [xx-6,yy] not in lugares_visitados and xx-6 > 0:
					lugares_visitados.append([xx-6,yy])
					caminho.append([xx-6,yy])
					parar = True
			elif rdm == 1:
				if [xx,yy+6] not in lugares_visitados and yy+6 < y*6:
					lugares_visitados.append([xx,yy+6])
					caminho.append([xx,yy+6])
					parar = True
			elif rdm == 2:
				if [xx+6,yy] not in lugares_visitados and xx+6 < x*6:
					lugares_visitados.append([xx+6,yy])
					caminho.append([xx+6,yy])
					parar = True
			else:
				if [xx,yy-6] not in lugares_visitados and yy-6 > 0:
					lugares_visitados.append([xx,yy-6])
					caminho.append([xx,yy-6])
					parar = True
		print(lugares_visitados)
		print(caminho)
		if not parar:
			caminho.pop()
	return caminho


class move():

	def esquerda(rgb, size, pos, id_jogador):
		r, g, b = rgb[pos[id_jogador][0][0]-size/2, pos[id_jogador][0][1]]
		jogou = False
		if r == 0:
			jogou = True
			pos[id_jogador][0][0] -= size
		pygame.mouse.set_pos(pos[id_jogador][0])
		return pos, jogou
	def direita(rgb, size, pos, id_jogador):
		r, g, b = rgb[pos[id_jogador][0][0]+size/2, pos[id_jogador][0][1]]
		jogou = False
		if r == 0:
			jogou = True
			pos[id_jogador][0][0] += size
		pygame.mouse.set_pos(pos[id_jogador][0])
		return pos, jogou
	def cima(rgb, size, pos, id_jogador):
		r, g, b = rgb[pos[id_jogador][0][0], pos[id_jogador][0][1]-size/2]
		jogou = False
		if r == 0:
			jogou = True
			pos[id_jogador][0][1] -= size
		pygame.mouse.set_pos(pos[id_jogador][0])
		return pos, jogou
	def baixo(rgb, size, pos, id_jogador):
		r, g, b = rgb[pos[id_jogador][0][0], pos[id_jogador][0][1]+size/2]
		jogou = False
		if r == 0:
			jogou = True
			pos[id_jogador][0][1] += size
		pygame.mouse.set_pos(pos[id_jogador][0])
		return pos, jogou


def verificar_vitoria(posicao, tamanho, size):
	for ID, p in posicao.items():
		if p[0] == [size/2, tamanho[1]*size-size/2]:
			return True

	return False


def gerar_labirinto(w = 10, h = 10):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    linhas_colunas = [[],[]]
    for (a, b) in zip(hor, ver):
        # print(''.join(a + ['\n'] + b), flush=True)
        for l in a:
        	if l == "+--":
        		linhas_colunas[0].append(1)
        	elif l == "+":
        		pass
        	else:
        		linhas_colunas[0].append(0)
        if len(b) != 0:
        	for c in b:
	        	if "|" in c:
	        		linhas_colunas[1].append(1)
	        	else:
	        		linhas_colunas[1].append(0)
    
    return linhas_colunas


def desenha_fim_pillow(tela, tamanho, size=11):
	(x,y) = tamanho
	#image = Image.open("data/Imagem6.png")
	#pygame.display.set_mode()
	#fim = pygame.image.load('data/Imagem6.png').convert_alpha()
	tela.rectangle((1,y*size-size+1,size-1,y*size-1), fill=(255,0,0), outline=(255,0,0))
	#tela.blit(pygame.transform.scale(fim,(size,size)),(x,y,size,size))

def cria_obs_pillow(tela, tamanho, size=20):
	(x,y) = tamanho
	size += 1
	#tela.rectangle((70, y*size-size+1,size+10,x*size-10), fill=(255,255,0), outline=(255,255,0)) #amarelo
	#tela.rectangle((55,32,size-1,18), fill=(255,255,255), outline=(255,255,255)) #branco
	img_new = Image.new('RGB', (20,20), (255,255,0)); img_new.save("data/tiles/amarelo.png")
	img_new = Image.new('RGB', (20,20), (255,0,255)); img_new.save("data/tiles/roxo.png")
	img_new = Image.new('RGB', (20,20), (98,0,255)); img_new.save("data/tiles/azul.png")
	img_new = Image.new('RGB', (20,20), (98,0,98)); img_new.save("data/tiles/roxoesc.png")
	img_new = Image.new('RGB', (20,20), (5,180,5)); img_new.save("data/tiles/verde.png")
	
	
def desenhar_labirinto_pillow(img, tamanho, posicoes, size=11):
	#recebe posições geradas no gerar_labirinto
	(x,y) = tamanho
	size = size + 1
	contX = contY = 0
	cor = (255,255,255)
	for yy in range(0,y*size+1,size):
		for xx in range(0,x*size+1,size):
			try:
				if posicoes[0][contX] == 1:
					#linhas nas horizontais
					img.line((xx, yy, xx+size, yy), fill=cor)
				if posicoes[1][contY] == 1:
					#linhas verticais 
					img.line((xx, yy, xx, yy+size), fill=cor)
				contX += 1
				contY += 1
			except:
				pass
		contX -= 1
	desenha_fim_pillow(img, tamanho, size)
	cria_obs_pillow(img, tamanho, size)
	

def venceu(x, y, var, size=11):
	# print(var)
	size = size + 1
	# print([x*22-11,y*22-11])
	if var == [3,y*size-size/2]:
		return True
	return False

