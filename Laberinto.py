#Se importan las librerías necesarias
from collections import deque
import pygame
import time

#Funciones para encontrar las soluciones del laberinto
def convertir_a_grafo(laberinto):
    """Retorna un grafo a partir de un laberinto"""
    grafo = dict()
    y = 0
    max_y = len(laberinto)
    for fila in laberinto:
        x = 0
        max_x = len(fila)
        for casilla in fila:
            if casilla == "#":
                x += 1
                continue
            vecinos = [
                (x-1, y),
                (x+1, y),
                (x, y-1),
                (x, y+1)
            ]
            aristas = []
            for vecino in vecinos:
                x_vecino = vecino[0]
                y_vecino = vecino[1]
                in_range = (0 <= x_vecino < max_x) and (0 <= y_vecino < max_y)
                if not in_range:
                    continue
                is_wall = (laberinto[y_vecino][x_vecino] == "#")
                if not is_wall:
                    aristas.append(vecino)
            grafo[(x,y)] = aristas
            x += 1
        y += 1
    return grafo

def buscar_inicio(laberinto):
    """Busca el punto incial en un laberinto"""
    x, y = 0, 0
    for fila in laberinto:
        x = 0
        for casilla in fila:
            if casilla == "A":
                return (x, y)
            x += 1
        y += 1

def buscar_fin(laberinto):
    """Busca el punto final en un laberinto"""
    x, y = 0, 0
    for fila in laberinto:
        x = 0
        for casilla in fila:
            if casilla == "B":
                return (x, y)
            x += 1
        y += 1

def buscar_ruta_corta(grafo, inicio, fin):
    """Imprime las posibles rutas de un laberinto desde el mas corto al mas largo"""
    curr = inicio
    cola = deque()
    visitados = set()
    cola.append((curr, [curr]))
    while len(cola) > 0:
        curr, ruta = cola.popleft()
        if curr == fin:
            return ruta
        if curr in visitados:
            continue
        visitados.add(curr)
        for vecino in grafo[curr]:
            cola.append((vecino, ruta + [vecino]))

def buscar_rutas(grafo, inicio, fin):
    """Buscar todas las rutas posibles de un laberinto"""
    return list(set(buscar_ruta(grafo, inicio, fin, [inicio], {inicio})))

def buscar_ruta(grafo, curr, fin, ruta, visitados):
    """Función recursiva para encontrar una ruta"""
    rutas = []
    if curr == fin:
        return [tuple(ruta)]
    for vecino in grafo[curr]:
        if vecino not in visitados:
            visitados.add(vecino)
            ruta.append(vecino)
            rutas = rutas + buscar_ruta(grafo, vecino, fin, ruta, visitados)
            ruta.pop()
            visitados.remove(vecino)
    return rutas

#Se une todo en una misma función
def hallar_soluciones(laberinto):
  for fila in laberinto:
    print(fila)
  grafo = convertir_a_grafo(laberinto)
  inicio = buscar_inicio(laberinto)
  fin = buscar_fin(laberinto)
  ruta = buscar_ruta_corta(grafo, inicio, fin)
  print("Ruta más corta:")
  for paso in ruta:
    print(f"{paso} -> ", end="")
  print("Fin")
  rutas = buscar_rutas(grafo, inicio, fin)
  rutas = sorted(rutas, key=len)
  print("Todas las rutas:")
  for r in rutas:
    for paso in r:
      print(f"{paso} -> ", end="")
    print("Fin")


#Laberintos de ejemplo
laberinto1 = [
    "#############",
    "#A.....#...B#",
    "#####.##.####",
    "#.....##..#.#",
    "#.###....##.#",
    "#############"
]

laberinto2 =[
    "A...B",
    ".###.",
    "....."
]

laberinto3 = [
    "A..B",
    "....",
    "...."
]
laberinto4 = [
    "#################",
    "#A#.......#.....#",
    "#.#.#####.#.###.#",
    "#.#.....#.#.#...#",
    "#.#.###.#.#.#.###",
    "#.#...#.#.#.#...#",
    "#.#.#.#.#.#.###.#",
    "#.#.#.#.........#",
    "#.#.#.#########.#",
    "#.#.#...........#",
    "#.#.###########.#",
    "#.#...........#.#",
    "#.###########.#.#",
    "#.............#.#",
    "#########.#####.#",
    "#...............#",
    "###############.B"
]

