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
    Day = 0
    global Night
    Night = 0
    global DaysThatDoNotHappen
    DaysThatDoNotHappen = []    #This is needed for the Beloved Princess
    global NightsOnWhichThereAreNoKills
    NightsOnWhichThereAreNoKills = []   #This is needed for the Virgin
    global InvestigationResults
    InvestigationResults = []
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


def ReturnBlankPlayer(PlayerID):
    PlayerToReturn = {}
    PlayerToReturn['PlayerID'] = PlayerID
    PlayerToReturn['Alignment'] = 'None'            # "Town" or "Mafia" or "None"
    PlayerToReturn['Team'] = 0                      # 0 (for no team) or the number of the team (Town and Mafia team numbers must be different)
    PlayerToReturn['BelovedPrincess'] = 'No'        # "Yes" or "No" (If yes, Alignment should be "Town")
    PlayerToReturn['Virgin'] = 'No'                 # "Yes" or "No"
    PlayerToReturn['LynchBomb'] = 'No'              # "Yes" or "No"
    PlayerToReturn['NightBomb'] = 'No'              # "Yes" or "No"
    PlayerToReturn['InnocentChild'] = 'No'          # "Yes" or "No"
    PlayerToReturn['Saulus'] = 'No'                 # "Yes" or "No" (If yes, Alignment should be "Mafia" and Team should be 0)
    PlayerToReturn['Judas'] = 'No'                  # "Yes" or "No" (If yes, Alignment should be "Town")
    PlayerToReturn['FriendlyNeighbour'] = 'No'      # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['FriendlyNeighbourShots'] = -1      # if -1, unlimited. Otherwise, # of possible investigations
    PlayerToReturn['Cop'] = 'No'                    # "Yes", "Odd", "Even" or "No" --- note, must add record of who the cop has investigated
    PlayerToReturn['CopShots'] = -1             # if -1, unlimited. Otherwise, # of possible investigations
    PlayerToReturn['Doctor'] = 'No'                 # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['DoctorShots'] = -1          # if -1, unlimited. Otherwise, # of possible doctorings
    PlayerToReturn['RoleBlocker'] = 'No'            # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['RoleBlockerShots'] = -1     # if -1, unlimited. Otherwise, # of possible roleblockings
    PlayerToReturn['BusDriver'] = 'No'              # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['BusDriverShots'] = -1       # if -1, unlimited. Otherwise, # of possible busdrivings
    PlayerToReturn['Vigilante'] = 'No'              # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['VigilanteShots'] = -1       # if -1, unlimited. Otherwise, # of possible vig kills
    PlayerToReturn['TeamRecruiter'] = 'No'          # "Yes" or "No" (If yes, Alignment should be "Town")
    PlayerToReturn['TeamNightKill'] = 'No'          # "Yes", "Odd", "Even" or "No" (If Alignment is "Mafia", should ordinarily not be "No")
    PlayerToReturn['TeamNightKillShots'] = -1   # if -1, unlimited. Otherwise, # of possible team night kills
    PlayerToReturn['DeputyCop'] = 'No'              # "Yes" or "No"
    PlayerToReturn['DeputyDoctor'] = 'No'           # "Yes" or "No"
    PlayerToReturn['DeputyRoleBlocker'] = 'No'      # "Yes" or "No"
    PlayerToReturn['DeputyBusDriver'] = 'No'        # "Yes" or "No"
    PlayerToReturn['DeputyVigilante'] = 'No'        # "Yes" or "No"
    PlayerToReturn['DeputyTeamRecruiter'] = 'No'    # "Yes" or "No"
    PlayerToReturn['NightKillResistant'] = 0        # -1 (for invulnerable), 0 (for normal), otherwise X-shot
    PlayerToReturn['LynchResistant'] = 0            # -1 (for invulnerable), 0 (for normal), otherwise X-shot
    return(PlayerToReturn)


