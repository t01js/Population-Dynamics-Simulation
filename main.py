import pygame
import random
import math
import numpy as np

# Configuración
WIDTH, HEIGHT = 1200, 800
NUM_FLECHAS = 1500
NUM_COMIDA = 50
COMIDA_REGEN = 0
COMIDA_REGEN_INTERVALO = 10000  # Intervalo de tiempo en milisegundos (5 segundos)

#GENES
ENERGIA_INICIAL = 100
ENERGIA_GASTO_MIN = 0.001
ENERGIA_GASTO_MAX = 0.09
VELOCIDAD_MIN = 1
VELOCIDAD_MAX = 3
RANGO_VISION_MIN = 20
RANGO_VISION_MAX = 80
TAMANO_MIN = 5
TAMANO_MAX = 10
REPRODUCCION_MIN = 10
REPRODUCCION_MAX = 20



# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación Dinamicas Poblacionales")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
individuos = []
nuevos_individuos = []  # Lista para almacenar los nuevos individuos

class Individuo:
    
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

        self.tamano = random.uniform(TAMANO_MIN, TAMANO_MAX)

        self.velocidad = random.uniform(VELOCIDAD_MIN, VELOCIDAD_MAX) - self.tamano/10

        self.energia = ENERGIA_INICIAL
        self.energia_gasto = random.uniform(ENERGIA_GASTO_MIN, ENERGIA_GASTO_MAX)

        self.rango_vision = random.uniform(RANGO_VISION_MIN, RANGO_VISION_MAX)

        self.color = (int(self.tamano * 2.55), random.randint(0, 255), random.randint(0, 255))

        self.direccion = random.uniform(0, 2*math.pi)
        self.angulo = 0
        
        self.tiempo_reproduccion = random.uniform(REPRODUCCION_MIN, REPRODUCCION_MAX)
        self.comida_consumida = 0

    def mover(self, comida):
        comida_cercana = [c for c in comida if math.sqrt((c.x - self.x) ** 2 + (c.y - self.y) ** 2) <= self.rango_vision]
        if comida_cercana:
            objetivo = min(comida_cercana, key=lambda c: math.sqrt((c.x - self.x) ** 2 + (c.y - self.y) ** 2))
            dx = objetivo.x - self.x
            dy = objetivo.y - self.y
            distancia = math.sqrt(dx ** 2 + dy ** 2)
            self.direccion = math.atan2(dy, dx)
            self.x += (dx / distancia) * self.velocidad
            self.y += (dy / distancia) * self.velocidad
            self.energia -= (self.velocidad**2 + self.tamano**3) * self.energia_gasto

            if distancia < 5:
                self.energia = ENERGIA_INICIAL
                comida.remove(objetivo)
                self.comida_consumida += 1

                if self.comida_consumida >= self.tiempo_reproduccion:
                    self.comida_consumida = 0
                    hijo = self.reproduccion()  # Crear nuevo individuo
                    if hijo.energia > 0:  # Asegurar que el hijo muera si su energía es menor o igual a 0
                        nuevos_individuos.append(hijo)  # Agregar el nuevo individuo a la lista de individuos

        else:
            self.direccion += random.uniform(-math.pi / 64, math.pi / 64)
            self.x += self.velocidad * math.cos(self.direccion)
            self.y += self.velocidad * math.sin(self.direccion)
            self.energia -= (self.velocidad**2 + self.tamano**3) * self.energia_gasto

            # asegurarse de que el individuo no se salga de la ventana
            if self.x < 0:
                self.x = 0
                self.direccion += math.pi
            elif self.x > WIDTH:
                self.x = WIDTH
                self.direccion += math.pi
            if self.y < 0:
                self.y = 0
                self.direccion += math.pi
            elif self.y > HEIGHT:
                self.y = HEIGHT
                self.direccion += math.pi

    def reproduccion(self):
        hijo = Individuo()
        hijo.x = self.x
        hijo.y = self.y
        hijo.velocidad = self.velocidad * random.uniform(0.09, 1.01)
        hijo.tamano = self.tamano * random.uniform(0.09, 1.01)
        self.color = (255,0,0)
        hijo.energia_gasto = self.energia_gasto * random.uniform(0.09, 1.01)
        hijo.energia = ENERGIA_INICIAL
        hijo.rango_vision = self.rango_vision * random.uniform(0.09, 1.01)
        hijo.tiempo_reproduccion = self.tiempo_reproduccion * random.uniform(0.09, 1.01)
        hijo.comida_consumida = 0
        # Asegurar que los atributos estén dentro de los límites
        if hijo.velocidad > VELOCIDAD_MAX:
            hijo.velocidad = VELOCIDAD_MAX
        elif hijo.velocidad < VELOCIDAD_MIN:
            hijo.velocidad = VELOCIDAD_MIN

        if hijo.tamano > TAMANO_MAX:
            hijo.tamano = TAMANO_MAX
        elif hijo.tamano < TAMANO_MIN:
            hijo.tamano = TAMANO_MIN

        if hijo.energia_gasto > ENERGIA_GASTO_MAX:
            hijo.energia_gasto = ENERGIA_GASTO_MAX
        elif hijo.energia_gasto < ENERGIA_GASTO_MIN:
            hijo.energia_gasto = ENERGIA_GASTO_MIN

        if hijo.rango_vision > RANGO_VISION_MAX:
            hijo.rango_vision = RANGO_VISION_MAX
        elif hijo.rango_vision < RANGO_VISION_MIN:
            hijo.rango_vision = RANGO_VISION_MIN

        if hijo.tiempo_reproduccion > REPRODUCCION_MAX:
            hijo.tiempo_reproduccion = REPRODUCCION_MAX
        elif hijo.tiempo_reproduccion < REPRODUCCION_MIN:
            hijo.tiempo_reproduccion = REPRODUCCION_MIN

        return hijo


    def dibujar(self, screen):
            self.angle = self.direccion
            x1 = int(self.x + self.tamano * math.cos(self.angle))
            y1 = int(self.y + self.tamano * math.sin(self.angle))
            x2 = int(self.x + self.tamano * math.cos(self.angle + 2.4 * math.pi / 3))
            y2 = int(self.y + self.tamano * math.sin(self.angle + 2.4 * math.pi / 3))
            x3 = int(self.x + self.tamano * math.cos(self.angle - 2.4 * math.pi / 3))
            y3 = int(self.y + self.tamano * math.sin(self.angle - 2.4 * math.pi / 3))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:
                pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), int(self.rango_vision), 1)
            
            pygame.draw.polygon(screen, self.color, [(x1, y1), (x2, y2), (x3, y3)])