laberinto5 = [
    "#############################################",
    "#A#.....#.......#.....#.....................#",
    "#.#.###.#.#####.#.###.#.###########.#.#####.#",
    "#.#.#...#.#...#.#.#...#.#.........#.#.....#.#",
    "#.#.#.###.#.#.#.#.#.###.#.#######.#.#####.#.#",
    "#.#.#...#.#.#.#.#.#.#...#.#.....#.#.#.....#.#",
    "#.#.###.#.#.#.#.#.#.#.###.#.###.#.#.#.#####.#",
    "#.#.....#.#.#.#.#.#.#.....#.#.#.#.#.#.#.....#",
    "#.#####.#.#.#.#.#.#########.#.#.#.#.#.#.#####",
    "#...........#.#.............#.#.#.#.#.#.....#",
    "###########.#.###############.#.#.#.#.#####.#",
    "#...........#.................#.#.#.#.......#",
    "#.#############################.#.#.#######.#",
    "#.#.............................#.#.........#",
    "#.#.#############################.#########.#",
    "#.#.......................................#.#",
    "###########################################B#"
]



#Funciones para visualizar el laberinto
def generar_laberinto(laberinto):
    """Genera un laberinto fijo como matriz de caracteres.'#' = pared, '.' = camino, 'A' = inicio, 'B' = fin"""
    return [list(fila) for fila in laberinto]

def dibujar_laberinto(pantalla, laberinto, tam_celda):
    """Dibuja el laberinto en la pantalla"""
    for y, fila in enumerate(laberinto):
        for x, casilla in enumerate(fila):
            rect = pygame.Rect(x * tam_celda, y * tam_celda, tam_celda, tam_celda)
            color = (0,0,0)
            if casilla == "#":
                color = COLOR_PARED
            elif casilla == ".":
                color = COLOR_CAMINO
            elif casilla == "A":
                color = COLOR_INICIO
            elif casilla == "B":
                color = COLOR_FIN
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, (200, 200, 200), rect, 1)  #Borde gris

def dibujar_agente(pantalla, posicion, tam_celda):
    """Dibuja el agente en la celda especificada"""
    x, y = posicion
    rect = pygame.Rect(x * tam_celda, y * tam_celda, tam_celda, tam_celda)
    pygame.draw.rect(pantalla, COLOR_AGENTE, rect)

def animar_ruta(pantalla, laberinto, ruta, tam_celda, delay=0.2):
    """Anima la ruta en la pantalla mostrando cómo el agente se mueve"""
    for paso in ruta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
        pantalla.fill((255, 255, 255))
        dibujar_laberinto(pantalla, laberinto, tam_celda)
        dibujar_agente(pantalla, paso, tam_celda)
        pygame.display.flip()
        time.sleep(delay)  #Pausa para animación

def calcular_tam_celda(laberinto, ancho_pantalla, alto_pantalla):
    """Calcula el tamaño máximo posible de cada celda para que el laberinto quepa en la pantalla"""
    filas = len(laberinto)
    columnas = len(laberinto[0])
    tam_celda_x = ancho_pantalla // columnas
    tam_celda_y = alto_pantalla // filas
    return min(tam_celda_x, tam_celda_y)

def dibujar_overlay(pantalla, ancho, alto, boton_rect):
    """Dibuja un overlay semitransparente con un botón en el centro"""
    #Fondo semitransparente
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  #Negro con 180 de transparencia
    pantalla.blit(overlay, (0, 0))

    #Botón central
    pygame.draw.rect(pantalla, (200, 200, 200), boton_rect)  #Gris claro
    pygame.draw.rect(pantalla, (50, 50, 50), boton_rect, 3)  #Borde oscuro

    #Texto del botón
    fuente = pygame.font.SysFont(None, 48)
    texto = fuente.render("Iniciar", True, (0, 0, 0))  #Texto negro
    texto_rect = texto.get_rect(center=boton_rect.center)
    pantalla.blit(texto, texto_rect)

def boton_presionado(mouse_pos, boton_rect):
    """Retorna True si el usuario hizo clic dentro del botón"""
    return boton_rect.collidepoint(mouse_pos)

