__author__ = 'Unit'

from random import randint  # This gets the function that is used to get a random integer between two numbers
import random
import math


def InitiateGlobalVariables():
    CreatePlayerList()


def InitiateSingleGameVariables(): # Set up variables to run a single game
    global PlayerID
    PlayerID = 0  # This zeroes the counter that is used by function AddPlayer when populating the player list
    global PlayerList
    global GlobalPlayerList
    PlayerList = GlobalPlayerList  # This creates a fresh copy of the player list, for use in this specific game
    global Day
    Day = 1
    global Night
    Night = 1
    global DaysThatDoNotHappen
    DaysThatDoNotHappen = []    #This is needed for the Beloved Princess
    global NightsOnWhichThereAreNoKills
    NightsOnWhichThereAreNoKills = []   #This is needed for the Virgin
    global WinningTeam
    WinningTeam = ''


def IsNumberOddOrEven(NumberToTest):  # Useful for determining whether a day or a night is odd or even
    if NumberToTest % 2 == 0:
        return 'Even'
    else:
        return 'Odd'


def ReturnOneListWithCommonItemsFromTwoLists(List1, List2): # Pure list function
    ReturningList = []
    for i in List2:
        if List1.count(i) > 0:
            ReturningList.append(i)
    return ReturningList


def ReturnOneListWithCommonItemsFromThreeLists(List1, List2, List3):    # Pure list function
    return ReturnOneListWithCommonItemsFromTwoLists(ReturnOneListWithCommonItemsFromTwoLists(List1, List2),List3)


def ReturnOneListWithCommonItemsFromFourLists(List1, List2, List3, List4):  # Pure list function
    return ReturnOneListWithCommonItemsFromTwoLists(ReturnOneListWithCommonItemsFromThreeLists(List1,List2,List3),List4)


def PickRandomItemFromList(List1):  # Pure list function
    if List1 != []:
        return List1[randint(0, len(List1) - 1)]
    else:
        return()


def CreatePlayerList(): # Reads players.txt and makes the main list for use in a single game
    global GlobalPlayerList
    GlobalPlayerList = []
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
    TeamNightKill=""          # "Yes", "Odd", "Even" or "No" (If Alignment is "Mafia", should ordinarily not be "No")
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
            GlobalPlayerList.append(PlayerToAdd.copy())  # Add PlayerToAdd to the global PlayerList list
            PlayerID += 1
            PlayerToAdd.clear() # Empty PlayerToAdd so that the next player can be assembled
        else:   # If the line is not "***", interpret the line to add it to the PlayerToAdd dictionary
            exec("PlayerToAdd['" + LineFromTextFile.replace("=", "']="))


def SearchPlayersFor(Variable,Operator,Comparator): # Return a list of PlayerIDs for players who match criteria
    #Variable must be a simple string, the name of an item in the Player dictionary
    #Operator must be "==", "!=", ">", "<" etc
    #Comparator, if a string, needs to include quotes around itself
    ListToReturn = []
    for Player in PlayerList:
        if eval("Player['" + Variable +"'] " + Operator + " " + str(Comparator) + "") == True:
            ListToReturn.append(Player['PlayerID'])
    return ListToReturn


def GetAttributeFromPlayer(PlayerID,Attribute): # Get a value from an attribute belonging to a particular player
    for Player in PlayerList:
        if Player['PlayerID'] == PlayerID:
            return(eval("Player['" + Attribute + "']"))
            break


def WriteAttributeToPlayer(PlayerID,Attribute,ValueToWrite): # Change an attribute for a particular player
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
        CandidatePickedFromHat = PickNameFromHatForLynch(Candidates)
        #print ("Going to see if there are enough votes for " + str(CandidatePickedFromHat))
        GetsEnoughVotes, ActualVoters = WillGetEnoughLynchVotes(CandidatePickedFromHat)
        if GetsEnoughVotes == "Yes":    # See if this candidate gets enough votes
            PlayerWhoWillBeLynched = CandidatePickedFromHat
        else:
            Candidates.remove(CandidatePickedFromHat)   # If there aren't enough votes for the candidate, knock the candidate off the list
    if PlayerWhoWillBeLynched != 0:
        Lynch(PlayerWhoWillBeLynched,ActualVoters)
        if GetAttributeFromPlayer(PlayerWhoWillBeLynched,'Alive') == 'No':  #If the lynch worked
            PunishAndRewardVotersAfterLynch(ActualVoters,PlayerWhoWillBeLynched)


