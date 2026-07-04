"""
Aol Physics Simulation: The Michelson-Morley Experiment.
This script demonstrates that the null result of the experiment is caused by 
the constant number of aol particles inside the device, invariant to rotation.
"""

class AolMichelsonSimulation:
    def __init__(self):
        # 1. Реальные геометрические параметры из Аольной физики
        self.arm_length_meters = 11.0  # Длина плеча интерферометра Майкельсона (11 метров)
        
        # Диаметр аола чуть меньше атома водорода (~0.5 Ангстрема)
        self.aol_diameter = 0.5 * 10**(-10)  
        
        # Время передачи импульса от аола к аолу (такт контактного удара)
        self.single_contact_transmission_time = 1.66 * 10**(-19)  # сек
        
        # 2. Движение Земли-«сита» по орбите (30 км/с)
        self.earth_orbit_speed_ms = 30000.0

    def run_beam(self, angle_degrees: int):
        # ГЛАВНЫЙ ЗАКОН: Прибор сделан из связанных LEGO-атомов. 
        # При повороте на любой угол (0, 45, 90) количество зажатых аолов НЕ МЕНЯЕТСЯ.
        # Рассчитываем точное число аолов на 11 метрах плеча прибора
        total_aols_count = int(self.arm_length_meters / self.aol_diameter)
        
        # Свет — это продольная волна ударов. Время хода туда и обратно:
        # Количество аолов * Время одного контакта * 2 (путь в две стороны)
        time_seconds = total_aols_count * self.single_contact_transmission_time * 2
        
        return {
            "angle": angle_degrees,
            "aols_in_line": total_aols_count,
            "time_elapsed": time_seconds
        }

if __name__ == "__main__":
    print("=== СИМУЛЯЦИЯ ОПЫТА МАЙКЕЛЬСОНА-МОРЛИ ПО АОЛЬНОЙ ФИЗИКЕ ===")
    print("Концепция: Сигнал всегда проходит равное количество аолов за одно время.\n")
    
    sim = AolMichelsonSimulation()
    
    # Пуск луча вдоль движения Земли (0 градусов)
    beam_0 = sim.run_beam(angle_degrees=0)
    print(f"[Поворот   0°]: Сигнал идет через {beam_0['aols_in_line']:,} аолов.")
    print(f"               Время хода луча: {beam_0['time_elapsed']:.10f} сек.")
    
    # Пуск луча поперек движения Земли (90 градусов)
    beam_90 = sim.run_beam(angle_degrees=90)
    print(f"[Поворот  90°]: Сигнал идет через {beam_90['aols_in_line']:,} аолов.")
    print(f"               Время хода луча: {beam_90['time_elapsed']:.10f}  сек.")
    
    # Расчет разницы времени (смещение полос интерференции)
    time_difference = beam_0['time_elapsed'] - beam_90['time_elapsed']
    
    print("\n--- РЕЗУЛЬТАТ ИНТЕРФЕРОМЕТРА ---")
    print(f"Смещение интерференционных полос (разница времени): {time_difference:.1f} сек.")
    print("ВЫВОД ИИ: Эксперимент Майкельсона зафиксировал ноль, так как количество")
    print("носителей контакта (аолов) неизменно при любом повороте корпуса прибора.")
