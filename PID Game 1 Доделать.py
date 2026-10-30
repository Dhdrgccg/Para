import tkinter as tk
import random


class PIDController:
    def __init__(self, kp, ki, kd, dt=0.02):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        
        self.integral = 0
        self.prev_error = 0

# =====================================================================
# Формулы для расчета движения
# =====================================================================

    def compute(self, setpoint, current_value):
        # =====================================================================
        # Задание: Реализуйте алгоритм ПИД-регулятора.
        # Входные данные:
        #   setpoint - целевое значение (куда хотим прилететь)
        #   current_value - текущее положение дрона
        #
        # Полезные переменные класса, которые нужно использовать и обновлять:
        #   self.kp, self.ki, self.kd - коэффициенты регулятора
        #   self.dt - шаг времени (дельта t)
        #   self.integral - накопленная интегральная ошибка (для I-составляющей)
        #   self.prev_error - ошибка с прошлого шага (для D-составляющей)
        # =====================================================================
        
        # Шаг 1. Вычислите текущую ошибку (рассогласование)
        error = 0 
        
        # Шаг 2. Вычислите интегральную часть
        # Подсказка: добавьте к self.integral текущую ошибку, умноженную на dt.
        # Чтобы дрон не улетал в космос, ограничьте self.integral в диапазоне от -100 до 100
        # (Используйте функции min() и max() или конструкцию if)
        
        
        # Шаг 3. Вычислите дифференциальную часть (скорость изменения ошибки)
        # Подсказка: (текущая ошибка - прошлая ошибка) разделить на dt
        derivative = 0
        
        # Шаг 4. Посчитайте итоговый выход (output) по формуле ПИД-регулятора
        output = 0
        
        # Шаг 5. Сохраните текущую ошибку в self.prev_error для следующего шага симуляции
        
        
        return output

# =====================================================================
# ДВИЖОК ИГРЫ (Не меняем)
# =====================================================================
class DroneGame:
    def __init__(self, root):
        self.root = root
        self.root.title("PID Drone Survival Game")
        
        self.canvas = tk.Canvas(root, width=400, height=500, bg="#222")
        self.canvas.pack()
        
        # Физические параметры среды
        self.drone_y = 400.0  # Стартовая позиция дрона
        self.velocity = 0.0
        self.gravity = 9.8
        self.wind_force = 0.0
        self.dt = 0.02
        
        # Целевая высота (Уставка)
        self.setpoint = 250.0
        
        # (Изначально стоят плохие настройки, дрон упадет)
        self.pid = PIDController(kp=0.5, ki=0.0, kd=0.0, dt=self.dt)
        
        self.create_ui()
        self.draw_elements()
        self.game_loop()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()
        
        tk.Label(frame, text="Kp:").grid(row=0, column=0)
        self.kp_entry = tk.Entry(frame, width=5)
        self.kp_entry.insert(0, str(self.pid.kp))
        self.kp_entry.grid(row=0, column=1)
        
        tk.Label(frame, text="Ki:").grid(row=0, column=2)
        self.ki_entry = tk.Entry(frame, width=5)
        self.ki_entry.insert(0, str(self.pid.ki))
        self.ki_entry.grid(row=0, column=3)
        
        tk.Label(frame, text="Kd:").grid(row=0, column=4)
        self.kd_entry = tk.Entry(frame, width=5)
        self.kd_entry.insert(0, str(self.pid.kd))
        self.kd_entry.grid(row=0, column=5)
        
        btn = tk.Button(frame, text="Применить и Сброс", command=self.reset_game)
        btn.grid(row=0, column=6, padx=5)

    def draw_elements(self):
        # Линия уставки (куда надо прилететь)
        self.canvas.create_line(0, self.setpoint, 400, self.setpoint, fill="green", dash=(4, 4), tags="setpoint")
        # Опасные зоны
        self.canvas.create_rectangle(0, 0, 400, 30, fill="red", tags="danger")
        self.canvas.create_rectangle(0, 470, 400, 500, fill="red", tags="danger")
        # Дрон
        self.drone_sprite = self.canvas.create_rectangle(180, self.drone_y-10, 220, self.drone_y+10, fill="cyan")
        # Текст статуса
        self.status_text = self.canvas.create_text(200, 50, text="Стабилизация...", fill="white", font=("Arial", 14))

    def reset_game(self):
        try:
            self.pid.kp = float(self.kp_entry.get())
            self.pid.ki = float(self.ki_entry.get())
            self.pid.kd = float(self.kd_entry.get())
        except ValueError:
            pass
        self.pid.integral = 0
        self.pid.prev_error = 0
        self.drone_y = 400.0
        self.velocity = 0.0
        self.canvas.itemconfig(self.status_text, text="Стабилизация...", fill="white")
        self.canvas.itemconfig(self.drone_sprite, fill="cyan")

    def game_loop(self):
        # 1. Симулируем случайные порывы ветра (возмущение системы)
        if random.random() < 0.1:
            self.wind_force = random.uniform(-15, 15)
            
        # 2. Вызываем  ПИД-регулятор
        # В физике tkinter Y идет сверху вниз, поэтому инвертируем значения для логики высоты
        current_height = 500.0 - self.drone_y
        target_height = 500.0 - self.setpoint
        
        thrust = self.pid.compute(target_height, current_height)
        
        # Ограничение тяги моторов (физический предел)
        thrust = max(-20, min(40, thrust)) 
        
        # 3. Физика движения (Ускорение -> Скорость -> Координата)
        total_acceleration = (thrust - self.gravity) + self.wind_force
        self.velocity += total_acceleration * self.dt
        self.drone_y -= self.velocity * self.dt  # Минус, так как Y идет вниз
        
        # Обновляем графику дрона
        self.canvas.coords(self.drone_sprite, 180, self.drone_y-10, 220, self.drone_y+10)
        
        # 4. Проверка условий проигрыша / победы
        if self.drone_y <= 30 or self.drone_y >= 470:
            self.canvas.itemconfig(self.status_text, text="ДРОН РАЗБИЛСЯ!", fill="red")
            self.canvas.itemconfig(self.drone_sprite, fill="red")
        else:
            # Если держится около зеленой линии — всё хорошо
            if abs(self.drone_y - self.setpoint) < 10:
                self.canvas.itemconfig(self.status_text, text="Полет стабильный", fill="lightgreen")
            self.root.after(20, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = DroneGame(root)
    root.mainloop()