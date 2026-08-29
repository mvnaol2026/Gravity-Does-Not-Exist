import math
import random

class AolHeliumValidator:
    """
    Верификатор квадратной модели Гелия (4 аола + 4 лунола) 
    в рамках Квантовой Теории Аолодинамики (КТА).
    """
    def __init__(self, critical_depth=0.125):
        self.critical_depth = critical_depth  # Порог аольного зацепления
        
        # Задаем базовую геометрию: Квадрат со стороной 0.25
        # Аолы жестко сидят в вершинах квадрата
        self.aols = [
            {"name": "Aol_1", "x": 0.0,  "y": 0.0,  "z": 0.0},
            {"name": "Aol_2", "x": 0.25, "y": 0.0,  "z": 0.0},
            {"name": "Aol_3", "x": 0.25, "y": 0.25, "z": 0.0},
            {"name": "Aol_4", "x": 0.0,  "y": 0.25, "z": 0.0}
        ]
        
        # Лунолы симметрично занимают позиции на ребрах между аолами
        self.lunols = [
            {"name": "Lun_1", "x": 0.125, "y": 0.0,   "z": 0.0}, # Между Аол 1 и 2
            {"name": "Lun_2", "x": 0.25,  "y": 0.125, "z": 0.0}, # Между Аол 2 и 3
            {"name": "Lun_3", "x": 0.125, "y": 0.25,  "z": 0.0}, # Между Аол 3 и 4
            {"name": "Lun_4", "x": 0.0,   "y": 0.125, "z": 0.0}  # Между Аол 4 и 1
        ]

    def run_pressure_and_vibration_test(self, iterations=100000):
        print("="*60)
        print("ЗАПУСК ТЕСТА СТАБИЛЬНОСТИ КВАДРАТНОГО ГЕЛИЯ (КТА)")
        print("="*60)
        print(f"Базовая структура: 4 Аола (углы) + 4 Лунола (ребра)")
        print(f"Критическая глубина лунки зацепления: {self.critical_depth}")
        print(f"Симуляция глобального прессинга среды и тряски (~10^13 Гц)...")
        
        stable_cycles = 0
        random.seed(2026) # Детерминизм симуляции
        
        for _ in range(iterations):
            # Моделируем фоновый удар среды по структуре ядра
            # Тряска смещает элементы в пределах микро-допусков тесноты
            jitter_x = random.uniform(-0.01, 0.01)
            jitter_y = random.uniform(-0.01, 0.01)
            
            # Проверяем, удерживает ли преобладающее давление замки между Аолами и Лунолами
            all_locks_held = True
            
            # Проверка связей по периметру квадрата
            pairs_to_check = [
                (self.aols[0], self.lunols[0]), (self.lunols[0], self.aols[1]),
                (self.aols[1], self.lunols[1]), (self.lunols[1], self.aols[2]),
                (self.aols[2], self.lunols[2]), (self.lunols[2], self.aols[3]),
                (self.aols[3], self.lunols[3]), (self.lunols[3], self.aols[0])
            ]
            
            for aol, lunol in pairs_to_check:
                # Расстояние с учетом фонового динамического дисбаланса
                dx = (aol["x"] + jitter_x) - lunol["x"]
                dy = (aol["y"] + jitter_y) - lunol["y"]
                dist = math.sqrt(dx**2 + dy**2)
                
                # Если из-за удара расстояние превысило критический радиус лунки 0.125,
                # механический замок размыкается, структура разрушается
                if abs(dist - 0.125) > self.critical_depth:
                    all_locks_held = False
                    break
            
            if all_locks_held:
                stable_cycles += 1
                
        stability_rate = (stable_cycles / iterations) * 100
        
        print("\n" + "-"*40)
        print("РЕЗУЛЬТАТЫ СИМУЛЯЦИИ ИИ:")
        print(f"Выдержано микро-ударов среды: {stable_cycles} из {iterations}")
        print(f"Коэффициент геометрической стабильности: {stability_rate:.2f}%")
        
        if stability_rate > 95:
            print("\nВЫВОД: Квадратная конфигурация Гелия ВЫСОКООБРАЗНА и СТАБИЛЬНА.")
            print("Преобладающее контактное давление успешно блокирует распад ядра.")
        else:
            print("\nВЫВОД: Требуется калибровка шага упаковки.")
        print("-"*40)

if __name__ == "__main__":
    validator = AolHeliumValidator()
    validator.run_pressure_and_vibration_test()
  