def CreatePlayerList(): # Reads players.txt and makes the main list for use in a single game
    global GlobalPlayerList
    GlobalPlayerList = []
    PlayerID=1
    PlayerSetupFile = list(open('players.txt', 'r')) #Read players.txt and create a list
    PlayerToAdd = ReturnBlankPlayer(1)
    for LineFromTextFile in PlayerSetupFile:
        if LineFromTextFile[:3] != '***':   # If the line is not "***", interpret the line to add it to the PlayerToAdd dictionary
            if (len(LineFromTextFile) > 0) and LineFromTextFile[:1] != '#': #If the line isn't commented or empty
                exec("PlayerToAdd['" + LineFromTextFile.replace("=", "']="))
        else:   # If the line is "***" it's time to add the Player to the List
            PlayerToAdd['Alive']='Yes'    # Default 'Alive' to 'Yes', can change to 'No' during game
            if PlayerToAdd['InnocentChild'] == "Yes":
                PlayerToAdd['NumberOfNamesInHat'] = 0
            else:
                PlayerToAdd['NumberOfNamesInHat'] = 100
            GlobalPlayerList.append(PlayerToAdd.copy())  # Add PlayerToAdd to the global PlayerList list
            PlayerID += 1
            PlayerToAdd = ReturnBlankPlayer(PlayerID) # Prepare the next player


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
        KillPlayer(ActualVoters,PlayerWhoWillBeLynched,"Lynch")
        if GetAttributeFromPlayer(PlayerWhoWillBeLynched,'Alive') == 'No':  #If the lynch worked
            PunishAndRewardVotersAfterLynch(ActualVoters,PlayerWhoWillBeLynched)


def KillPlayer(Killer,Victim,KillType):
    print("Killer = " + str(Killer))
    print("Victim = " + str(Victim))
    print("KillType = " + str(KillType))
    ResistancesOvercome = "No" #Test resistances first
    if KillType == "Lynch":
        if GetAttributeFromPlayer(Victim,'LynchResistant') != 0:  #If player is lynch resistant
            WriteAttributeToPlayer(Victim,'LynchResistant',int(GetAttributeFromPlayer(Victim,'LynchResistant'))-1)
            print("Player was lynch-resistant.")
        else:
            ResistancesOvercome = "Yes"
    elif KillType == "Night":
        if GetAttributeFromPlayer(Victim,'NightKillResistant') != 0:  #If player is NK resistant
            #print ("So here's the victim id: " + str(Victim))
            #print ("So here's the NKR: " + str(GetAttributeFromPlayer(Victim,'NightKillResistant')))
            WriteAttributeToPlayer(Victim,'NightKillResistant',int(GetAttributeFromPlayer(Victim,'NightKillResistant'))-1)
            print("Player was night-kill-resistant.")
        else:
            ResistancesOvercome = "Yes"
    if ResistancesOvercome == "Yes": #Proceed if resistances are overcome
        KillBecomesConvert = "No"   #Check whether kill fails because player is Judas or Saulus
        if GetAttributeFromPlayer(Victim,'Judas') == 'Yes' and GetAttributeFromPlayer(Victim,'Alignment') == 'Town': #If Player is a Judas
            WriteAttributeToPlayer(Victim,'Alignment','Mafia')
            KillBecomesConvert = "Yes"
        elif GetAttributeFromPlayer(Victim,'Saulus') == 'Yes' and GetAttributeFromPlayer(Victim,'Alignment') == 'Mafia': #If Player is a Saulus
            WriteAttributeToPlayer(Victim,'Alignment','Town')
            KillBecomesConvert = "Yes"
        if KillBecomesConvert == "No": #Proceed if kill wasn't converted
            WriteAttributeToPlayer(Victim,'Alive','No')   #kill player
            if GetAttributeFromPlayer(Victim,'BelovedPrincess') == 'Yes': # If player is a Beloved Princess
                print("Player " + str(Victim) + " was a Beloved Princess! Day " + str(Day + 1) + " will be skipped.")
                global DaysThatDoNotHappen
                DaysThatDoNotHappen.append(Day+1)
            if GetAttributeFromPlayer(Victim,'Virgin') == "Yes": # If player is a Virgin
                print("Player " + str(Victim) + " was a Virgin! There can be no night kills on " + str(Night + 1) + ".")
                global NightsOnWhichThereAreNoKills
                NightsOnWhichThereAreNoKills.append(Night+1)
            if KillType == 'Lynch' and GetAttributeFromPlayer(Victim,'LynchBomb') == 'Yes':
                RandomVoterKilled = PickRandomItemFromList(Killer)
                print("Player " + str(Victim) + " was a LynchBomb. Random voter, Player " + str(RandomVoterKilled) + ", is targeted by the bomb.")
                KillPlayer(Victim,[RandomVoterKilled],'LynchBomb')   #Kill random voter
            elif KillType == 'Night' and GetAttributeFromPlayer(Victim,'NightBomb') == 'Yes':
                print("Player " + str(Victim) + " was a NightBomb. Their killer, Player " + str(Killer[0]) + ", is targeted by the bomb.")
                KillPlayer(Victim,Killer,'NightBomb')   #Kill killer


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
    print("Seeing if any one MafiaTeam out of Teams " + str(MafiaTeams) + " has " + str(Majority) + " votes.")
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


