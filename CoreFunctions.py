__author__ = 'Unit'

from random import randint  # This gets the function that is used to get a random integer between two numbers
import random
import math


def InitiateVariables():
    global PlayerID
    global PlayerList
    PlayerID = 0  # This zeroes the counter that is used by function AddPlayer when populating the player list
    PlayerList = []  # This creates an empty list to fill with players


def IsNumberOddOrEven(NumberToTest):  # Useful for determining whether a day or a night is odd or even
    if NumberToTest % 2 == 0:
        return 'Even'
    else:
        return 'Odd'


def ReturnOneListWithCommonItemsFromTwoLists(List1, List2):
    ReturningList = []
    for i in List2:
        if List1.count(i) > 0:
            ReturningList.append(i)
    return ReturningList


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
            PlayerToAdd['Alive']='Yes'    # Default 'Alive' to 'Yes', can change to 'No' during game
            if PlayerToAdd['InnocentChild'] == "Yes":
                PlayerToAdd['NumberOfNamesInHat'] = 0
            else:
                PlayerToAdd['NumberOfNamesInHat'] = 100
            PlayerList.append(PlayerToAdd.copy())  # Add PlayerToAdd to the global PlayerList list
            PlayerID += 1
            PlayerToAdd.clear() # Empty PlayerToAdd so that the next player can be assembled
        else:   # If the line is not "***", interpret the line to add it to the PlayerToAdd dictionary
            exec("PlayerToAdd['" + LineFromTextFile.replace("=", "']="))


def SearchPlayersFor(Variable,Operator,Comparator):
    #Variable must be a simple string, the name of an item in the Player dictionary
    #Operator must be "==", "!=", ">", "<" etc
    #Comparator, if a string, needs to include quotes around itself
    ListToReturn = []
    for Player in PlayerList:
        if eval("Player['" + Variable +"'] " + Operator + " " + Comparator + "") == True:
            ListToReturn.append(Player['PlayerID'])
    return ListToReturn


def GetAttributeFromPlayer(PlayerID,Attribute):
    for Player in PlayerList:
        if Player['PlayerID'] == PlayerID:
            return(eval("Player['" + Attribute + "']"))
            break


def WriteAttributeToPlayer(PlayerID,Attribute,ValueToWrite):
    global PlayerList
    for Player in PlayerList:
        if Player['PlayerID'] == PlayerID:
            Player[Attribute] = ValueToWrite
            break


def TryToLynch():
    Candidates = SearchPlayersFor('Alive',"==","'Yes'")
    PlayerWhoWillBeLynched = 0
    while len(Candidates) > 0 and PlayerWhoWillBeLynched == 0:  # While there are still candidates and no one has been voted for
        #print ("The current candidates for the lynch are " + str(Candidates))
        CandidatePickedFromHat = PickNameFromHat(Candidates)
        #print ("Going to see if there are enough votes for " + str(CandidatePickedFromHat))
        if WillGetEnoughLynchVotes(CandidatePickedFromHat) == "Yes":    # See if this candidate gets enough votes
            PlayerWhoWillBeLynched = CandidatePickedFromHat
        else:
            Candidates.remove(CandidatePickedFromHat)   # If there aren't enough votes for the candidate, knock the candidate off the list
    if PlayerWhoWillBeLynched != 0:
        #print("Lynching " + str(PlayerWhoWillBeLynched))


def PickNameFromHat(PlayersToGoInHat):
    Hat = []
    for Player in PlayersToGoInHat:
        i = 0
        while i < int(GetAttributeFromPlayer(Player,'NumberOfNamesInHat')):
            Hat.append(Player)
            i +=1
    return(PickRandomItemFromList(Hat))


def WillGetEnoughLynchVotes(TargetPlayerID):
    LivingPlayers = SearchPlayersFor('PlayerID','!=',str(TargetPlayerID))
    NotTargetPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    PossibleVoters = ShuffleList(ReturnOneListWithCommonItemsFromTwoLists(LivingPlayers,NotTargetPlayers))
    #print("Going to see if the following players will vote 'yes': " + str(PossibleVoters))
    Votes = 0
    for Player in PossibleVoters:
        #print("Going to see if the following player will vote 'yes': " + str(Player))
        if DoesPlayer1VoteForPlayer2(Player,TargetPlayerID) == 'Yes':
            Votes += 1
            #print("Player " + str(Player) + " will vote yes, bringing the total votes to " + str(Votes))
            if Votes >= NumberOfVotesRequiredToLynch():
                #print("That's enough for a lynch!")
                return('Yes')
    return('No')


def DoesPlayer1VoteForPlayer2(Player1,Player2):
    AnswerToReturn = 'Yes'    # The default assumption is that the vote will be cast.
    # First test to see if the vote will be nullified because of teams
    if (GetAttributeFromPlayer(Player1,'Team') != 0) and (GetAttributeFromPlayer(Player1,'Team') == GetAttributeFromPlayer(Player2,'Team')):
        if GetAttributeFromPlayer(Player1,'Alignment') == 'Mafia':
            if randint(1,3) != 1:   # Mafia that are on the same team only have a 33% chance of voting for each other
                AnswerToReturn='No'
        elif GetAttributeFromPlayer(Player1,'Alignment') == 'Town':
            if randint(1,50) != 1:   # Town that are on the same team only have a 2% chance of voting for each other
                AnswerToReturn='No'
    return(AnswerToReturn)

def NumberOfVotesRequiredToLynch():
    return(math.ceil(float(len(SearchPlayersFor('Alive','==',"'Yes'")))/2))

def ShuffleList(InputList):
    ReturnList = []
    for i in range(len(InputList)):
        element = random.choice(InputList)
        InputList.remove(element)
        ReturnList.append(element)
    return ReturnList

InitiateVariables()
CreatePlayerList()
TryToLynch()