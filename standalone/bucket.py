# Enter your code here. Read input from STDIN. Print output to STDOUT
import math, cProfile, pstats, io
from pstats import SortKey

def isPrime(n):
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True

def isPrime2(n):
    factors = [factor for factor in range(2,n) if n % factor == 0]
    if len(factors) > 0:
        return False

    return True

def isPrime3(n):
    for i in range(1,n+1):
        if i != 1 and i != n and n % i == 0:
            return False

    return True

for num in range(2,1000000):
    prime1_solution = isPrime(num)
    prime2_solution = isPrime2(num)
    prime3_solution = isPrime3(num)

    print(f"Number: {num}\tPrime1: {prime1_solution}\tPrime2: {prime2_solution}\tPrime3: {prime3_solution}")
    if (prime1_solution != prime2_solution or prime1_solution != prime3_solution):
        print(f"Mismatch at number {num}");

#pr = cProfile.Profile()
#pr.enable()
#for num in range(2,1000000):
    #print(f"Number: {num}\tPrime: {isPrime(num)}")
#    prime = isPrime(num)
#pr.disable()
#s = io.StringIO()
#sortby = SortKey.CUMULATIVE
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print(s.getvalue())
