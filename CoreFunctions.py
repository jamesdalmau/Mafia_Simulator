__author__ = 'Unit'

# Alignment="Town" or "Mafia" or "Neither"
# Team=0 (for no team) or the number of the team
# Survivor="Yes" or "No" (If yes, Alignment should be "Neither" and Team should be 0)
# BelovedPrincess="Yes" or "No" (If yes, Alignment should be "Town")
# LynchBomb="Yes" or "No"
# NightBomb="Yes" or "No"
# InnocentChild="Yes" or "No"
# FriendlyNeighbour="Yes", "Odd", "Even" or "No"
# Saulus="Yes" or "No"
# Judas="Yes" or "No"
# Cop="Yes", "Odd", "Even" or "No" --- note, must add record of who the cop has investigated
# Doctor="Yes", "Odd", "Even" or "No"
# Roleblocker="Yes", "Odd", "Even" or "No"
# Busdriver="Yes", "Odd", "Even" or "No"
# Vigilante="Yes", "Odd", "Even" or "No"
# TeamRecruiter="Yes" or "No" (If yes, Alignment should be "Town")
# DeputyCop="Yes" or "No"
# DeputyDoctor="Yes" or "No"
# DeputyRoleblocker="Yes" or "No"
# DeputyBusdriver="Yes" or "No"
# DeputyVigilante="Yes" or "No"
# DeputyTeamRecruiter="Yes" or "No"
# NightKillResistant=-1 (for invulnerable), 0 (for normal), otherwise X-shot
# LynchResistant=-1 (for invulnerable), 0 (for normal), otherwise X-shot

from random import randint  # This gets the function that is used to get a random integer between two numbers


def InitiateVariables():
    global PlayerID
    global PlayerList
    global PlayerAttributes
    PlayerID = 0  # This zeroes the counter that is used by function AddPlayer when populating the player list
    PlayerList = []  # This creates an empty list to fill with players
    PlayerAttributes = (
        'Alignment', 'Team', 'Survivor',
        ## This is a list of all the attributes that players get created with
        'BelovedPrincess', 'LynchBomb', 'NightBomb', 'InnocentChild', 'FriendlyNeighbour', 'Saulus', 'Judas',
        'Cop', 'Doctor', 'Roleblocker', 'Busdriver', 'Vigilante', 'TeamRecruiter',
        'DeputyCop', 'DeputyDoctor', 'DeputyRoleblocker', 'DeputyBusdriver', 'DeputyVigilante', 'DeputyTeamRecruiter',
        'NightKillResistant', 'LynchResistant')


def IsNumberOddOrEven(NumberToTest):  # Useful for determining whether a day or a night is odd or even
    if (NumberToTest % 2 == 0):
        return 'Even'
    else:
        return 'Odd'


def ReturnFromList1RandomItemNotInList2(List1,
                                        List2):  # Input two lists, return from the first a random item that's not in the second
    # First, go through List2. Check each item. If Item in List1, remove that Item from List1
    for i in List2:
        if List1.count(i) > 0:
            List1.remove(i)
    # Then, pick a randum
    return List1[randint(0, len(List1) - 1)]


def CreatePlayerList():
    global PlayerID
    PlayerID += 1
    Alignment = ""
    Team = ""
    Survivor = ""
    BelovedPrincess = ""
    LynchBomb = ""
    NightBomb = ""
    InnocentChild = ""
    FriendlyNeighbour = ""
    Saulus = ""
    Judas = ""
    Cop = ""
    Doctor = ""
    Roleblocker = ""
    Busdriver = ""
    Vigilante = ""
    TeamRecruiter = ""
    DeputyCop = ""
    DeputyDoctor = ""
    DeputyRoleblocker = ""
    DeputyBusdriver = ""
    DeputyVigilante = ""
    DeputyTeamRecruiter = ""
    NightKillResistant = ""
    LynchResistant = ""
    AddPlayer(PlayerID, Alignment, Team, Survivor, BelovedPrincess, LynchBomb, NightBomb, InnocentChild,
              FriendlyNeighbour, Saulus, Judas, Cop, Doctor, Roleblocker, Busdriver, Vigilante, TeamRecruiter,
              DeputyCop, DeputyDoctor, DeputyRoleblocker, DeputyBusdriver, DeputyVigilante, DeputyTeamRecruiter,
              NightKillResistant, LynchResistant)


def AddPlayer(PlayerIDToInsert, Alignment, Team, Survivor, BelovedPrincess, LynchBomb, NightBomb, InnocentChild,
              FriendlyNeighbour, Saulus, Judas, Cop, Doctor, Roleblocker, Busdriver, Vigilante, TeamRecruiter,
              DeputyCop, DeputyDoctor, DeputyRoleblocker, DeputyBusdriver, DeputyVigilante, DeputyTeamRecruiter,
              NightKillResistant, LynchResistant):
    global PlayerList
    PlayerToAdd = []
    PlayerToAdd['Playerid'] = PlayerIDToInsert
    for Attribute in PlayerAttributes:
        exec("PlayerToAdd['" + Attribute + "']=" + Attribute)
    PlayerToAdd['HasInvestigated']=0
    PlayerToAdd['BeingBusDrivenWith']=0
    PlayerToAdd['NumberOfNamesInHat']=100
    PlayerList.append(PlayerToAdd)
    PlayerToAdd.clear()
