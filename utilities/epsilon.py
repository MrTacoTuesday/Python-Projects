from enum import ReprEnum
from sys import float_info

__all__ = {"Epsilon"}

class Epsilon(float, ReprEnum):
    Integral = 1
    FloatingPoint = float_info.epsilon