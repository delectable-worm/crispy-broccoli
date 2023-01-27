# TODO
from cs50 import get_int
while(True):
    rows = get_int("Height: ")
    if rows>0 and rows<9:
        break

for i in range(rows):
    print(" "*(rows-i-1), end="")
    print("#"*(i+1), end="")
    print("  ", end="")
    print("#"*(i+1))