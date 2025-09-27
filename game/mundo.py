import pygame
import random
import math
from game.entidades import Jugador, Gema, Cofre, Enemigo

class Mundo:
    def __init__(self, ancho, alto, pantalla):
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pantalla  
        self.jugador = Jugador(ancho // 2, alto // 2)
        self.gemas = []
        self.poderes= set()
        self.cofres = []
        self.enemigos = []
        self.mensaje = ""
        self.mensaje_tiempo = 0
        self.gemas_recolectadas = 0
        self.cofres_abiertos = 0

        self.enemigos_generados = 0
        self.max_enemigos = 3
        
        poderes_generados= set()
        self.generar_gemas(15)
        self.generar_cofres(8)
        self.generar_enemigo()

         ##-----------------------------NUEVO PORTALES-----------------------------------
        self.portales = []
        self.generar_portal()
        self.cambiar_fondo = False
        self.jugador_cruzo_portal = False

        # Cargar sprites de árboles una sola vez
        ruta = "assets/sprites/"
        arbol1 = pygame.image.load(ruta + "arbol1.png").convert_alpha()
        arbol2 = pygame.image.load(ruta + "arbol2.png").convert_alpha()

        self.arboles_tipos = [
        pygame.transform.scale(arbol1, (100, 100)),
        pygame.transform.scale(arbol2, (100, 100))
        ]

        N= 30 #Cantidad de Arboles    
        self.positions = [
            (100, 120), (300, 120), (500, 120), (700, 120), (900, 120), (1100, 120),
            (200, 220), (400, 220), (600, 220), (800, 220), (1000, 220), (1200, 220),
            (150, 340), (350, 340), (950, 340), (1150, 340),
            (200, 460), (400, 460), (600, 460), (800, 460), (1000, 460), (1200, 460),
            (100, 580), (300, 580), (500, 580), (700, 580), (900, 580), (1100, 580),
            (250, 620), (1050, 620),
        ]

        self.tree_types = [random.choice(self.arboles_tipos) for _ in range(N)]

    def generar_gemas(self, cantidad):
        poderes_disponibles = list((set(range(1, 79))) - self.poderes)
        random.shuffle(poderes_disponibles)

        for i in range(cantidad):
            if i >= len(poderes_disponibles):
                print("No hay más poderes únicos disponibles")
                break

            x = random.randint(0, self.ancho - 50)
            y = random.randint(100, self.alto - 50)

            # Elegir directamente un poder único de la lista mezclada
            poder = poderes_disponibles[i]

            gema = Gema(x, y)
            gema.poder = poder

            self.gemas.append(gema)
            self.poderes.add(poder)


    
    def generar_cofres(self, cantidad):
        for _ in range(cantidad):
            x = random.randint(0, self.ancho)
            y = random.randint(90, self.alto - 50)
            # Asegurar que no esté demasiado cerca del jugador inicial
            if abs(x - self.ancho//2) > 100 and abs(y - self.alto//2) > 100:
                self.cofres.append(Cofre(x, y))


    def generar_enemigo(self): 
        if self.enemigos_generados >= self.max_enemigos:
            return
        
        intento = 0
        while True:
            intento += 1
            x = random.randint(50, self.ancho - 50)
            y = random.randint(50, self.alto - 50)
            if abs(x - self.ancho // 2) > 150 and abs(y - self.alto // 2) > 150:
                enemigo = Enemigo(x, y)
                # Asegura que la lista tenga exactamente el siguiente enemigo
                self.enemigos.append(enemigo)
                self.enemigos_generados += 1
                print(f"[Mundo] Enemigo #{self.enemigos_generados} generado en ({x},{y})")
                break
            if intento > 50:
                # Fallback para no quedar en loop infinito si el mapa es pequeño
                enemigo = Enemigo(x, y)
                self.enemigos.append(enemigo)
                self.enemigos_generados += 1
                print(f"[Mundo] Enemigo (forced) #{self.enemigos_generados} generado en ({x},{y})")
                break


    def generar_portal(self):
        x = random.randint(100, self.ancho - 100)
        y = random.randint(100, self.alto - 100)
        from game.entidades import Portal
        nuevo = Portal(x, y)
        self.portales.append(nuevo)
    
    def actualizar(self):
        # Verificar colisión con gemas
        for gema in self.gemas[:]:
            if self.jugador.rect.colliderect(gema.obtener_rect()):
                if self.jugador.recolectar_gema(gema):
                    self.gemas.remove(gema)
                    self.gemas_recolectadas += 1
                    self.mostrar_mensaje(f"¡Recogiste {gema.nombre}!")
        
        # Verificar colisión con cofres
        for cofre in self.cofres:
            if not cofre.abierto and self.jugador.rect.colliderect(cofre.obtener_rect()):
                self.intentar_abrir_cofre(cofre)

        for enemigo in self.enemigos:
            enemigo.mover_hacia(self.jugador)
            if self.jugador.rect.colliderect(enemigo.rect):
                self.mostrar_mensaje("¡Has sido atrapado por un enemigo!")
                gema_perdida =  enemigo.solicitar_gema(self.jugador.inventario)
                if gema_perdida is not None:
                    #self.gemas.append(Gema(x, y, nombre=gema_perdida.nombre, poder=gema_perdida.poder))
                    # Generar nueva gema en el mapa
                    x = random.randint(30, self.ancho - 30)
                    y = random.randint(30, self.alto - 30)
                    self.gemas.append(Gema(x, y, nombre=gema_perdida.nombre, poder=gema_perdida.poder))
                else:
                    self.mostrar_mensaje("No tienes gemas para perder.")
                self.enemigos.remove(enemigo)
                self.generar_enemigo()

        # Verificar colisión con portales
        for portal in self.portales:
            if portal.activo and self.jugador.rect.colliderect(portal.obtener_rect()):
                self.intentar_usar_portal(portal)

        self.verificar_portal()
    
        self.arboles_tipos = [pygame.transform.scale(a, (128, 128)) for a in self.arboles_tipos]


    def arboles(self):
        pygame.display.set_caption("Árboles en posiciones aleatorias")
        # Dibujar los árboles en las posiciones ya guardadas
        for i in range(len(self.positions)):
            self.pantalla.blit(self.tree_types[i], self.positions[i])

    
    def intentar_abrir_cofre(self, cofre):
        # Buscar la gema exacta
        gema_exacta = self.jugador.inventario.buscar(cofre.poder_requerido)
        
        if gema_exacta:
            self.jugador.usar_gema(cofre.poder_requerido)
            cofre.abierto = True
            self.cofres_abiertos += 1
            self.mostrar_mensaje(f"¡Cofre abierto con {gema_exacta.nombre}!")
            cofre.recoger()

        else:
            # Buscar la gema más cercana
            inventario = self.jugador.inventario.inorden()
            if inventario:
                mejor_diff = float('inf')
                mejor_gema = None
                
                for gema in inventario:
                    diff = abs(gema.poder - cofre.poder_requerido)
                    if diff < mejor_diff:
                        mejor_diff = diff
                        mejor_gema = gema
                
                if mejor_gema:
                    self.jugador.usar_gema(mejor_gema.poder)
                    cofre.abierto = True
                    self.cofres_abiertos += 1
                    self.mostrar_mensaje(f"¡Cofre abierto con {mejor_gema.nombre} (cercana)!")
                    cofre.recoger()
                else:
                    self.mostrar_mensaje("No tienes gemas para abrir este cofre.")
            else:
                self.mostrar_mensaje("Inventario vacío - no puedes abrir el cofre")
    
    ##-----------------------------NUEVO PORTALES-----------------------------------
    def intentar_usar_portal(self, portal):
        gema_max = self.jugador.inventario.encontrar_maximo()  # mayor poder en BST
        if gema_max:
            # Eliminar la gema directamente del inventario
            poder_max = gema_max.poder
            nombre_max = gema_max.nombre
            self.jugador.inventario.eliminar(poder_max)

            # Mensaje
            self.mostrar_mensaje(f"¡Usaste {nombre_max} para cruzar el portal!")

            # Desactivar portal y marcar cruce
            portal.activo = False
            self.jugador_cruzo_portal = True

            # Alternar cambio de fondo
            self.cambiar_fondo = not self.cambiar_fondo
        else:
            self.mostrar_mensaje("Necesitas una gema poderosa para usar el portal.")


    def todos_cofres_recolectados(self):
        """
        Retorna True si todos los cofres han sido recolectados.
        """
        if not self.cofres:
            return False
        return all(cofre.recolectado for cofre in self.cofres)

    # --- DETECTAR CRUCE DE PORTAL ---
    def verificar_portal(self):
        # Marca jugador_cruzo_portal = True si el jugador toca algún portal activo.
        
        for portal in self.portales:
            if portal.activo and self.jugador and self.jugador.rect.colliderect(portal.obtener_rect()):
                self.jugador_cruzo_portal = True
                break



    def mostrar_mensaje(self, mensaje):
        self.mensaje = mensaje
        self.mensaje_tiempo = pygame.time.get_ticks()
    
    def dibujar(self, pantalla, fuente, fuente_pequena):
        # Dibujar gemas
        for gema in self.gemas:
            gema.dibujar(pantalla, fuente_pequena)
        
        # Dibujar cofres
        for cofre in self.cofres:
            cofre.dibujar(pantalla, fuente_pequena)

        for enemigo in self.enemigos:
            #enemigo.mover_hacia(self.jugador)
            enemigo.dibujar(pantalla)

        for portal in self.portales:
            portal.dibujar(pantalla)
        
        # Dibujar jugador
        self.jugador.dibujar(pantalla)

        #Dibujar arboles
        self.arboles()
        
        # Dibujar HUD
        self.dibujar_hud(pantalla, fuente)
    
    def dibujar_hud(self, pantalla, fuente):
        # --- Fondo superior HUD ---
        hud_altura = 90
        pygame.draw.rect(pantalla, (0, 11, 61), (0, 0, self.ancho, hud_altura))  # Color base
        pygame.draw.rect(pantalla, (0, 180, 90), (0, hud_altura, self.ancho, 3))  # Línea verde
        
        # --- Título del juego ---
        titulo_fuente = pygame.font.Font(None, 48)
        texto_titulo = titulo_fuente.render("Gems Seeker", True, (180, 220, 220))
        pantalla.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 20))

        # --- Estadísticas ---
        texto_gemas = fuente.render(f"Gemas: {self.gemas_recolectadas}", True, (255, 255, 255))
        texto_cofres = fuente.render(f"Cofres: {self.cofres_abiertos}/{len(self.cofres)}", True, (200, 200, 255))
        pantalla.blit(texto_gemas, (20, 20))
        pantalla.blit(texto_cofres, (20, 50))

        # --- Inventario ---
        inventario = self.jugador.inventario.inorden()
        if inventario:
            texto_inv = fuente.render("Inventario: " + ", ".join([str(g.poder) for g in inventario]), 
                                    True, (0, 191, 99))
            pantalla.blit(texto_inv, (200, 55))

        # --- Mensaje temporal centrado abajo ---
        if pygame.time.get_ticks() - self.mensaje_tiempo < 3000 and self.mensaje:
            texto_mensaje = fuente.render(self.mensaje, True, (255, 255, 255))
            pantalla.blit(texto_mensaje, (self.ancho // 2 - texto_mensaje.get_width() // 2, 
                                        self.alto - 60))

        # --- Controles (lado derecho) ---
        fuente_controles = pygame.font.Font(None, 20)  # Fuente más pequeña
        texto_control = fuente_controles.render(
            "ESPACIO:Evento especial I:Inventario detallado O:Posorden P:Preorden",
            True,
            (180, 220, 220)
        )
        pantalla.blit(texto_control, (self.ancho - 500, 25))