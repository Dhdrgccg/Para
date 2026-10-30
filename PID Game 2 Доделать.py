import tkinter as tk
import random
import math

class PIDController:
    def __init__(self, kp, ki, kd, dt=0.02):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        
        self.integral = 0
        self.prev_error = 0


#Добавим динамическое движение целевой высоты: 
        # self.time_counter = 0.0 
        #self.time_counter += self.dt
        #self.setpoint = 250.0 + 100.0 * math.sin(self.time_counter * 2) 
        #self.canvas.coords("setpoint", 0, self.setpoint, 400, self.setpoint)

#Также добавим шумов для данных, которые передаются в PID регулятор:
    # Добавляем шум датчика в пределах +-5 единиц
    #sensor_noise = random.uniform(-5, 5) 
    #noisy_height = current_height + sensor_noise
    #В ПИД передаем зашумленное значение
    #thrust = self.pid.compute(target_height, noisy_height)

# =====================================================================
# Формулы для расчета движения
# =====================================================================

    def compute(self, setpoint, current_value):

        #Представим ситуацию, когда на мехатронную систему действуют сильные шумы
        #Для их сглаживания используют программные фильтра
        #Реализуем Low-Pass Filter

        #Создайте переменную alpha и выдайте ей значение от 0 до 1
        alpha = Ваше значение

        #Когда симуляция только запускается (или сбрасывается кнопкой), у нас еще нет истории показаний. 
        #Если этого не сделать, переменная self.filtered_value будет пустой (None), и программа упадет с ошибкой. 
        # Поэтому в самый первый шаг мы просто приравниваем отфильтрованное значение к текущему положению дрона.
        if not hasattr(self, 'filtered_value') or self.filtered_value is None:
            self.filtered_value = current_value


        #Реализуйте математическую формулу фильтра
        self.filtered_value = формула


        # 1. Вычислить ошибку
        error = setpoint - отфильтрованное значение    #P #вместо current_value теперь будем вычитать отфильтрованное значение
        
        # 2. Интегральная часть (с защитой от Windup!)      #I
        self.integral += error * self.dt
        self.integral = max(-100, min(100, self.integral)) # Ограничение накопления
        
        # 3. Дифференциальная часть
        derivative = (error - self.prev_error) / self.dt    #D
        
        # 4. Итоговый выход регулятора (сила тяги моторов)
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.prev_error = error
        return output

# =====================================================================
# ДВИЖОК ИГРЫ (Не меняем)
# =====================================================================
class DroneGame:
    def __init__(self, root):
        self.root = root
        self.root.title("PID Drone Survival Game")

        self.time_counter = 0.0 #Счётчик времени

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
        self.pid.filtered_value = None

    def game_loop(self):
        # 1. Симулируем случайные порывы ветра (возмущение системы)
        if random.random() < 0.1:
            self.wind_force = random.uniform(-15, 15)

        self.time_counter += self.dt
        self.setpoint = 250.0 + 100.0 * math.sin(self.time_counter * 0.1)
        self.canvas.coords("setpoint", 0, self.setpoint, 400, self.setpoint)
        
        # 2. Вызываем  ПИД-регулятор
        # В физике tkinter Y идет сверху вниз, поэтому инвертируем значения для логики высоты
        current_height = 500.0 - self.drone_y
        target_height = 500.0 - self.setpoint
        sensor_noise = random.uniform(-5, 5) 
        noisy_height = current_height + sensor_noise

# В ПИД передаем зашумленное значение
        thrust = self.pid.compute(target_height, noisy_height)
        #thrust = self.pid.compute(target_height, current_height)
        
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