import random

u = {'b': 1.,
     'h': 1e2,
     'd': 1e2,
     'k': 1e3,  # kl = m3
     'M': 1e4,
     'kh': 1e3 * 3600}


t_u = {'s': 1.,
       'm': 60,
       'h': 3600,
       'd': 3600*24}


G = 0.0125   # how many gas GZ-50 [m3] is needed to hit 1hl of water to 1C
E = 0.06     # an evaporation rate per hour [6%/h]


def e_per_s():
    return E / t_u['h']


# returns used gas in [m3]
# cp [J/(kg*C)]- density of liquid (4200 - water)
# q [kg/m3] - density of liquid
# v [hl] - volume of liquid
# dt [C | K] - change of temperature
# n - heater efficiency
# w [MJ / m3]- heating value of gas
def calc_gas(cp, q, v, dt, n, w):
    return cp * q * u['h'] * v * dt / (n * w) / 1e5


# returns time of water heating in [h]
# n - heater efficiency
# cp [J/(kg*C)]- density of liquid (4200 - water)
# v [hl] - volume of liquid
# dt [C | K] - change of temperature
# p [kW] - power of heater
# q [kg/m3] - density of liquid
def calc_time(v, dt, p, q=1., cp=4180, n=1.):
    return cp * v * q * u['h'] * dt / (p * u['k'] * n) / t_u['h']


# returns energy needed for water heating in [kWh]
# n - heater efficiency
# cp [J/(kg*C)]- density of liquid (4200 - water)
# v [hl] - volume of liquid
# dt [C | K] - change of temperature
# q [kg/m3] - density of liquid
def calc_energy(v, dt, q=1., cp=4180, n=1.):
    return cp * v * u['h'] * q * dt / n / u['kh']


# returns energy needed for water heating in [Wh]
# n - heater efficiency
# p [kW] - power of heater
# r [h] - time
def calc_energy(p, r, n=1.):
    return p * u['k'] * n * r * t_u['h'] / u['kh']


# returns temperature change in [C]
# n - heater efficiency
# cp [J/(kg*C)- density of liquid (4200 - water)
# v [hl] - volume of liquid
# r [h] - time of heating
# p [kW] - power of heater
# q [kg/m3] - density of liquid
def calc_temperature_change(r, v, p, q=1., cp=4180, n=1.):
    return r * t_u['h'] * p * u['k'] * n / cp / (v * u['h'] * q)


def convert_unit(from_u, to_u, value):
    return value * u[from_u] / u[to_u]


def convert_time(from_u, to_u, value):
    return value * t_u[from_u] / t_u[to_u]


def test():
    masa = 10
    dtemp = 30
    power = 8470

    time = calc_time(masa, dtemp, power)
    gas = calc_gas(masa, dtemp)
    energy = calc_energy(masa, dtemp)
    temp = calc_temperature_change(time, masa, power)

    print "czas: %.3lf h (%.3lf min| %.3lf s)" % (time, convert_time('h', 'm', time), convert_time('h', 's', time))
    print "zuzyty gaz: %.3lf m3 (%.3lf hl| %.3lf l)" % (gas, convert_unit('k', 'h', gas), convert_unit('k', 'b', gas))
    print "zuzyta energia: %.3lf kWh (%.3lf MJ| %.3lf J)" % (energy, convert_unit('kh', 'M', energy), convert_unit('kh', 'b', energy))
    print "zmiana temperatury: %.3lf C" % (temp)

