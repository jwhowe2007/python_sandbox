if __name__ == '__main__':
    N = int(input())
    commands = []
    data_list = []

    for i in range(N):
        commands.append(input())

    for operation in commands:
        op_args = operation.split(' ')
        op = op_args[0]

        if op == 'append':
            data = int(op_args[1])
            data_list.append(data)
        elif op == 'insert':
            index = int(op_args[1])

            if index is not None and index >= 0:
                data_list.insert(index, int(op_args[2]))
        elif op == 'remove':
            datum = int(op_args[1])
            data_list.remove(datum)
        else:
            operations = {
                'print': lambda data: print(data),
                'sort': lambda data: data.sort(),
                'pop': lambda data: data.pop(),
                'reverse': lambda data: data.reverse()
            }
            operations[op](data_list)

