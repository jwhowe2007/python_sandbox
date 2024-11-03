def minion_game(string):
    vowels, n, scores = 'AEIOU', len(s), {'Kevin': 0, 'Stuart': 0}

    print(list(enumerate(s)))
    for i, char in enumerate(s):
        print(n - i)
        print(scores)
        scores['Kevin' if char in vowels else 'Stuart'] += n - i

    winner = max(scores, key=scores.get)
    print(f"{winner} {scores[winner]}" if len(set(scores.values())) > 1 else 'Draw')

if __name__ == '__main__':
    s = input().strip()
    minion_game(s)
