__author__ = 'Unit'
from random import randint

def IsNumberOddOrEven(NumberToTest): # Useful for determining whether a day or a night is odd or even
    if (NumberToTest % 2 == 0):
        return 'Even'
    else:
        return 'Odd'

def ReturnFromList1RandomItemNotInList2(List1,List2): # Input two lists, return from the first a random item that's not in the second
    # First, go through List2. Check each item. If Item in List1, remove that Item from List1
    for i in List2:
        if List1.count(i) > 0:
            List1.remove(i)
    # Then, pick a
    return List1[randint(0,len(List1)-1)]

