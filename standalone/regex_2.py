# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

n = int(input())
for i in range(n):
    credit_card_number = input().strip()

    valid = re.match(r"^(?!.*(\d)(?:-?\1){3,})([4-6]\d{3}(-?\d{4}){3})$", credit_card_number)

    print("Valid" if valid else "Invalid")
