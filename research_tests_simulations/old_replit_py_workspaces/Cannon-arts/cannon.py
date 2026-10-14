from math import degrees, radians
from typing_extensions import Self

from cannon_fx import air_time, launching_time, launching_velocity, maximum_x, maximum_y


class Cannon:
    """
    Provides context for cannon-shooting calculations, assumes stand height is 1 meter
    """

    def __init__(self: Self, length: float, load: float) -> None:
        """
        param length: length of cannon in meters
        param load: mass of the cannon ball in kilograms
        """

        self.length = length
        self.load = load

    def getMaxRange(self: Self, angle: float) -> float:
        """
        Calculates the maximum horizontal distance the cannon can shoot.
        param angle: Angle of the cannon from the ground in radians
        """

        return maximum_x(self.length, self.load, angle)

    def getMaxHeight(self: Self, angle: float) -> float:
        """
        Calculates the maximum vertical distance the cannon can shoot.
        param angle: Angle of the cannon from the ground in radians
        """

        return maximum_y(self.length, self.load, angle)

    def getLaunchVelocity(self: Self, angle: float) -> float:
        """
        Speed at which the cannonball leaves the cannon.
        param angle: Angle of the cannon from the ground in radians
        """

        return launching_velocity(self.length, self.load, angle)

    def getLaunchTime(self: Self, angle: float) -> float:
        """
        Time it takes for the cannonball to leave the cannon.
        param angle: Angle of the cannon from the ground in radians
        """

        return launching_time(self.length, self.load, angle)

    def getAirTime(self: Self, angle: float) -> float:
        """
        Time the cannonball takes to land on the ground after being fired.
        param angle: Angle of the cannon from the ground in radians
        """

        return air_time(self.length, self.load, angle)

    def test(self: Self, angle: float | None = None) -> None:
        if angle is None:
            theta = radians(
                float(input("Enter the angle of the cannon (DEG): ")))
        else:
            theta = angle
            print(
                f"Angle of the cannon is set at {degrees(theta):.1f} degrees")

        vel = self.getLaunchVelocity(theta)
        time = self.getLaunchTime(theta)
        print(
            f"Successfully launched in {time:.3f}s with a speed of {vel:.2f}m/s"
        )

        height = self.getMaxHeight(theta)
        print(f"\tPeak Height: {height:.2f}m")

        range = self.getMaxRange(theta)
        print(f"\tRange: {range:.2f}m")

        airtime = self.getAirTime(theta)
        print(f"\tAirtime: {airtime:.2f}s")
