import krpc
import math
import time
import matplotlib.pyplot as plt
import numpy as np


all_fuel_for_curr_stage = {
    0: 7700,
    1: 3900,
    2: 3200,
    3: 1700
}

x_data = []

# x - h
# y, z - x in graph
speed_data = []
speed_x_data = []
speed_y_data = []
# speed_x_data = []

altitude_data = []
mass_data = []
time_data = []
pitch_data = []

def main():
        
    conn = krpc.connect(name = 'AutoPilot')
    vessel = conn.space_center.active_vessel
    ap = vessel.auto_pilot
    control = vessel.control
    initial_propellant_mass = vessel.mass

    #контрольные параметры
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.auto_pilot.engage()

    # фиксируем 0 координаты
    body = conn.space_center.bodies['Kerbin']
    position = vessel.position(body.reference_frame)
    x0 = position[0]
    y0 = position[1]
    z0 = position[2]


    # проверяем, достаточно ли топлива в ступени
    def enough_fuel(stage):
        curr_fuel = vessel.resources_in_decouple_stage(0).amount('LiquidFuel')
        if curr_fuel < all_fuel_for_curr_stage[stage]:
            return False
        return True


    # меняем ступень
    def change_stage(stage):
        vessel.control.throttle = 0.0
        time.sleep(1)
        vessel.control.activate_next_stage()
        vessel.control.throttle = 1.0
        time.sleep(1)
        print(f'{stage} stage out')
        return stage + 1



    altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
    apoapsis = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
    periapsis = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")
    surface_velocity_stream = conn.add_stream(
        getattr, vessel.flight(vessel.orbit.body.reference_frame), "velocity"
    )

    def add_spd(spd_x, spd_y, spd_z):
        speed_data.append(math.sqrt(spd_x**2 + spd_y**2 + spd_z**2))
        speed_y_data.append(spd_x)
        speed_x_data.append(math.sqrt(spd_y**2 + spd_z**2))
        # speed_x_data.append(spd_y)
        # speed_x_data.append(spd_z)
        
    def add_point(x, y, z):
        x_data.append(math.sqrt(x**2 + y**2))
        # y_data.append(y)
        # z_data.append(z)

    def add_inf(altit, mass, curr_time, ptch):
        altitude_data.append(altit)
        mass_data.append(mass)
        time_data.append(curr_time)
        pitch_data.append(ptch)


    # start
    vessel.control.throttle = 1.0
    print(vessel.name)
    time.sleep(3)
    print('3 seconds before the start...')
    time.sleep(1)
    print('2 seconds before the start...')
    time.sleep(1)
    print('1 second before the start...')
    time.sleep(1)
    print('Poehali!')

    #выход на орбиту
    vessel.control.activate_next_stage()
    vessel.auto_pilot.target_pitch_and_heading(90, 0)
    apoasis_flag = False

    t0 = time.time()
    altitude = vessel.flight().surface_altitude
    add_inf(round(altitude), vessel.mass, 0, 90)
    add_point(0, 0, 0)
    add_spd(0, 0, 0)
    surface_velocity = surface_velocity_stream()

    curr_stage = 0
    while True:
        # altitude = vessel.flight().surface_altitude
        altitude = vessel.orbit.radius - 600000

        if not enough_fuel(curr_stage):
            curr_stage = change_stage(curr_stage)
        
        # меняем угол наклона ракеты
        target_pitch = 90
        if altitude < 60000:
            target_pitch = 90 * (1 - altitude / 60000)  # Чем выше высота, тем меньше наклон
            vessel.auto_pilot.target_pitch_and_heading(target_pitch, 90)
        else:
            target_pitch = 0
            vessel.auto_pilot.target_pitch_and_heading(0, 90)

        # вышли на требуемый апоцентр
        if (vessel.orbit.apoapsis_altitude > 150000):
            print("Needed apoasis OKed\n")
            vessel.control.throttle = 0.0
            break

        # inf
        nowt = round(time.time() - t0)

        pos = vessel.position(body.reference_frame)
        x = pos[0] - x0
        y = pos[1] - y0
        z = pos[2] - z0

        surface_velocity = surface_velocity_stream()
        x_speed = surface_velocity[0]
        y_speed = surface_velocity[1]
        z_speed = surface_velocity[2]
        
        add_inf(altitude, vessel.mass, nowt, target_pitch)
        add_point(x, y, z)
        add_spd(x_speed, y_speed, z_speed)



    # #орбита
    # tta = vessel.orbit.time_to_apoapsis
    # print(f'time to apoapsis {tta}')
    # while tta > 10:
    #     altitude = vessel.orbit.radius - 600000
    #     nowt = round(time.time() - t0)

    #     pos = vessel.position(body.reference_frame)
    #     x = pos[0] - x0
    #     y = pos[1] - y0
    #     z = pos[2] - z0

    #     surface_velocity = surface_velocity_stream()
    #     x_speed = surface_velocity[0]
    #     y_speed = surface_velocity[1]
    #     z_speed = surface_velocity[2]

    #     tta = vessel.orbit.time_to_apoapsis
    #     continue

    # vessel.control.throttle = 1.0
    # while abs(vessel.orbit.periapsis_altitude - vessel.orbit.apoapsis_altitude) > 10000:
    #     nowt = round(time.time() - t0)
    #     altitude = vessel.orbit.radius - 600000

    #     pos = vessel.position(body.reference_frame)
    #     x = pos[0] - x0
    #     y = pos[1] - y0
    #     z = pos[2] - z0

    #     surface_velocity = surface_velocity_stream()
    #     x_speed = surface_velocity[0]
    #     y_speed = surface_velocity[1]
    #     z_speed = surface_velocity[2]

    #     if not enough_fuel(curr_stage):
    #         curr_stage = change_stage(curr_stage)
    #     continue
    # vessel.control.throttle = 0.0
    # print('Orbit Oked')
    # print(f'orbit {vessel.flight().surface_altitude} diff {vessel.orbit.periapsis_altitude - vessel.orbit.apoapsis_altitude}')


    # # графики строим
    # fig1, axs1 = plt.subplots(2, 1, figsize=(10, 20))
    
    # # график высоты
    # # axs1[0].figure(figsize=(10, 6))
    # axs1[0].plot(time_data, altitude_data, label="Высота от времени", color="blue", linewidth=2)
    # axs1[0].set_xlabel("Время (с)")
    # axs1[0].set_ylabel("Высота (км)")
    # axs1[0].set_title("График высоты от времени")
    # axs1[0].legend()
    # axs1[0].grid()


    # # график наклона
    # # axs1[1].figure(figsize=(10, 6))
    # axs1[1].plot(time_data, pitch_data, label="наклона от времени", color="blue", linewidth=2)
    # axs1[1].set_xlabel("Время (с)")
    # axs1[1].set_ylabel("наклон в градусах")
    # axs1[1].set_title("График наклона от времени")
    # axs1[1].legend()
    # axs1[1].grid()

    
    # # графики строим
    # fig2, axs2 = plt.subplots(3, 1, figsize=(10, 20))

    # # График общей скорости
    # axs2[0].plot(time_data, speed_y_data, label="KSP", color="red")
    # axs2[0].set_title("График скорости x")
    # axs2[0].set_xlabel("Время (с)")
    # axs2[0].set_ylabel("Скорость (м/с)")
    # axs2[0].legend()
    # axs2[0].grid()
    
    # # График скорости по х
    # axs2[1].plot(time_data, speed_x_data, label="KSP", color="red")
    # axs2[1].set_title("График скорости по y")
    # axs2[1].set_xlabel("Время (с)")
    # axs2[1].set_ylabel("Скорость (м/с)")
    # axs2[1].legend()
    # axs2[1].grid()

    # fig3, axs3 = plt.subplots(3, 1, figsize=(10, 20))
    
    
    # # смещение по x
    # axs3[0].plot(time_data, x_data, label="KSP", color="red")
    # axs3[0].set_title("x")
    # axs3[0].set_xlabel("Время (с)")
    # axs3[0].set_ylabel("m")
    # axs3[0].legend()
    # axs3[0].grid()

    # plt.show()
    

if __name__ == "__main__":
    main()
