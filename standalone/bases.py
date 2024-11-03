import math

def print_formatted(number):
    # your code goes here
    for i in range(1, number + 1):
        field_width = int(math.log2(number)) + 1
        print(f"{i:>{field_width}d} {i:>{field_width}o} {i:>{field_width}X} {i:>{field_width}b}")

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)
