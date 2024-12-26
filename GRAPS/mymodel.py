import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы Кербина

Temp = 300 # температура
R = 8.310 # универсальная граф пост
earth_r = 600000  # Радиус Кербина (м)
earth_mass = 5.2915158e22  # Масса Кербина (кг)
G = 6.67430e-11  # Гравитационная постоянная (м^3/кг/с^2)
g0 = 9.81  # Ускорение свободного падения (м/с^2)
H = 5000  # Высота масштаба атмосферы (м)
p0 = 1.225  # Плотность воздуха на уровне моря (кг/м^3)

# Ракетные параметры
T_stage1 = 2900000  # Тяга первой ступени (Н)
T_stage2 = 1300000  # Тяга второй ступени (Н)
T_stage3 = 400000 # Тяга третьей ступени (Н)
Isp1 = 280  # Удельный импульс первой ступени (с)
Isp2 = 280  # Удельный импульс второй ступени (с)
Isp3 = 320  # Удельный импульс второй ступени (с)
m0 = 274000  # Начальная масса ракеты (кг)
m_stage1 = 160000  # Масса первой ступени (кг)
m_stage2 = 61000  # Масса первой ступени (кг)
Cd = 0.2  # Коэффициент лобового сопротивления
A = 1  # Площадь поперечного сечения ракеты (м^2)
# alpha_r = np.radians(0.02)  # Угловое ускорение (рад/км)

# Высоты событий
stage_1_sep = 120  # Время отд 1 ступ
stage_2_sep = 180
# start_pitch_over_height = 30000  # Высота начала изменения угла (м)

# Орбитальные параметры
apoapsis_target = 150000  # Апоцентр орбиты (м)

# Функции

def F_sopr(V, h):
    # f сопр воздуха
    return 0.5 * Cd * rho(h) * A * V**2

def rho(h):
    """Плотность атмосферы."""
    return p0 * np.exp(-h / H)

def g(h):
    """Ускорение свободного падения."""
    return G * earth_mass / ((earth_r + h)**2)

def thrust(t):
    """Тяга ракеты."""
    if t < stage_1_sep:
        return T_stage1
    elif t < stage_2_sep:
        return T_stage2
    return T_stage3

def mass(t, h):
    if t < stage_1_sep:
        mdot = T_stage1 / (Isp1 * g0)
        m = m0 - mdot * t
    elif t < stage_2_sep:
        mdot = T_stage2 / (Isp2 * g0)
        m = m0 - m_stage1 - mdot * (t - stage_1_sep)
    else:
        mdot = T_stage3 / (Isp3 * g0)
        m = m0 - m_stage1 - m_stage2 - mdot * (t - stage_2_sep)
    print(f"Mass: {m}, Thrust: {thrust(h)}")  # Вывод для диагностики
    return m

def equations(t, state):
    """Система уравнений."""
    x, y, vx, vy, theta = state

    h = y - earth_r
    if h < 0:
        h = 0

    if h < 60000 and h > 1:
        theta = 90 * (1 - h / 60000)  # Чем выше высота, тем меньше наклон
    elif h > 60000:
        theta = 0
    else:
        theta = 90
    
    # theta = int(theta)
    v = np.sqrt(vx**2 + vy*2)
    print(f'theta is {theta}, h is {h}')
    
    # theta = h


    m = mass(t, h)
    T = thrust(t)
    print(f"Time: {t}, h: {h}, m: {m}, Thrust: {T}, Speed: {v}")

    if m <= 0:
        return [0, 0, 0, 0, 0]

    # alpha_s = h * alpha_r
    alpha = np.radians(theta)

    # Вывод для диагностики

    ax = (T - 0.5 * Cd * rho(h) * A * vx**2) * np.cos(alpha) / m
    ay = ((T - 0.5 * Cd * rho(h) * A * vy**2) * np.sin(alpha)) / m - g(h)

    return [vx, vy, ax, ay, theta]
    # return [v, vx, vy, alpha, h, x]

# Начальные условия
x0, y0 = 0, earth_r
vx0, vy0 = 0, 0
v0 = 0
theta0 = 90
state0 = [x0, y0, vx0, vy0, theta0]

# Решение системы
t_span = (0, 200)
t_eval = np.linspace(t_span[0], t_span[1], 1000)

def terminate_event(t, state):
    h = state[1] - earth_r
    return h - apoapsis_target
terminate_event.terminal = True
terminate_event.direction = 1

solution = solve_ivp(equations, t_span, state0, t_eval=t_eval, events=terminate_event)

# Результаты
t = solution.t
x, y, vx, vy, theta = solution.y

# Графики
# plt.figure(figsize=(10, 6))
# plt.plot(x, (y - earth_r), label="Траектория")
# plt.xlabel("Горизонтальное расстояние (км)")
# plt.ylabel("Высота (км)")
# plt.legend()
# plt.grid()
# #plt.show()

# График высоты от времени
# plt.figure(figsize=(10, 6))
# plt.plot(t, (y - earth_r), label="Высота от времени", color="blue", linewidth=2)
# plt.xlabel("Время (с)")
# plt.ylabel("Высота (км)")
# plt.title("График высоты от времени")
# plt.legend()
# plt.grid()
#plt.show()

# speed = np.sqrt(vx**2 + vy**2)  # Общая скорость в каждый момент времени

# plt.figure(figsize=(10, 6))
# plt.plot(t, vy, label="Скорость от времени", color="green", linewidth=2)
# plt.xlabel("Время (с)")
# plt.ylabel("Скорость (м/с)")
# plt.title("График общей скорости от времени")
# plt.legend()
# plt.grid()
# plt.show()
