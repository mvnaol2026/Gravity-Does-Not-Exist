"""
Aol Physics Mechanics Engine (Based on Thesis 16 & The Fundamental Law of Motion).
This simulation models inertia and motion strictly as a consequence of continuous, 
unbalanced contact pressure from the aol medium, completely eliminating abstract kinetic energy.
"""
 
class AolUniverseEngine:
    def __init__(self, external_force_regulator: float, body_length: float, body_density: int):
        # 1. Свойства аольной среды (Тезисы 4, 5, 6)
        self.aol_diameter = 1.0          # Толщина клина всегда равна диаметру аола
        self.medium_pressure = 1500.0     # Базовое всеобъемлющее давление среды
        self.vibration_frequency = 10**13 # Фоновая микровибрация среды (Гц)
        
        # 2. Параметры пассивного тела (Тезис 3: материя пассивна, "всегда никакая")
        self.body_length = body_length
        self.body_density = body_density  # Количество связанных частиц ("густота сита")
        self.position_x = 0.0
        self.speed = 0.0
        
        # 3. Внешний регулятор процесса
        self.external_regulator = external_force_regulator

    def process_time_step(self, dt: float) -> str:
        # --- СТАДИЯ ПОКОЯ И НАЧАЛА ДВИЖЕНИЯ ---
        if self.speed == 0.0:
            if self.external_regulator > 0:
                # Внешняя сила преодолевает сопротивление среды перед "ситом" и задает стартовый темп
                self.speed = self.external_regulator * self.aol_diameter * 0.5
                return (f"[СТАРТ]: Внешний регулятор ({self.external_regulator}) нарушил равновесие. "
                        f"Запущен первый цикл вколачивания клиньев. Скорость: {self.speed:.2f}")
            else:
                return "[ПОКОЙ]: Тело в полном равновесии. Со всех сторон одинаковое вибрационное давление."

        # --- СТАДИЯ ДВИЖЕНИЯ ПО ИНЕРЦИИ (РЕАЛЬНЫЙ МЕХАНИЗМ КЛИНЬЕВ) ---
        # Геометрическое число клиньев (слоев) определяется длиной тела и его скоростью
        wedge_layers = self.body_length * self.speed
        
        # Плотность клина (число аолов в слое) зависит от густоты "сита" атомов тела
        aols_in_layer = self.body_density / self.body_length
        
        # Сила давления одного дискретного акта (вбивания клина за атомом)
        single_wedge_pressure = aols_in_layer * self.medium_pressure
        
        # Суммарная растущая сила аольных клиньев за единицу времени
        total_wedge_force = wedge_layers * single_wedge_pressure
        
        # --- ГЛАВНЫЙ ЗАКОН ФИЗИКИ В ДЕЙСТВИИ ---
        # Движение возможно ТОЛЬКО при контактном, неуравновешенном, непрерывном давлении!
        # Смещение происходит строго на суммарную толщину вбитых сзади клиньев
        delta_x = total_wedge_force * self.aol_diameter * dt
        self.position_x += delta_x
        
        # Скорость меняется, так как среда из-за роста частоты актов работает всё интенсивнее
        previous_speed = self.speed
        self.speed += (total_wedge_force * 0.001) * dt
        acceleration = (self.speed - previous_speed) / dt

        return (f"Позиция X: {self.position_x:.2f} | Скорость: {self.speed:.2f} | "
                f"Сила клиньев среды сзади: {total_wedge_force:.1f} | Ускорение: {acceleration:.2f}")

    def check_single_aol_inertia(self) -> str:
        """Проверка парадокса: почему сами аолы не имеют инерции."""
        geometric_loss_in_hollow = 0.21 # Аол проседает во впадину, теряя ~21% дистанции хода
        effective_stroke = self.aol_diameter * (1.0 - geometric_loss_in_hollow)
        
        if effective_stroke < self.aol_diameter:
            # Геометрический запрет: зазор меньше диаметра аола, клин сзади физически не помещается
            return (f"[АОЛ]: Одиночный аол просел во впадину упаковки. Ход {effective_stroke:.2f} < {self.aol_diameter}. "
                    f"Клин не сформирован. Инерция = 0. Передал импульс волновым колебанием и остался вибрировать.")

if __name__ == "__main__":
    print("=== ЗАПУСК ЦИФРОВОЙ МОДЕЛИ АОЛЬНОЙ ФИЗИКИ (ГЛАВА: ИНЕРЦИЯ) ===")
    
    # Моделируем массивное тело (длина 5, густота атомов 1000) под действием силы-регулятора 10.0
    universe = AolUniverseEngine(external_force_regulator=10.0, body_length=5.0, body_density=1000)
    
    # Наблюдаем за пошаговым непрерывным давлением среды в течение 4 секунд
    for second in range(5):
        print(f"[Секунда {second}]: {universe.process_time_step(dt=1.0)}")
        
    print("\n=== ПРОВЕРКА ФУНДАМЕНТА СРЕДЫ ===")
    print(universe.check_single_aol_inertia())