def ConsiderRevealingInvestigations():
    global InvestigationResults
    for Result in InvestigationResults:
        if Result['Revealed'] == 'No':
            if GetAttributeFromPlayer(Result['Cop'],'Alive') == "Yes":
                if randint(1,5) < 4: #Replace this code with something proper
                    #Assuming that only town can be cops
                    Result['Revealed'] = "Yes"
                    WriteAttributeToPlayer(Result['Cop'],'NumberOfNamesInHat',10)
                    if Result['Alignment'] == "Town":
                        WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',10)
                    if Result['Alignment'] == "Mafia":
                        WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',300)
                    print("Player " + str(Result['Cop']) + " just revealed that they investigated Player " + str(Result['Target']) + " and found that they are " + Result['Alignment'])

def SimulateSingleGame():
    InitiateSingleGameVariables()
    global DaysThatDoNotHappen
    global Day
    global Night
    global WinningTeam
    while WinningTeam == '':
        Day += 1
        Night += 1
        #Day cycle
        print()
        print("Day " + str(Day))
        if not Day in DaysThatDoNotHappen:
            ConsiderRevealingInvestigations()
            TryToLynch()
        CheckForVictory()
        LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
        print("The remaining living players at the end of Day " + str(Day) + " are " + str(LivingPlayers))
        if WinningTeam != '':
            DayOrNightWhenGameEnded = "D" + str(Day)
        else:   #If no winning team at the end of the day, do the night
            #Night cycle
            print()
            print("Night " + str(Night))
            NightRoutine()
            CheckForVictory()
            if WinningTeam != '':
                DayOrNightWhenGameEnded = "N" + str(Night)
            LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
            print("The remaining living players at the end of Night " + str(Night) + " are " + str(LivingPlayers))
    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    print()
    print("Winners = " + WinningTeam)


def NightRoutine():
    global PlayersBeingRoleBlocked
    global BusDrivings
    global ThisTurnsInvestigationActions
    global InvestigationResults
    global TeamNightKillActions
    global VigilanteActions
    global PlayersTargetedByDoctors
    global PlayersProtectedByDoctors
    global ActualNightKills
    global NightsOnWhichThereAreNoKills
    PlayersBeingRoleBlocked =[]
    PlayersProtectedByDoctors = []
    ThisTurnsInvestigationActions = []
    ActualNightKills = []
    ReceiveRoleBlockingActions()
    ReceiveBusDrivingActions()
    ReceiveCopActions()
    ReceiveDoctorActions()
    ReceiveTeamNightKillActions()
    ReceiveVigilanteKillActions()
    ProcessCopActions()
    ProcessDoctorActions()
    ProcessTeamNightKillActions()
    ProcessVigilanteKillActions()
    if Night not in NightsOnWhichThereAreNoKills:
        for ActualNightKill in ActualNightKills:
            print("Player " + str(ActualNightKill['Killer']) + " is night killing " + str(ActualNightKill['Victim']))
            KillPlayer(ActualNightKill['Killer'],ActualNightKill['Victim'],'Night')


