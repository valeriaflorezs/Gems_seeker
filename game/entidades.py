import pygame
import random
import os
from core.arbol_bst import ArbolBST

import pygame
import os

ruta = "assets/sprites"

class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocidad = 7
        self.inventario = ArbolBST()
        self.nombre = "Minero"

        # --- Cargar sprite del jugador ---
        self.sprite = pygame.image.load(os.path.join(ruta, "pico.png"))
        self.sprite = pygame.transform.scale(self.sprite, (60, 60))  # ajustar tamaño

    def mover(self, dx, dy):
        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad

        # Limitar al área de juego
        self.rect.x = max(0, min(self.rect.x, 1280 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 720 - self.rect.height))

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, self.rect)

    def recolectar_gema(self, gema):
        exito = self.inventario.insertar(gema.nombre, gema.poder, gema.x, gema.y)
        return exito

    def usar_gema(self, poder):
        gema = self.inventario.buscar(poder)
        if gema:
            self.inventario.eliminar(poder)
            return gema
        return None

class Gema:
    def __init__(self, x, y, nombre=None, poder=None):
        self.x = x
        self.y = y
        self.radio = 15
        
        # Generar poder aleatorio si no se pasa
        self.poder = poder if poder is not None else random.randint(1, 80)
        self.nombre = nombre if nombre is not None else f"Gema {self.poder}"
        
        # --- Cargar sprites de gemas ---
        self.sprites = {
            "Black": pygame.image.load(os.path.join(ruta, "Black.png")),
            "Blue": pygame.image.load(os.path.join(ruta, "Blue.png")),
            "Dark_red": pygame.image.load(os.path.join(ruta, "Dark_red.png")),
            "Green": pygame.image.load(os.path.join(ruta, "Green.png")),
            "Pink": pygame.image.load(os.path.join(ruta, "Pink.png")),
            "Red": pygame.image.load(os.path.join(ruta, "Red.png")),
            "Violet": pygame.image.load(os.path.join(ruta, "Violet.png")),
            "White": pygame.image.load(os.path.join(ruta, "White.png")),
            "Yellow": pygame.image.load(os.path.join(ruta, "Yellow.png")),
            "Yellow_green": pygame.image.load(os.path.join(ruta, "Yellow_green.png")),
        }
        
        # Escoger un sprite aleatorio
        self.sprite_nombre = random.choice(list(self.sprites.keys()))
        self.sprite = self.sprites[self.sprite_nombre]
        
        # Ajustar tamaño del sprite
        self.sprite = pygame.transform.scale(self.sprite, (40, 40))
        
    def dibujar(self, pantalla, fuente):
        rect = self.sprite.get_rect(center=(self.x, self.y))
        pantalla.blit(self.sprite, rect)
        
        # Dibujar texto encima
        name= self.nombre
        if len(name) > 9:
            texto = fuente.render(name[9], True, (255,255,255))
        else:
            texto = fuente.render(str(self.poder), True, (255, 255, 255))

        pantalla.blit(texto, (self.x - texto.get_width() // 2, self.y-30))
    
    def obtener_rect(self):
        return self.sprite.get_rect(center=(self.x, self.y))

class Cofre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.poder_requerido = random.randint(1, 100)
        self.abierto = False
        self.tamaño = 60
        self.recolectado = False

        # --- Cargar sprite ---  
        self.sprite_cerrado = pygame.image.load(os.path.join(ruta, "cofre.png"))
        self.sprite_cerrado = pygame.transform.scale(self.sprite_cerrado, (self.tamaño, self.tamaño))

        # Si tienes un sprite distinto para abierto puedes cargarlo aquí
        # De momento reutilizo el mismo pero oscurecido
        self.sprite_abierto = self.sprite_cerrado.copy()
        self.sprite_abierto.fill((150, 150, 150, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def dibujar(self, pantalla, fuente):
        if not self.abierto:
            sprite = self.sprite_cerrado
        else:
            sprite = self.sprite_abierto

        rect = sprite.get_rect(center=(self.x, self.y))
        pantalla.blit(sprite, rect)

        # Mostrar poder requerido si no está abierto
        if not self.abierto:
            texto = fuente.render(str(self.poder_requerido), True, (255, 255, 255))
            pantalla.blit(texto, (self.x - texto.get_width() // 2, self.y + self.tamaño // 2 + 5))

    def obtener_rect(self):
        return pygame.Rect(self.x - self.tamaño // 2, self.y - self.tamaño // 2,
                           self.tamaño, self.tamaño)
    
    def recoger(self):
        self.recolectado = True
    


class Enemigo:    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocidad = 0.6
        self.nombre = "Jefe Enemigo"
        self.tocar  = False
        self.tamaño = 60 

        self.sprite = pygame.image.load(os.path.join(ruta, "enemigo.png"))
        self.sprite = pygame.transform.scale(self.sprite, (70, 70)) 


    def mover_hacia(self, jugador):
        if jugador.rect.x > self.rect.x:
            self.rect.x += self.velocidad
        elif jugador.rect.x < self.rect.x:
            self.rect.x -= self.velocidad
        
        if jugador.rect.y > self.rect.y:
            self.rect.y += self.velocidad
        elif jugador.rect.y < self.rect.y:
            self.rect.y -= self.velocidad

    

    def solicitar_gema(self, inventario):
        if inventario.raiz is None:
            return None

        gema_solicitada = random.randint(1, inventario.encontrar_maximo().poder)

        # Buscar gema exacta
        nodo_encontrado = inventario.buscar(gema_solicitada)
        if nodo_encontrado:
            inventario.eliminar(gema_solicitada)
            return gema_solicitada

        # Buscar sucesor
        print("Oh no! No tienes la gema solicitada. Eliminación por sucesor")
        nodo = inventario.raiz
        sucesor = None

        while nodo:
            if gema_solicitada < nodo.poder:
                sucesor = nodo
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho

        if sucesor:
            inventario.eliminar(sucesor.poder)
            return sucesor

        # Buscar predecesor
        print("No hay sucesor, se elimina el predecesor")
        nodo = inventario.raiz
        predecesor = None

        while nodo:
            if gema_solicitada > nodo.poder:
                predecesor = nodo
                nodo = nodo.derecho
            else:
                nodo = nodo.izquierdo

        if predecesor:
            inventario.eliminar(predecesor.poder)
            return  predecesor

        # Si no hay sucesor ni predecesor, eliminar raíz
        print("No tienes sucesor ni predecesor, se elimina la raíz")
        poder_raiz = inventario.raiz.poder
        nombre_raiz = inventario.raiz.nombre
        inventario.eliminar(poder_raiz)
        return inventario.raiz

         # --- Cargar sprite --- 

    def obtener_rect(self):
        return pygame.Rect(self.x - self.tamaño // 2, self.y - self.tamaño // 2,
                           self.tamaño, self.tamaño)
    

    def dibujar(self, pantalla):
        pantalla.blit(self.sprite, self.rect)


class Portal:
    def __init__(self, x, y, ancho=100, alto=100):
        self.rect = pygame.Rect(x, y, ancho, alto)

        # --- Cargar sprite ---
        import os
        ruta = "assets/sprites"
        self.sprite = pygame.image.load(os.path.join(ruta, "portal.png")) 
        self.sprite = pygame.transform.scale(self.sprite, (ancho, alto))

        self.activo = True

    def dibujar(self, pantalla):
        if self.activo:
            pantalla.blit(self.sprite, self.rect)

    def obtener_rect(self):
        return self.rect
   
    

