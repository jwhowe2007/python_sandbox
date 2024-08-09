import math

"""
    Args:
        point1 - tuple of two real number coordinates indicating start point of line (defaults to origin)
        point2 - tuple of two real number coordinates indicating end point of line (defaults to origin)
"""
def distance_between_linear_points(point_1: tuple[float, float]=(0,0), point_2: tuple[float, float]=(0,0)):
    # Modelling linear lengths on a 2-dimensional Cartesian Grid using points as tuples
    print(point_1, point_2)

    # Unpack both tuples
    x1, y1 = point_1
    x2, y2 = point_2

    x_length = math.fabs(x2-x1)
    y_length = math.fabs(y2-y1)
    distance = 0


    if (x_length != 0 or y_length != 0):
        if (x_length == y_length):
            if (x_length == 0):
                return distance

            distance = math.sqrt(2) * x_length
        else:
            distance = math.sqrt(x_length ** 2 + y_length ** 2)

    return distance

point1 = (0.0, 0.0)
point2 = (1.0, 1.0)
length = distance_between_linear_points(point1, point2)
null_length = distance_between_linear_points()

print("The distance between", point1, "and", point2, "is:", length)
print("The null distance is:", null_length)