def ProcessDoctorActions():
    global PlayersTargetedByDoctors
    global PlayersProtectedByDoctors
    for Target in PlayersTargetedByDoctors:
        ProtectionsResultingFromBusDriving = FindBusDrivingPairs(Target)
        for Protection in ProtectionsResultingFromBusDriving:
            PlayersProtectedByDoctors.append(Target)


def ProcessVigilanteKillActions():
    global VigilanteActions
    global ActualNightKills
    global PlayersProtectedByDoctors
    for VigilanteKill in VigilanteActions:
        DeathsResultingFromBusDriving = FindBusDrivingPairs(VigilanteKill['Victim'])
        for Death in DeathsResultingFromBusDriving:
            if Death not in PlayersProtectedByDoctors:
                ActualNightKills.append({'Killer': VigilanteKill['Killer'], 'Victim': Death})


def ProcessCopActions(): 
    global InvestigationResults
    global ThisTurnsInvestigationActions
    for Investigation in ThisTurnsInvestigationActions:
        ActualTarget = FindBusDrivingPairs(Investigation['Target'])
        if Len(ActualTarget) == 1: #Investigation fails if busdriving means there's multiple targets
            InvestigationResults.append({'Cop':Investigation['Cop'],'Target':Investigation['Target'],'Alignment':GetAttributeFromPlayer(ActualTarget(0),'Alignment'),'Revealed':'No'})


def ProcessTeamNightKillActions():
    global TeamNightKillActions
    global ActualNightKills
    for TeamNightKill in TeamNightKillActions:
        DeathsResultingFromBusDriving = FindBusDrivingPairs(TeamNightKill['Victim'])
        for Death in DeathsResultingFromBusDriving:
            if Death not in PlayersProtectedByDoctors:
                ActualNightKills.append({'Killer': TeamNightKill['Killer'], 'Victim': Death})


def FindBusDrivingPairs(PlayerID):
    ReturnedPlayerIDs = []
    global BusDrivings
    if BusDrivings == []:
        return([PlayerID])
    else:
        for BusDriving in BusDrivings:
            if BusDriving[0] == PlayerID:
                ReturnedPlayerIDs.append(BusDriving[1])
            elif BusDriving[1] == PlayerID:
                ReturnedPlayerIDs.append(BusDriving[0])
    return(ReturnedPlayerIDs)


def ReceiveRoleBlockingActions():
    global PlayersBeingRoleBlocked
    global Night
    PlayersBeingRoleBlocked = []
    LivingRoleBlockers = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("RoleBlocker","!=","'No'"))
    if LivingRoleBlockers != []: #If there are any roleblockers
        for Player in LivingRoleBlockers:
            RoleBlockerActiveTonight = "No"
            #See if this roleblocker is to be active on this particular night
            RoleBlockerValueFromPlayerlist = GetAttributeFromPlayer(Player,"RoleBlocker")
            if RoleBlockerValueFromPlayerlist == "Yes":
                RoleBlockerActiveTonight = "Yes"
            elif RoleBlockerValueFromPlayerlist == IsNumberOddOrEven(Night):
                RoleBlockerActiveTonight = "Yes"
            if RoleBlockerActiveTonight == "Yes":
                if GetAttributeFromPlayer(Player,'Alignment') == 'Mafia':
                    PlayerToBeRoleBlocked = TryToPickTownPlayer(Player,[])
                else:
                    PlayerToBeRoleBlocked = TryToPickMafiaPlayer(Player,[])
                if PlayersBeingRoleBlocked != 0:
                    PlayersBeingRoleBlocked.append(PlayerToBeRoleBlocked)
                    print("On this night, Player " + str(Player) + " is roleblocking " + str(PlayerToBeRoleBlocked))


