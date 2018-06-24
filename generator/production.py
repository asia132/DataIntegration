import random
import os
from physic_calc import calc_temperature_change, convert_time, calc_energy, calc_gas
from noise_generator import apply_noise_to_input, apply_noise_to_output
from settings import *
import datetime


# returns the temperature of water in the pipes
def start_temp(month):
    dt = (temp_start[1] - temp_start[0]) / 3
    if month in (12, 1, 2):
        t_0 = temp_start[0]
        t_n = temp_start[0] + dt
    elif month in (5, 6, 7, 8):
        t_0 = temp_start[1]
        t_n = temp_start[1] - dt
    else:
        t_0 = temp_start[0] + dt
        t_n = temp_start[1] - dt
    return random.uniform(t_0, t_n)


# only water warming
def blurring(v, temp, temp_stop, gas_type, power=power, time_step=5):
    time_s = energy = gas = 0
    while temp < temp_stop:
        time_s += time_step
        if input_noise:
            new_v, p, q, cp, n, w = apply_noise_to_input(
                v, power, 1, heat_capacity['water'], 1, gas_heating_value[gas_type])
        else:
            cp = heat_capacity['water']
            n = 1.
            new_v = v
            q = 1.
            w = gas_heating_value[gas_type]
        dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
        temp += dt
        energy += calc_energy(power, convert_time('s', 'h', time_step))
        gas += calc_gas(cp, q, new_v, dt, n, w)
        if output_noise:
            dt, energy, gas = apply_noise_to_output(dt, energy, gas)
    return temp, time_s, energy, gas


def between_breaks(v, temp, temp_stop, gas_type, power=power, time_step=5):
    time_s = energy = gas = 0
    while temp < temp_stop:
        time_s += time_step
        if input_noise:
            new_v, p, q, cp, n, w = apply_noise_to_input(
                v, power, 1, heat_capacity['mash 20 P'], 1, gas_heating_value[gas_type])
        else:
            cp = heat_capacity['mash 20 P']
            n = 1.
            new_v = v
            q = 1.
            w = gas_heating_value[gas_type]
        dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
        temp += dt
        energy += calc_energy(power, convert_time('s', 'h', time_step))
        gas += calc_gas(cp, q, new_v, dt, n, w)
        if output_noise:
            dt, energy, gas = apply_noise_to_output(dt, energy, gas)
    return temp, time_s, energy, gas


def to_mash_out(v, temp, temp_stop, gas_type, power=power, time_step=5):
    time_s = energy = gas = 0
    while temp < temp_stop:
        time_s += time_step
        if input_noise:
            new_v, p, q, cp, n, w = apply_noise_to_input(
                v, power, 1, heat_capacity['mash 20 P'], 1, gas_heating_value[gas_type])
        else:
            cp = heat_capacity['mash 20 P']
            n = 1.
            new_v = v
            q = 1.
            w = gas_heating_value[gas_type]
        dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
        temp += dt
        energy += calc_energy(power, convert_time('s', 'h', time_step))
        gas += calc_gas(cp, q, new_v, dt, n, w)
        if output_noise:
            dt, energy, gas = apply_noise_to_output(dt, energy, gas)
    return temp, time_s, energy, gas


def to_boil(v, temp, temp_stop, gas_type, power=power, time_step=5):
    time_s = energy = gas = 0
    while temp < temp_stop:
        time_s += time_step
        if input_noise:
            new_v, p, q, cp, n, w = apply_noise_to_input(
                v, power, 1, heat_capacity['wort min'], 1, gas_heating_value[gas_type])
        else:
            cp = heat_capacity['wort min']
            n = 1.
            new_v = v
            q = 1.
            w = gas_heating_value[gas_type]
        dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
        temp += dt
        energy += calc_energy(power, convert_time('s', 'h', time_step))
        gas += calc_gas(cp, q, new_v, dt, n, w)
        if output_noise:
            dt, energy, gas = apply_noise_to_output(dt, energy, gas)
    return temp, time_s, energy, gas