def pantalla_inicio(pantalla, laberinto, tam_celda):
    """Muestra la pantalla inicial y espera a que el usuario presione el botón"""
    ancho, alto = pantalla.get_size()
    #Definir botón central proporcional al tamaño de pantalla
    boton_ancho = ancho * 0.3
    boton_alto = alto * 0.12
    boton_x = (ancho - boton_ancho) / 2
    boton_y = (alto - boton_alto) / 2
    boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_presionado(evento.pos, boton_rect):
                    esperando = False

        #Dibujar laberinto de fondo
        pantalla.fill((255, 255, 255))
        dibujar_laberinto(pantalla, laberinto, tam_celda)

        #Dibujar overlay con botón
        dibujar_overlay(pantalla, ancho, alto, boton_rect)

        pygame.display.flip()

def dibujar_overlay_opciones(pantalla, ancho, alto, boton_repetir, boton_siguiente):
    """Dibuja un overlay con las opciones de 'Repetir' y 'Siguiente'"""
    #Fondo semitransparente
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Negro con transparencia
    pantalla.blit(overlay, (0, 0))

    #Botón repetir
    pygame.draw.rect(pantalla, (200, 200, 200), boton_repetir)
    pygame.draw.rect(pantalla, (50, 50, 50), boton_repetir, 3)
    fuente = pygame.font.SysFont(None, int(alto * 0.04))
    texto_repetir = fuente.render("Repetir", True, (0, 0, 0))
    texto_repetir_rect = texto_repetir.get_rect(center=boton_repetir.center)
    pantalla.blit(texto_repetir, texto_repetir_rect)

    #Botón siguiente
    pygame.draw.rect(pantalla, (200, 200, 200), boton_siguiente)
    pygame.draw.rect(pantalla, (50, 50, 50), boton_siguiente, 3)
    texto_siguiente = fuente.render("Siguiente", True, (0, 0, 0))
    texto_siguiente_rect = texto_siguiente.get_rect(center=boton_siguiente.center)
    pantalla.blit(texto_siguiente, texto_siguiente_rect)

def pantalla_opciones(pantalla, laberinto, tam_celda):
    """Muestra el overlay de opciones y espera a que el usuario seleccione alguna"""
    ancho, alto = pantalla.get_size()

    #Calcular dimensiones relativas para los botones
    boton_ancho = ancho * 0.2
    boton_alto = alto * 0.1
    espacio_entre_botones = ancho * 0.05

    #Calcular posición horizontal para centrar los dos botones
    total_anchura_botones = boton_ancho * 2 + espacio_entre_botones
    inicio_x = (ancho - total_anchura_botones) / 2
    pos_y = alto * 0.5

    #Definir botones centrados uno al lado del otro
    boton_repetir = pygame.Rect(inicio_x, pos_y, boton_ancho, boton_alto)
    boton_siguiente = pygame.Rect(inicio_x + boton_ancho + espacio_entre_botones, pos_y, boton_ancho, boton_alto)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_repetir.collidepoint(evento.pos):
                    return "repetir"
                elif boton_siguiente.collidepoint(evento.pos):
                    return "siguiente"

        #Dibujar laberinto de fondo
        pantalla.fill((255, 255, 255))
        dibujar_laberinto(pantalla, laberinto, tam_celda)

        #Dibujar overlay con botones
        dibujar_overlay_opciones(pantalla, ancho, alto, boton_repetir, boton_siguiente)

        pygame.display.flip()

