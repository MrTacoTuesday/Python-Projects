from math import cos, degrees, radians


def stride(height: float, leg_length: float = -1, knee_extensibility: float = 1.00, foot_extensibility: float = 1.00) -> float:
    """
    Parameters:
        height (float) - height in units of X
        leg_length (float) - leg length in units of X (-1 if unknown)
        knee_extensibility (float) - percentage of how far the knee naturally moves within 105 to 165 deg when moving [0,1]
        foot_extensibility (float) - percentage of how far the foot naturally moves within -60 to 30 def when moving [0,1]
    Returns:
        float: The guestimated stride length in units of X
    """
    q = 105 + abs(knee_extensibility) * 60;
    
    A = abs(foot_extensibility) * 30;
    B = 180 - q + A;
    
    Z = 90 - abs(foot_extensibility) * 60;
    Y = q + Z - 180;
    
    leg = 0.529*height if leg_length < 0 else leg_length;
    
    return round(leg * (0.4945 * (cos(radians(A)) + cos(radians(Z))) + 0.5055 * (cos(radians(B)) + cos(radians(Y)))), 2);

def step(height: float, leg_length: float = -1, knee_extensibility: float = 1.00, foot_extensibility: float = 1.00) -> float:
    """
    Parameters:
        height (float) - height in units of X
        leg_length (float) - leg length in units of X (-1 if unknown)
        knee_extensibility (float) - percentage of how far the knee naturally moves within 105 to 165 deg when moving [0,1]
        foot_extensibility (float) - percentage of how far the foot naturally moves within -60 to 30 def when moving [0,1]
    Returns:
        float: The guestimated stride length in units of X
    """
    q = 105 + abs(knee_extensibility) * 60;
    
    A = abs(foot_extensibility) * 30;
    B = 180 - q + A;
    
    Z = 90 - abs(foot_extensibility) * 60;
    Y = q + Z - 180;
    
    leg = 0.529*height if leg_length < 0 else leg_length;
    
    return round(leg / 2 * (0.4945 * (cos(radians(A)) + cos(radians(Z))) + 0.5055 * (cos(radians(B)) + cos(radians(Y)))), 2);

    
print("Stride  :  ", stride(5*12+11), "in"); # in
print("        :    ", stride(5+11/12), "ft"); # ft

print("Step    :  ", step(5*12+11), "in"); # in
print("        :    ", step(5+11/12), "ft"); # ft

print(stride(5+10/12));