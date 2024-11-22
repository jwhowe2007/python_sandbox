# Enter your code here. Read input from STDIN. Print output to STDOUT

def sum_divisible_by_3_or_5_not_both(numbers):
    total = 0

    for num in numbers:
        if num % 3 == 0 or num % 5 == 0:
            total += num
        if num % 15 == 0:
            total -= num

        print(f"{num}: {total}")

    return total

print(sum_divisible_by_3_or_5_not_both([1,3,5,6,7,8,9,15,30,22,25,50,75]))
