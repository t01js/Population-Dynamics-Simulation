import pygame
import random
import math

# Configuración
WIDTH, HEIGHT = 1200, 800
NUM_FLECHAS = 100
NUM_COMIDA = 100
REG_COMIDA = int(NUM_COMIDA/NUM_FLECHAS)
#GENES
ENERGIA_INICIAL = 100
ENERGIA_GASTO_MIN = 0.1
ENERGIA_GASTO_MAX = 1
VELOCIDAD_MIN = 1
VELOCIDAD_MAX = 3
RANGO_VISION_MIN = 20
RANGO_VISION_MAX = 80
TAMANO_MIN = 5
TAMANO_MAX = 10


# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación buscando comida")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Individuo:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.velocidad = random.uniform(VELOCIDAD_MIN, VELOCIDAD_MAX)
        self.tamano = random.uniform(TAMANO_MIN, TAMANO_MAX)
        self.energia = ENERGIA_INICIAL + (ENERGIA_INICIAL * self.tamano/100)
        self.energia_gasto = random.uniform(ENERGIA_GASTO_MIN, ENERGIA_GASTO_MAX)
        self.rango_vision = random.uniform(RANGO_VISION_MIN, RANGO_VISION_MAX)
        self.color = (int(self.tamano * 2.55), random.randint(0, 255), random.randint(0, 255))
        self.direccion = random.uniform(0, 2*math.pi)
        self.angulo = 0


    def mover(self, comida):
        comida_cercana = [c for c in comida if math.sqrt((c.x - self.x)**2 + (c.y - self.y)**2) <= self.rango_vision]
        if comida_cercana:
            objetivo = min(comida_cercana, key=lambda c: math.sqrt((c.x - self.x)**2 + (c.y - self.y)**2))
            dx = objetivo.x - self.x
            dy = objetivo.y - self.y
            distancia = math.sqrt(dx**2 + dy**2)
            self.direccion = math.atan2(dy, dx)
            self.x += (dx / distancia) * self.velocidad
            self.y += (dy / distancia) * self.velocidad
            self.energia -= self.velocidad * self.energia_gasto * 3 *(self.tamano/100)

            if distancia < 5:
                self.energia = ENERGIA_INICIAL
                comida.remove(objetivo)
                comida.append(Comida())
        else:
            self.direccion += random.uniform(-math.pi/32, math.pi/32)
            self.x += self.velocidad * math.cos(self.direccion)
            self.y += self.velocidad * math.sin(self.direccion)
            self.energia -= self.velocidad * self.energia_gasto * 3 *(self.tamano/100)

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

    def dibujar(self, screen):
        self.angle = math.atan2(self.velocidad, self.velocidad)*self.direccion
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

def main():
    flechas = [Individuo() for _ in range(NUM_FLECHAS)]
    comida = [Comida() for _ in range(NUM_COMIDA)]

    while (len(flechas)!=0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((255, 255, 255))

        for f in flechas:
            f.mover(comida)
            f.dibujar(screen)

        for c in comida:
            c.dibujar(screen)

        flechas = [f for f in flechas if f.energia > 0]

        # Dibujar contador de flechas
        contador_text = font.render(f"Individuos Vivos: {len(flechas)}", True, (0, 0, 0))

        screen.blit(contador_text, (10, 10))

        pygame.display.flip()
        c.dibujar(screen)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


