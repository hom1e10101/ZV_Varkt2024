import matplotlib.pyplot as plt
import numpy as np

# Примерные данные для демонстрации
time = np.linspace(0, 500, 500)  # Время (0-500 секунд)

# Высота от времени
altitude = 150000 * (1 - np.exp(-time / 200))  # Примерная модель высоты
# Скорость от времени
speed = np.gradient(altitude, time)  # Примерная скорость (производная высоты)
# Угол тангажа от времени
pitch = np.maximum(90 * (1 - time / 200), 0)  # Примерная модель тангажа

# ======== Окно 1: Графики данных из KSP ========
fig1, axs1 = plt.subplots(3, 1, figsize=(10, 12))

# График высоты
axs1[0].plot(time, altitude, color='red', label='Высота')
axs1[0].set_title('Высота во времени (данные из KSP)', fontsize=14)
axs1[0].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs1[0].set_ylabel('Высота (м)', fontsize=12, labelpad=15)  # Увеличен отступ
axs1[0].legend()
axs1[0].grid()
axs1[0].set_xlim([0, 500])  # Ограничение оси времени

# График скорости
axs1[1].plot(time, speed, color='red', label='Скорость')
axs1[1].set_title('Скорость во времени (данные из KSP)', fontsize=14)
axs1[1].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs1[1].set_ylabel('Скорость (м/с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs1[1].legend()
axs1[1].grid()
axs1[1].set_xlim([0, 500])  # Ограничение оси времени

# График угла тангажа
axs1[2].plot(time, pitch, color='red', label='Тангаж')
axs1[2].set_title('Тангаж во времени (данные из KSP)', fontsize=14)
axs1[2].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs1[2].set_ylabel('Тангаж (градусы)', fontsize=12, labelpad=15)  # Увеличен отступ
axs1[2].legend()
axs1[2].grid()
axs1[2].set_xlim([0, 500])  # Ограничение оси времени

# ======== Окно 2: Графики данных математической модели ========
fig2, axs2 = plt.subplots(3, 1, figsize=(10, 12))

# График высоты
axs2[0].plot(time, altitude, color='cyan', label='Высота')
axs2[0].set_title('Высота во времени (математическая модель)', fontsize=14)
axs2[0].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs2[0].set_ylabel('Высота (м)', fontsize=12, labelpad=15)  # Увеличен отступ
axs2[0].legend()
axs2[0].grid()
axs2[0].set_xlim([0, 500])  # Ограничение оси времени

# График скорости
axs2[1].plot(time, speed, color='cyan', label='Скорость')
axs2[1].set_title('Скорость во времени (математическая модель)', fontsize=14)
axs2[1].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs2[1].set_ylabel('Скорость (м/с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs2[1].legend()
axs2[1].grid()
axs2[1].set_xlim([0, 500])  # Ограничение оси времени

# График угла тангажа
axs2[2].plot(time, pitch, color='cyan', label='Тангаж')
axs2[2].set_title('Тангаж во времени (математическая модель)', fontsize=14)
axs2[2].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs2[2].set_ylabel('Тангаж (градусы)', fontsize=12, labelpad=15)  # Увеличен отступ
axs2[2].legend()
axs2[2].grid()
axs2[2].set_xlim([0, 500])  # Ограничение оси времени

# ======== Окно 3: Сравнение данных ========
fig3, axs3 = plt.subplots(3, 1, figsize=(10, 12))

# Наложение графиков высоты
axs3[0].plot(time, altitude, color='red', label='KSP (Высота)')
axs3[0].plot(time, altitude, color='cyan', linestyle='--', label='Модель (Высота)')
axs3[0].set_title('Сравнение высоты во времени', fontsize=14)
axs3[0].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs3[0].set_ylabel('Высота (м)', fontsize=12, labelpad=15)  # Увеличен отступ
axs3[0].legend()
axs3[0].grid()
axs3[0].set_xlim([0, 500])  # Ограничение оси времени

# Наложение графиков скорости
axs3[1].plot(time, speed, color='red', label='KSP (Скорость)')
axs3[1].plot(time, speed, color='cyan', linestyle='--', label='Модель (Скорость)')
axs3[1].set_title('Сравнение скорости во времени', fontsize=14)
axs3[1].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs3[1].set_ylabel('Скорость (м/с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs3[1].legend()
axs3[1].grid()
axs3[1].set_xlim([0, 500])  # Ограничение оси времени

# Наложение графиков тангажа
axs3[2].plot(time, pitch, color='red', label='KSP (Тангаж)')
axs3[2].plot(time, pitch, color='cyan', linestyle='--', label='Модель (Тангаж)')
axs3[2].set_title('Сравнение тангажа во времени', fontsize=14)
axs3[2].set_xlabel('Время (с)', fontsize=12, labelpad=15)  # Увеличен отступ
axs3[2].set_ylabel('Тангаж (градусы)', fontsize=12, labelpad=15)  # Увеличен отступ
axs3[2].legend()
axs3[2].grid()
axs3[2].set_xlim([0, 500])  # Ограничение оси времени

# Автоматическая корректировка расположения элементов
fig1.subplots_adjust(hspace=0.4)  # Увеличение пространства между графиками
fig2.subplots_adjust(hspace=0.4)  # Увеличение пространства между графиками
fig3.subplots_adjust(hspace=0.4)  # Увеличение пространства между графиками

# Показываем все три окна
plt.show()
