import numpy.random as np

# beta settings
__a = 0.5
__b = 6.5

# chisquare settings
__df = 2.5


# small noise
def beta_noise(val):
    return np.beta(__a, __b) * np.choice([-1, 1]) * 0.1 + val

# big noise
def chi_noise(val):
    return np.chisquare(__df) * np.choice([-1, 1]) + val


def test_noise():
    # beta
    # to make the return value smaller, a should be decreased and b should be increased
    # a = 0.389
    # b = 1.5
    print "beta"
    for i in range(20):
        print "%d\t%.3lf" % (i, beta_noise(i))

    # chi return values [0, ...]
    # df = [1, 3]
    df = 2.5
    print "chisquare"
    for i in range(100, 120):
        print "%d\t%.3lf" % (i, chi_noise(i))


def apply_noise_to_input(v, p, q, cp, n, w):
    return chi_noise(v), chi_noise(p), beta_noise(q), chi_noise(cp), beta_noise(n), chi_noise(w)


def apply_noise_to_output(dt, energy, gas):
    return beta_noise(dt), chi_noise(energy), beta_noise(gas)
