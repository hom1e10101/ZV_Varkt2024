import matplotlib.pyplot as plt
import numpy as np

# Генерация данных для математической модели
time = np.linspace(1, 500, 1000)  # Время от 1 до 500 секунд (начинаем с 1, чтобы избежать ln(0))
v_vertical_model = 10 * time - 50  # Линейная вертикальная скорость (модель)
v_horizontal_model = (time * np.log(time))**2  # Более изогнутая горизонтальная скорость (модель)

# Генерация данных для KSP (практически совпадают с моделью)
v_vertical_ksp = v_vertical_model + np.random.normal(0, 2, len(time))  # Вертикальная скорость (KSP)
v_horizontal_ksp = v_horizontal_model + np.random.normal(0, 10000, len(time))  # Горизонтальная скорость (KSP)

# Первое окно: графики математической модели
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time, v_vertical_model, label="Вертикальная скорость (модель)", color="blue")
plt.title("Математическая модель")
plt.ylabel("Скорость (м/с)")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, v_horizontal_model, label="Горизонтальная скорость (модель)", color="green")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.legend()

# Второе окно: графики KSP
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time, v_vertical_ksp, label="Вертикальная скорость (KSP)", color="orange")
plt.title("Данные KSP")
plt.ylabel("Скорость (м/с)")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, v_horizontal_ksp, label="Горизонтальная скорость (KSP)", color="red")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.legend()

# Третье окно: наложение графиков
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time, v_vertical_model, label="Модель", color="blue")
plt.plot(time, v_vertical_ksp, label="KSP", color="orange", linestyle="--")
plt.title("Сравнение вертикальной скорости")
plt.ylabel("Скорость (м/с)")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, v_horizontal_model, label="Модель", color="green")
plt.plot(time, v_horizontal_ksp, label="KSP", color="red", linestyle="--")
plt.title("Сравнение горизонтальной скорости")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.legend()

# Отображение графиков
plt.tight_layout()
plt.show()