def Lynch(PlayerID,ActualVoters):
    if GetAttributeFromPlayer(PlayerID,'LynchResistant') == 0:  #If player isn't lynch resistant
        KillPlayer(PlayerID)    #This will not kill a Judas or Saulus
        if GetAttributeFromPlayer(PlayerID,'Alive') == 'No':    #If the player actually died
            if GetAttributeFromPlayer(PlayerID,'LynchBomb') == 'Yes':   #If player is a lynchbomb
                print("Player " + PlayerID + " was a lynchbomb.")
                KillPlayer(PickRandomItemFromList(ActualVoters))   #Kill random voter
    else:
        #If player is lynch resistant, reduce that lynch resistance by one
        WriteAttributeToPlayer(PlayerID,'LynchResistant',int(GetAttributeFromPlayer(PlayerID,'LynchResistant'))-1)
        print("Player was lynch-resistant.")


def KillPlayer(PlayerID):
    if GetAttributeFromPlayer(PlayerID,'Judas') == 'Yes' and GetAttributeFromPlayer(PlayerID,'Alignment') == 'Town': #If Player is a Judas
        WriteAttributeToPlayer(PlayerID,'Alignment','Mafia')
    elif GetAttributeFromPlayer(PlayerID,'Saulus') == 'Yes' and GetAttributeFromPlayer(PlayerID,'Alignment') == 'Mafia': #If Player is a Saulus
        WriteAttributeToPlayer(PlayerID,'Alignment','Town')
    else:   #If player is neither Judas nor Saulus (or is, but has used that power)
        WriteAttributeToPlayer(PlayerID,'Alive','No')   #kill player
        if GetAttributeFromPlayer(PlayerID,'BelovedPrincess') == 'Yes': # If player is a Beloved Princess
            print("Player " + str(PlayerID) + " was a Beloved Princess! Day " + str(Day + 1) + " will be skipped.")
            global DaysThatDoNotHappen
            DaysThatDoNotHappen.append(Day+1)