def ReceiveBusDrivingActions():
    global BusDrivings
    BusDrivings = []
    LivingBusDrivers = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("BusDriver","!=","'No'"))
    if LivingBusDrivers != []: #If there are any BusDrivers
        for BusDriver in LivingBusDrivers:
            BusDriverActiveTonight = "No"
            #See if this BusDriver is to be active on this particular night
            BusDriverValueFromPlayerlist = GetAttributeFromPlayer(BusDriver,"BusDriver")
            if BusDriverValueFromPlayerlist == "Yes":
                BusDriverActiveTonight = "Yes"
            elif BusDriverValueFromPlayerlist == IsNumberOddOrEven(Night):
                BusDriverActiveTonight = "Yes"
            if BusDriver in PlayersBeingRoleBlocked: #BusDriver is inactive if roleblocked
                BusDriverActiveTonight = "No"
            if BusDriverActiveTonight == "Yes":
                BusDrivenPlayer1 = TryToPickMafiaPlayer(BusDriver,[])
                BusDrivenPlayer2 = TryToPickTownPlayer(BusDriver,[])
                if (BusDrivenPlayer1 != 0) and (BusDrivenPlayer2 != 0):
                    if BusDrivenPlayer1 > BusDrivenPlayer2:
                        InsertSlot1 = BusDrivenPlayer2
                        InsertSlot2 = BusDrivenPlayer1
                    else:
                        InsertSlot1 = BusDrivenPlayer1
                        InsertSlot2 = BusDrivenPlayer2
                    if [InsertSlot1,InsertSlot2] not in BusDrivings:
                        BusDrivings.append([BusDrivenPlayer1,BusDrivenPlayer2])
                        print("On this night, Player " + str(BusDriver) + " is busdriving Player " + str(BusDrivenPlayer1) + " and Player " + str(BusDrivenPlayer2))


def ReceiveTeamNightKillActions():
    global TeamNightKillActions
    TeamNightKillActions = []
    TeamsStillAlive = BuildListOfTeamNumbers('Mafia') + BuildListOfTeamNumbers('Town')
    for Team in TeamsStillAlive:
        TeamKillPlayerPresent = "No"
        TeamKillers = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team),SearchPlayersFor("TeamNightKill","!=","'No'"))
        if TeamKillers != []:
            ChosenTeamKiller = PickRandomItemFromList(TeamKillers)
            TeamKillerActiveTonight = "No"
            #See if this TeamKiller is to be active on this particular night
            TeamNightKillValueFromPlayerList = GetAttributeFromPlayer(ChosenTeamKiller,"TeamNightKill")
            if TeamNightKillValueFromPlayerList == "Yes":
                TeamKillerActiveTonight = "Yes"
            elif TeamNightKillValueFromPlayerList == IsNumberOddOrEven(Night):
                TeamKillerActiveTonight = "Yes"
            if ChosenTeamKiller in PlayersBeingRoleBlocked: #Teamkiller is inactive if roleblocked
                TeamKillerActiveTonight = "No"
            if TeamKillerActiveTonight == "Yes":
                if GetAttributeFromPlayer(ChosenTeamKiller,'Alignment') == "Mafia":
                    Target = TryToPickTownPlayer(ChosenTeamKiller,[])
                else:
                    Target = TryToPickMafiaPlayer(ChosenTeamKiller,[])
                if Target != 0:
                    TeamNightKillActions.append({'Killer': ChosenTeamKiller,'Victim': Target})
                    print("On this night, Player " + str(ChosenTeamKiller) + " is NightKilling Player " + str(Target) + " for team " + str(Team))


