#!/bin/python3

import math
import os
import random
import re
import sys

n, m = map(int, input().rstrip().split())
matrix = []

for _ in range(n):
    matrix_item = input()
    matrix.append(matrix_item)

decoded_strings = []
fully_decoded_string = ""

for i in range(m):
    decoded_strings.append("")

# Append all characters in the columns together
for item in matrix:
    for i in range(m):
        decoded_strings[i] += item[i]

fully_decoded_string = ''.join(decoded_strings)
pattern = r"(?<=\w)(?:[^\w]+)(?=\w)"
stripped_message = re.sub(pattern, ' ', fully_decoded_string)
print(stripped_message)