def recorrer_rutas(pantalla, laberinto, rutas, tam_celda, ancho, alto):
    """Reproduce una por una las rutas del laberinto animándolas en pantalla y permite al usuario elegir entre repetir la ruta actual o pasar a la siguiente"""
    #Inicializar índice de la ruta actual
    indice_ruta = 0
    total_rutas = len(rutas)

    while True:
        ruta_actual = rutas[indice_ruta]

        #Animar la ruta actual
        print(f"Animando ruta {indice_ruta + 1} de {total_rutas}...")
        animar_ruta(pantalla, laberinto, ruta_actual, tam_celda, delay=0.2)

        #Mostrar opciones al usuario
        opcion = pantalla_opciones(pantalla, laberinto, tam_celda)

        if opcion == "repetir":
            #Repetir la misma ruta
            continue
        elif opcion == "siguiente":
            #Avanzar a la siguiente ruta
            indice_ruta += 1
            if indice_ruta >= total_rutas:
                print("Has recorrido todas las rutas")
                indice_ruta = 0  #Reinicia desde la primera o termina con break

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_repetir.collidepoint(evento.pos):
                    return "repetir"
                elif boton_siguiente.collidepoint(evento.pos):
                    return "siguiente"

        #Dibujar laberinto de fondo
        pantalla.fill((255, 255, 255))
        dibujar_laberinto(pantalla, laberinto, tam_celda)

        #Dibujar overlay con botones
        dibujar_overlay_opciones(pantalla, ancho, alto, boton_repetir, boton_siguiente)

        pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_repetir.collidepoint(evento.pos):
                    return "repetir"
                elif boton_siguiente.collidepoint(evento.pos):
                    return "siguiente"

        #Dibuja laberinto de fondo
        pantalla.fill((255, 255, 255))
        dibujar_laberinto(pantalla, laberinto, tam_celda)

        #Dibuja overlay con botones
        dibujar_overlay_opciones(pantalla, ancho, alto, boton_repetir, boton_siguiente)

        pygame.display.flip()


def main():
    """Función principal del programa para visualizar el laberinto seleccionado"""
    pygame.init()
    pygame.mixer.init()

    #Cargar la música
    pygame.mixer.music.load("musica.mp3")

    #Reproducir en bucle infinito
    pygame.mixer.music.play(-1)

    #Cargar imagen para el icono
    logo = pygame.image.load("Logo.png")
    pygame.display.set_icon(logo)

    #Pedir al usuario que elija un laberinto
    print("Selecciona un laberinto:")
    print("1 -> Laberinto 1")
    print("2 -> Laberinto 2")
    print("3 -> Laberinto 3")
    print("4 -> Laberinto 4")
    print("5 -> Laberinto 5")
    seleccion = input("Ingresa el número del laberinto: ")

    #Mapea el número a los laberintos
    laberintos = {
        "1": laberinto1,
        "2": laberinto2,
        "3": laberinto3,
        "4": laberinto4,
        "5": laberinto5
    }

    if seleccion in laberintos:
        lab = laberintos[seleccion]
        laberinto = generar_laberinto(lab)
        print(f"Laberinto {seleccion}")
        hallar_soluciones(lab)
    else:
        print("Número inválido. Debes ingresar 1, 2, 3, 4 o 5.")
        pygame.quit()
        return

    #Obtener tamaño de pantalla
    info_pantalla = pygame.display.Info()
    ancho_pantalla = info_pantalla.current_w
    alto_pantalla = info_pantalla.current_h

    #Calcular tamaño de cada celda
    tam_celda = calcular_tam_celda(laberinto, int(ancho_pantalla * 0.8), int(alto_pantalla * 0.8))

    #Calcular dimensiones de la ventana
    ancho = len(laberinto[0]) * tam_celda
    alto = len(laberinto) * tam_celda
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(f"Laberinto {seleccion}")

    #Hallar solución
    grafo = convertir_a_grafo(laberinto)
    inicio = buscar_inicio(laberinto)
    fin = buscar_fin(laberinto)

    #Encontrar todas las rutas ordenadas por longitud
    rutas = buscar_rutas(grafo, inicio, fin)
    rutas = sorted(rutas, key=len)

    #Mostrar pantalla de inicio
    pantalla_inicio(pantalla, laberinto, tam_celda)

    #Iniciar la animación con control de botones
    recorrer_rutas(pantalla, laberinto, rutas, tam_celda, ancho_pantalla, alto_pantalla)


    #Bucle principal
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        pantalla.fill((255, 255, 255))  #Fondo blanco
        dibujar_laberinto(pantalla, laberinto, tam_celda)
        pygame.display.flip()

    pygame.quit()


#Definir colores
COLOR_PARED = (0, 0, 0)
COLOR_CAMINO = (255, 255, 255)
COLOR_INICIO = (0, 255, 0)
COLOR_FIN = (0, 0, 255)
COLOR_AGENTE = (255, 0, 0)


#Ejecución de la función principal
main()