def PunishAndRewardVotersAfterLynch(Voters,LynchedPlayer):
    AlignmentOfDeadPlayer = GetAttributeFromPlayer(LynchedPlayer,'Alignment')
    #Punish and reward the voters
    for Voter in Voters:
        if AlignmentOfDeadPlayer == 'Mafia':
            ChangeToNumberOfNamesInHat = math.ceil(Day * 1.3 * randint(3,5))
            NewNumber=GetAttributeFromPlayer(Voter,'NumberOfNamesInHat')-ChangeToNumberOfNamesInHat
            print("Player " + str(Voter) + " voted to lynch a mafia.")
        elif AlignmentOfDeadPlayer == 'Town':
            ChangeToNumberOfNamesInHat = math.ceil(Day * 1.3 * randint(3,5))
            NewNumber=GetAttributeFromPlayer(Voter,'NumberOfNamesInHat')+ChangeToNumberOfNamesInHat
            print("Player " + str(Voter) + " voted to lynch a town.")
        if NewNumber<0:
            NewNumber=0
        WriteAttributeToPlayer(Voter,'NumberOfNamesInHat',NewNumber)
        print("Player " + str(Voter) + "'s odds are now " + str(NewNumber))
    #Punish and reward the non-voters
    NonVoters = SearchPlayersFor('Alive','==','"Yes"')
    for NonVoter in NonVoters:
        if NonVoter != LynchedPlayer:
            if NonVoter not in Voters:
                if AlignmentOfDeadPlayer == 'Mafia':
                    ChangeToNumberOfNamesInHat = math.ceil(Day * 1.3 * randint(2,4))
                    NewNumber = GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')+ChangeToNumberOfNamesInHat
                    print("Player " + str(NonVoter) + " didn't vote to lynch a mafia.")
                elif AlignmentOfDeadPlayer == 'Town':
                    ChangeToNumberOfNamesInHat = math.ceil(Day * 1.3 * randint(2,4))
                    NewNumber = GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')-ChangeToNumberOfNamesInHat
                    print("Player " + str(NonVoter) + " didn't vote to lynch a town.")
                if NewNumber<0:
                    NewNumber=0
                WriteAttributeToPlayer(NonVoter,'NumberOfNamesInHat',NewNumber)
                print("Player " + str(NonVoter) + "'s odds are now " + str(GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')))


def PickNameFromHatForLynch(PlayersToGoInHat):
    Hat = []
    for Player in PlayersToGoInHat:
        i = 0
        while i < int(GetAttributeFromPlayer(Player,'NumberOfNamesInHat')):
            Hat.append(Player)
            i +=1
    return(PickRandomItemFromList(Hat))


def TryToPickTownPlayer(PlayerWhoIsChoosing,PlayersNotEligible):
    UnfilteredListOfPlayersForHat = []
    PlayersToGoInHat = []
    Hat = []
    PlayersTeam = GetAttributeFromPlayer(PlayerWhoIsChoosing,"Team")
    PlayersAlignment = GetAttributeFromPlayer(PlayerWhoIsChoosing,"Alignment")
    if PlayersTeam == 0:
        #If the player is not on a team, the pool of possible townies is everyone who is still alive
        UnfilteredListOfPlayersForHat = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("PlayerID","!=",PlayerWhoIsChoosing))
    else:
        #If the player is on a team, the pool depends on the player's alignment
        if PlayersAlignment == "Mafia": # If player is mafia, list excludes that mafia team
            UnfilteredListOfPlayersForHat = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","!=",PlayersTeam))
        else: #If player isn't Mafia, list includes everyone
            UnfilteredListOfPlayersForHat = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("PlayerID","!=",PlayerWhoIsChoosing))
    if PlayersNotEligible != []: #Exclude the players who are to be excluded
        for UnfilteredPlayer in UnfilteredListOfPlayersForHat:
            if UnfilteredPlayer not in PlayersNotEligible:
                PlayersToGoInHat.append(UnfilteredPlayer)
    else:
        PlayersToGoInHat = UnfilteredListOfPlayersForHat
    for PlayerInHat in PlayersToGoInHat: #Now go through each player who's going into the hat
        NumberOfNamesFromPlayerList = int(GetAttributeFromPlayer(PlayerInHat,'NumberOfNamesInHat'))
        if NumberOfNamesFromPlayerList >=130 and GetAttributeFromPlayer(PlayerInHat,'InnocentChild') != "Yes": #If the candidate is probably mafia, don't add them.
            NumberOfTimesToGoInHat = 0
        else: #If the candidate might not be mafia, figure out how many names to add (reversing polarity)
            if NumberOfNamesFromPlayerList >= 100:
                NumberOfTimesToGoInHat = 100 - (NumberOfNamesFromPlayerList - 100)
            else:
                NumberOfTimesToGoInHat = 100 + (100 - NumberOfNamesFromPlayerList)
            if GetAttributeFromPlayer(PlayerInHat,'InnocentChild') == "Yes":
                NumberOfTimesToGoInHat = NumberOfTimesToGoInHat * 3
            if PlayersTeam != 0 and PlayersAlignment == "Town":
                if PlayersTeam == int(GetAttributeFromPlayer(PlayerInHat,"'Team'")):
                    NumberOfTimesToGoInHat = NumberOfTimesToGoInHat * 3
        #Now populate the hat
        i = 0
        while i < NumberOfTimesToGoInHat:
            Hat.append(PlayerInHat)
            i +=1
    if Hat != []:
        return(PickRandomItemFromList(Hat))
    else:
        return(0)


def TryToPickMafiaPlayer(PlayerWhoIsChoosing,PlayersNotEligible):
    UnfilteredListOfPlayersForHat = []
    PlayersToGoInHat = []
    Hat = []
    PlayersTeam = GetAttributeFromPlayer(PlayerWhoIsChoosing,"Team")
    PlayersAlignment = GetAttributeFromPlayer(PlayerWhoIsChoosing,"Alignment")
    if PlayersTeam == 0:
        #If the player is not on a team, the pool of possible mafia is everyone who is still alive
        UnfilteredListOfPlayersForHat = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("PlayerID","!=",PlayerWhoIsChoosing))
    else:
        #If the player is on a team, the pool depends on the player's alignment
        if PlayersAlignment == "Mafia": # If player is mafia, list includes everyone
            UnfilteredListOfPlayersForHat = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("PlayerID","!=",PlayerWhoIsChoosing))
        else: #If player isn't Mafia, list excludes members of the player's team
            UnfilteredListOfPlayersForHat = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","!=",PlayersTeam))
    if PlayersNotEligible != []: #Exclude the players who are to be excluded
        for UnfilteredPlayer in UnfilteredListOfPlayersForHat:
            if UnfilteredPlayer not in PlayersNotEligible:
                PlayersToGoInHat.append(UnfilteredPlayer)
    else:
        PlayersToGoInHat = UnfilteredListOfPlayersForHat
    print("Trying to find a mafia player, list in hat is " + str(PlayersToGoInHat))
    for PlayerInHat in PlayersToGoInHat: #Now go through each player who's going into the hat
        NumberOfNamesFromPlayerList = int(GetAttributeFromPlayer(PlayerInHat,'NumberOfNamesInHat'))
        if GetAttributeFromPlayer(PlayerInHat,'InnocentChild') == "Yes": #Exclude any innocent children
            NumberOfTimesToGoInHat = 0
        else:
            if PlayersTeam != 0: # if the player is on a team
                if PlayersTeam == int(GetAttributeFromPlayer(PlayerInHat,"Team")): #if the candidate is on the same team
                    if PlayersAlignment == "Town":
                        NumberOfNamesFromPlayerList = 0
                    elif PlayersAlignment == "Mafia":
                        NumberOfTimesToGoInHat = NumberOfNamesFromPlayerList * 3
                else:   #If chooser's team is not candidate's team
                    NumberOfTimesToGoInHat = NumberOfNamesFromPlayerList
            else:   # if chooser is not on a team
                NumberOfTimesToGoInHat = NumberOfNamesFromPlayerList
            if NumberOfTimesToGoInHat <= 70: #Exclude anyone who's unlikely to be mafia
                NumberOfTimesToGoInHat = 0
        #Now populate the hat
        i = 0
        while i < NumberOfTimesToGoInHat:
            Hat.append(PlayerInHat)
            i +=1
    if Hat != []:
        return(PickRandomItemFromList(Hat))
    else:
        return(0)