def start_prod():
    # start_date = raw_input("Provide start date [YY-MM-DD HH:MM:SS]: ")
    # i = input("Provide the number of iterations: ")

    i = 1000

    date = datetime.datetime.strptime(start_date, "%y_%m_%d %H:%M:%S")

    tag_prod = 'the_production'
    tag_blur = 'blurring'
    tag_last = 'last_break'
    tag_mash = 'mash_out'
    tag_boil = 'boil'

    if not os.path.exists('../' + folder):
        os.makedirs('../' + folder)

    if not os.path.exists('../' + folder + '/' + start_date[:8] + '/'):
        os.makedirs('../' + folder + '/' + start_date[:8] + '/')

    i_n = o_n = 'n'
    if input_noise:
        i_n = 't'
    if output_noise:
        o_n = 't'

    if input_noise or output_noise:
        f_prod = open('../' + folder + '/' + start_date[:8] + '/' + tag_prod + '_' + i_n + o_n + '.arff', 'w')
        f_blur = open('../' + folder + '/' + start_date[:8] + '/' + tag_blur + '_' + i_n + o_n + '.arff', 'w')
        f_last = open('../' + folder + '/' + start_date[:8] + '/' + tag_last + '_' + i_n + o_n + '.arff', 'w')
        f_mash = open('../' + folder + '/' + start_date[:8] + '/' + tag_mash + '_' + i_n + o_n + '.arff', 'w')
        f_boil = open('../' + folder + '/' + start_date[:8] + '/' + tag_boil + '_' + i_n + o_n + '.arff', 'w')
    else:
        f_prod = open('../' + folder + '/' + tag_prod + '.arff', 'w')
        f_blur = open('../' + folder + '/' + tag_blur + '.arff', 'w')
        f_last = open('../' + folder + '/' + tag_last + '.arff', 'w')
        f_mash = open('../' + folder + '/' + tag_mash + '.arff', 'w')
        f_boil = open('../' + folder + '/' + tag_boil + '.arff', 'w')

    f_prod.write("@RELATION %s\n\n" % tag_prod)
    f_blur.write("@RELATION %s\n\n" % tag_blur)
    f_last.write("@RELATION %s\n\n" % tag_last)
    f_mash.write("@RELATION %s\n\n" % tag_mash)
    f_boil.write("@RELATION %s\n\n" % tag_boil)

    f_prod.write("@ATTRIBUTE used_energy_kWh numeric\n@ATTRIBUTE used_gas_m3 numeric\n")
    f_prod.write("@ATTRIBUTE duration_time_s numeric\n")
    f_prod.write("@ATTRIBUTE start_temp_C numeric\n@ATTRIBUTE stop_temp_C numeric\n")
    f_prod.write("@ATTRIBUTE gas_type {GZ-50, GZ-35}\n@ATTRIBUTE liquid_volume_hl {blur_1, blur_2}\n")
    f_prod.write("\n@DATA\n")

    f_blur.write("@ATTRIBUTE used_energy_kWh numeric\n@ATTRIBUTE used_gas_m3 numeric\n")
    f_blur.write("@ATTRIBUTE duration_time_s numeric\n")
    f_blur.write("@ATTRIBUTE start_temp_C numeric\n@ATTRIBUTE stop_temp_C numeric\n")
    f_blur.write("@ATTRIBUTE gas_type {GZ-50, GZ-35}\n@ATTRIBUTE liquid_volume_hl {blur_1, blur_2}\n")
    f_blur.write("\n@DATA\n")

    f_last.write("@ATTRIBUTE used_energy_kWh numeric\n@ATTRIBUTE used_gas_m3 numeric\n")
    f_last.write("@ATTRIBUTE duration_time_s numeric\n")
    f_last.write("@ATTRIBUTE start_temp_C numeric\n@ATTRIBUTE stop_temp_C numeric\n")
    f_last.write("@ATTRIBUTE gas_type {GZ-50, GZ-35}\n@ATTRIBUTE liquid_volume_hl {blur_1, blur_2}\n")
    f_last.write("\n@DATA\n")

    f_mash.write("@ATTRIBUTE used_energy_kWh numeric\n@ATTRIBUTE used_gas_m3 numeric\n")
    f_mash.write("@ATTRIBUTE duration_time_s numeric\n")
    f_mash.write("@ATTRIBUTE start_temp_C numeric\n@ATTRIBUTE stop_temp_C numeric\n")
    f_mash.write("@ATTRIBUTE gas_type {GZ-50, GZ-35}\n@ATTRIBUTE liquid_volume_hl {blur_1, blur_2}\n")
    f_mash.write("\n@DATA\n")

    f_boil.write("@ATTRIBUTE used_energy_kWh numeric\n@ATTRIBUTE used_gas_m3 numeric\n")
    f_boil.write("@ATTRIBUTE duration_time_s numeric\n")
    f_boil.write("@ATTRIBUTE start_temp_C numeric\n@ATTRIBUTE stop_temp_C numeric\n")
    f_boil.write("@ATTRIBUTE gas_type {GZ-50, GZ-35}\n@ATTRIBUTE liquid_volume_hl {blur_1, blur_2}\n")
    f_boil.write("\n@DATA\n")

    while i > 0:
        print i
        gas_type = random.choice(gas_heating_value.keys())
        vol_type = random.choice(volume_blurring.keys())

        temp = start_temp(date.month)
        temp_malt_break = random.uniform(temp_maltose_break[0], temp_maltose_break[1])
        temp_stop = temp_malt_break + 2

        v_lost = volume_blurring[vol_type] * 20 / 100

        blurring_temp, time_stop_blurring, energy_blurring, gas_blurring = blurring(
            volume_blurring[vol_type], temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_blurring)
        f_blur.write("%.2lf %.2lf %.2lf %.2lf %d %s %s\n" % (energy_blurring,
                                                             gas_blurring, time_stop_blurring,
                                                             temp, temp_stop,
                                                             gas_type, vol_type))

        temp_stop = random.uniform(temp_dextrinization_break[0], temp_dextrinization_break[1])
        last_break_temp, time_stop_break, energy_break, gas_break = between_breaks(
            volume_blurring[vol_type] - v_lost, blurring_temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_break)
        f_last.write("%.2lf %.2lf %.2lf %.2lf %d %s %s\n" % (energy_break, gas_break, time_stop_break,
                                                             blurring_temp, temp_stop,
                                                             gas_type, vol_type))

        temp_stop = random.uniform(temp_mash_out[0], temp_mash_out[1])
        mash_temp, time_stop_mash, energy_mash, gas_mash = to_mash_out(
            volume_blurring[vol_type] - v_lost, last_break_temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_mash)
        f_mash.write("%.2lf %.2lf %.2lf %.2lf %d %s %s\n" % (energy_mash, gas_mash,
                                                             time_stop_mash, last_break_temp, temp_stop,
                                                             gas_type, vol_type))

        temp_stop = random.uniform(temp_boiling[0], temp_boiling[1])
        boil_temp, time_stop_boil, energy_boil, gas_boil = to_boil(
            volume_blurring[vol_type] - v_lost, mash_temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_mash)
        f_boil.write("%.2lf %.2lf %.2lf %.2lf %d %s %s\n" % (energy_boil, gas_boil,
                                                             time_stop_boil, mash_temp, temp_stop,
                                                             gas_type, vol_type))

        energy = energy_blurring + energy_break + energy_mash + energy_boil
        gas = gas_blurring + gas_break + gas_mash + gas_boil
        time_stop = time_stop_blurring + time_stop_break + time_stop_mash + time_stop_boil
        f_prod.write("%.2lf %.2lf %.2lf %.2lf %d %s %s\n" % (energy, gas, time_stop,
                                                             temp, temp_stop, gas_type, vol_type))
        i -= 1

    f_prod.close()
    f_blur.close()
    f_last.close()
    f_mash.close()
    f_boil.close()


