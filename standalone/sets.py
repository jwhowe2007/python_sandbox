set_data_file = 'set_data.txt';

with open(set_data_file, 'r') as file:
    set_data_content = file.read()

set_data_lines = list(map(str.strip, set_data_content.split('\n')))
test_cases = int(set_data_lines[0])

for i in range(0, test_cases):
    set_A_length = int(set_data_lines[i*test_cases + 1])
    set_A = set(map(int, set_data_lines[i*test_cases + 2].split(' ')))

    set_B_length = int(set_data_lines[i*test_cases + 3])
    set_B = set(map(int, set_data_lines[i*test_cases + 4].split(' ')))

    print(set_A.issubset(set_B))