class Comida:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.color = (0, 255, 0)

    def dibujar(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)


class Graficos:
    def dibujar_grafico_velocidad(screen, individuos):
        bins = np.linspace(VELOCIDAD_MIN, VELOCIDAD_MAX, 10)
        hist, _ = np.histogram([f.velocidad for f in individuos], bins=bins)
        max_height = 200
        bar_width = 30
        x_start = WIDTH // 16  # Posición inicial x del gráfico
        y_start = HEIGHT - max_height - 15  # Posición inicial y del gráfico
        title = font.render("Velocidad", True, (0, 0, 0))
        title_width, title_height = font.size("Velocidad")
        screen.blit(title, (x_start + bar_width // 2 - title_width // 2, y_start - title_height + 99))

        for i, h in enumerate(hist):
            height = int(h / len(individuos) * max_height)
            x = x_start + i * (bar_width + 5)
            y = y_start + max_height - height
            pygame.draw.rect(screen, (0, 0, 255), (x, y, bar_width, height))

    def dibujar_grafico_tamano(screen, individuos):
        bins = np.linspace(TAMANO_MIN, TAMANO_MAX, 10)
        hist, _ = np.histogram([f.tamano for f in individuos], bins=bins)
        max_height = 200
        bar_width = 30
        x_start = WIDTH // 3 - bar_width // 3  # Posición inicial x del gráfico
        y_start = HEIGHT - max_height - 15  # Posición inicial y del gráfico
        title = font.render("Tamaño", True, (0, 0, 0))
        title_width, title_height = font.size("Tamaño")
        screen.blit(title, (x_start + bar_width // 2 - title_width // 2, y_start - title_height + 99))

        for i, h in enumerate(hist):
            height = int(h / len(individuos) * max_height)
            x = x_start + i * (bar_width + 5)
            y = y_start + max_height - height
            pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width, height))

    def dibujar_grafico_vision(screen, individuos):
        bins = np.linspace(RANGO_VISION_MIN, RANGO_VISION_MAX, 10)
        hist, _ = np.histogram([f.rango_vision for f in individuos], bins=bins)
        max_height = 200
        bar_width = 30
        x_start = WIDTH - WIDTH // 3 - bar_width  # Posición inicial x del gráfico
        y_start = HEIGHT - max_height - 15  # Posición inicial y del gráfico
        title = font.render("Visión", True, (0, 0, 0))
        title_width, title_height = font.size("Visión")
        screen.blit(title, (x_start + bar_width // 2 - title_width // 2, y_start - title_height + 99))

        for i, h in enumerate(hist):
            height = int(h / len(individuos) * max_height)
            x = x_start + i * (bar_width + 5)
            y = y_start + max_height - height
            pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, height))


def generar_comida(comida):
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - generar_comida.ultima_generacion >= COMIDA_REGEN_INTERVALO:
        generar_comida.ultima_generacion = tiempo_actual
        for _ in range(NUM_COMIDA):
            comida.append(Comida())

generar_comida.ultima_generacion = 0




def main():
    # Inicializaciones
    individuos = [Individuo() for i in range(NUM_FLECHAS)]
    comida = [Comida() for _ in range(NUM_COMIDA)]
    global nuevos_individuos

    grafico_visible = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    grafico_visible = not grafico_visible

        screen.fill((255, 255, 255))

        individuos.extend(nuevos_individuos)  # Agregar nuevos individuos a la lista principal
        individuos = [i for i in individuos if i.energia > 0]
        

        for i in individuos:
            i.mover(comida)
            i.dibujar(screen)

        for c in comida:
            c.dibujar(screen)

        generar_comida(comida)

        individuos.extend(nuevos_individuos)

        nuevos_individuos = [] #Vaciamos la lista de nuevos individuos

        # Dibujar contador de flechas
        contador_text = font.render(f"Individuos Vivos: {len(individuos)}", True, (0, 0, 0))
        screen.blit(contador_text, (10, 10))

        
        if grafico_visible:
            Graficos.dibujar_grafico_velocidad(screen, individuos)
            Graficos.dibujar_grafico_tamano(screen, individuos)
            Graficos.dibujar_grafico_vision(screen, individuos)

        pygame.display.flip()
        clock.tick(60)


        if len(individuos) == 0:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
