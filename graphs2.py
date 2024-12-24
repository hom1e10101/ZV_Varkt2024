import matplotlib.pyplot as plt
import numpy as np

# Примерные данные для демонстрации
time = np.linspace(0, 500, 500)  # Время (0-500 секунд)

# Высота от времени (Модель)
altitude = 150000 * (1 - np.exp(-time / 200))  # Примерная модель высоты
# Скорость от времени (Модель)
speed = np.gradient(altitude, time)  # Примерная скорость (производная высоты)
# Угол тангажа от времени (Модель)
pitch = np.maximum(90 * (1 - time / 200), 0)  # Примерная модель тангажа

# Вертикальная скорость (Модель)
vertical_speed = speed * np.sin(np.radians(pitch))  # Вертикальная составляющая скорости (Модель)
# Горизонтальная скорость (Модель)
horizontal_speed = speed * np.cos(np.radians(pitch))  # Горизонтальная составляющая скорости (Модель)

# Расчёт смещений (Модель)
vertical_displacement_model = np.cumsum(vertical_speed) * (time[1] - time[0])  # Интеграл вертикальной скорости
horizontal_displacement_model = np.cumsum(horizontal_speed) * (time[1] - time[0])  # Интеграл горизонтальной скорости

# ======== Данные из KSP ========
# Для данных из KSP мы будем использовать те же значения для смещений, но с другими моделями (например, линейное изменение)
altitude_KSP = 150000 * (1 - np.exp(-time / 250))  # Данные из KSP (например, другая модель)
speed_KSP = np.gradient(altitude_KSP, time)  # Производная для скорости
pitch_KSP = np.maximum(80 * (1 - time / 250), 0)  # Угол тангажа (другая модель)

# Вертикальная скорость (KSP)
vertical_speed_KSP = speed_KSP * np.sin(np.radians(pitch_KSP))  # Вертикальная составляющая скорости (KSP)
# Горизонтальная скорость (KSP)
horizontal_speed_KSP = speed_KSP * np.cos(np.radians(pitch_KSP))  # Горизонтальная составляющая скорости (KSP)

# Расчёт смещений (KSP)
vertical_displacement_KSP = np.cumsum(vertical_speed_KSP) * (time[1] - time[0])  # Интеграл вертикальной скорости (KSP)
horizontal_displacement_KSP = np.cumsum(horizontal_speed_KSP) * (time[1] - time[0])  # Интеграл горизонтальной скорости (KSP)

# ======== Окно 1: Графики данных из KSP ========
fig1, axs1 = plt.subplots(5, 1, figsize=(10, 20))

# График высоты (KSP)
axs1[0].plot(time, altitude_KSP, color='blue', label='Высота (KSP)')
axs1[0].set_title('Высота во времени (данные из KSP)', fontsize=14)
axs1[0].set_xlabel('Время (с)', fontsize=12)
axs1[0].set_ylabel('Высота (м)', fontsize=12)
axs1[0].legend()
axs1[0].grid()

# График скорости (KSP)
axs1[1].plot(time, speed_KSP, color='blue', label='Скорость (KSP)')
axs1[1].set_title('Скорость во времени (данные из KSP)', fontsize=14)
axs1[1].set_ylabel('Скорость (м/с)', fontsize=12)
axs1[1].legend()
axs1[1].grid()

# График угла тангажа (KSP)
axs1[2].plot(time, pitch_KSP, color='blue', label='Тангаж (KSP)')
axs1[2].set_title('Тангаж во времени (данные из KSP)', fontsize=14)
axs1[2].set_ylabel('Тангаж (градусы)', fontsize=12)
axs1[2].legend()
axs1[2].grid()

# График вертикальной скорости (KSP)
axs1[3].plot(time, vertical_speed_KSP, color='blue', label='Вертикальная скорость (KSP)')
axs1[3].set_title('Вертикальная скорость (данные из KSP)', fontsize=14)
axs1[3].set_ylabel('Скорость (м/с)', fontsize=12)
axs1[3].legend()
axs1[3].grid()

# График горизонтальной скорости (KSP)
axs1[4].plot(time, horizontal_speed_KSP, color='blue', label='Горизонтальная скорость (KSP)')
axs1[4].set_title('Горизонтальная скорость (данные из KSP)', fontsize=14)
axs1[4].set_ylabel('Скорость (м/с)', fontsize=12)
axs1[4].legend()
axs1[4].grid()

# ======== Окно 2: Графики данных математической модели ========
fig2, axs2 = plt.subplots(2, 1, figsize=(10, 10))

# График вертикального смещения (Математическая модель)
axs2[0].plot(time, vertical_displacement_model, color='red', label='Вертикальное смещение (Модель)')
axs2[0].set_title('Вертикальное смещение (Математическая модель)', fontsize=14)
axs2[0].set_ylabel('Смещение (м)', fontsize=12)
axs2[0].legend()
axs2[0].grid()
# График горизонтального смещения (Математическая модель)
axs2[1].plot(time, horizontal_displacement_model, color='red', label='Горизонтальное смещение (Модель)')
axs2[1].set_title('Горизонтальное смещение (Математическая модель)', fontsize=14)
axs2[1].set_ylabel('Смещение (м)', fontsize=12)
axs2[1].legend()
axs2[1].grid()

# ======== Окно 3: Сравнение данных ========
fig3, axs3 = plt.subplots(2, 1, figsize=(10, 15))

# Наложение графиков вертикальных смещений
axs3[0].plot(time, vertical_displacement_KSP, color='blue', label='KSP (Вертикальное смещение)')
axs3[0].plot(time, vertical_displacement_model, color='red', linestyle='--', label='Модель (Вертикальное смещение)')
axs3[0].set_title('Сравнение вертикального смещения', fontsize=14)
axs3[0].set_ylabel('Смещение (м)', fontsize=12)
axs3[0].legend()
axs3[0].grid()

# Наложение графиков горизонтальных смещений
axs3[1].plot(time, horizontal_displacement_KSP, color='blue', label='KSP (Горизонтальное смещение)')
axs3[1].plot(time, horizontal_displacement_model, color='red', linestyle='--', label='Модель (Горизонтальное смещение)')
axs3[1].set_title('Сравнение горизонтального смещения', fontsize=14)
axs3[1].set_ylabel('Смещение (м)', fontsize=12)
axs3[1].legend()
axs3[1].grid()

# Автоматическая корректировка расположения элементов
fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()

# Показываем все окна
plt.show()  