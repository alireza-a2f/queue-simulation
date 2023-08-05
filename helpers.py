import math

Yt = 1985072130 * 16807 % 2147483648  # Demand Time
Yl = 748932582 * 16807 % 2147483648  # Lead Time
Ya = 1631331038 * 16807 % 2147483648  # Demand Amount


def randomDemandTime():
    global Yt
    u = Yt / 2147483648
    Yt = 16807 * Yt % 2147483648
    return u


def randomLeadTime():
    global Yl
    u = Yl / 2147483648
    Yl = 16807 * Yl % 2147483648
    return u


def randomDemandAmount():
    global Ya
    u = Ya / 2147483648
    Ya = 16807 * Ya % 2147483648
    return -5 * math.log(u)