def start_prod_temp():
    # start_date = raw_input("Provide start date [YY-MM-DD HH:MM:SS]: ")
    # i = input("Provide the number of iterations: ")

    i = 1000

    date = datetime.datetime.strptime(start_date, "%y_%m_%d %H:%M:%S")

    tag_prod = 'the_production_temp'

    if not os.path.exists('../' + folder):
        os.makedirs('../' + folder)

    if not os.path.exists('../' + folder + '/' + start_date[:8] + '/'):
        os.makedirs('../' + folder + '/' + start_date[:8] + '/')

    i_n = o_n = 'n'
    if input_noise:
        i_n = 't'
    if output_noise:
        o_n = 't'

    if input_noise or output_noise:
        f_prod = open('../' + folder + '/' + start_date[:8] + '/' + tag_prod + '_' + i_n + o_n + '.arff', 'w')
    else:
        f_prod = open('../' + folder + '/' + tag_prod + '.arff', 'w')

    f_prod.write("@RELATION %s\n\n" % tag_prod)

    f_prod.write("@ATTRIBUTE used_energy_kWh numeric\n@ATTRIBUTE used_gas_m3 numeric\n")
    f_prod.write("@ATTRIBUTE duration_time_s numeric\n")
    f_prod.write("@ATTRIBUTE pipes_temp_C numeric\n@ATTRIBUTE blurring_temp_C numeric\n")
    f_prod.write("@ATTRIBUTE last_break_temp_C numeric\n@ATTRIBUTE mash_temp_C numeric\n")
    f_prod.write("@ATTRIBUTE boil_temp_C numeric\n")
    f_prod.write("@ATTRIBUTE gas_type {GZ-50, GZ-35}\n@ATTRIBUTE liquid_volume_hl {blur_1, blur_2}\n")
    f_prod.write("\n@DATA\n")

    while i > 0:
        print i
        gas_type = random.choice(gas_heating_value.keys())
        vol_type = random.choice(volume_blurring.keys())

        temp = start_temp(date.month)
        if temp_maltose_break[0] > temp_maltose_break[1]:
            temp_malt_break = temp_maltose_break[1]
        else:
            temp_malt_break = random.uniform(temp_maltose_break[0], temp_maltose_break[1])
        temp_stop = temp_malt_break + 2

        v_lost = volume_blurring[vol_type] * 20 / 100

        blurring_temp, time_stop_blurring, energy_blurring, gas_blurring = blurring(
            volume_blurring[vol_type], temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_blurring)

        temp_stop = random.uniform(temp_dextrinization_break[0], temp_dextrinization_break[1])
        last_break_temp, time_stop_break, energy_break, gas_break = between_breaks(
            volume_blurring[vol_type] - v_lost, blurring_temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_break)

        temp_stop = random.uniform(temp_mash_out[0], temp_mash_out[1])
        mash_temp, time_stop_mash, energy_mash, gas_mash = to_mash_out(
            volume_blurring[vol_type] - v_lost, last_break_temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_mash)

        temp_stop = random.uniform(temp_boiling[0], temp_boiling[1])
        boil_temp, time_stop_boil, energy_boil, gas_boil = to_boil(
            volume_blurring[vol_type] - v_lost, mash_temp, temp_stop, gas_type)
        date = date + datetime.timedelta(seconds=time_stop_mash)

        energy = energy_blurring + energy_break + energy_mash + energy_boil
        gas = gas_blurring + gas_break + gas_mash + gas_boil
        time_stop = time_stop_blurring + time_stop_break + time_stop_mash + time_stop_boil
        f_prod.write("%.2lf %.2lf %.2lf %.2lf %.2lf %.2lf %.2lf %.2lf %s %s\n" % (energy, gas, time_stop,
                                                                                  temp, blurring_temp, last_break_temp,
                                                                                  mash_temp, boil_temp,
                                                                                  gas_type, vol_type))
        i -= 1

    f_prod.close()


