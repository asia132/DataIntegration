# Production constraints:
# Heat capacity [J/(kg*C)]:
heat_capacity = {'water': 4180,
                 'mash 15 P': 3730,
                 'mash 20 P': 3600,
                 'mash 25 P': 3460,
                 'wort min': 4000,
                 'wort max': 4100,
                 'air': 1005}

temp_start = (7., 13.)  # start - temp of water in tap - 7 in winter, 12 - in summer

volume_blurring = {'blur_1': 232, 'blur_2': 316}  # max volume of blurring vat [hl] (only water warming)

temp_maltose_break = (62., 65.)  # whole mash
time_maltose_break = (15., 60.)  # 60 = maltose break time + dextrinization break time [min]

temp_dextrinization_break = (70., 75.)  # whole mash
time_dextrinization_break = (15., 60.)  # 60 = maltose break time + dextrinization break time [min]

temp_mash_out = (75.5, 76.)  # whole mash warming
volume_mash = 493  # max volume of mash cauldron [hl]

temp_sweetens = (77.5, 78)  # only water

temp_boiling = (90., 90.5)  # whole wort
time_boiling = (60., 60.)  # [min]


power = 5210  # [kW]

gas_heating_value = {'GZ-50': 34430, 'GZ-35': 28000}  # [kJ/m3]

start_date = '16_01_01 09:01:22'

# provide noise:
input_noise = True
output_noise = True


folder = 'outputs'
