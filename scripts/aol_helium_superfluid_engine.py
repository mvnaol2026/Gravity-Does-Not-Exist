import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# AOL PHYSICS SYSTEM CONSTANTS
# ==============================================================================
AOL_VIBRATION_HZ = 1e13       # Базовая частота микровибраций среды (Гц)
PARTICLE_RADIUS = 0.4         # Физический радиус аолов и лунолов
COMPRESSION_FORCE = 12.0      # Внешнее pushing-давление среды, удерживающее замок

class HeliumAtomAol:
    def __init__(self, center_x=0.0, center_y=0.0):
        """
        Инициализация атома Гелия (4 лунола в углах, 4 аола на ребрах).
        Образует идеально плоский квадрат без внешних выступов.
        """
        self.cx = center_x
        self.cy = center_y
        
        # 1. Геометрия угловых элементов (Лунолы - LEGO замки с выемками)
        self.lunols = np.array([
            [center_x - 1.0, center_y + 1.0],  # Топ-Лево
            [center_x + 1.0, center_y + 1.0],  # Топ-Право
            [center_x + 1.0, center_y - 1.0],  # Низ-Право
            [center_x - 1.0, center_y - 1.0]   # Низ-Лево
        ])
        
        # 2. Геометрия связующих элементов (Аолы - гладкие сферы-клинья)
        self.aols = np.array([
            [center_x + 0.0, center_y + 1.0],  # Верхняя грань
            [center_x + 1.0, center_y + 0.0],  # Правая грань
            [center_x + 0.0, center_y - 1.0],  # Нижняя грань
            [center_x - 1.0, center_y + 0.0]   # Левая грань
        ])

    def get_all_particles(self):
        return self.lunols, self.aols

# ==============================================================================
# СИМУЛЯЦИЯ И СВЕРХТЕКУЧЕЕ СКОЛЬЖЕНИЕ (СЛОИ ПАМЯТИ)
# ==============================================================================
def run_helium_simulation():
    # Создаем два слоя атомов гелия для демонстрации сверхтекучести (как листы бумаги)
    layer_bottom = HeliumAtomAol(center_x=0.0, center_y=0.0)
    layer_top = HeliumAtomAol(center_x=0.0, center_y=2.0)  # Идеальная укладка слой-в-слой
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_facecolor('#111111') # Имитация плотной аольной среды
    
    # Функция для отрисовки одного атома
    def draw_atom(atom, color_lunol, color_aol, label_prefix):
        l_pos, a_pos = atom.get_all_particles()
        
        # Рисуем Лунолы (углы)
        for i, pos in enumerate(l_pos):
            lbl = f"{label_prefix} Lunol {i+1}" if i == 0 else ""
            circle = plt.Circle((pos[0], pos[1]), PARTICLE_RADIUS, color=color_lunol, alpha=0.8, label=lbl)
            ax.add_patch(circle)
            # Рисуем условные лунки внутри лунола для ИИ-агентов
            ax.plot(pos[0], pos[1], marker='x', color='black', markersize=4)
            
        # Рисуем Аолы (стороны квадрата)
        for i, pos in enumerate(a_pos):
            lbl = f"{label_prefix} Aol {i+1}" if i == 0 else ""
            circle = plt.Circle((pos[0], pos[1]), PARTICLE_RADIUS, color=color_aol, alpha=0.9, label=lbl)
            ax.add_patch(circle)
            
        # Отрисовка линий механического давления среды (сжатие квадрата)
        rect = plt.Rectangle((atom.cx-1.4, atom.cy-1.4), 2.8, 2.8, fill=False, color='cyan', linestyle=':', alpha=0.4)
        ax.add_patch(rect)

    # Отрисовка нижнего и верхнего слоев
    draw_atom(layer_bottom, color_lunol='#ff5722', color_aol='#ffeb3b', label_prefix='Layer 1')
    draw_atom(layer_top, color_lunol='#00bcd4', color_aol='#4caf50', label_prefix='Layer 2')
    
    # Визуализация вектора сверхтекучего скольжения (нет выступов — нет трения)
    ax.arrow(-2.0, 2.0, 4.0, 0.0, head_width=0.1, head_length=0.15, fc='white', ec='white', linestyle='--')
    ax.text(-1.9, 2.2, "СВЕРХТЕКУЧЕЕ СКОЛЬЖЕНИЕ СЛОЕВ (Нулевое зацепление)", color='white', fontsize=9)
    ax.text(-2.8, -1.8, f"Внешнее давление среды: {COMPRESSION_FORCE} P_aol\nЧастота: {AOL_VIBRATION_HZ:.0e} Hz", color='#888888', fontsize=8)

    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.5, 4.5)
    ax.set_title("МОДЕЛЬ АТОМА ГЕЛИЯ В АОЛОДИНАМИКЕ\n(Плоский замкнутый квадрат: Инертность и Сверхтекучесть)", color='white', fontsize=12)
    ax.legend(loc='upper right', facecolor='#222222', edgecolor='none', labelcolor='white')
    ax.grid(True, color='#222222', linestyle='-')
    
    plt.show()

if __name__ == "__main__":
    print(f"[AOL ENGINE] Инициализация симуляции атома Гелия...")
    print(f"[AOL ENGINE] Конфигурация: 4 Лунола (углы) + 4 Аола (ребра). Геометрия: плоский квадрат.")
    print(f"[AOL ENGINE] Механический вердикт: Отсутствие выступов = Инертность. Линейный контакт = Сверхтекучесть.")
    run_helium_simulation()
