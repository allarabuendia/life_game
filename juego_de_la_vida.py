#Importar librerías
import numpy as np
import pygame
import time

#Iniciar pantalla
pygame.init()

width, height = 600, 600
screen = pygame.display.set_mode((height, width))

#Color de fondo(Casi negro)
bg = 25, 25, 25

#Pintar fondo
screen.fill(bg)

#Especificar celdas del juego
nxC, nyC = 50, 50

#Tamaño de las celdas ( División entre el n de celdas y el tamaño del tablero)
dimCW = width / nxC
dimCH = height / nyC

#Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros((nxC, nyC))

'''#Estado inicial 1(Autómata palo):
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1'''

#Estado inicial 2(Autómata móvil):
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

#Control de la ejecución del juego
pauseExect = False

#Bucle de ejecución

while True:

    #Creamos una copia del estado de la pantalla por cada iteración.
    newGameState = np.copy(gameState)

    #Volver a colorear para que no se superponga la info por cada iteración
    screen.fill(bg)

    #Ponemos módulo Time para que no vaya tan rápido.
    time.sleep(0.1)

    #Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        #Si la suma del vector mouseclick es mayor a 0 significa que se está pulsando alguna tecla del ratón
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            #Como nos devuelve posición y queremos saber la celda exacta, dividimos por el ancho y alto de las celdas.
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    '''Generar los gráficos que se dibujan en cada uno de los fotogramas,
    lo primero es recorrer tanto eje x como eje y por cada una de las celdas'''

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                '''Calculamos el n de vecinos cercanos para ver su estado,
                usamos la funcion módulo, para nunca se salga del mapa.
                Como si el tablero fuera un toride.'''

                n_neigh = gameState[(x-1) % nxC,(y-1) % nyC] + \
                          gameState[(x) % nxC, (y-1) % nxC] + \
                          gameState[(x+1) % nxC, (y-1) % nxC] + \
                          gameState[(x-1) % nxC, (y) % nxC] + \
                          gameState[(x+1) % nxC, (y) % nxC] + \
                          gameState[(x-1) % nxC, (y+1) % nxC] + \
                          gameState[(x) % nxC, (y+1) % nxC] + \
                          gameState[(x+1) % nxC, (y+1) % nxC]

                # Regla 1: Una célula muerta con exactamente 3 vecinas vivas: 'Revive'.

                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas: 'Muere'

                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            #Crear poligono de cada celda a dibujar
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            #Dibujamos la celda
            if newGameState[x, y] == 0:
                #Si la célula está muerta, el fondo es negro, con bordes de 1 pixel
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            else:
                #Si la célula está viva, dibujamos el fondo blanco sin bordes.
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)


    #Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    pygame.display.flip()
