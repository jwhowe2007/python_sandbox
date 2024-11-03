def merge_the_tools(string, k):
    n = len(string)

    # Split the string into k substring chunks
    substrings = [string[i:i + k] for i in range(0, n, k)]

    # Dedupe the repeat strings (collapse them into the first character)
    substrings = [''.join(list(dict.fromkeys(substring))) for substring in substrings]


if __name__ == '__main__':
    s = input().strip()
    k = int(input())
    merge_the_tools(s, k)
