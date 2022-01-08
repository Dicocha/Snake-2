# Este programa se basa en https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/ 
# Librerias
import pygame, random, pymysql
from pygame.locals import *

# Iniciar pygame
pygame.init()

# Variables de tamano
Win_x = 720
Win_y = 480
Bottom_x = Win_x/4

# Configuracion de ventanas
# pygame.display.

# Variables del personaje
VelocidadPersonaje = 15
PosicionPersonaje  = [100, 50]
CuerpoPersonaje = [[100, 50], [85, 50], [75, 50], [65, 50]]

# Colores
Negro = pygame.Color(0, 0, 0)
Blanco = pygame.Color(255, 255, 255)
color_active = pygame.Color(Blanco)
color_passive = pygame.Color(Blanco)
color = color_passive

# FPS
FPS = pygame.time.Clock()

# Variables del alimento
PosicionFruta = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]
SpawnFruta = True

# Esto es para iniciar a la derecha 
Direccion = 'RIGHT'
change_to = Direccion

# Fuente de letras
font = pygame.font.Font("Recursos/Jackpot.ttf", 50)
fontbot = pygame.font.Font("Recursos/Jackpot.ttf", 40)
font_base = pygame.font.Font("Recursos/Jackpot.ttf", 30)
font_P = pygame.font.Font("Recursos/Jackpot.ttf", 20)

# Ventanas
# Ciclo principal para el juego
def main():
	global click
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

		# Objetos para la pantalla principal 
		screen = pygame.display.set_mode((Win_x, Win_y))

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

		# Control
		mx, my = pygame.mouse.get_pos()

		# Acciones de los botones
		if button_1.collidepoint(mx, my):
			if click:
				Game(change_to, Direccion, PosicionPersonaje, CuerpoPersonaje, PosicionFruta, VelocidadPersonaje, SpawnFruta)

		if button_2.collidepoint(mx, my):
			if click:
				TablaPosiciones()

		if button_3.collidepoint(mx,my):
			if click:
				pygame.quit()
				exit()

		click = False

		pygame.display.update()
		FPS.tick(60)

