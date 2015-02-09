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
    global PlayerList
    PlayerID=1
    PlayerSetupFile = list(open('players.txt', 'r')) #Read players.txt and create a list
    Alignment=""            # "Town" or "Mafia" or "Neither"
    Team=""                      # 0 (for no team) or the number of the team (Town and Mafia team numbers must be different)
    Survivor=""               # "Yes" or "No" (If yes, Alignment should be "Neither" and Team should be 0)
    BelovedPrincess=""        # "Yes" or "No" (If yes, Alignment should be "Town")
    LynchBomb=""              # "Yes" or "No"
    NightBomb=""              # "Yes" or "No"
    InnocentChild=""          # "Yes" or "No"
    FriendlyNeighbour=""      # "Yes", "Odd", "Even" or "No"
    Saulus=""                 # "Yes" or "No" (If yes, Alignment should be "Mafia" and Team should be 0)
    Judas=""                  # "Yes" or "No" (If yes, Alignment should be "Town")
    Cop=""                    # "Yes", "Odd", "Even" or "No" --- note, must add record of who the cop has investigated
    Doctor=""                 # "Yes", "Odd", "Even" or "No"
    Roleblocker=""            # "Yes", "Odd", "Even" or "No"
    Busdriver=""              # "Yes", "Odd", "Even" or "No"
    Vigilante=""              # "Yes", "Odd", "Even" or "No"
    TeamRecruiter=""          # "Yes" or "No" (If yes, Alignment should be "Town")
    DeputyCop=""              # "Yes" or "No"
    DeputyDoctor=""           # "Yes" or "No"
    DeputyRoleblocker=""      # "Yes" or "No"
    DeputyBusdriver=""        # "Yes" or "No"
    DeputyVigilante=""        # "Yes" or "No"
    DeputyTeamRecruiter=""    # "Yes" or "No"
    NightKillResistant=""        # -1 (for invulnerable), 0 (for normal), otherwise X-shot
    LynchResistant=""            # -1 (for invulnerable), 0 (for normal), otherwise X-shot
    PlayerToAdd = {}
    for LineFromTextFile in PlayerSetupFile:
        if LineFromTextFile[:3] == '***':   # If the line is "***" it's time to add the Player to the List
            PlayerToAdd['PlayerID']=PlayerID    # New PlayerID is not take from text file but dynamically generated
            if PlayerToAdd['InnocentChild'] == "Yes":
                PlayerToAdd['NumberOfNamesInHat'] = 0
            else:
                PlayerToAdd['NumberOfNamesInHat'] = 100
            PlayerList.append(PlayerToAdd.copy())  # Add PlayerToAdd to the global PlayerList list
            PlayerID += 1
            PlayerToAdd.clear() # Empty PlayerToAdd so that the next player can be assembled
        else:   # If the line is not "***", interpret the line to add it to the PlayerToAdd dictionary
            exec("PlayerToAdd['" + LineFromTextFile.replace("=", "']="))

InitiateVariables()
CreatePlayerList()


def ReturnAllPlayersWhereVariableIsComparator(Variable,Comparator):
    ListToReturn = []
    for Player in PlayerList:
        PlayerIdToAddToList=""
        VariableRetrieved=""
        exec("VariableRetrieved = Player['" + Variable +"']")
        If VariableRetrieved = Comparator
