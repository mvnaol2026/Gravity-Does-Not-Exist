import math

class AolGravityEngine:
    """
    Математическая симуляция Всенаправленного Вибрационного Придавливания (Глава 20).
    Формализует близкодействующий механизм гравитации в Аольной Физике:
    1. Пространство заполнено стационарной средой аолов, вибрирующих с частотой 10^13 Гц.
    2. Тела выступают как пространственные фильтры (сита), частично экранирующие вибрации.
    3. Сила прижима убывает как 1/r^2 из-за геометрии площадей заслонок на сфере пространства.
    4. Инертная масса (объем парусности вытеснения) строго равна гравитационной массе.
    """
    def __init__(self, base_frequency=1e13, background_pressure=100.0):
        # Базовая частота микровибраций среды Вселенной (Гц)
        self.freq = base_frequency 
        # Базовое изотропное (всестороннее) давление среды на покоящееся изолированное тело (%)
        self.bg_pressure = background_pressure 

    def calculate_body_properties(self, total_elements, volume_displacement):
        """
        Тезис №15: Масса — это объемная аольная парусность тела.
        Зависит от количества связанных аолов/лунолов в LEGO-структуре.
        """
        # Инертная масса определяется мерой вытеснения среды (парусностью структуры)
        m_inertial = volume_displacement
        # Гравитационная масса — мера способности структуры задерживать/фильтровать вибрации
        # Коэффициент прозрачности "сита" атомов (чем больше элементов, тем сильнее тень экранирования)
        shielding_cross_section = total_elements * 1.5e-15 
        return m_inertial, shielding_cross_section

    def simulate_press_interaction(self, body1_data, body2_data, distance):
        """
        Механизм прижимания за счет разности давлений в зоне геометрической тени.
        Выводит закон 1/r^2 из чистой стереометрии трехмерного пространства.
        """
        m_inert_1, shield_1 = body1_data
        m_inert_2, shield_2 = body2_data

        if distance <= 0:
            raise ValueError("Дистанция между телами должна быть больше нуля.")

        # Площадь воображаемой сферы взаимодействия на дистанции r (S = 4 * pi * r^2)
        sphere_area = 4 * math.pi * (distance ** 2)

        # Тело-заслонка имеет фиксированный размер. Доля экранируемой площади на сфере падает как 1/r^2.
        # Тело 1 затеняет вибрации для Тела 2, Тело 2 затеняет для Тела 1.
        geometric_shadow_1_to_2 = shield_1 / sphere_area
        geometric_shadow_2_to_1 = shield_2 / sphere_area

        # Из-за экранирования всепроникающих вибраций, давление среды в промежутке между телами падает
        inner_pressure_on_body1 = self.bg_pressure * (1.0 - geometric_shadow_2_to_1)
        inner_pressure_on_body2 = self.bg_pressure * (1.0 - geometric_shadow_1_to_2)

        # С внешних (открытых Вселенной) сторон давление остается максимальным (bg_pressure)
        # Возникает неуравновешенный градиент давлений (разность сил)
        delta_p_body1 = self.bg_pressure - inner_pressure_on_body1
        delta_p_body2 = self.bg_pressure - inner_pressure_on_body2

        # Результирующая механическая сила внешнего придавливания открытым космосом (в условных Ньютонах)
        # Сила прямо пропорциональна гравитационной массе (способности экранировать) и обратно пропорциональна r^2
        force_press_1 = delta_p_body1 * m_inert_1
        force_press_2 = delta_p_body2 * m_inert_2

        # Согласно Третьему закону Ньютона (действию контактных сил), силы прижима взаимны
        total_pressing_force = (force_press_1 + force_press_2) / 2.0

        return {
            "dist": distance,
            "area": sphere_area,
            "shadow_1_on_2_pct": geometric_shadow_1_to_2 * 100,
            "inner_p1": inner_pressure_on_body1,
            "inner_p2": inner_pressure_on_body2,
            "f_press": total_pressing_force
        }

# --- Демонстрационный запуск симуляции ---
if __name__ == "__main__":
    engine = AolGravityEngine()

    # Задаем параметры Тела 1 (например, условная Земля) и Тела 2 (условная Луна)
    # Структура связанных элементов определяет массу вытеснения (парусность)
    earth_properties = engine.calculate_body_properties(total_elements=6e24, volume_displacement=5.97)
    moon_properties = engine.calculate_body_properties(total_elements=7e22, volume_displacement=0.073)

    print("=== СИМУЛЯЦИЯ АОЛЬНОГО ВИБРАЦИОННОГО ПРИДАВЛИВАНИЯ ===")
    print(f"Базовая частота среды Вселенной: {engine.freq:.0e} Гц")
    print(f"Инертная масса Земли (парусность вытеснения): {earth_properties[0]}")
    print(f"Инертная масса Луны (парусность вытеснения): {moon_properties[0]}\n")

    # Проверяем изменение силы прижима на разных расстояниях (r, 2r, 3r), чтобы доказать закон 1/r^2
    distances = [10.0, 20.0, 40.0]
    
    for r in distances:
        res = engine.simulate_press_interaction(earth_properties, moon_properties, distance=r)
        print(f"Дистанция между телами: {res['dist']} уед.")
        print(f" -> Площадь сферы распределения вибраций (4*pi*r^2): {res['area']:.2f} кв.уед.")
        print(f" -> Доля неба Земли, экранированная заслонкой Луны: {res['shadow_1_on_2_pct']:.6f}%")
        print(f" -> Давление среды в зоне тени между телами: {res['inner_p1']:.5f}% (вместо 100.0%)")
        print(f" -> РЕЗУЛЬТИРУЮЩАЯ СИЛА ВНЕШНЕГО ПРИЖИМАНИЯ: {res['f_press']:.6f} уед.")
        print("-" * 60)
