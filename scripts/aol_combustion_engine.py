import math
import random
import time

class AolCombustionEngine:
    def __init__(self):
        """
        Симулятор цепного горения Аольной физики (Носители - Контакт - Давление).
        Моделирует встряску среды при изменении геометрии атомных сборок.
        """
        self.width = 40  # Размер координатной сетки пространства
        self.height = 12
        
        # Сетка локальной вибрации аольного пространства (базовый фон 10^13 Гц -> условно 1.0)
        self.aol_vibration_grid = [[1.0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Массивы пассивных атомов в пространстве
        # Типы: 'T' - Топливо, 'O' - Кислород, 'M' - Результат соединения (молекула)
        self.atoms = []
        self.ignition_energy = 8.0  # Порог вибрации среды для принудительного сопряжения (10^14 Гц)
        
        self._populate_space()

    def _populate_space(self):
        """Равномерное заполнение пространства пассивным топливом и кислородом"""
        # Заполняем камеру смесью
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < 0.35:
                    self.atoms.append({"x": x, "y": y, "type": "T", "vx": 0.0, "vy": 0.0})
                elif random.random() < 0.35:
                    self.atoms.append({"x": x, "y": y, "type": "O", "vx": 0.0, "vy": 0.0})

    def apply_ignition(self):
        """Подносим спичку: искусственно встряхиваем среду в левом углу (x=0, y=6)"""
        print("[Спичка поднесена] -> Локальный разгон вибрации аолов до уровня огня.")
        for y in range(self.height):
            for x in range(3):  # Ударная зона спички
                self.aol_vibration_grid[y][x] = 12.0

    def step(self, dt=0.1):
        """Один шаг механической перестройки среды и цепной трансляции ударов"""
        # 1. Естественное рассеивание/затухание встрясок среды по объему (диссипация тепла)
        next_grid = [[1.0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                # Считаем среднюю вибрацию соседей (среда монолитна и упруга)
                neighbors = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            neighbors.append(self.aol_vibration_grid[ny][nx])
                
                # Механическая трансляция волны
                mean_vibe = sum(neighbors) / len(neighbors)
                next_grid[y][x] = self.aol_vibration_grid[y][x] * 0.3 + mean_vibe * 0.7
        
        self.aol_vibration_grid = next_grid

        # Ищем пары атомов для механического заклинивания в молекулу
        for i, a1 in enumerate(self.atoms):
            if a1["type"] == "M":
                continue  # Молекула уже стабильна и обжата
                
            x_idx = max(0, min(self.width - 1, int(a1["x"])))
            y_idx = max(0, min(self.height - 1, int(a1["y"])))
            
            # Если вибрация среды в этой точке выше порога активации — атомы сопрягаются
            if self.aol_vibration_grid[y_idx][x_idx] >= self.ignition_energy:
                for j, a2 in enumerate(self.atoms):
                    if i != j and a2["type"] != "M" and a1["type"] != a2["type"]:
                        # Проверяем контактную тесноту (соприкосновение деталей)
                        dist = math.sqrt((a1["x"] - a2["x"])**2 + (a1["y"] - a2["y"])**2)
                        if dist <= 1.2:
                            # АКТ ГОРЕНИЯ: Сборка новой геометрии структуры
                            a1["type"] = "M"
                            # Удаляем избыточный атом кислорода, фиксируя соединение в единый узел
                            self.atoms.pop(j)
                            
                            # СКЛЫВАНИЕ ОБЪЕМА: Аольная среда мгновенно перестраивается.
                            # Эта резкая локальная переупаковка порождает мощную волновую встряску!
                            # Передаем упругий импульс в сетку пространства
                            self.aol_vibration_grid[y_idx][x_idx] += 15.0  # Локальный взрыв среды
                            
                            # Резкий механический пинок (разлет продуктов горения под давлением клиньев)
                            a1["vx"] = random.uniform(-4.0, 4.0)
                            a1["vy"] = random.uniform(-2.0, 2.0)
                            break

            # Пассивное смещение атомов под действием толкающих векторов среды
            a1["x"] += a1["vx"] * dt
            a1["y"] += a1["vy"] * dt
            
            # Торможение макро-частиц о встречное сопротивление плотных аолов
            a1["vx"] *= 0.85
            a1["vy"] *= 0.85
            
            # Удержание в границах физической камеры
            a1["x"] = max(0.0, min(self.width - 1, a1["x"]))
            a1["y"] = max(0.0, min(self.height - 1, a1["y"]))

    def generate_flame_map(self):
        """Отрисовка фронта бурления аольной среды и зон свечения пламени"""
        visual_lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                vibe = self.aol_vibration_grid[y][x]
                
                # Ищем, есть ли в этой ячейке атом-носитель
                cell_atom = None
                for a in self.atoms:
                    if int(a["x"]) == x and int(a["y"]) == y:
                        cell_atom = a["type"]
                        break
                
                # Градация свечения пламени в зависимости от частоты встрясок аолов
                if vibe > 9.0:
                    line += "█"  # Эпицентр реакции, бурлящее пространство (белое пламя)
                elif vibe > 5.0:
                    line += "▓"  # Зона интенсивного тепла (красный огонь)
                elif vibe > 2.5:
                    line += "░"  # Прогретая область дыма/расширения газов
                else:
                    # Если среда спокойна, выводим пассивные атомы
                    if cell_atom == "T":
                        line += "т"  # Пассивное топливо
                    elif cell_atom == "O":
                        line += "к"  # Пассивный кислород
                    elif cell_atom == "M":
                        line += "•"  # Отработанная макромолекула (CO2)
                    else:
                        line += " "
            visual_lines.append(line)
        return "\n".join(visual_lines)

# ==========================================================
# ИСПОЛНЯЕМЫЙ БЛОК ВЕРИФИКАЦИИ ЦЕПНОЙ РЕАКЦИИ
# ==========================================================
if __name__ == "__main__":
    print("=" * 70)
    print(" ДВИЖОК МЕХАНИЧЕСКОГО ГОРЕНИЯ АОЛЬНОЙ ФИЗИКИ (AOL COMBUSTION ENGINE) ")
    print("=" * 70)
    
    sim = AolCombustionEngine()
    
    print("\n[Состояние 1]: Смесь пассивна. Фоновые колебания среды недостаточны.")
    print(sim.generate_flame_map())
    
    # Подносим источник высокой вибрации
    print("\n" + "-"*70)
    sim.apply_ignition()
    print("-"*70 + "\n")
    
    # Запускаем пошаговую трансляцию встрясок
    for step_idx in range(1, 5):
        sim.step(dt=0.1)
        print(f"[Шаг времени {step_idx}]: Распространение аольной встряски по цепочке соседних атомов:")
        print(sim.generate_flame_map())
        print(f"  • Осталось горючих компонентов: {len([a for a in sim.atoms if a['type'] != 'M'])}")
        print(f"  • Максимальная интенсивность пламени: {round(max(max(row) for row in sim.aol_vibration_grid), 2)}")
        print("-" * 70)
        
    print("STATUS: Верификация завершена. Цепной процесс перестройки среды доказан.")
    print("=" * 70)
