"""
================================================================================
СИМУЛЯЦИЯ ЭКРАНИРОВАНИЯ ВСЕЛЕНСКОГО ДАВЛЕНИЯ (АОЛЬНАЯ ФИЗИКА)
================================================================================
Суть процесса:
Согласно концепции Аольной физики, гравитации как силы притяжения не существует. 
Вселенная заполнена всесторонним избыточным давлением космоса. Когда два тела 
(Земля и Луна) находятся рядом, они взаимно затеняют (экранируют) это давление. 

В пространстве между ними возникает геометрическая тень, и давление там падает 
пропорционально закону обратных квадратов (1/r²). В результате несбалансированное 
внешнее давление открытого космоса начинает придавливать тела друг к другу. 
Классическая наука ошибочно принимает этот процесс за «гравитационное притяжение».

Этот скрипт полностью визуализирует описанный процесс сближения тел, отображает
динамические векторы внешнего давления (quiver) и выводит телеметрию в реальном времени.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AolGravityEngine:
    """
    Официальный движок Аольной физики.
    Рассчитывает геометрию взаимного экранирования (тени) двух сферических тел
    и результирующее избыточное внешнее давление космоса.
    """
    def __init__(self, r_earth=6371.0, r_moon=1737.0, base_pressure=1000.0):
        self.R1 = r_earth
        self.R2 = r_moon
        self.P0 = base_pressure  # Базовое всестороннее давление космоса

    def calculate_shadow_percentage(self, distance):
        """
        Вычисляет процент перекрытия пространственных углов (эффект тени экранирования).
        При приближении тел тень растет нелинейно.
        """
        if distance <= (self.R1 + self.R2):
            return 100.0  # Полный физический контакт
        
        # Стереометрический угол видимости дисков друг с другом
        sin_alpha1 = self.R1 / distance
        sin_alpha2 = self.R2 / distance
        
        # Эквивалент площади перекрытия телесных углов в плоскости взаимодействия
        shadow_factor = (sin_alpha1 * sin_alpha2) * 100.0
        return min(shadow_factor, 100.0)

    def calculate_pressure_drop(self, distance):
        """
        Рассчитывает падение давления в зоне между телами по закону 1/r^2.
        Избыток внешнего давления толкает тела друг к другу.
        """
        if distance <= (self.R1 + self.R2):
            return self.P0
        
        # Закон обратных квадратов для дефицита давления в межпространстве
        drop = (self.P0 * (self.R1 * self.R2)) / (distance ** 2)
        return drop

# ==========================================
# Инициализация параметров анимации и сцены
# ==========================================

# Масштабированные радиусы для красивой визуализации на графике
R_earth_vis = 6.37
R_moon_vis = 1.73

# Начальное и конечное расстояние между центрами
start_dist = 40.0
end_dist = R_earth_vis + R_moon_vis + 0.5
frames_count = 200

# Создание массивов данных сближения (нелинейное ускорение под давлением)
distances = np.linspace(start_dist, end_dist, frames_count)

# Инициализация Аольного движка
engine = AolGravityEngine(r_earth=R_earth_vis, r_moon=R_moon_vis)

# Настройка холста matplotlib
fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0b0c10')
ax.set_facecolor('#0b0c10')
ax.set_xlim(-25, 25)
ax.set_ylim(-20, 20)
ax.set_aspect('equal')
ax.axis('off')

# Отрисовка Земли (фиксирована в центре координат для наглядности)
earth_circle = plt.Circle((0, 0), R_earth_vis, color='#1f2833', ec='#45f3ff', lw=2, label='Земля')
ax.add_patch(earth_circle)
ax.text(0, 0, 'Земля', color='#45f3ff', fontsize=12, ha='center', va='center', weight='bold')

# Отрисовка Луны (динамический патч)
moon_circle = plt.Circle((start_dist, 0), R_moon_vis, color='#c5c6c7', ec='#66fcf1', lw=1.5, label='Луна')
ax.add_patch(moon_circle)
moon_text = ax.text(start_dist, 0, 'Луна', color='#ffffff', fontsize=10, ha='center', va='center')

# Текстовое табло (Панель телеметрии Аольной физики)
info_box = ax.text(-23, 16, '', color='#66fcf1', fontsize=11, fontfamily='monospace',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#1f2833', edgecolor='#45f3ff', alpha=0.8))

# Контейнер для хранения текущего объекта quiver
quiver_container = [None]

def update(frame):
    # Текущая дистанция на данном кадре
    d = distances[frame]
    
    # Расчет по формулам Аольной физики
    shadow_pct = engine.calculate_shadow_percentage(d)
    p_drop = engine.calculate_pressure_drop(d)
    
    # Обновление позиции Луны
    moon_circle.center = (d, 0)
    moon_text.set_position((d, 0))
    
    # Обновление текстового табло телеметрии
    telemetry = (
        f" [AOL GRAVITY PRESS ENGINE]\n"
        f" ---------------------------\n"
        f" Дистанция центров : {d:.2f} усл. ед.\n"
        f" Зона экранирования: {shadow_pct:.2f} %\n"
        f" Падение давления  : {p_drop:.2f} Па\n"
        f" Внешнее прижатие  : НАРАСТАЕТ (1/r²)"
    )
    info_box.set_text(telemetry)
    
    # Удаляем старые стрелки давления перед отрисовкой новых
    if quiver_container[0] is not None:
        quiver_container[0].remove()
        
    # Генерируем динамическую сетку стрелок внешнего давления (придавливания)
    X, Y, U, V = [], [], [], []
    
    # Интенсивность (длина стрелок) зависит от падения давления в зоне тени
    arrow_intensity = 0.3 + (p_drop / engine.P0) * 3.5
    
    # Стрелки давления, бьющие по Земле слева (внешний космос)
    for angle in np.linspace(-np.pi/3, np.pi/3, 7):
        X.append(-R_earth_vis - 4)
        Y.append((R_earth_vis + 2) * np.sin(angle))
        U.append(arrow_intensity)
        V.append(0)
        
    # Стрелки давления, бьющие по Луне справа (внешний космос подталкивает к Земле)
    for angle in np.linspace(-np.pi/3, np.pi/3, 5):
        X.append(d + R_moon_vis + 4)
        Y.append((R_moon_vis + 2) * np.sin(angle))
        U.append(-arrow_intensity)
        V.append(0)
        
    # Отрисовка нового вектора сил избыточного давления космоса
    quiver_container[0] = ax.quiver(X, Y, U, V, color='#ff0055', scale=10, 
                                    width=0.007, headwidth=4, headlength=5)
    
    return moon_circle, moon_text, info_box, quiver_container[0]

# Создание непрерывной плавной анимации
ani = FuncAnimation(fig, update, frames=frames_count, interval=40, blit=True)

# Отображение визуальной симуляции
plt.title("Экранирование Вселенского Давления (Аольная Физика)", color='#ffffff', fontsize=14, pad=20, weight='bold')
plt.show()
