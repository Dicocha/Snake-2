# Libraries
import sys
from time import sleep
import pygame, random, pymysql
from pygame.locals import *

class Screens:
	# Ciclo principal para el juego
	def main():
		# Iniciar pygame
		pygame.init()

		# Variables de tamano
		global Win_x, Win_y, screen
		Win_x = 1366
		Win_y = 768
		Bottom_x = Win_x/2.5
		MBottom_x = 480
		
		# Configuracion de ventanas
		screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.NOFRAME)

		# Colores
		global Negro, Blanco
		Negro = pygame.Color(0, 0, 0)
		Blanco = pygame.Color(255, 255, 255)

		# FPS
		global FPS
		FPS = pygame.time.Clock()

		# Fuente de letras
		global font, fontbot
		font = pygame.font.Font("Recourses/Jackpot.ttf", 50)
		fontbot = pygame.font.Font("Recourses/Jackpot.ttf", 40)

		# Background
		global bg_img
		bg_img = pygame.image.load('Recourses/bg.jpg')
		bg_img = pygame.transform.scale(bg_img,(Win_x,Win_y))

		click = False
		
		while True:
			# Este ciclo es para cerrar el programa
			# handling key events
			for event in pygame.event.get():
				if event.type == QUIT: # Cerrar el programa con la equis
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: # Cerrar el programa con esc
						pygame.quit()
						sys.exit()
				if event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

			# Fondo de pantalla
			screen.blit(bg_img,(0,0))
			Borde = pygame.Rect(0, 0, Win_x, Win_y)
			pygame.draw.rect(screen, Blanco, Borde, width=2)

			# Botones Win_x, Win_y
			button_1 = pygame.Rect(MBottom_x, 300, 350, 70)
			button_2 = pygame.Rect(MBottom_x, 400, 350, 70)
			button_3 = pygame.Rect(MBottom_x, 500, 350, 70)
			pygame.draw.rect(screen, Blanco, button_1, width=2)
			pygame.draw.rect(screen, Blanco, button_2, width=2)
			pygame.draw.rect(screen, Blanco, button_3, width=2)

			# Textos
			Resorces.start_text('SNAKE 2', font, Blanco, screen, 
								Win_x/2.8, 80)
			Resorces.start_text('Inicio', fontbot, Blanco, screen, 
								Bottom_x+10, 298)
			Resorces.start_text('Puntaje', fontbot, Blanco, screen, 
								Bottom_x-40, 395)
			Resorces.start_text('Salir', fontbot, Blanco, screen, 
								Bottom_x+10, 495)

			# Controles
			mx, my = pygame.mouse.get_pos()

			# Acciones de los botones
			if button_1.collidepoint(mx, my):
				Resorces.start_text('Inicio', fontbot, (130,130,130), screen, Bottom_x+10, 298)
				if click:
					Screens.Game()

			if button_2.collidepoint(mx, my):
				Resorces.start_text('Puntaje', fontbot, (130,130,130), screen, Bottom_x-40, 395)
				if click:
					Screens.TablaPosiciones()

			if button_3.collidepoint(mx,my):
				Resorces.start_text('Salir', fontbot, (130,130,130), screen, Bottom_x+10, 495)
				if click:
					pygame.quit()
					sys.exit()

			click = False

			pygame.display.update()
			FPS.tick(60)

	# Modulo de las Scorees
	def TablaPosiciones():
		click = False
		while True:
			# Este ciclo es para cerrar el programa
			# handling key events
			for event in pygame.event.get():
				if event.type == QUIT: # Cerrar el programa con la equis
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: # Cerrar el programa con esc
						Screens.main()
				if event.type == MOUSEBUTTONDOWN: # Habilita el mouse
					if event.button == 1:
						click = True

			screen.blit(bg_img,(0,0))
			Borde = pygame.Rect(0, 0, Win_x, Win_y)
			pygame.draw.rect(screen, Blanco, Borde, width=2)

			# Botones
			Regresar = pygame.Rect(300, 600, 370, 75)
			Salir = pygame.Rect(800, 600, 220, 75)
			pygame.draw.rect(screen, Blanco, Regresar, width=2)
			pygame.draw.rect(screen, Blanco, Salir, width=2)

			# Text
			Resorces.start_text('Los 5 mejores', font, Blanco, screen, Win_x/4, 80)
			Resorces.start_text('Regresar', fontbot, Blanco, screen, 310, 595)
			Resorces.start_text('Salir', fontbot, Blanco, screen, 810, 595)

			# Llamar la funcion conexion
			Connections.ConexionConsulta()

			# Controles
			mx, my = pygame.mouse.get_pos()

			# Acciones de los botones
			if Regresar.collidepoint(mx, my):
				Resorces.start_text('Regresar', fontbot, (130,130,130), screen, 310, 595)
				if click:
					Screens.main()

			if Salir.collidepoint(mx, my):
				Resorces.start_text('Salir', fontbot, (130,130,130), screen, 810, 595)
				if click:
					pygame.quit()
					sys.exit()

			click = False
			pygame.display.update()

	# Modulo del juego
	def Game():
		global Negro, Blanco, FPS, PosicionPwrUp

		# Variables del personaje
		VelocidadPersonaje = 20
		PosicionPersonaje  = [100, 50]
		CuerpoPersonaje = [[100, 50], [85, 50], [75, 50], [65, 50]]

		# Variables del alimento
		PosicionFruta = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]
		PosicionPwrUp = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]
		SpawnPwrUp = True
		SpawnFruta = True

		# Fuente
		font_P = pygame.font.Font("Recourses/Jackpot.ttf", 20)

		# Score
		Score = 0

		# Esto es para iniciar a la derecha 
		Direccion = 'RIGHT'
		change_to = Direccion

		#Musica
		# music = pygame.mixer.Sound("")
		# music.play()

		while True:
			# handling key events
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: # Cerrar el programa con esc
						pygame.quit()
						sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						change_to = 'UP'
					if event.key == pygame.K_w:
						change_to = 'UP'
					if event.key == pygame.K_DOWN:
						change_to = 'DOWN'
					if event.key == pygame.K_s:
						change_to = 'DOWN'
					if event.key == pygame.K_LEFT:
						change_to = 'LEFT'
					if event.key == pygame.K_a:
						change_to = 'LEFT'
					if event.key == pygame.K_RIGHT:
						change_to = 'RIGHT'
					if event.key == pygame.K_d:
						change_to = 'RIGHT'

			# If two keys pressed simultaneously
			# we don't want snake to move into two
			# directions simultaneously
			if change_to == 'UP' and Direccion != 'DOWN':
				Direccion = 'UP'
			if change_to == 'DOWN' and Direccion != 'UP':
				Direccion = 'DOWN'
			if change_to == 'LEFT' and Direccion != 'RIGHT':
				Direccion = 'LEFT'
			if change_to == 'RIGHT' and Direccion != 'LEFT':
				Direccion = 'RIGHT'

			# Moving the snake
			if Direccion == 'UP':
				PosicionPersonaje[1] -= 10
			if Direccion == 'DOWN':
				PosicionPersonaje[1] += 10
			if Direccion == 'LEFT':
				PosicionPersonaje[0] -= 10
			if Direccion == 'RIGHT':
				PosicionPersonaje[0] += 10

			# Snake body growing mechanism
			# if fruits and snakes collide then scores
			# will be incremented by 10
			CuerpoPersonaje.insert(0, list(PosicionPersonaje))
			if PosicionPersonaje[0] == PosicionFruta[0] and PosicionPersonaje[1] == PosicionFruta[1]:
				Score +=  1
				VelocidadPersonaje += 2
				SpawnFruta = False
			else:
				CuerpoPersonaje.pop()
				
			if not SpawnFruta:
				PosicionFruta = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]

			SpawnFruta = True

			if PosicionPersonaje[0] == PosicionPwrUp[0] and PosicionPersonaje[1] == PosicionPwrUp[1]:
				VelocidadPersonaje = 20
				SpawnPwrUp = False

			if not SpawnPwrUp:
				PosicionPwrUp = [random.randrange(1, (Win_x//10)) * 10, 
				random.randrange(1, (Win_y//10)) * 10]

			SpawnPwrUp = True

			screen.blit(bg_img,(0,0))
			Borde = pygame.Rect(0, 0, Win_x, Win_y)
			pygame.draw.rect(screen, Blanco, Borde, width=2)

			for pos in CuerpoPersonaje:
				pygame.draw.rect(screen, Blanco, pygame.Rect(pos[0], pos[1], 14, 14))
			pygame.draw.rect(screen, Blanco, pygame.Rect(PosicionFruta[0], PosicionFruta[1], 14, 14))
			
			Resorces.PowerUp(PosicionPersonaje)

			# Game Over conditions
			if PosicionPersonaje[0] < 0 or PosicionPersonaje[0] > Win_x-10:
				#music.stop()
				Mecanics.game_over(Score)

			if PosicionPersonaje[1] < 0 or PosicionPersonaje[1] > Win_y-10:
				#music.stop()
				Mecanics.game_over(Score)

			# Touching the snake body
			for block in CuerpoPersonaje[1:]:
				if PosicionPersonaje[0] == block[0] and PosicionPersonaje[1] == block[1]:
					#music.stop()
					Mecanics.game_over(Score)
		
			# displaying score countinuously
			Resorces.start_text('Score: ' + str(Score), font_P, Blanco, screen, Win_x/2.4, 2)

			# Refresh game screen
			pygame.display.update()

			# Frame Per Second /Refres Rate
			FPS.tick(VelocidadPersonaje)

class Connections:
	# Conexion a la base de datos 
	# Modulo para consultar
	def ConexionConsulta():
		font_base = pygame.font.Font("Recourses/Jackpot.ttf", 30)
		# Conexion con la base de datos
		conn = pymysql.connect( 
			host='127.0.0.1', 
			user='Cliente',
			password = '', 
			db='Projects', 
		)
					
		ix = 400
		iy = 200

		cur = conn.cursor()
		cur.execute("SELECT concat(`Name`,'                            ',`Score`) from Snake order by `Score` desc limit 5")
		Name = [Nombre[0] for Nombre in cur.fetchall()]
		for i in Name:
			Resorces.start_text(i,font_base, Blanco, screen, ix, iy)
			iy += 50

		conn.close()

	# Modulo para insertas datos
	def ConexionInsertar(user_text, Score, screen, Mensaje):
		# Conexion con la base de datos
		conn = pymysql.connect( 
			host='127.0.0.1', 
			user='Cliente',  
			password = '', 
			db='Projects', 
		)

		# Eliminar el registro con el mismo nombre
		cur = conn.cursor()
		sql = "DELETE FROM `Snake` WHERE `Name` = %s"
		val = (user_text);

		cur.execute(sql, val)
		conn.commit()

		# Insertar el registro
		cur = conn.cursor()
		sql = "INSERT INTO `Snake`(`Name`, `Score`) VALUES (%s,%s)"
		val = (user_text, Score);

		cur.execute(sql, val)
		conn.commit()

		conn.close()

class Mecanics:
	# Modulo de game over
	def game_over(Score):
		font = pygame.font.Font("Recourses/Jackpot.ttf", 30)
		font_ins = pygame.font.Font("Recourses/Jackpot.ttf", 10)
		click = False
		user_text = ''
		Mensaje = ''

		while True:
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

				if event.type == pygame.KEYDOWN:
					# Check for backspace
					if event.key == pygame.K_BACKSPACE:
						user_text = user_text[:-1]
					else:
						user_text += event.unicode
					# Limit characters
						if text_surface.get_width() > Entrada.w - 15:
							user_text = user_text[:-1]

			screen.blit(bg_img,(0,0))
			Borde = pygame.Rect(0, 0, Win_x, Win_y)
			pygame.draw.rect(screen, Blanco, Borde, width=2)
			
			# Mostrando la Score
			ScoreGameOver = font.render('Tu Score es: ' + str(Score), True, Blanco)
			game_over_rect = ScoreGameOver.get_rect()
			
			# Configuracion de la Score
			game_over_rect.midtop = (670, 80)
			
			# Mostrar la Score
			screen.blit(ScoreGameOver, game_over_rect)

			# Botones
			Entrada = pygame.Rect(710, 200, 150, 70)
			MenuPrincipal = pygame.Rect(460, 300, 430, 60)
			Guardar = pygame.Rect(520, 400, 300, 60)
			Salir = pygame.Rect(520, 500, 300, 60)

			pygame.draw.rect(screen, Blanco, Entrada, width=2)
			pygame.draw.rect(screen, Blanco, MenuPrincipal, width=2)
			pygame.draw.rect(screen, Blanco, Guardar, width=2)
			pygame.draw.rect(screen, Blanco, Salir, width=2)

			# Text
			text_surface = font.render(user_text, True, Blanco)
			Resorces.start_text('Nombre: ', font, Blanco, screen, 460, 200)
			Resorces.start_text('Menu Principal', font, Blanco, screen, 475, 300)
			Resorces.start_text('Guardar', font, Blanco, screen, 550, 400)
			Resorces.start_text('Salir', font, Blanco, screen, 600, 500)
			Resorces.start_text(Mensaje, font_ins, Blanco, screen, Win_x-120, Win_y-25)

			# Posicion de la entrada
			screen.blit(text_surface, (Entrada.x+5, Entrada.y+5))
			Entrada.w = max(100, text_surface.get_width()+10)

			# Controles
			mx, my = pygame.mouse.get_pos()

			# Acciones de los botones
			if MenuPrincipal.collidepoint(mx, my):
				Resorces.start_text('Menu Principal', font, (130,130,130), screen, 475, 300)
				if click:	
					Screens.main()
						
			if Salir.collidepoint(mx, my):
				Resorces.start_text('Salir', font, (130,130,130), screen, 600, 500)
				if click:
					pygame.quit()
					sys.exit()

			if Guardar.collidepoint(mx, my):
				Resorces.start_text('Guardar', font, (130,130,130), screen, 550, 400)
				if click:
					Connections.ConexionInsertar(user_text, Score, screen, Mensaje)
					sleep(0.5)
					Mensaje = 'Guardado!!'

			click = False
			pygame.display.update()
			pygame.display.flip()

class Resorces:
	# Fuente del texto
	def start_text(text, font, color, surface, x, y):
		textobj = font.render(text, True, color)
		textrect = textobj.get_rect()
		textrect.topleft = (x, y)
		surface.blit(textobj, textrect)

	def PowerUp(PosicionPersonaje):
		# PowerUp
		global PosicionPwrUp
		Rojo = pygame.Color(255,0,0)

		#sleep(1)

		pygame.draw.rect(screen, Rojo, pygame.Rect(PosicionPwrUp[0], PosicionPwrUp[1], 14, 14))

# Ejecutador del programa
if __name__ == "__main__" : 
    Screens.main()