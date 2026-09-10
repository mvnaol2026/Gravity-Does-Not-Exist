import numpy as np

class AolSpaceSimulation:
    def __init__(self):
        # Базовые константы КТА (Квантовой Теории Аолодинамики)
        self.freq_hz = 1e13       # Базовая частота вибро-зажима среды (10^13 Гц)
        self.c_speed = 299792458  # Скорость упругой волны в аольной матрице (скорость света)
        self.p_background = 1.0   # Изотропное фоновое давление упругой среды Аолов
        
        # Параметры системы (Звезда и Планета)
        self.star_aperture = 5.0  # Парусность (экранирующая способность) ядра Звезды
        self.planet_aperture = 0.1 # Парусность (экран) Планеты
        self.planet_mass = 1.0     # Масса планеты (сопротивление среды смещению)
        
        # Начальный кинематический статус планеты (Декартовы координаты)
        self.pos = np.array([150.0, 0.0, 0.0])  # Дистанция от центра Звезды (R)
        self.vel = np.array([0.0, 1.8, 0.0])    # Вектор тангенциальной скорости
        
    def calculate_gravity_press(self):
        """
        УЗЕЛ 1: Расчет гравитационного прижима через затенение (экранирование).
        Выводит закон обратных квадратов (1/r^2) чисто из стереометрии тени.
        """
        r_vector = -self.pos # Вектор направлен к центру Звезды
        distance = np.linalg.norm(r_vector)
        direction = r_vector / distance
        
        # Площадь геометрической тени падает строго пропорционально площади сферы 4*pi*r^2
        shadow_area = (self.star_aperture * self.planet_aperture) / (4 * np.pi * (distance**2))
        
        # Сила прижима — это нескомпенсированный остаток внешнего давления среды
        f_press = direction * (self.p_background * shadow_area * self.freq_hz * 1e-15)
        return f_press
        
    def calculate_aol_wedge_inertia(self):
        """
        УЗЕЛ 2: Расчет движения по инерции через гидродинамический подталкивающий клин.
        Среда создает избыточное давление сзади движущегося тела, компенсируя лобовое сопротивление.
        """
        speed = np.linalg.norm(self.vel)
        if speed == 0:
            return np.array([0.0, 0.0, 0.0])
        
        direction = self.vel / speed
        
        # Механический клин: упругий импульс восстановления среды позади Аолов тела
        # Зависит от соотношения скорости тела к скорости упругой волны матрицы (c_speed)
        wedge_efficiency = 1.0 / (1.0 - (speed / self.c_speed))
        
        # Сила инерции — это автоколебательное подталкивание средой вдоль вектора хода
        f_inertia = direction * (self.planet_aperture * self.p_background * wedge_efficiency * 1e-3)
        
        # Лобовое гидродинамическое сопротивление тупой материи
        f_drag = -direction * (self.planet_aperture * self.p_background * speed * 1e-3)
        
        # Векторный баланс инерции в КТА
        return f_inertia + f_drag

    def update_orbit(self, dt=0.1):
        """
        УЗЕЛ 3: Сквозной итератор декартовой траектории планеты.
        """
        # Сборка сил, действующих на пассивный LEGO-каркас планеты
        f_gravity = self.calculate_gravity_press()
        f_inertia_balance = self.calculate_aol_wedge_inertia()
        
        f_total = f_gravity + f_inertia_balance
        
        # Изменение координат по закону прямого контактного давления
        acceleration = f_total / self.planet_mass
        self.vel += acceleration * dt
        self.pos += self.vel * dt
        
        return self.pos, self.vel

# Запуск верификационного теста орбитального движка КТА
if __name__ == "__main__":
    sim = AolSpaceSimulation()
    print("СТАРТ СИМУЛЯЦИИ ОРБИТЫ КТА (Aolodynamics Core Engine)")
    print(f"Начальная позиция Планеты: {sim.pos}")
    print(f"Частота вибро-пресса Вселенной: {sim.freq_hz} Гц\n")
    
    # Расчет первых 5 витков/шагов для проверки стабильности декартова шага
    for step in range(1, 6):
        pos, vel = sim.update_orbit(dt=1.0)
        dist = np.linalg.norm(pos)
        print(f"Шаг {step}: Координаты = [{pos[0]:.2f}, {pos[1]:.2f}], Дистанция до Звезды = {dist:.2f}, Скорость = {np.linalg.norm(vel):.4f}")