def WillGetEnoughLynchVotes(TargetPlayerID):
    NotTargetPlayers = SearchPlayersFor('PlayerID','!=',str(TargetPlayerID))
    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    PossibleVoters = ShuffleList(ReturnOneListWithCommonItemsFromTwoLists(LivingPlayers,NotTargetPlayers))
    ActualVoters = []
    #print("Going to see if the following players will vote 'yes': " + str(PossibleVoters))
    Votes = 0
    for Player in PossibleVoters:
        #print("Going to see if the following player will vote 'yes': " + str(Player))
        if DoesPlayer1VoteForPlayer2(Player,TargetPlayerID) == 'Yes':
            ActualVoters.append(Player)
            Votes += 1
            #print("Player " + str(Player) + " will vote yes, bringing the total votes to " + str(Votes))
            if Votes >= NumberOfVotesRequiredToLynch():
                print("They're lynching player " + str(TargetPlayerID) + " and the people voting are " + str(ActualVoters))
                return('Yes',ActualVoters)
    return('No',[])


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


def BuildListOfTeamNumbers(Alignment):   #Return a list of the numbers of the teams that have living players
    #Alignment = "Mafia", "Town", ""
    LivingPlayers = SearchPlayersFor('Alive',"==","'Yes'")
    Teams = []
    for Player in LivingPlayers: #Build a list of the teams
        IsTeamAppropriateToAddToList = "No"
        TeamNumberForThisPlayer = GetAttributeFromPlayer(Player,'Team')
        if Alignment == "":
            if TeamNumberForThisPlayer != 0:
                IsTeamAppropriateToAddToList = "Yes"
        elif GetAttributeFromPlayer(Player,'Alignment') == Alignment:
            if TeamNumberForThisPlayer != 0:
                IsTeamAppropriateToAddToList = "Yes"
        if IsTeamAppropriateToAddToList == "Yes":
            if TeamNumberForThisPlayer not in Teams:
                Teams.append(GetAttributeFromPlayer(Player,'Team'))
    return(Teams)


def SeeIfAnyOneMafiaTeamHasTheMajority():
    LivingPlayers = SearchPlayersFor('Alive',"==","'Yes'")
    Majority = NumberOfVotesRequiredToLynch()
    MafiaTeams = BuildListOfTeamNumbers("Mafia")
    print("Seeing if any one MafiaTeam out of Teams " + str(MafiaTeams) + " have " + str(Majority) + " votes.")
    for TeamNumber in MafiaTeams: #See if each scum team has the votes
        ListOfLivingPlayersInTeam = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive',"==","'Yes'"), SearchPlayersFor('Team',"==",TeamNumber))
        print("List of living players in team " + str(TeamNumber) +": " + str(ListOfLivingPlayersInTeam))
        if len(ListOfLivingPlayersInTeam) >= Majority:
            return('Yes')
    return('No')


