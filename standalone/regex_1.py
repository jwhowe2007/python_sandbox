# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

def validate_uid(uid):
    valid = False

    if len(uid) == 10:
        print("UID:", uid)
        criterion_1 = re.match(r"^.*(.*[A-Z]){2,}.*$", uid)
        criterion_2 = re.match(r"^.*(.*\d){3,}.*$", uid)
        criterion_3 = re.match(r"^\w*$", uid, re.A)
        criterion_4 = re.match(r"^(?:(\w)(?!.*\1))*$", uid)

        if (criterion_1 is None):
            print("Must contain at least 2 uppercase English letters.")
        if (criterion_2 is None):
            print("Must contain at least 3 digits.")
        if (criterion_3 is None):
            print("Must only contain alphanumeric characters.")
        if (criterion_4 is None):
            print("No character should repeat.")

        valid = criterion_1 and criterion_2 and criterion_3 and criterion_4

    return valid

n = int(input())
for i in range(n):
    uid = input().strip()
    print("Valid" if validate_uid(uid) else "Invalid")
