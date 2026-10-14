from math import cos, sin, sqrt

Fc = CANNON_FORCE_PER_METER_LENGTH = 30000  # N/m
Mu = COEFFICIENT_OF_FRICTION_BETWEEN_BALL_AND_CANNON = 0.78
g = 9.81  # m/s^2


def launching_acceleration(length: float, mass: float, theta: float) -> float:
    """
    Acceleration of the ball while in the cannon.
    param length: Length of the cannon in meters.
    param mass: Mass of the cannonball in kilograms.
    param theta: Angle of the cannonball in radians.
    """

    F_applied = Fc * length / mass
    F_resistance = g * (sin(theta) - Mu * cos(theta))

    return F_applied - F_resistance


def launching_velocity(length: float, mass: float, theta: float) -> float:
    """
    Velocity of the ball when leaving the cannon.
    param length: Length of the cannon in meters.
    param mass: Mass of the cannonball in kilograms.
    param theta: Angle of the cannonball in radians.
    """

    a_launch = launching_acceleration(length, mass, theta)

    return sqrt(2 * a_launch * length)


def launching_time(length: float, mass: float, theta: float) -> float:
    """
    Time the ball takes to leave the cannon.
    param length: Length of the cannon in meters.
    param mass: Mass of the cannonball in kilograms.
    param theta: Angle of the cannonball in radians.
    """

    a_launch = launching_acceleration(length, mass, theta)

    return sqrt(2 * length / a_launch)


def air_time(length: float, mass: float, theta: float) -> float:
    """
    Time the ball takes to hit the ground after leaving the cannon.
    param length: Length of the cannon in meters.
    param mass: Mass of the cannonball in kilograms.
    param theta: Angle of the cannonball in radians.
    """

    Vy = launching_velocity(length, mass, theta) * sin(theta)
    Ly = length * sin(theta)

    return (Vy + sqrt(Vy**2 + 2 * g * (
        Ly + 1
    ))) / g


def maximum_y(length: float, mass: float, theta: float) -> float:
    """
    Peak height the ball reaches.
    param length: Length of the cannon in meters.
    param mass: Mass of the cannonball in kilograms.
    param theta: Angle of the cannonball in radians.
    """

    Vy = launching_velocity(length, mass, theta) * sin(theta)
    Ly = length * sin(theta)

    return (Vy**2 / (2 * g)) + Ly + 1


def maximum_x(length: float, mass: float, theta: float) -> float:
    """
    Peak distance the ball reaches.
    param length: Length of the cannon in meters.
    param mass: Mass of the cannonball in kilograms.
    param theta: Angle of the cannonball in radians.
    """

    Vx = launching_velocity(length, mass, theta) * cos(theta)
    t_air = air_time(length, mass, theta)
    Lx = length * cos(theta)

    return Vx * t_air + Lx

