# Este programa se basa en https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/ 
# Librerias
from time import sleep
import pygame, random, pymysql
from pygame.locals import *

# Ventanas
# Ciclo principal para el juego
def main():
	# Iniciar pygame
	pygame.init()

	# Variables de tamano
	global Win_x, Win_y, screen
	Win_x = 720
	Win_y = 480
	Bottom_x = Win_x/4
	# Configuracion de ventanas
	screen = pygame.display.set_mode((Win_x, Win_y), pygame.NOFRAME)

	# Colores
	global Negro, Blanco
	Negro = pygame.Color(0, 0, 0)
	Blanco = pygame.Color(255, 255, 255)


	# FPS
	global FPS
	FPS = pygame.time.Clock()

	# Fuente de letras
	global font, fontbot
	font = pygame.font.Font("Recursos/Jackpot.ttf", 50)
	fontbot = pygame.font.Font("Recursos/Jackpot.ttf", 40)

	click = False
	
	while True:
		# Este ciclo es para cerrar el programa
		# handling key events
		for event in pygame.event.get():
			if event.type == QUIT: # Cerrar el programa con la equis
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: # Cerrar el programa con esc
					pygame.quit()
					exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		# Fondo de pantalla
		screen.fill(Negro)
		Borde = pygame.Rect(0, 0, Win_x, Win_y)
		pygame.draw.rect(screen, Blanco, Borde, width=2)

		# Botones 
		button_1 = pygame.Rect(Bottom_x, 130, 350, 70)
		button_2 = pygame.Rect(Bottom_x, 230, 350, 70)
		button_3 = pygame.Rect(Bottom_x, 330, 350, 70)
		pygame.draw.rect(screen, Blanco, button_1, width=2)
		pygame.draw.rect(screen, Blanco, button_2, width=2)
		pygame.draw.rect(screen, Blanco, button_3, width=2)

		# Textos
		start_text('SNAKE 2', font, Blanco, screen, 180, 20)
		start_text('Inicio', fontbot, Blanco, screen, 265, 129)
		start_text('Puntaje', fontbot, Blanco, screen, 210, 225)
		start_text('Salir', fontbot, Blanco, screen, 260, 325)

		# Controles
		mx, my = pygame.mouse.get_pos()

		# Acciones de los botones
		if button_1.collidepoint(mx, my):
			start_text('Inicio', fontbot, (130,130,130), screen, 265, 129)
			if click:
				Game()

		if button_2.collidepoint(mx, my):
			start_text('Puntaje', fontbot, (130,130,130), screen, 210, 225)
			if click:
				TablaPosiciones()

		if button_3.collidepoint(mx,my):
			start_text('Salir', fontbot, (130,130,130), screen, 260, 325)
			if click:
				pygame.quit()
				exit()

		click = False

		pygame.display.update()
		FPS.tick(60)

