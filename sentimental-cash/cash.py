# TODO
from cs50 import get_float

def main():
    while(True):
        cash = get_float("Change owed: ")
        if cash > 0:
            break

    cents = cash * 100
    q = get_quarters(cents)
    cents = cents - 25*q

    n = get_nickels(cents)
    cents = cents - 10*n

    d = get_dimes(cents)
    cents = cents - 5*d

    p = get_pennies(cents)
    cents = cents - p

    print(q+n+d+p)



def get_quarters(cents):
    q = int(cents/25)
    return q

def get_nickels(cents):
    d = int(cents/10)
    return d

def get_dimes(cents):
    n = int(cents/5)
    return n

def get_pennies(cents):
    p = int(cents/1)
    return p

main()