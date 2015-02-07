__author__ = 'Unit'
from random import randint  # This gets the function that is used to get a random integer between two numbers

def InitiateVariables:
    PlayerID=0  # This zeroes the counter that is used by function AddPlayer when populating the player list
    PlayerList=[] # This creates an empty list to fill with players
    PlayerToAdd={} # This creates an empty dictionary to be used to add players to the list
    PlayerAttributes=('PlayerID','Alignment','Team','Survivor', ## This is a list of all the attributes that players get created with
                'BelovedPrincess','LynchBomb','NightBomb','InnocentChild',
                'Cop','Doctor','Roleblocker','Busdriver',
                'DeputyCop','DeputyDoctor','DeputyRoleblocker','DeputyBusdriver',
                'NightKillResistant','LynchResistant')

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
    # Then, pick a randum
    return List1[randint(0,len(List1)-1)]

def CreatePlayerList
    PlayerID = PlayerID +1
    AddPlayer()

def AddPlayer(PlayerID,Alignment,Team,Survivor,
                BelovedPrincess,LynchBomb,NightBomb,InnocentChild,
                Cop,Doctor,Roleblocker,Busdriver,
                DeputyCop,DeputyDoctor,DeputyRoleblocker,DeputyBusdriver,
                NightKillResistant,LynchResistant):
    PlayerNumber=PlayerNumber+1
    PlayerToAdd.clear()

    for Attribute in PlayerAttributes:

    exec 'PlayerToAdd[\'Alignment\']=Alignment'
    PlayerToAdd['Team']=Team
    PlayerToAdd['Su']

    PlayerT