# Enter your code here. Read input from STDIN. Print output to STDOUT
def triangle(n):
    # Print a triangle of numbers from 1 to n
    # ex with n = 3:
    # 1
    # 22
    # 333
    step = ""
    for i in range(1, n):
        step = str(i) * i
        print(f"{step:<{n}}")

triangle(46)
