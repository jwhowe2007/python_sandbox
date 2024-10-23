if __name__ == '__main__':
    def print_pattern(max_lines, reverse = False):
        pattern_range = range(max_lines // 2) if not reverse else range(max_lines // 2)[::-1]

        for i in pattern_range:
            repeat = 2*i + 1
            odd_design = design * repeat
            print(f"{odd_design:-^{m}s}")

    data = list(map(int, input().split(' ')))
    n = int(data[0])
    m = int(data[1])

    center = 'WELCOME'

    # The design must use only these chars
    chars = ['|', '.', '-']
    design = '.|.' # Repeating design in the pattern 1, 3, 5... (odd sets)

    # print the top of the design
    print_pattern(n)
    print(f"{center:-^{m}s}")
    print_pattern(n, reverse = True)

