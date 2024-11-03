# Enter your code here. Read input from STDIN. Print output to STDOUT
import numpy

n, m = map(int, input().strip().split(' '))
a, b = numpy.empty((0, m), int), numpy.empty((0, m), int)

# Get the rows for matrix A
for i in range(0, n):
    input_list = list(map(int, input().strip().split(' ')))
    input_array = numpy.array([input_list])
    a = numpy.append(a, input_array, axis=0)

# Get the rows for matrix B
for i in range(0, n):
    input_list = list(map(int, input().strip().split(' ')))
    input_array = numpy.array([input_list])
    b = numpy.append(b, input_array, axis=0)

print(a + b)
print(a - b)
print(a * b)
print(a // b)
print(a % b)
print(a ** b)
