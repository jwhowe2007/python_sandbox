# Enter your code here. Read input from STDIN. Print output to STDOUT
import re, string;

def reverse_word(word):
    reversed = ""
    for letter in word:
        reversed = letter + reversed
    return reversed

def is_palindrome(word):
    return word == reverse_word(word)

def check_all_palindromes(arr):
    for word in arr:
        word = re.sub("[\\W_]", "", word)
        if is_palindrome(word.strip().lower()) == False:
            return False

    return True

words = ["Bob", "Otto", "Si loops spool is!", "Foof"]
print(check_all_palindromes(words))

