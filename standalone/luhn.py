# This algorithm is a check 10 algorithm, meaning it checks numbers against modulo 10
# to determine the validity of a string of identification numbers.

import re

def luhn_check(number):
    """
    Computes the checksum of a given string of digits and appends the check digit to the end for verification purposes.

    Arguments:
        number {1} -- Numeric data string

    Returns:
        string -- Original number with its check digit appended
    """
    checksum = 0

    # Strip out non-numeric characters
    number = re.sub(r"\D", '', number)

    # Compute the sum of the digits of the double of every other digit including the last one.
    for datum in number[-1::-2]:
        entry = 2 * int(datum)
        digits = list(str(entry))
        digit_sum = sum(map(int, digits))

        print(f"Sum of the digits in the number {entry}: {digit_sum}")
        checksum += digit_sum

    # Add the rest of the digits as-is
    for datum in number[-2::-2]:
        checksum += int(datum)

    print(f"Checksum: {checksum}")

    check_digit = 10 - (checksum % 10)
    print(f"Check digit: {check_digit}")

    return number + str(check_digit)

test_num = "4151-6633-4328-7903"
checked_num = luhn_check(test_num)

print(f"\n\nNumber with check digit: {checked_num}")
print(f"Original number: {test_num}")

if test_num[-1] == checked_num[-1]:
    print("The number checks out and it is therefore valid!")
else:
    print(f"The number is not valid - check digits {test_num[-1]} and {checked_num[-1]} do not match.")
