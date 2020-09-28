import pygame, sys, os

class obstaculos(pygame.sprite.Sprite):

	W = 200
	x,y = W,0
	tiles = {}
	selected = 'tiles'

	
	def __init__(self,window_size, tamanho, sizescreen):
		self.w,self.h = window_size
		self.loadTiles(37,tamanho, sizescreen)


	def reloadImages(self):
		s = int(self.s)+1; size = s,s
		for id in self.imageCopiesColored: self.images[id] = pygame.transform.scale(self.imageCopiesColored[id],size)

	#carrega as imagens para serem usadas como obstaculos
	def loadTiles(self,size, tamanho, sizescreen):
		self.sideBar = pygame.Surface((self.W,self.h)); self.rects = {}; self.getID = {}; self.getName = {}
		self.images = {}; self.imageCopies = {}; self.imageCopiesColored = {}
		data = open('data/tiles/order.txt').read().split('\n'); row = 0; self.loop = []
		for i in range(len(data)):
			y,x = divmod(row,5); y*=size; x*=size
			id = i+1; self.rects[id] = pygame.Rect(x+sizescreen*tamanho[0]-1,y,size,size); self.getID[data[i]] = id; self.getName[id] = data[i]
			self.imageCopies[id] = pygame.image.load('data/tiles/%s.png'%data[i]).convert_alpha()
			self.sideBar.blit(pygame.transform.scale(self.imageCopies[id],(size,size)),(x,y,size,size))
			row+=1; self.loop+=[id]
			
		id='tiles'; y,x = divmod(row,5); y*=size; x*=size; self.rects['tiles'] = pygame.Rect(x,y,size,size); self.loop+=[id]


	def events(self,event,mouse, tela, r, i):
		#if event.type == pygame.MOUSEMOTION and mouse[1]: self.x+=event.rel[0]; self.y+=event.rel[1]
        #desenha os os icones
		if event.type == pygame.MOUSEBUTTONDOWN:
            #contorno retangulos no icone selecionado
			if event.button == 1: #botão esquerdo do mouse acionado
				for id in self.loop:
					if self.rects[id].collidepoint(event.pos): 
						self.selected = id

		#permite 'apagar' o objeto através da colisão
		if event.type == pygame.MOUSEBUTTONUP:
			if self.selected =='tiles': pass
			else:
				locationx, locationy = pygame.mouse.get_pos()
				pointerImg_rect = self.imageCopies[self.selected].get_rect()
				pointerImg_rect.x = locationx
				pointerImg_rect.y = locationy
				pointerImg_rect.topleft = (locationx, locationy)

				if pointerImg_rect.colliderect(r) and self.selected==i:
						r.height = 0
						r.width = 0

	
	def update(self, mouse, mpos, tela):
		#mx,my = self.mpos = self.get_pos(mpos)

        #arrastando o objeto que foi selecionado
		if mouse[0]:
			if self.selected=='tiles': pass
			else:
				self.selected: self.tiles[pos] = self.selected
				id = self.selected
				
				if(self.selected == id):
					pointerImg_rect = self.imageCopies[id].get_rect()
					pointerImg_rect.center = pygame.mouse.get_pos()
					tela.blit(self.imageCopies[id], pointerImg_rect)
		

	#desenha todos obstaculos na tela
	def draw(self, screen, xpos, ypos, size, tamanho):
        #mostra os icones na lateral
		screen.blit(self.sideBar, (tamanho[0]*size+1,0))
		#Mostra retangulo nos obstaculos ao passar o mouse
		for id in self.loop:
			if self.rects[id].collidepoint(xpos, ypos): 
				pygame.draw.rect(screen,(0, 255, 0),self.rects[id], 1)