# Modulo del juego
def Game(change_to, Direccion, PosicionPersonaje, CuerpoPersonaje, PosicionFruta, VelocidadPersonaje, SpawnFruta):
	# Puntuacion
	global Puntuacion 
	Puntuacion = 0

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
			SpawnFruta = False
		else:
			CuerpoPersonaje.pop()
			
		if not SpawnFruta:
			PosicionFruta = [random.randrange(1, (Win_x//10)) * 10, random.randrange(1, (Win_y//10)) * 10]

		SpawnFruta = True

		screen_game = pygame.display.set_mode((Win_x, Win_y))
		screen_game.fill(Negro)

		for pos in CuerpoPersonaje:
			pygame.draw.rect(screen_game, Blanco, pygame.Rect(pos[0], pos[1], 15, 15))
		pygame.draw.rect(screen_game, Blanco, pygame.Rect(PosicionFruta[0], PosicionFruta[1], 15, 15))

		# Game Over conditions
		if PosicionPersonaje[0] < 0 or PosicionPersonaje[0] > Win_x-10:
			game_over()

		if PosicionPersonaje[1] < 0 or PosicionPersonaje[1] > Win_y-10:
			game_over()

		# Touching the snake body
		for block in CuerpoPersonaje[1:]:
			if PosicionPersonaje[0] == block[0] and PosicionPersonaje[1] == block[1]:
				game_over()
	
		# displaying score countinuously
		start_text('Puntuacion: ' + str(Puntuacion), font_P, Blanco, screen_game, 250, 2)

		# Refresh game screen
		pygame.display.update()

		# Frame Per Second /Refres Rate
		FPS.tick(VelocidadPersonaje)

# Modulo de las puntuaciones
def TablaPosiciones():
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

		screen_Tabla = pygame.display.set_mode((Win_x, Win_y))
		screen_Tabla.fill(Negro)
		Borde = pygame.Rect(0, 0, Win_x, Win_y)
		pygame.draw.rect(screen_Tabla, Blanco, Borde, width=2)

		# Control
		mx, my = pygame.mouse.get_pos()

		# Botones 
		Regresar = pygame.Rect(50, 350, 370, 75)
		Salir = pygame.Rect(460, 350, 220, 75)
		pygame.draw.rect(screen_Tabla, Blanco, Regresar, width=2)
		pygame.draw.rect(screen_Tabla, Blanco, Salir, width=2)

		# Text
		start_text('Puntuaciones', font, Blanco, screen_Tabla, 70, 20)
		start_text('Regresar', fontbot, Blanco, screen_Tabla, 63, 344)
		start_text('Salir', fontbot, Blanco, screen_Tabla, 477, 344)

		# Llamar la funcion conexion
		ConexionConsulta(screen_Tabla)

		# Acciones de los botones
		if Regresar.collidepoint(mx, my):
			if click:
				main()

		if Salir.collidepoint(mx, my):
			if click:
				pygame.quit()
				exit()

		click = False
		pygame.display.update()

# Conexion a la base de datos 
# Modulo para consultar
def ConexionConsulta(screen_Tabla):
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
	cur.execute("SELECT * FROM `Snake` ORDER BY `Puntuacion` DESC")
	for Nombre, Puntos in cur.fetchall():
		for i,j in Nombre, Puntos:
			start_text(i+'.....'+j,font_base, Blanco, screen_Tabla, ix, iy)
			iy += 50

#	cur = conn.cursor()
#	cur.execute("SELECT `Nombres` FROM `Snake`")
#	Nombres = [Nombre[0] for Nombre in cur.fetchall()]
#	for i in Nombres:
#		start_text(i,font_base, Blanco, screen_Tabla, ix, iy)
#		iy += 50

#	jx = 470
#	jy = 120

#	cur = conn.cursor()
#	cur.execute("SELECT `Puntuacion` FROM `Snake`")
#	Puntuacion = [Puntos[0] for Puntos in cur.fetchall()]
#	for j in Puntuacion:
#		start_text(str(j), font_base, Blanco, screen_Tabla, jx, jy)
#		jy += 50

	conn.close()

# Modulo para insertas datos
def ConexionInsertar():
	# Conexion con la base de datos
	conn = pymysql.connect( 
		host='localhost', 
		user='Cliente',  
		password = '', 
		db='Proyectos', 
	)

	cur = conn.cursor()
	sql = "INSERT INTO `Snake`(`Nombres`, `Puntuacion`) VALUES (%s,%s)"
	val = (user_text, Puntuacion);

	cur.execute(sql, val)
	conn.commit()
	print(cur.rowcount, "record inserted.")
	conn.close()

# Mecanicas
# Modulo de game over
def game_over():
	global user_text
	user_text = ''
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

		screen_GameOver = pygame.display.set_mode((Win_x, Win_y))
		screen_GameOver.fill(Negro)
		Borde = pygame.Rect(0, 0, Win_x, Win_y)
		pygame.draw.rect(screen_GameOver, Blanco, Borde, width=2)
		
		# Mostrando la puntuacion
		PuntuacionGameOver = font_base.render('Tu puntuacion es: ' + str(Puntuacion), True, Blanco)
		game_over_rect = PuntuacionGameOver.get_rect()
		
		# Configuracion de la puntuacion
		game_over_rect.midtop = (380, 20)
		
		# Mostrar la puntuacion
		screen_GameOver.blit(PuntuacionGameOver, game_over_rect)

		# Botones
		Entrada = pygame.Rect(320, 120, 300, 60)
		MenuPrincipal = pygame.Rect(160, 225, 430, 60)
		Guardar = pygame.Rect(220, 300, 300, 60)
		Salir = pygame.Rect(220, 375, 300, 60)

		pygame.draw.rect(screen_GameOver, Blanco, Entrada, width=2)
		pygame.draw.rect(screen_GameOver, Blanco, MenuPrincipal, width=2)
		pygame.draw.rect(screen_GameOver, Blanco, Guardar, width=2)
		pygame.draw.rect(screen_GameOver, Blanco, Salir, width=2)

		# Text
		start_text('Nombre: ', font_base, Blanco, screen_GameOver, 70, 120)
		start_text(user_text, font_base, Blanco, screen_GameOver, 330, 117)
		start_text('Menu Principal', font_base, Blanco, screen_GameOver, 180, 225)
		start_text('Guardar', font_base, Blanco, screen_GameOver, 250, 300)
		start_text('Salir', font_base, Blanco, screen_GameOver, 295, 373)

		# Control
		mx, my = pygame.mouse.get_pos()

		# Acciones de los botones
		if MenuPrincipal.collidepoint(mx, my):
			if click:	
				main()
					
		if Salir.collidepoint(mx, my):
			if click:
				pygame.quit()
				exit()

		if Guardar.collidepoint(mx, my):
			if click:
				ConexionInsertar()

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

if __name__ == "__main__" : 
    main()
