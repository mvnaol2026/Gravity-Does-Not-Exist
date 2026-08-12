import numpy as np

class AolAtomicConstructor:
    def __init__(self, r=1.0, h_factor=0.125, jitter_amp=0.01, medium_pressure=0.05):
        self.R = r
        self.D = 2 * r
        self.h = h_factor * self.D
        self.locked_dist = self.D - self.h  # Расстояние контакта "сфера на дне лунки Лунола"
        self.jitter_amp = jitter_amp
        self.pressure = medium_pressure
        
    def generate_initial_cloud(self, num_lunols, num_aols):
        """Создает случайное начальное облако пассивных частиц около центра масс"""
        total = num_lunols + num_aols
        positions = np.random.uniform(-self.D, self.D, size=(total, 3))
        
        # Массив типов: 0 - Лунол, 1 - сферический Аол
        types = np.array([0] * num_lunols + [1] * num_aols)
        
        # Инициализация случайных пространственных осей для выемок Лунолов
        axes = np.random.normal(size=(num_lunols, 3))
        norms = np.linalg.norm(axes, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        axes = axes / norms
        
        return positions, types, axes

    def step_simulation(self, positions, types, lunol_axes):
        """Один такт перманентного сжатия среды и джиттера"""
        num_particles = len(positions)
        new_positions = positions.copy()
        
        # 1. Воздействие Всенаправленного Движителя (Среда давит к центру масс)
        center_of_mass = np.mean(positions, axis=0)
        for i in range(num_particles):
            to_center = center_of_mass - positions[i]
            dist_to_center = np.linalg.norm(to_center)
            if dist_to_center > 0:
                new_positions[i] += (to_center / dist_to_center) * self.pressure
                
        # 2. Фоновый джиттер среды (микро-тряска матрицы вакуума)
        jitter = np.random.uniform(-self.jitter_amp, self.jitter_amp, size=(num_particles, 3))
        new_positions += jitter
        
        # 3. Разрешение геометрических контактов абсолютной твердости
        for i in range(num_particles):
            for j in range(num_particles):
                if i == j: continue
                
                vec = new_positions[i] - new_positions[j]
                dist = np.linalg.norm(vec)
                if dist == 0: continue
                dir_vec = vec / dist
                
                # Обсчет контакта через лунки Лунола 'j'
                if types[j] == 0:
                    cos_angle = np.dot(lunol_axes[j], -dir_vec)
                    in_lunka = abs(cos_angle) > 0.866 # Сектор захода ~30 градусов
                    min_d = self.locked_dist if in_lunka else self.D
                else:
                    min_d = self.D # Классический контакт сфера-сфера вне лунки Лунола
                    
                if dist < min_d:
                    # Расталкивание перекрывающихся объемов (теснота)
                    overlap = min_d - dist
                    new_positions[i] += dir_vec * (overlap * 0.5)
                    new_positions[j] -= dir_vec * (overlap * 0.5)
                    
        return new_positions

    def calculate_compactness(self, positions):
        """Мера тесноты упаковки (среднее расстояние между частицами)"""
        center = np.mean(positions, axis=0)
        return np.mean(np.linalg.norm(positions - center, axis=1))

    def search_stable_structure(self, num_lunols, num_aols, steps=500):
        """Запуск цикла утряски под давлением Вселенной"""
        pos, types, axes = self.generate_initial_cloud(num_lunols, num_aols)
        for _ in range(steps):
            pos = self.step_simulation(pos, types, axes)
        return pos, types, self.calculate_compactness(pos)

    def export_to_xyz(self, positions, types, filename):
        """Экспорт получившейся 3D-геометрии в международный формат .xyz"""
        num_particles = len(positions)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{num_particles}\n")
            f.write(f"Aol_Atomic_Constructor Framework. h_factor={self.h/self.D}\n")
            for i in range(num_particles):
                # He - Лунолы (крупные, с пазами), H - сферические Аолы (для цвета в 3D)
                p_type = "He" if types[i] == 0 else "H"
                x, y, z = positions[i]
                f.write(f"{p_type} {x:10.5f} {y:10.5f} {z:10.5f}\n")
        print(f"📦 [УСПЕХ]: 3D-координаты сохранены в файл: {filename}")


# --- ГЛАВНЫЙ ИСПОЛНИТЕЛЬНЫЙ БЛОК ---
if __name__ == "__main__":
    # Фиксируем константу глубины лунки на 1/8 (0.125)
    constructor = AolAtomicConstructor(h_factor=0.125)
    print("==================================================================")
    print("   АОЛЬНЫЙ ИИ-КОНСТРУКТОР АТОМОВ: ИССЛЕДОВАНИЕ СТЕРЕОМЕТРИИ ТЕСНОТЫ")
    print("==================================================================\n")

    # ----------------------------------------------------
    # СБОРКА 1: ГЕЛИЙ (4 Лунола, 4 Аола = 8 элементов)
    # ----------------------------------------------------
    print("Шаг 1: Запуск слепого перебора для ГЕЛИЯ (4+4)...")
    he_best_comp = float('inf')
    he_best_pos, he_best_types = None, None
    
    for attempt in range(1, 16):  # 15 попыток утряски
        pos, types, comp = constructor.search_stable_structure(num_lunols=4, num_aols=4, steps=400)
        if comp < he_best_comp:
            he_best_comp = comp
            he_best_pos = pos
            he_best_types = types
            
    print(f"-> Лучшая теснота для Гелия: {he_best_comp:.4f}")
    constructor.export_to_xyz(he_best_pos, he_best_types, filename="helium_4_4.xyz")
    print("-" * 66)

    # ----------------------------------------------------
    # СБОРКА 2: ИСТИННЫЙ ЛИТИЙ (5 Лунолов, 5 Аолов = 10 элементов)
    # ----------------------------------------------------
    print("\nШаг 2: Запуск прецизионного перебора для ИСТИННОГО ЛИТИЯ (5+5)...")
    li_best_comp = float('inf')
    li_best_pos, li_best_types = None, None
    
    for attempt in range(1, 16):  # 15 попыток утряски
        pos, types, comp = constructor.search_stable_structure(num_lunols=5, num_aols=5, steps=500)
        if comp < li_best_comp:
            li_best_comp = comp
            li_best_pos = pos
            li_best_types = types
            
    print(f"-> Лучшая теснота для Истинного Лития: {li_best_comp:.4f}")
    constructor.export_to_xyz(li_best_pos, li_best_types, filename="lithium_5_5.xyz")
    print("==================================================================")
    print(" Симуляция завершена. Файлы готовы к загрузке в 3D-визуализаторы.")
    print("==================================================================")
