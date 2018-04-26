#!/usr/bin/python3
# Standard libraries
from abc import ABC, abstractmethod

class Wing(ABC):
    """
    Abstract class defining the basic wing properties and methods.
    """
    # density calculated with (dewpoint=6C, temp=15C, H=43m, P=1008HPa(43m))
    AIR_DENSITY = 1.214 # [kg/m^3]
    GRAVITY = 9.81
    # Increases the weight of the aircraft with the specified factor.
    WEIGHT_CORRECTION = 1.5

    def __init__(self, weight=0.2, aircraft_span=1.2, cruise_speed=10):
        # Aircraft physical properties, constrained by designer
        self.weight = weight #kg
        self.aircraft_span = aircraft_span # m
        self.wing_span = self.aircraft_span / 2
        self.area = None
        self.chord_root = None
        self.chord_tip = None
        # Aerodynamics properties
        self.cruise_speed = cruise_speed #m/s
        self.lift = None
        self.mac = None
        # Coefficient obtained from tables.
        self.C_l = 0.2
        # Initialization methods
        self.get_lift()
        self.get_area()
        self.get_wing_chords()
        self.get_mac()

    def get_lift(self):
        """
        Calculation of the lift force, needed to compensate the gravity.
        """
        F_g = self.weight * self.GRAVITY
        self.lift = F_g * self.WEIGHT_CORRECTION
        return

    def get_area(self):
        """
        Total area of the aircraft, constrained by the lift force.
        """
        # Area obtained using the lift force equation.
        area = (2*self.lift*self.AIR_DENSITY) / (self.C_l*self.cruise_speed**2)
        self.area = area
        return

    def get_wing_chords(self, wing_area, aircraft_span=1.2)
        """
        Get the length of the chords at the tip and root of the wings.
        """
        # TODO: Complete the mathod.
        wing_span = aircraft_span / 2
        # Get the chords at the tip and root, in function of the wing_span
        # Trapezoid area = (wing_span/2) * (chord_tip + chord_root)
        chord_tip = None
        chord_root = None
        return (chord_root, chord_tip)

    @abstractmethod
    def get_mac(self):
        """
        Abstract method for getting the Mean Aerodynamic Chord (MAC).

        Obtained using a geometrical rule-of-thumb.

        http://airfieldmodels.com/information_source/
        math_and_science_of_model_aircraft/formulas/mean_aerodynamic_chord.htm
        """
        return

    @abstractmethod
    def get_wing_ymean(self):
        """
        Abstract method for getting the y coord. of the center of mass.
        """
        return


class RightWing(Wing):
    """
    Basic wing class, with a right trapezoid shape.
    """
    def __init__(self, weight=0.2, aircraft_span=1.2, cruise_speed=10)
        Wing.__init__(self, weight, aircraft_span, cruise_speed)

    def get_mac(self):
        """
        Mean Aerodynamic Chord (MAC).

        Obtained using a geometrical rule-of-thumb.

        http://airfieldmodels.com/information_source/
        math_and_science_of_model_aircraft/formulas/mean_aerodynamic_chord.htm
        """
        root_side = 3 * self.chord_root
        tip_side = 2*self.chord_root + self.chord_tip
        # Get the linear equation defining the diagonal segments of the,
        # trapezoid and find the point where they cross. (Y = a*X + b)
        # 1st diagonal equation
        b_1 = 0
        a_1 = root_side / self.wing_span
        # 2nd diagonal equation
        b_2 = tip_side
        a_2 = -b_2 / self.wing_span
        # Find the crossing coordinates (Y_1=Y_2, X_1=X_2)
        X_crossing = (b_2-b_1) / (a_1-a_2)
        Y_crossing = X_crossing * a_1 + b_1
        # The MAC is the sum of 2 lengths: the root_span plus the height of the 
        # trapezoid triangle at that point (the crossing)
        # Thales theorem for getting the triangle height at X_crossing
        h = ((self.wing_span-X_crossing) * (self.chord_tip-self.chord_root)
            / self.wing_span)
        self.mac = self.chord_root + h
        return

    def get_wing_ymean(self):
        """Calculate wing Y_mean"""
        return


class ObtuseWing(Wing):
    """
    Wing class representing an obtuse trapezoid shape.

    Wing_Area = wing_span/2 * (b_t + b_r + d/2 - 1)
    """
    def __init__(self, weight=0.2, aircraft_span=1.2, cruise_speed=10,
                 displacement=0.2)
        Wing.__init__(self, weight, aircraft_span, cruise_speed)
        # Displacement from the right trapezoid
        self.displacement = displacement # m
    
    def get_displacement(self):
        """
        Calculate the displacement from the ideal right trapezoid.Wing

        The calculation is constrained by the distance to the center of
        gravity rule-of-thumb.
        """
        return

    def get_mac(self):
        """
        Mean Aerodynamic Chord (MAC)

        Obtained using a geometrical rule-of-thumb.

        http://airfieldmodels.com/information_source/
        math_and_science_of_model_aircraft/formulas/mean_aerodynamic_chord.htm
        """
        root_side =  self.chord_tip + self.displacement + 2*self.chord_root
        tip_side = self.chord_tip + 2*self.chord_root
        # Get the linear equation defining the diagonal segments of the,
        # trapezoid and find the point where they cross. (Y = a*X + b)
        # 1st diagonal equation
        b_1 = 0
        a_1 = root_side / self.wing_span
        # 2nd diagonal equation
        b_2 = tip_side
        a_2 = ((self.chord_tip+self.displacement-self.chord_root-tip_side)
              / self.wing_span)
        # Find the crossing coordinates (Y_1=Y_2, X_1=X_2)
        X_crossing = (b_2-b_1) / (a_1-a_2)
        Y_crossing = X_crossing * a_1 + b_1
        # Find the MAC. Parametrize both edges of the wing, and subtract the
        # y-coordinates for getting the MAC.
        # Eq. parameters for the top edge.
        a_top = ((self.chord_tip-self.chord_root+self.displacement)
               / self.wing_span)
        b_top = 0
        # Eq. parameters for the bottom edge.
        a_bottom = self.displacement / self.wing_span
        b_bottom = self.chord_tip
        # Find and subtract the y-coordinate for both edges at the X-crossing.
        y_top = a_top * X_crossing + b_top
        y_bottom = a_bottom * X_crossing + b_bottom
        self.mac = y_top - y_bottom
        return

    def get_wing_ymean(self):
        """Calculate wing Y_mean"""
        return