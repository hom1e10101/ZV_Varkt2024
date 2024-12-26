import matplotlib.pyplot as plt
import numpy as np
import time

# Импорт функций физической модели
from mymodel import solve_ivp, equations, earth_r

# Импорт автопилота
from mypilot import main as run_autopilot, time_data, mass_data, speed_data, speed_x_data, speed_y_data, x_data, altitude_data

# Выполняем автопилот
# run_autopilot()

# Данные из физической модели
t_eval = np.linspace(0, 205, 1000)
solution = solve_ivp(equations, (0, 250), [0, earth_r, 0, 0, 90], t_eval=t_eval)
time_phys = solution.t
x, y, vx, vy, _ = solution.y
mass_phys = [equations(t, state)[-1] for t, state in zip(time_phys, solution.y.T)]
speed_phys = np.sqrt(vx**2 + vy**2)
height_phys = (y - earth_r) / 1000

# Данные из автопилота
# time_auto = time_data
# mass_auto = mass_data
# speed_auto = speed_data
# height_auto = [h for h in altitude_data]

# Построение графиков
fig1, axs1 = plt.subplots(1, 1, figsize=(10, 15))

# График скорости
axs1.plot(time_phys, speed_phys, label="Физическая модель", color="red")
# axs1.plot(time_auto, speed_auto, label="Автопилот", color="blue", linewidth=2)
# axs1[1].set_title("График скорости")
axs1.set_xlabel("Время (с)")
axs1.set_ylabel("Скорость (м/с)")
axs1.legend()
axs1.grid()


fig1, axs2 = plt.subplots(2, 1, figsize=(10, 15))
# График скорости высоты
axs2[0].plot(time_phys, vx, label="Физическая модель", color="green")
# axs2[0].plot(time_auto, speed_y_data, label="Автопилот", color="violet", linewidth=2)
#axs12].set_title("График высоты")
axs2[0].set_xlabel("Время (с)")
axs2[0].set_ylabel("Скорость (м/с)")
axs2[0].legend()
axs2[0].grid()

# График скорости x
axs2[1].plot(time_phys, vy, label="Физическая модель", color="green")
# axs2[1].plot(time_auto, speed_x_data, label="Автопилот", color="violet", linewidth=2)
#axs1.set_title("График высоты")
axs2[1].set_xlabel("Время (с)")
axs2[1].set_ylabel("Скорость (м/с)")
axs2[1].legend()
axs2[1].grid()

fig2, axs3 = plt.subplots(2, 1, figsize=(10, 15))

# График высоты
axs3[0].plot(time_phys, y - earth_r, label="Физическая модель", color="green")
# axs3[0].plot(time_auto, height_auto, label="Автопилот", color="violet", linewidth=2)
#axs2[0].set_title("График высоты")
axs3[0].set_xlabel("Время (с)")
axs3[0].set_ylabel("Высота (м)")
axs3[0].legend()
axs3[0].grid()

# График x
axs3[1].plot(time_phys, x, label="Физическая модель", color="green")
# axs3[1].plot(time_auto, x_data, label="Автопилот", color="violet", linewidth=2)
#axs2[0].set_title("График высоты")
axs3[1].set_xlabel("Время (с)")
axs3[1].set_ylabel("смещение по х (м)")
axs3[1].legend()
axs3[1].grid()


plt.tight_layout()
plt.show()