def save_settings():

    if not os.path.exists('../input/'):
        os.makedirs('../input/')

    with open('../input/settings.conf', 'w') as f:
        f.write(start_date[:8] + '\n')
        f.write('%lf %lf\n' % (temp_start[0], temp_start[1]))
        f.write('%lf %lf\n' % (temp_maltose_break[0], temp_maltose_break[1]))
        f.write('%lf %lf\n' % (temp_dextrinization_break[0], temp_dextrinization_break[1]))
        f.write('%lf %lf\n' % (temp_mash_out[0], temp_mash_out[1]))
        f.write('%lf %lf\n' % (temp_boiling[0], temp_boiling[1]))


def update_settings_from_conf():
    global temp_maltose_break, temp_dextrinization_break, temp_mash_out, temp_boiling, start_date

    if os.path.exists('../input/settings.conf'):
        input = open('../input/settings.conf', 'r')
        start = '../input/%s' % input.readline()[:-1]
        order = input.readline()
        temp_maltose_break = map(lambda x: float(x), input.readline().split())
        temp_dextrinization_break = map(lambda x: float(x), input.readline().split())
        temp_mash_out = map(lambda x: float(x), input.readline().split())
        temp_boiling = map(lambda x: float(x), input.readline().split())
        input.close()


def update_settings_from_message():
    global temp_maltose_break, temp_dextrinization_break, temp_mash_out, temp_boiling, start_date

    if os.path.exists('../input/message'):
        input = open('../input/message', 'r')
        temp = input.readline().split()
        line = input.readline().split()
        temp_maltose_break[int(line[0])] = float(line[1])
        line = input.readline().split()
        temp_dextrinization_break[int(line[0])] = float(line[1])
        line = input.readline().split()
        temp_mash_out[int(line[0])] = float(line[1])
        line = input.readline().split()
        temp_boiling[int(line[0])] = float(line[1])
        input.close()


update_settings_from_conf()
update_settings_from_message()
start_prod_temp()
save_settings()
