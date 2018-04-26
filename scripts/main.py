#!/usr/bin/python3


def get_area():
    # Coefficient obtained from graphs/tables.
    C_l = 0.2
    weight = 0.2 # [kg]
    F_g = weight * 9.81 # [N]
    lift = F_g * 1.5 # [N]
    # dewpoint=6C, temp=15C, H=43m, P=1008HPa(43m)
    air_density = 1.214 # [kg/m^3]
    # Rule of thumb estimated speed.
    speed = 10 # [m/s]

    area = (2*lift*air_density) / (C_l*speed**2)
    return area


def get_weight():
    # Electronics components weight.
    # Weights of the components, in grams.
    weights = {
        "motor"     : 14,
        "rc"        : 5.6,
        "bat"       : 19,
        "servo"     : 2*8,
        "prop"      : 3,
        "payload"   : 2,
        "esc"       : 6,
        "hinge"     : 1,
    }
    electronics_weight = sum(weights.values())

    # beam weight, given density and correction factor.
    pla_density = 1250 * 10**(-9)  # Kg/mm**3
    correction = 0.7
    b_thick = 4
    b_height = 20
    b_len = 500
    beam_volume = b_thick*b_height*b_len*2 + (b_height-2*b_thick)*b_thick*b_len 
    beam_weight = beam_volume * pla_density * correction * 1000
    
    # foam weight
    foam_density = 14.75  # Kg/mm**3
    f_thick = 3
    f_len = 600
    f_width = 480
    foam_volume = 2 * (f_thick*f_len*f_width)
    foam_weight = foam_volume * foam_density * 1000

    total_weight = electronics_weight + beam_weight + foam_weight
    return total_weight


def get_wing_chords(wing_area, aircraft_span=1.2):
    """Mean Aerodynamic Chord"""
    wing_span = aircraft_span / 2
    # Get the chords at the tip and root, in function of the wing_span
    # Trapezoid area = (wing_span/2) * (chord_tip + chord_root)
    chord_tip = None
    chord_root = None
    return (chord_root, chord_tip)


def get_mac(wing_span, chord_root, chord_tip):
    root_side = 3 * chord_root
    tip_side = 2*chord_root + chord_tip
    # Get the linear equation defining the diagonal segments of the trapezoid,
    # and find the point where they cross. (Y = a*X + b)
    # 1st diagonal equation
    b_1 = 0
    a_1 = root_side / wing_span
    # 2nd diagonal equation
    b_2 = tip_side
    a_2 = -b_2 / wing_span
    # Find the crossing coordinates (Y_1=Y_2, X_1=X_2)
    X_crossing = (b_2-b_1) / (a_1-a_2)
    Y_crossing = X_crossing * a_1 + b_1
    # The MAC is the sum of 2 lengths: the root_span plus the height of the 
    # trapezoid triangle at that point (the crossing)
    # Thales theorem for getting the triangle height at X_crossing
    h = (wing_span-X_crossing) * (chord_tip-chord_root) / wing_span
    mac = chord_root + h
    return mac


def main():
    aircraft_weight = get_weight()
    aircraft_area = get_area()
    return aircraft_area


if __name__ == "__main__":
    print(main())