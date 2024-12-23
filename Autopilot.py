import krpc
import math
import time


conn = krpc.connect(name = 'AutoPilot')
vessel = conn.space_center.active_vessel


#контрольные параметры
vessel.control.sas = False
vessel.control.rcs = False
vessel.auto_pilot.engage()
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


all_fuel_for_curr_stage = {
    0: 7700,
    1: 3900,
    2: 3200,
    3: 1700
}

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

#выход на орбиту
vessel.control.activate_next_stage()
vessel.auto_pilot.target_pitch_and_heading(90, 0)
apoasis_flag = False

curr_stage = 0
while True:
    altitude = vessel.flight().surface_altitude

    # проверяем, достаточно ли топлива в ступени
    if not enough_fuel(curr_stage):
        curr_stage = change_stage(curr_stage)
    
    # меняем угол наклона ракеты
    if altitude < 60000:
        target_pitch = 90 * (1 - altitude / 60000)  # Чем выше высота, тем меньше наклон
        vessel.auto_pilot.target_pitch_and_heading(target_pitch, 90)
    else:
        vessel.auto_pilot.target_pitch_and_heading(0, 90)

    # вышли на требуемый апоцентр
    if (vessel.orbit.apoapsis_altitude > 150000):
        print("Needed apoasis OKed\n")
        vessel.control.throttle = 0.0
        break



#орбита
tta = vessel.orbit.time_to_apoapsis
print(f'time to apoapsis {tta}')
while tta > 10:
    # if (int(tta) % 10 == 0):
    print(tta)
    tta = vessel.orbit.time_to_apoapsis
    continue

vessel.control.throttle = 1.0
while abs(vessel.orbit.periapsis_altitude - vessel.orbit.apoapsis_altitude) > 10000:
    if not enough_fuel(curr_stage):
        curr_stage = change_stage(curr_stage)
    continue
vessel.control.throttle = 0.0
print('Orbit Oked')
print(f'orbit {vessel.flight().surface_altitude} diff {vessel.orbit.periapsis_altitude - vessel.orbit.apoapsis_altitude}')
