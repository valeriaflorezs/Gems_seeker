import pygame
import sys
import random
from game.mundo import Mundo


class JuegoGuardianes:
    def __init__(self):
        pygame.init()
        self.ancho, self.alto = 1280, 720
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Guardianes del Bosque Ancestral")

        self.reloj = pygame.time.Clock()
        self.mundo = Mundo(self.ancho, self.alto, self.pantalla)
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)

        # === ESTADOS DEL JUEGO ===
        self.estado = "inicio"  # "inicio", "jugando", "final"

        # Inventarios
        self.mostrar_inventario_detallado = False
        self.mostrar_inventario_preorden = False
        self.mostrar_inventario_posorden = False

        # Cargar imágenes
        self.img_inicio = pygame.image.load("assets/sprites/inicio.png")
        self.img_final = pygame.image.load("assets/sprites/final.png")

        # Escalar imágenes al tamaño de la pantalla
        self.img_inicio = pygame.transform.scale(self.img_inicio, (self.ancho, self.alto))
        self.img_final = pygame.transform.scale(self.img_final, (self.ancho, self.alto))

    # ---------------------------
    # MANEJO DE EVENTOS
    # ---------------------------
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if self.estado == "inicio":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    if 532 <= x <= 532+216 and 613 <= y <= 613+70: # Botón JUGAR
                        self.estado = "jugando"
                    # Botón SALIR
                    if 37 <= x <= 37+70 and 25 <= y <= 25+70:
                        return False

            elif self.estado == "jugando":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_i:
                        self.mostrar_inventario_detallado = not self.mostrar_inventario_detallado
                    elif evento.key == pygame.K_SPACE:
                        self.ejecutar_evento_especial()
                    elif evento.key == pygame.K_r:
                        self.recargar_mundo()
                    elif evento.key == pygame.K_p:  # Inventario preorden
                        self.mostrar_inventario_preorden = not self.mostrar_inventario_preorden
                        self.mostrar_inventario_posorden = False
                    elif evento.key == pygame.K_o:  # Inventario posorden
                        self.mostrar_inventario_posorden = not self.mostrar_inventario_posorden
                        self.mostrar_inventario_preorden = False

                # Movimiento continuo
                teclas = pygame.key.get_pressed()
                dx, dy = 0, 0
                if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                    dy = -5
                if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                    dy = 5
                if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                    dx = -5
                if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                    dx = 5
                self.mundo.jugador.mover(dx, dy)

            elif self.estado == "final":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    # Botón REINICIAR
                    if 532 <= x <= 532+216 and 613 <= y <= 613+70:
                        self.recargar_mundo()
                        self.estado = "jugando"
                    # Botón SALIR
                    if 37 <= x <= 37+70 and 25 <= y <= 25+70:
                        return False
        return True

    # ---------------------------
    # EVENTOS ESPECIALES
    # ---------------------------
    def ejecutar_evento_especial(self):
        eventos = [
            self.evento_trampa,
            self.evento_gema_especial,
            self.evento_busqueda_gema
        ]
        evento = random.choice(eventos)
        evento()

    def evento_trampa(self):
        if self.mundo.jugador.inventario.esta_vacio():
            self.mundo.mostrar_mensaje("¡Esquivaste la trampa! (inventario vacío)")
            return

        gemas = self.mundo.jugador.inventario.inorden()
        gema_perdida = random.choice(gemas)
        self.mundo.jugador.usar_gema(gema_perdida.poder)
        self.mundo.mostrar_mensaje(f"¡Caíste en una trampa! Perdiste {gema_perdida.nombre}")

    def evento_gema_especial(self):
        nombres_especiales = ["Gema del Fuego", "Gema del Agua", "Gema del Viento",
                              "Gema de la Tierra", "Gema del Rayo"]
        nombre = random.choice(nombres_especiales)
        poder = random.randint(80, 100)

        x = random.randint(50, self.ancho - 50)
        y = random.randint(50, self.alto - 50)

        from game.entidades import Gema
        nueva_gema = Gema(x, y)
        nueva_gema.nombre = nombre
        nueva_gema.poder = poder

        self.mundo.gemas.append(nueva_gema)
        self.mundo.mostrar_mensaje(f"¡Apareció una {nombre} en el mapa!")

    def evento_busqueda_gema(self):
        poder_buscado = random.randint(1, 100)
        gema = self.mundo.jugador.inventario.buscar(poder_buscado)

        if gema:
            self.mundo.mostrar_mensaje(f"¡Tienes la gema buscada! {gema.nombre}")
        else:
            self.mundo.mostrar_mensaje(f"Buscaste gema poder {poder_buscado} - no la tienes")

    def recargar_mundo(self):
        self.mundo = Mundo(self.ancho, self.alto, self.pantalla)
        self.mostrar_inventario_detallado = False
        self.mundo.mostrar_mensaje("¡Mundo recargado!")

    # ---------------------------
    # DIBUJADO DE INVENTARIOS
    # ---------------------------
    def dibujar_inventario_detallado(self):
        superficie = pygame.Surface((400, 400))
        superficie.fill((0, 11, 61))
        superficie.set_alpha(220)

        titulo = self.fuente.render("INVENTARIO DETALLADO", True, (255, 255, 0))
        superficie.blit(titulo, (20, 20))

        gemas = self.mundo.jugador.inventario.inorden()
        for i, gema in enumerate(gemas[:15]):
            texto = self.fuente_pequena.render(f"{gema.nombre} - Poder: {gema.poder}", True, (255, 255, 255))
            superficie.blit(texto, (20, 60 + i * 25))

        if len(gemas) > 15:
            texto_extra = self.fuente_pequena.render(f"... y {len(gemas) - 15} más", True, (200, 200, 200))
            superficie.blit(texto_extra, (20, 60 + 18 * 25))

        info_y = 60 + min(len(gemas), 15) * 25 + 20
        info_textos = [
            f"Total gemas: {len(gemas)}",
            f"Gema mínima: {self.mundo.jugador.inventario.encontrar_minimo().poder if gemas else 'N/A'}",
            f"Gema máxima: {self.mundo.jugador.inventario.encontrar_maximo().poder if gemas else 'N/A'}"
        ]

        for i, texto_info in enumerate(info_textos):
            texto = self.fuente_pequena.render(texto_info, True, (200, 255, 200))
            superficie.blit(texto, (20, info_y + i * 20))

        self.pantalla.blit(superficie, (self.ancho // 2 - 200, self.alto // 2 - 250))

    def dibujar_inventario_preorden(self):
        superficie = pygame.Surface((400, 400))
        superficie.fill((0, 11, 61))
        superficie.set_alpha(220)

        titulo = self.fuente.render("INVENTARIO PREORDEN", True, (255, 255, 0))
        superficie.blit(titulo, (20, 20))

        gemas = self.mundo.jugador.inventario.preorden()
        for i, gema in enumerate(gemas[:15]):
            texto = self.fuente_pequena.render(str(gema), True, (255, 255, 255))
            superficie.blit(texto, (20, 60 + i * 25))

        self.pantalla.blit(superficie, (self.ancho // 2 - 200, self.alto // 2 - 250))

    def dibujar_inventario_posorden(self):
        superficie = pygame.Surface((400, 400))
        superficie.fill((0, 11, 61))
        superficie.set_alpha(220)

        titulo = self.fuente.render("INVENTARIO POSTORDEN", True, (255, 255, 0))
        superficie.blit(titulo, (20, 20))

        gemas = self.mundo.jugador.inventario.postorden()
        for i, gema in enumerate(gemas[:15]):
            texto = self.fuente_pequena.render(str(gema), True, (255, 255, 255))
            superficie.blit(texto, (20, 60 + i * 25))

        self.pantalla.blit(superficie, (self.ancho // 2 - 200, self.alto // 2 - 250))

    # ---------------------------
    # DIBUJADO PRINCIPAL
    # ---------------------------
    def dibujar(self):
        if self.estado == "inicio":
            self.pantalla.blit(self.img_inicio, (0, 0))

        elif self.estado == "jugando":
            if self.mundo.cambiar_fondo:
                self.pantalla.fill((150, 50, 200))
            else:
                self.pantalla.fill((20, 40, 20))
            self.mundo.dibujar(self.pantalla, self.fuente, self.fuente_pequena)

            if self.mostrar_inventario_detallado:
                self.dibujar_inventario_detallado()
            elif self.mostrar_inventario_preorden:
                self.dibujar_inventario_preorden()
            elif self.mostrar_inventario_posorden:
                self.dibujar_inventario_posorden()

        elif self.estado == "final":
            self.pantalla.blit(self.img_final, (0, 0))

        pygame.display.flip()

    # ---------------------------
    # LOOP PRINCIPAL
    # ---------------------------
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()

            if self.estado == "jugando":
                self.mundo.actualizar()
                # Verificar condición de victoria
                if self.mundo.todos_cofres_recolectados() and self.mundo.jugador_cruzo_portal:
                    self.estado = "final"

            self.dibujar()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("=== GUARDIANES DEL BOSQUE ANCESTRAL ===")
    print("ESPACIO para eventos, I para inventario")
    juego = JuegoGuardianes()
    juego.ejecutar()