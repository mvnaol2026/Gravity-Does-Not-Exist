"""
================================================================================
Aol Physics (Аольная Физика) - Квантовая Теория Аолодинамики (КТА)
Скрипт-симулятор: aol_gas_pressure_simulator.py
================================================================================
ПРИНЦИП: Везде, где есть масса, происходит учёт действия аольного пространства 
         — учёт аольных клиньев и давления аольного пространства.

Описание:
Моделирует замкнутый макро-объем (сосуд), заполненный пассивными LEGO-молекулами.
Пространство между молекулами заполнено плотной аольной матрицей, совершающей
перманентные высокочастотные микро-вибрации (джиттер фона). 
Масса молекулы определяет её объемную парусность (количество точек контакта).
Давление на стенки рассчитывается как сумма импульсов чисто механических ударов.
================================================================================
"""

import pygame
import random
import sys
import math

# --- Инициализация графической среды тесноты ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CTA Gas Pressure Simulator v1.0")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Courier", 18, bold=True)

# --- Физические параметры среды КТА ---
aol_jitter_amplitude = 2.0  # Температура (T) как амплитуда джиттера
aol_base_pressure = 10.0     # Базовый зажим среды
container_left = 50
container_top = 50
container_right = 500       # Изменяемая граница объема V
container_bottom = 550

# --- Класс пассивной LEGO-молекулы ---
class Molecule:
    def __init__(self, m_type):
        self.type = m_type
        if m_type == "light":
            self.mass = 4.0      # Парусность m=4
            self.radius = 6
            self.color = (100, 200, 255)
        else:
            self.mass = 16.0     # Парусность m=16
            self.radius = 12
            self.color = (255, 100, 100)
        
        # Начальные координаты внутри контейнера ущемления
        self.x = random.randint(container_left + 20, 400)
        self.y = random.randint(container_top + 20, container_bottom - 20)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

# --- Генерация ансамбля заслонок ---
molecules = [Molecule("light") for _ in range(30)] + [Molecule("heavy") for _ in range(15)]

# --- Переменные учета давления аольного пространства ---
accumulated_impulse = 0.0
calculated_pressure = 0.0
frame_counter = 0
running = True

# --- Главный физический цикл КТА (Ядро близкодействия) ---
while running:
    screen.fill((15, 20, 30))
    
    # --- Опрос интерфейса управления геометрией Малой Вселенной ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and container_right > 200:
        container_right -= 2  # Сжатие объема V
    if keys[pygame.K_RIGHT] and container_right < 550:
        container_right += 2  # Расширение объема V
    if keys[pygame.K_UP] and aol_jitter_amplitude < 10.0:
        aol_jitter_amplitude += 0.1  # Нагрев среды T (усиление джиттера)
    if keys[pygame.K_DOWN] and aol_jitter_amplitude > 0.2:
        aol_jitter_amplitude -= 0.1  # Охлаждение среды T (ослабление джиттера)

    for event in pygame.event.get_loop():
        if event.type == pygame.QUIT:
            running = False

    # --- Отрисовка стенок сосуда (Границ ущемления среды) ---
    pygame.draw.rect(screen, (0, 255, 150), (container_left, container_top, container_right - container_left, container_bottom - container_top), 3)

    # --- Расчет Аолодинамики и механического контакта ---
    for i, mol in enumerate(molecules):
        # Постулат КТА: Среда трясет пассивное тело пропорционально парусности (массе)
        # Сила "ударчиков"-квантов зависит от амплитуды хаотического джиттера
        jitter_force = aol_jitter_amplitude * math.sqrt(mol.mass)
        mol.vx += random.uniform(-1, 1) * (jitter_force / mol.mass)
        mol.vy += random.uniform(-1, 1) * (jitter_force / mol.mass)
        
        # Интеграция движения: среда вбивает аольные клинья вслед за смещением
        mol.x += mol.vx
        mol.y += mol.vy

        # Столкновения со стенками и фиксация нормального импульса давления
        if mol.x - mol.radius < container_left:
            mol.x = container_left + mol.radius
            mol.vx *= -1
            accumulated_impulse += abs(mol.vx * mol.mass)
        elif mol.x + mol.radius > container_right:
            mol.x = container_right - mol.radius
            mol.vx *= -1
            accumulated_impulse += abs(mol.vx * mol.mass)

        if mol.y - mol.radius < container_top:
            mol.y = container_top + mol.radius
            mol.vy *= -1
            accumulated_impulse += abs(mol.vy * mol.mass)
        elif mol.y + mol.radius > container_bottom:
            mol.y = container_bottom - mol.radius
            mol.vy *= -1
            accumulated_impulse += abs(mol.vy * mol.mass)

        # Парные соударения LEGO-молекул в тесноте
        for j in range(i + 1, len(molecules)):
            other = molecules[j]
            dx = other.x - mol.x
            dy = other.y - mol.y
            dist = math.hypot(dx, dy)
            min_dist = mol.radius + other.radius
            
            if dist < min_dist:
                # Геометрический зажим среды (раздвигание наложенных пазов)
                overlap = min_dist - dist
                nx = dx / (dist if dist > 0 else 1)
                ny = dy / (dist if dist > 0 else 1)
                mol.x -= nx * overlap * 0.5
                mol.y -= ny * overlap * 0.5
                other.x += nx * overlap * 0.5
                other.y += ny * overlap * 0.5
                
                # Обмен механическими "ударчиками" (импульсами)
                kx = mol.vx - other.vx
                ky = mol.vy - other.vy
                p = 2 * (kx * nx + ky * ny) / (mol.mass + other.mass)
                mol.vx -= p * other.mass * nx
                mol.vy -= p * other.mass * ny
                other.vx += p * mol.mass * nx
                other.vy += p * mol.mass * ny

        # Отрисовка пассивного тела
        pygame.draw.circle(screen, mol.color, (int(mol.x), int(mol.y)), mol.radius)

    # --- Подсчет макро-давления P по периметру за фиксированный интервал ---
    frame_counter += 1
    if frame_counter >= 30:
        container_perimeter = 2 * ((container_right - container_left) + (container_bottom - container_top))
        calculated_pressure = accumulated_impulse / (container_perimeter * 30)
        accumulated_impulse = 0.0
        frame_counter = 0

    # --- Информационная панель КТА (Вывод данных на экран) ---
    surface_area = (container_right - container_left) * (container_bottom - container_top)
    panel_x = 580
    info_texts = [
        "   АОЛОДИНАМИЧЕСКИЙ АУДИТ ГАЗА",
        "=================================",
        f"Объем сосуда (V)   : {surface_area} пкс",
        f"Джиттер среды (T)  : {aol_jitter_amplitude:.1f} (Вверх/Вниз)",
        f"Базовый зажим     : {aol_base_pressure:.1f} атм",
        "=================================",
        "МАССА как ПАРУСНОСТЬ (m):",
        "  - Легкие молекулы (m=4) : 30 шт",
        "  - Тяжелые молекулы(m=16): 15 шт",
        "=================================",
        f"ДАВЛЕНИЕ СРЕДЫ (P) : {calculated_pressure * 1000:.2f} усл. ед.",
        "=================================",
        "Управление геометрией:",
        " Стрелки [<-] [->] : Сжатие/Расширение V",
        " Стрелки [вверх] [вниз] : Изменение T"
    ]

    for idx, text in enumerate(info_texts):
        # Строгая подсветка индикатора P зеленым цветом верификации
        color = (0, 255, 150) if "P) :" in text else (200, 220, 240)
        text_surface = FONT.render(text, True, color)
        screen.blit(text_surface, (panel_x, 60 + idx * 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
