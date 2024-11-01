# junk file for code snippets
def count_substring(string, sub_string):
    count = 0
    for i in string:
        if sub_string in string:
            i = string.find(sub_string)
            string = string[i+1:]
            count += 1

    return count

if __name__ == "__main__":
    string = input("Main String:").strip()
    sub_string = input("Substring:").strip()

    count = count_substring(string, sub_string)
    print(count)