# Modulo del juego
def Game():
	global Negro, Blanco, FPS
	Rojo = pygame.Color(255,0,0)

	# Variables del personaje
	VelocidadPersonaje = 15
	PosicionPersonaje  = [100, 50]
	CuerpoPersonaje = [[100, 50], [85, 50], [75, 50], [65, 50]]

	# Variables del alimento
	PosicionFruta = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]
	PosicionPwrUp = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]
	SpawnPwrUp = True
	SpawnFruta = True

	# Fuente
	font_P = pygame.font.Font("Recursos/Jackpot.ttf", 20)

	# Puntuacion
	Puntuacion = 0

	# Esto es para iniciar a la derecha 
	Direccion = 'RIGHT'
	change_to = Direccion

	#Musica
	music = pygame.mixer.Sound("")
	music.play()

	while True:
		# handling key events
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: # Cerrar el programa con esc
					pygame.quit()
					exit()

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
			Puntuacion +=  1
			VelocidadPersonaje +=1
			SpawnFruta = False
		else:
			CuerpoPersonaje.pop()
			
		if not SpawnFruta:
			PosicionFruta = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]

		SpawnFruta = True

		# 
		#Tiempo = sleep(1.0)
		#if Tiempo == 0:
			# PowerUp
		if PosicionPersonaje[0] == PosicionPwrUp[0] and PosicionPersonaje[1] == PosicionPwrUp[1]:
			VelocidadPersonaje = 15
			Puntuacion *= 2
			SpawnPwrUp = False
				
		if not SpawnPwrUp:
			PosicionPwrUp = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]

		SpawnPwrUp = True

		screen.fill(Negro)
		Borde = pygame.Rect(0, 0, Win_x, Win_y)
		pygame.draw.rect(screen, Blanco, Borde, width=2)

		for pos in CuerpoPersonaje:
			pygame.draw.rect(screen, Blanco, pygame.Rect(pos[0], pos[1], 15, 15))
		pygame.draw.rect(screen, Blanco, pygame.Rect(PosicionFruta[0], PosicionFruta[1], 15, 15))
		pygame.draw.rect(screen, Rojo, pygame.Rect(PosicionPwrUp[0], PosicionPwrUp[1], 15, 15))

		# Game Over conditions
		if PosicionPersonaje[0] < 0 or PosicionPersonaje[0] > Win_x-10:
			music.stop()
			game_over(Puntuacion)

		if PosicionPersonaje[1] < 0 or PosicionPersonaje[1] > Win_y-10:
			music.stop()
			game_over(Puntuacion)

		# Touching the snake body
		for block in CuerpoPersonaje[1:]:
			if PosicionPersonaje[0] == block[0] and PosicionPersonaje[1] == block[1]:
				music.stop()
				game_over(Puntuacion)
	
		# displaying score countinuously
		start_text('Puntuacion: ' + str(Puntuacion), font_P, Blanco, screen, 250, 2)

		# Refresh game screen
		pygame.display.update()

		# Frame Per Second /Refres Rate
		FPS.tick(VelocidadPersonaje)

# Modulo de las puntuaciones
def TablaPosiciones():
	click = False
	while True:
		# Este ciclo es para cerrar el programa
		# handling key events
		for event in pygame.event.get():
			if event.type == QUIT: # Cerrar el programa con la equis
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: # Cerrar el programa con esc
					main()
			if event.type == MOUSEBUTTONDOWN: # Habilita el mouse
				if event.button == 1:
					click = True

		screen.fill(Negro)
		Borde = pygame.Rect(0, 0, Win_x, Win_y)
		pygame.draw.rect(screen, Blanco, Borde, width=2)

		# Botones 
		Regresar = pygame.Rect(50, 350, 370, 75)
		Salir = pygame.Rect(460, 350, 220, 75)
		pygame.draw.rect(screen, Blanco, Regresar, width=2)
		pygame.draw.rect(screen, Blanco, Salir, width=2)

		# Text
		start_text('Los 3 mejores', font, Blanco, screen, 60, 20)
		start_text('Regresar', fontbot, Blanco, screen, 63, 344)
		start_text('Salir', fontbot, Blanco, screen, 477, 344)

		# Llamar la funcion conexion
		ConexionConsulta()

		# Controles
		mx, my = pygame.mouse.get_pos()

		# Acciones de los botones
		if Regresar.collidepoint(mx, my):
			start_text('Regresar', fontbot, (130,130,130), screen, 63, 344)
			if click:
				main()

		if Salir.collidepoint(mx, my):
			start_text('Salir', fontbot, (130,130,130), screen, 477, 344)
			if click:
				pygame.quit()
				exit()

		click = False
		pygame.display.update()

# Conexion a la base de datos 
# Modulo para consultar
def ConexionConsulta():
	font_base = pygame.font.Font("Recursos/Jackpot.ttf", 30)
	# Conexion con la base de datos
	conn = pymysql.connect( 
		host='localhost', 
		user='Cliente',  
		password = '', 
		db='Proyectos', 
	)
				
	ix = 100
	iy = 120

	cur = conn.cursor()
	cur.execute("SELECT concat(`Nombres`,'                            ',`Puntuacion`) from Snake order by `Puntuacion` desc limit 3")
	Nombres = [Nombre[0] for Nombre in cur.fetchall()]
	for i in Nombres:
		start_text(i,font_base, Blanco, screen, ix, iy)
		iy += 50

	conn.close()

