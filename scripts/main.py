#!/usr/bin/python3
# Local libraries
import wing

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
    electronics_weight = sum(weights.values()) * 10**(-3)

    # beam weight, given density and correction factor.
    pla_density = 1250 * 10**(-9)  # [Kg/mm**3]
    correction = 0.7
    b_thick = 4
    b_height = 20
    b_len = 500
    beam_volume = b_thick*b_height*b_len*2 + (b_height-2*b_thick)*b_thick*b_len 
    beam_weight = beam_volume * pla_density * correction
    beam_weight = 0
    
    # foam weight
    foam_density = 14.75  # [Kg/mm**3]
    estimated_wing_area = 0.35
    f_thick = 0.0125
    foam_volume = 2 * (f_thick*estimated_wing_area)
    foam_weight = foam_volume * foam_density

    print ("electronics weight: {}".format(electronics_weight))
    print ("beam weight: {}".format(beam_weight))
    print ("foam weight: {}".format(foam_weight))

    total_weight = electronics_weight + beam_weight + foam_weight
    return total_weight


def main():
    aircraft_weight = get_weight()
    aircraft_wing = wing.RightWing(weight=aircraft_weight)
    print("Right-wing aircraft.")
    print("- Aircraft weight: {}[Kg]".format(aircraft_wing.weight))
    print("- Aircraft area: {}[m^2]".format(aircraft_wing.area))
    print("- Aircraft lift: {}[m^2]".format(aircraft_wing.lift))
    print("- Aircraft cruise speed: {}[m/s]".format(aircraft_wing.cruise_speed))
    print("- Wing span: {}[m]".format(aircraft_wing.wing_span))
    print("- Wing tip chord: {}[m]".format(aircraft_wing.chord_tip))
    print("- Wing root chord: {}[m]".format(aircraft_wing.chord_root))
    return


if __name__ == "__main__":
    main()