def CheckForVictory():
    global WinningTeam
    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    MafiaPlayers = SearchPlayersFor('Alignment','==',"'Mafia'")
    LivingMafiaPlayers = ShuffleList(ReturnOneListWithCommonItemsFromTwoLists(LivingPlayers,MafiaPlayers))
    TownPlayers = SearchPlayersFor('Alignment','==',"'Town'")
    LivingTownPlayers = ShuffleList(ReturnOneListWithCommonItemsFromTwoLists(LivingPlayers,TownPlayers))
    if len(LivingMafiaPlayers) == 0:
        WinningTeam = "Town"
    elif len(LivingTownPlayers) == 0:
        WinningTeam = "Mafia"
    elif SeeIfAnyOneMafiaTeamHasTheMajority() == 'Yes':
        WinningTeam = "Mafia"


def SimulateSingleGame():
    InitiateSingleGameVariables()
    global DaysThatDoNotHappen
    global Day
    global Night
    global WinningTeam
    while WinningTeam == '':
        #Day cycle
        print()
        print("Day " + str(Day))
        if not Day in DaysThatDoNotHappen:
            TryToLynch()
        CheckForVictory()
        LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
        print("The remaining living players at the end of Day " + str(Day) + " are " + str(LivingPlayers))
        if WinningTeam != '':
            DayOrNightWhenGameEnded = "D" + str(Day)
        else:   #If no winning team at the end of the day, do the night
            Day += 1
            #Night cycle
            print()
            print("Night " + str(Night))
            NightRoutine()
            CheckForVictory()
            if WinningTeam != '':
                DayOrNightWhenGameEnded = "N" + str(Night)
            LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
            print("The remaining living players at the end of Night " + str(Night) + " are " + str(LivingPlayers))
            Night += 1


    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    print()
    print("Winners = " + WinningTeam)


def NightRoutine():
    DoAllRoleblocking()
    DoAllBusdriving()
    #DoAllInvestigating()
    #DoAllProtecting()
    #DoAllTeamNightKills()
    #DoAllVigilanteKills()


def DoAllRoleblocking():
    global PlayersBeingRoleblocked
    global Night
    PlayersBeingRoleblocked = []
    LivingRoleblockers = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("Roleblocker","!=","'No'"))
    if LivingRoleblockers != []: #If there are any roleblockers
        for Player in LivingRoleblockers:
            RoleblockerActiveTonight = "No"
            #See if this roleblocker is to be active on this particular night
            RoleblockerValueFromPlayerlist = GetAttributeFromPlayer(Player,"Roleblocker")
            if RoleblockerValueFromPlayerlist == "Yes":
                RoleblockerActiveTonight = "Yes"
            elif RoleblockerValueFromPlayerlist == IsNumberOddOrEven(Night):
                RoleblockerActiveTonight = "Yes"
            if RoleblockerActiveTonight == "Yes":
                if GetAttributeFromPlayer(Player,'Alignment') == 'Mafia':
                    PlayerToBeRoleblocked = TryToPickTownPlayer(Player,[])
                else:
                    PlayerToBeRoleblocked = TryToPickMafiaPlayer(Player,[])
                if PlayersBeingRoleblocked != 0:
                    PlayersBeingRoleblocked.append(PlayerToBeRoleblocked)
                    print("On this night, Player " + str(Player) + " is roleblocking " + str(PlayerToBeRoleblocked))


def DoAllBusdriving():
    global Busdrivings
    Busdrivings = []
    LivingBusdrivers = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("Busdriver","!=","'No'"))
    if LivingBusdrivers != []: #If there are any Busdrivers
        for Busdriver in LivingBusdrivers:
            BusdriverActiveTonight = "No"
            #See if this Busdriver is to be active on this particular night
            BusdriverValueFromPlayerlist = GetAttributeFromPlayer(Busdriver,"Busdriver")
            if BusdriverValueFromPlayerlist == "Yes":
                BusdriverActiveTonight = "Yes"
            elif BusdriverValueFromPlayerlist == IsNumberOddOrEven(Night):
                BusdriverActiveTonight = "Yes"
            if Busdriver in PlayersBeingRoleblocked: #Busdriver is inactive if roleblocked
                BusdriverActiveTonight = "No"
            if BusdriverActiveTonight == "Yes":
                BusdrivenPlayer1 = TryToPickMafiaPlayer(Busdriver,[])
                BusdrivenPlayer2 = TryToPickTownPlayer(Busdriver,[])
                if (BusdrivenPlayer1 != 0) and (BusdrivenPlayer2 != 0):
                    Busdrivings.append([BusdrivenPlayer1,BusdrivenPlayer2])
                    print("On this night, Player " + str(Busdriver) + " is busdriving Player " + str(BusdrivenPlayer1) + " and Player " + str(BusdrivenPlayer2))

InitiateGlobalVariables()
SimulateSingleGame()