def ReceiveVigilanteKillActions():
    global VigilanteActions
    VigilanteActions = []
    Vigilantes = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Vigilante","!=","'No'"))
    if Vigilantes != []:
        for Vigilante in Vigilantes:
            VigilanteActiveTonight = "No"
            #See if this Vigilante is to be active on this particular night
            VigilanteValueFromPlayerList = GetAttributeFromPlayer(Vigilante,"Vigilante")
            if VigilanteValueFromPlayerList == "Yes":
                VigilanteActiveTonight = "Yes"
            elif VigilanteValueFromPlayerList == IsNumberOddOrEven(Night):
                VigilanteActiveTonight = "Yes"
            if Vigilante in PlayersBeingRoleBlocked: #BusDriver is inactive if roleblocked
                VigilanteActiveTonight = "No"
            if VigilanteActiveTonight == "Yes":
                if GetAttributeFromPlayer(Vigilante,'Alignment') == "Mafia":
                    Target = TryToPickTownPlayer(Vigilante,[])
                else:
                    Target = TryToPickMafiaPlayer(Vigilante,[])
                if Target != 0:
                    VigilanteActions.append({'Killer': Vigilante,'Victim': Target})
                    print("On this night, Player " + str(Vigilante) + " is NightKilling Player " + str(Target) + " as a Vigilante.")


def ReceiveDoctorActions():
    global PlayersTargetedByDoctors
    global Night
    PlayersTargetedByDoctors = []
    LivingDoctors = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("Doctor","!=","'No'"))
    if LivingDoctors != []: #If there are any Doctors
        for Doctor in LivingDoctors:
            DoctorActiveTonight = "No"
            #See if this Doctor is to be active on this particular night
            DoctorValueFromPlayerList = GetAttributeFromPlayer(Player,"Doctor")
            if DoctorValueFromPlayerList == "Yes":
                DoctorActiveTonight = "Yes"
            elif DoctorValueFromPlayerList == IsNumberOddOrEven(Night):
                DoctorActiveTonight = "Yes"
            if Doctor in PlayersBeingRoleBlocked: #Doctor is inactive if roleblocked
                DoctorActiveTonight = "No"
            if DoctorActiveTonight == "Yes":
                if GetAttributeFromPlayer(Player,'Alignment') == 'Mafia':
                    PlayerToBeDoctored = TryToPickMafiaPlayer(Player,[])
                else:
                    PlayerToBeDoctored = TryToPickTownPlayer(Player,[])
                if PlayerToBeDoctored != 0:
                    PlayersTargetedByDoctors.append(PlayerToBeDoctored)
                    print("On this night, Player " + str(Doctor) + " is Doctoring " + str(PlayerToBeDoctored))


def ReceiveCopActions():
    global ThisTurnsInvestigationActions
    ThisTurnsInvestigationActions = []
    #Build a list of cops who will be asked for night actions
    Cops = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Cop","!=","'No'"))
    if Cops != []:
        for Cop in Cops:
            WillNotInvestigate = []
            #Build a list of people who have been the target of a revealed investigation by anyone or an unrevealed investigation by this cop
            if len(InvestigationResults) > 0:
                for Investigation in InvestigationResults:
                    if (Investigation['Cop'] == Cop) or (Investigation['Revealed'] == 'Yes'):
                        WillNotInvestigate.append(Investigation['Target'])
            CopActiveTonight = "No"
            #See if this Cop is to be active on this particular night
            CopValueFromPlayerList = GetAttributeFromPlayer(Cop,"Cop")
            if CopValueFromPlayerList == "Yes":
                CopActiveTonight = "Yes"
            elif CopValueFromPlayerList == IsNumberOddOrEven(Night):
                CopActiveTonight = "Yes"
            if Cop in PlayersBeingRoleBlocked: #Cop is inactive if roleblocked
                CopActiveTonight = "No"
            if CopActiveTonight == "Yes":
                if GetAttributeFromPlayer(Cop,'Alignment') == "Mafia":
                    Target = TryToPickTownPlayer(Cop,WillNotInvestigate)
                else:
                    Target = TryToPickMafiaPlayer(Cop,WillNotInvestigate)
                if Target != 0:
                    ThisTurnsInvestigationActions.append({'Cop': Cop, 'Target' : Target})
                    print("On this night, Player " + str(Cop) + " is Investigating Player " + str(Target) + " as a Vigilante.")


InitiateGlobalVariables()
SimulateSingleGame()
