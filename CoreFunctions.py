__author__ = 'Unit'

from random import randint  # This gets the function that is used to get a random integer between two numbers


def InitiateVariables():
    global PlayerID
    global PlayerList
    global PlayerAttributes
    PlayerID = 0  # This zeroes the counter that is used by function AddPlayer when populating the player list
    PlayerList = []  # This creates an empty list to fill with players
    PlayerAttributes = (
        'Alignment', 'Team', 'Survivor',
        # This is a list of all the attributes that players get created with
        'BelovedPrincess', 'LynchBomb', 'NightBomb', 'InnocentChild', 'FriendlyNeighbour', 'Saulus', 'Judas',
        'Cop', 'Doctor', 'Roleblocker', 'Busdriver', 'Vigilante', 'TeamRecruiter',
        'DeputyCop', 'DeputyDoctor', 'DeputyRoleblocker', 'DeputyBusdriver', 'DeputyVigilante', 'DeputyTeamRecruiter',
        'NightKillResistant', 'LynchResistant')


def IsNumberOddOrEven(NumberToTest):  # Useful for determining whether a day or a night is odd or even
    if NumberToTest % 2 == 0:
        return 'Even'
    else:
        return 'Odd'


def ReturnOneListWithCommonItemsFromTwoLists(List1, List2):
    for i in List2:
        if List1.count(i) > 0:
            List1.remove(i)
    return List1


def ReturnOneListWithCommonItemsFromThreeLists(List1, List2, List3):
    return ReturnOneListWithCommonItemsFromTwoLists(ReturnOneListWithCommonItemsFromTwoLists(List1, List2),List3)


def ReturnOneListWithCommonItemsFromFourLists(List1, List2, List3, List4):
    return ReturnOneListWithCommonItemsFromTwoLists(ReturnOneListWithCommonItemsFromThreeLists(List1,List2,List3),List4)


def PickRandomItemFromList(List1):
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


# noinspection PyUnusedLocal
def AddPlayer(PlayerIDToInsert, Alignment, Team, Survivor, BelovedPrincess, LynchBomb, NightBomb, InnocentChild,
              FriendlyNeighbour, Saulus, Judas, Cop, Doctor, Roleblocker, Busdriver, Vigilante, TeamRecruiter,
              DeputyCop, DeputyDoctor, DeputyRoleblocker, DeputyBusdriver, DeputyVigilante, DeputyTeamRecruiter,
              NightKillResistant, LynchResistant):
    global PlayerList
    PlayerToAdd = []
    PlayerToAdd['Playerid'] = PlayerIDToInsert
    for Attribute in PlayerAttributes:
        exec("PlayerToAdd['" + Attribute + "']=" + Attribute)
    PlayerToAdd['HasInvestigated'] = 0
    PlayerToAdd['BeingBusDrivenWith'] = 0
    PlayerToAdd['NumberOfNamesInHat'] = 100
    PlayerList.append(PlayerToAdd)
    PlayerToAdd.clear()
