import random
from physic_calc import e_per_s, calc_temperature_change, convert_time, calc_energy, calc_gas
from noise_generator import apply_noise_to_input, apply_noise_to_output

# Production constraints:
# Heat capacity [J/(kg*C)]:
__heat_capacity = {'water': 4180,
                 'mash 15 P': 3730,
                 'mash 20 P': 3600,
                 'mash 25 P': 3460,
                 'wort min': 4000,
                 'wort max': 4100,
                 'air': 1005}

__temp_start = (7., 12.)  # start - temp of water in tap - 7 in winter, 12 - in summer

__volume_blurring = (232, 232, 316)  # max volume of blurring vat [hl] (only water warming)

__temp_maltose_break = (62., 65.)  # whole mash
__time_maltose_break = (15., 60.)  # 60 = maltose break time + dextrinization break time [min]

__temp_dextrinization_break = (70., 75.)  # whole mash
__time_dextrinization_break = (15., 60.)  # 60 = maltose break time + dextrinization break time [min]

__temp_mash_out = (75.5, 76.)  # whole mash warming
__volume_mash = 493  # max volume of mash cauldron [hl]

__temp_sweetens = (77.5, 78)  # only water

__temp_boiling = (90., 90.5)  # whole wort
__time_boiling = (60., 60.)  # [min]


__power = [5210, 8470]  # [kW]


# provide noise:
__input_noise = True
__output_noise = False


# only water warming
def blurring(v, power=__power[0], time_step=5):
    temp = random.uniform(__temp_start[0], __temp_start[1])
    temp_maltose_break = random.uniform(__temp_maltose_break[0], __temp_maltose_break[1])
    temp_stop = temp_maltose_break + 2

    # TODO: sprawdz v i przydziel kociol

    time_s = 0
    filename = 'prepare_to_blurring_n'

    with open(filename + '.arff', 'w') as f:
        f.write("@RELATION %s\n\n" % filename)
        f.write("@ATTRIBUTE liquid_volume_hl numeric\n")
        f.write("@ATTRIBUTE time_s numeric\n")
        f.write("@ATTRIBUTE temp_C numeric\n")
        f.write("@ATTRIBUTE energy_kWh numeric\n")
        f.write("@ATTRIBUTE gas_m3 numeric\n")
        f.write("\n@DATA\n")
        while temp < temp_stop:
            time_s += time_step
            if __input_noise:
                new_v, p, q, cp, n = apply_noise_to_input(v, power, 1, __heat_capacity['water'], 1)
            else:
                cp = __heat_capacity['water']
                n = 1.
                new_v = v
            dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
            temp += dt
            energy = calc_energy(power, convert_time('s', 'h', time_step))
            gas = calc_gas(new_v, dt)
            if __output_noise:
                dt, energy, gas = apply_noise_to_output(dt, energy, gas)
            f.write("%.3lf,%d,%.5lf,%.3lf,%.5lf\n" % (new_v, time_s, dt, energy, gas))
    return temp, v


def between_breaks(v, temp, power=__power[0], time_step=5):
    temp_stop = random.uniform(__temp_dextrinization_break[0], __temp_dextrinization_break[1])

    # TODO: sprawdz v i przydziel kociol

    time_s = 0
    filename = 'between_breaks_n'

    with open(filename + '.arff', 'w') as f:
        f.write("@RELATION %s\n\n" % filename)
        f.write("@ATTRIBUTE liquid_volume_hl numeric\n")
        f.write("@ATTRIBUTE time_s numeric\n")
        f.write("@ATTRIBUTE temp_C numeric\n")
        f.write("@ATTRIBUTE energy_kWh numeric\n")
        f.write("@ATTRIBUTE gas_m3 numeric\n")
        f.write("\n@DATA\n")
        while temp < temp_stop:
            time_s += time_step
            if __input_noise:
                new_v, p, q, cp, n = apply_noise_to_input(v, power, 1070., __heat_capacity['mash 25 P'], 1)
            else:
                cp = __heat_capacity['water']
                n = 1.
                new_v = v
            dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
            temp += dt
            energy = calc_energy(power, convert_time('s', 'h', time_step))
            gas = calc_gas(new_v, dt)
            if __output_noise:
                dt, energy, gas = apply_noise_to_output(dt, energy, gas)
            f.write("%.3lf,%d,%.5lf,%.3lf,%.5lf\n" % (new_v, time_s, dt, energy, gas))
    return temp, v


def to_mash_out(v, temp, power=__power[0], time_step=5):
    temp_stop = random.uniform(__temp_mash_out[0], __temp_mash_out[1])

    time_s = 0
    filename = 'to_mash_out_n'

    with open(filename + '.arff', 'w') as f:
        f.write("@RELATION %s\n\n" % filename)
        f.write("@ATTRIBUTE liquid_volume_hl numeric\n")
        f.write("@ATTRIBUTE time_s numeric\n")
        f.write("@ATTRIBUTE temp_C numeric\n")
        f.write("@ATTRIBUTE energy_kWh numeric\n")
        f.write("@ATTRIBUTE gas_m3 numeric\n")
        f.write("\n@DATA\n")
        while temp < temp_stop:
            time_s += time_step
            if __input_noise:
                new_v, p, q, cp, n = apply_noise_to_input(v, power, 1060., __heat_capacity['mash 20 P'], 1)
            else:
                cp = __heat_capacity['water']
                n = 1.
                new_v = v
            dt = calc_temperature_change(convert_time('s', 'h', time_step), new_v, power, q=q, cp=cp, n=n)
            temp += dt
            energy = calc_energy(power, convert_time('s', 'h', time_step))
            gas = calc_gas(new_v, dt)
            if __output_noise:
                dt, energy, gas = apply_noise_to_output(dt, energy, gas)
            f.write("%.3lf,%d,%.5lf,%.3lf,%.5lf\n" % (new_v, time_s, dt, energy, gas))
    return temp, v


print "start:", __volume_blurring[0]
blurring_temp, new_v = blurring(__volume_blurring[0])
print "blurring temp:", blurring_temp, new_v
last_break_temp, new_v = between_breaks(__volume_blurring[0], blurring_temp)
print "last break temp:", last_break_temp, new_v
mash_temp, new_v = to_mash_out(__volume_blurring[0], last_break_temp)
print "mash out:", mash_temp, new_v
