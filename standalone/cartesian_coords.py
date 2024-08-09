import math

# Modelling linear lengths on a 2-dimensional Cartesian Grid using points as tuples
coords_origin = (0,0)
line_point_1 = (2,2)
line_point_2 = (-4,-2)

x0, y0 = coords_origin
x1, y1 = line_point_1
x2, y2 = line_point_2

x_length = math.fabs(x2-x1)
y_length = math.fabs(y2-y1)

if (x_length == y_length):
    line_length = math.sqrt(2) * x_length
else:
    line_length = math.sqrt(x_length ** 2 + y_length ** 2)

print("The distance between", line_point_1, "and", line_point_2, "is:", line_length)

one_el_tuple = (1)
foo = one_el_tuple

print(one_el_tuple)
print(foo)
