# Hackerrank Logo
if __name__ == "__main__":
    thickness = int(input())
    c = 'H'

    def top_cone():
        for i in range(thickness):
            print((c * i).rjust(thickness - 1) + c + (c * i).ljust(thickness - 1))

    def pillars():
        for i in range(thickness + 1):
            print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))

    def belt():
        for i in range((thickness + 1) // 2):
            print((c * thickness * 5).center(thickness * 6))

    def bottom_cone():
        for i in range(thickness):
            print(((c * (thickness - (i + 1))).rjust(thickness) + c + (c * (thickness - (i + 1))).ljust(thickness)).rjust(thickness * 6))


    top_cone()
    pillars()
    belt()
    pillars()
    bottom_cone()
