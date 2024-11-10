def freq_map(n):
    frequency_map = {}
    while n > 0:
        digit = str(n % 10)
        if digit not in frequency_map:
            frequency_map[digit] = 1
        else:
            frequency_map[digit] += 1
        n = n // 10

    return frequency_map
num = 12433634475329
print(f"Frequency map of digits in number {num}: {freq_map(num)}")