# Modulo para insertas datos
def ConexionInsertar(user_text, Puntuacion, screen, Mensaje):
	# Conexion con la base de datos
	conn = pymysql.connect( 
		host='localhost', 
		user='Cliente',  
		password = '', 
		db='Proyectos', 
	)

	# Eliminar el registro con el mismo nombre
	cur = conn.cursor()
	sql = "DELETE FROM `Snake` WHERE `Nombres` = %s"
	val = (user_text);

	cur.execute(sql, val)
	conn.commit()

	# Insertar el registro
	cur = conn.cursor()
	sql = "INSERT INTO `Snake`(`Nombres`, `Puntuacion`) VALUES (%s,%s)"
	val = (user_text, Puntuacion);

	cur.execute(sql, val)
	conn.commit()

	conn.close()

# Mecanicas
# Modulo de game over
def game_over(Puntuacion):
	font = pygame.font.Font("Recursos/Jackpot.ttf", 30)
	font_ins = pygame.font.Font("Recursos/Jackpot.ttf", 10)
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

		screen.fill(Negro)
		Borde = pygame.Rect(0, 0, Win_x, Win_y)
		pygame.draw.rect(screen, Blanco, Borde, width=2)
		
		# Mostrando la puntuacion
		PuntuacionGameOver = font.render('Tu puntuacion es: ' + str(Puntuacion), True, Blanco)
		game_over_rect = PuntuacionGameOver.get_rect()
		
		# Configuracion de la puntuacion
		game_over_rect.midtop = (350, 20)
		
		# Mostrar la puntuacion
		screen.blit(PuntuacionGameOver, game_over_rect)

		# Botones
		Entrada = pygame.Rect(320, 120, 150, 70)
		MenuPrincipal = pygame.Rect(160, 225, 430, 60)
		Guardar = pygame.Rect(220, 300, 300, 60)
		Salir = pygame.Rect(220, 375, 300, 60)

		pygame.draw.rect(screen, Blanco, Entrada, width=2)
		pygame.draw.rect(screen, Blanco, MenuPrincipal, width=2)
		pygame.draw.rect(screen, Blanco, Guardar, width=2)
		pygame.draw.rect(screen, Blanco, Salir, width=2)

		# Text
		text_surface = font.render(user_text, True, Blanco)
		start_text('Nombre: ', font, Blanco, screen, 80, 120)
		start_text('Menu Principal', font, Blanco, screen, 180, 225)
		start_text('Guardar', font, Blanco, screen, 250, 300)
		start_text('Salir', font, Blanco, screen, 295, 373)
		start_text(Mensaje, font_ins, Blanco, screen, 500, 140)

		# Posicion de la entrada
		screen.blit(text_surface, (Entrada.x+5, Entrada.y+5))
		Entrada.w = max(100, text_surface.get_width()+10)

		# Controles
		mx, my = pygame.mouse.get_pos()

		# Acciones de los botones
		if MenuPrincipal.collidepoint(mx, my):
			start_text('Menu Principal', font, (130,130,130), screen, 180, 225)
			if click:	
				main()
					
		if Salir.collidepoint(mx, my):
			start_text('Salir', font, (130,130,130), screen, 295, 373)
			if click:
				pygame.quit()
				exit()

		if Guardar.collidepoint(mx, my):
			start_text('Guardar', font, (130,130,130), screen, 250, 300)
			if click:
				ConexionInsertar(user_text, Puntuacion, screen, Mensaje)
				sleep(0.5)
				Mensaje = 'Guardado!!'

		click = False
		pygame.display.update()
		pygame.display.flip()

# Otros recursos
# Fuente del texto
def start_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Ejecutador del programa
if __name__ == "__main__" : 
    main()