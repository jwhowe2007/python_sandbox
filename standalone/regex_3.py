regex_integer_in_range = r"[1-9]\d{5}"	# Do not delete 'r'.
regex_alternating_repetitive_digit_pair = r"(?:(\d)(?=\d\1)+)"	# Do not delete 'r'.


import re
string = input()

print(re.findall(regex_alternating_repetitive_digit_pair, string))

print (bool(re.match(regex_integer_in_range, string))
and len(re.findall(regex_alternating_repetitive_digit_pair, string)) < 2)
