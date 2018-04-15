import random
from physic_calc import e_per_s, calc_temperature_change, convert_time, calc_energy, calc_gas

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


# only water warming
def blurring(v, power=__power[0], time_step=1):
    temp = random.uniform(__temp_start[0], __temp_start[1])
    temp_maltose_break = random.uniform(__temp_maltose_break[0], __temp_maltose_break[1])
    temp_stop = temp_maltose_break + 2

    # TODO: sprawdz v i przydziel kociol

    time_s = 0
    gas = 0
    energy = 0
    filename = 'prepare_to_blurring'

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
            dt = calc_temperature_change(convert_time('s', 'h', time_step), v, power, q=1., cp=__heat_capacity['water'])
            temp += dt
            energy = calc_energy(power, convert_time('s', 'h', time_step))
            gas = calc_gas(v, dt)
            v -= e_per_s()
            f.write("%.3lf,%d,%.3lf,%.3lf,%.5lf\n" % (v, time_s, dt, energy, gas))
    return temp, v


def between_breaks(v, temp, power=__power[0], time_step=1):
    temp_stop = random.uniform(__temp_dextrinization_break[0], __temp_dextrinization_break[1])

    # TODO: sprawdz v i przydziel kociol

    time_s = 0
    gas = 0
    energy = 0
    filename = 'between_breaks'

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
            dt = calc_temperature_change(
                convert_time('s', 'h', time_step), v, power, q=1070., cp=__heat_capacity['mash 25 P'])
            temp += dt
            energy = calc_energy(power, convert_time('s', 'h', time_step))
            gas = calc_gas(v, dt)
            v -= e_per_s()
            f.write("%.3lf,%d,%.3lf,%.3lf,%.5lf\n" % (v, time_s, dt, energy, gas))
    return temp, v


def to_mash_out(v, temp, power=__power[0], time_step=1):
    temp_stop = random.uniform(__temp_mash_out[0], __temp_mash_out[1])

    time_s = 0
    gas = 0
    energy = 0
    filename = 'to_mash_out'

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
            dt = calc_temperature_change(
                convert_time('s', 'h', time_step), v, power, q=1060., cp=__heat_capacity['mash 20 P'])
            temp += dt
            energy = calc_energy(power, convert_time('s', 'h', time_step))
            gas = calc_gas(v, dt)
            v -= e_per_s()
            f.write("%.3lf,%d,%.3lf,%.3lf,%.5lf\n" % (v, time_s, dt, energy, gas))
    return temp, v


print "start:", __volume_blurring[0]
blurring_temp, new_v = blurring(__volume_blurring[0])
print "blurring temp:", blurring_temp, new_v
last_break_temp, new_v = between_breaks(new_v, blurring_temp)
print "last break temp:", last_break_temp, new_v
mash_temp, new_v = to_mash_out(new_v, last_break_temp)
print "last break temp:", mash_temp, new_v
