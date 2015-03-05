__author__ = 'Unit'

from random import randint  # This gets the function that is used to get a random integer between two numbers
import random
import math
import copy

def InitiateSingleGameVariables(): # Set up variables to run a single game
    global PlayerID
    PlayerID = 0  # This zeroes the counter that is used by function AddPlayer when populating the player list
    global PlayerList
    global GlobalPlayerList
    PlayerList = copy.deepcopy(GlobalPlayerList)  # This creates a fresh copy of the player list, for use in this specific game
    global MafiaRevealedByLynchedCop
    MafiaRevealedByLynchedCop = []
    global Day
    Day = 0
    global Night
    Night = 0
    global TimeCounter
    TimeCounter = 0
    global DaysThatDoNotHappen
    DaysThatDoNotHappen = []    #This is needed for the Beloved Princess
    global NightsOnWhichThereAreNoKills
    NightsOnWhichThereAreNoKills = []   #This is needed for the InkBomb
    global InvestigationResults
    InvestigationResults = []
    global FriendlyNeighbourResults
    FriendlyNeighbourResults = []
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


def TestForDeputies(DyingPlayer):
    TestForDeputy(DyingPlayer,'Cop')
    TestForDeputy(DyingPlayer,'Doctor')
    TestForDeputy(DyingPlayer,'RoleBlocker')
    TestForDeputy(DyingPlayer,'BusDriver')
    TestForDeputy(DyingPlayer,'Vigilante')

def TestForDeputy(DyingPlayer,RoleType):
    FoundDeputy = 0
    if GetAttributeFromPlayer(DyingPlayer,RoleType) != 'No': #Test for deputy
        DebugPrint("Dying player was a " + RoleType + ". Looking for deputies.")
        PossibleDeputies = []
        LivingDeputiesOfSameAlignmentAndTeam = []
        LivingDeputiesOfSameAlignment = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alignment','==',"'" + GetAttributeFromPlayer(DyingPlayer,'Alignment') + "'"),SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor('Deputy' + RoleType,'==',"'Yes'"))
        if len(LivingDeputiesOfSameAlignment) != 0: # If there are any living deputies of same alignment
            DebugPrint("There are some deputy "+ RoleType + "s of that alignment.")
            if GetAttributeFromPlayer(DyingPlayer,'Team') != 0: # If the dying player has a team, and there are deputies alive on that team, narrow the list to those on that team
                DebugPrint("The player had a team, so we're looking for deputies on that team.")
                LivingDeputiesOfSameAlignmentAndTeam = ReturnOneListWithCommonItemsFromTwoLists(LivingDeputiesOfSameAlignment,SearchPlayersFor('Team','==',GetAttributeFromPlayer(DyingPlayer,'Team')))
                if len(LivingDeputiesOfSameAlignmentAndTeam) == 0:
                    DebugPrint("There were no deputies on that team, so we're looking for any deputies.")
                    LivingDeputiesOfSameAlignmentAndTeam = LivingDeputiesOfSameAlignment
            else: # If the dying player has no team, any deputy of that alignment will do
                DebugPrint("The player had no team, so we're looking for any deputies.")
                LivingDeputiesOfSameAlignmentAndTeam = LivingDeputiesOfSameAlignment
        if len(LivingDeputiesOfSameAlignmentAndTeam) != 0:
            FoundDeputy = PickRandomItemFromList(LivingDeputiesOfSameAlignmentAndTeam)
            DebugPrint("We found a living Deputy " + RoleType + "! It was player " + str (FoundDeputy))
    if FoundDeputy != 0:
        WriteAttributeToPlayer(FoundDeputy,RoleType,GetAttributeFromPlayer(DyingPlayer,RoleType))
        WriteAttributeToPlayer(FoundDeputy,RoleType + 'Shots',GetAttributeFromPlayer(DyingPlayer,RoleType + 'Shots'))
        WriteAttributeToPlayer(FoundDeputy,'Deputy' + RoleType,'No')


def ReturnLivingParanoidGunOwners():
    return(ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==','Yes'),SearchPlayersFor('ParanoidGunOwner','==','Yes')))


def ReturnBlankPlayer(PlayerID):
    PlayerToReturn = {}
    PlayerToReturn['PlayerID'] = PlayerID
    PlayerToReturn['Alignment'] = 'None'            # "Town" or "Mafia" or "None"
    PlayerToReturn['Team'] = 0                      # 0 (for no team) or the number of the team (Town and Mafia team numbers must be different)
    PlayerToReturn['BelovedPrincess'] = 'No'        # "No", "Lynch", "Night" or "Either" (if not "No", must be Town. Other values refer to triggering type of kill.)
    PlayerToReturn['InkBomb'] = 'No'                 # # "No", "Lynch", "Night" or "Either" (if not "No", must be Mafia. Other values refer to triggering type of kill.)
    PlayerToReturn['ParanoidGunOwner'] = 'No'              # "Yes" or "No"
    PlayerToReturn['LynchBomb'] = 'No'              # "Yes" or "No"
    PlayerToReturn['NightBomb'] = 'No'              # "Yes" or "No"
    PlayerToReturn['InnocentChild'] = 'No'          # "Yes" or "No"
    PlayerToReturn['Godfather'] = 'No'              # "Yes" or "No"
    PlayerToReturn['Saulus'] = 'No'                 # "Yes" or "No" (If yes, Alignment should be "Mafia" and Team should be 0)
    PlayerToReturn['Judas'] = 'No'                  # "Yes" or "No" (If yes, Alignment should be "Town")
    PlayerToReturn['FriendlyNeighbour'] = 'No'      # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['FriendlyNeighbourShots'] = -1      # if -1, unlimited. Otherwise, # of possible investigations
    PlayerToReturn['ParanoidGunOwner'] = 'No'              # "Yes" or "No"
    PlayerToReturn['ParanoidGunOwnerShots'] = -1              # if -1, unlimited. Otherwise, # of times the PGO can fire
    PlayerToReturn['Cop'] = 'No'                    # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['CopShots'] = -1             # if -1, unlimited. Otherwise, # of possible investigations
    PlayerToReturn['Commuter'] = 'No'                    # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['CommuterShots'] = -1             # if -1, unlimited. Otherwise, # of possible commutings
    PlayerToReturn['Doctor'] = 'No'                 # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['DoctorShots'] = -1          # if -1, unlimited. Otherwise, # of possible doctorings
    PlayerToReturn['RoleBlocker'] = 'No'            # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['RoleBlockerShots'] = -1     # if -1, unlimited. Otherwise, # of possible roleblockings
    PlayerToReturn['BusDriver'] = 'No'              # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['BusDriverShots'] = -1       # if -1, unlimited. Otherwise, # of possible busdrivings
    PlayerToReturn['Vigilante'] = 'No'              # "Yes", "Odd", "Even" or "No"
    PlayerToReturn['VigilanteShots'] = -1       # if -1, unlimited. Otherwise, # of possible vig kills
    PlayerToReturn['TeamNightKill'] = 'No'          # "Yes", "Odd", "Even" or "No" (If Alignment is "Mafia", should ordinarily not be "No")
    PlayerToReturn['TeamNightKillShots'] = -1   # if -1, unlimited. Otherwise, # of possible team night kills
    PlayerToReturn['DeputyCop'] = 'No'              # "Yes" or "No"
    PlayerToReturn['DeputyDoctor'] = 'No'           # "Yes" or "No"
    PlayerToReturn['DeputyRoleBlocker'] = 'No'      # "Yes" or "No"
    PlayerToReturn['DeputyBusDriver'] = 'No'        # "Yes" or "No"
    PlayerToReturn['DeputyVigilante'] = 'No'        # "Yes" or "No"
    PlayerToReturn['NightKillResistant'] = 0        # -1 (for invulnerable), 0 (for normal), otherwise X-shot
    PlayerToReturn['LynchResistant'] = 0            # -1 (for invulnerable), 0 (for normal), otherwise X-shot
    PlayerToReturn['Labrador'] = -1            # Should only be >0 for Mafia
    return(PlayerToReturn)


def GetNumberOfPlayersFromTextFile(): # Reads players.txt and makes the main list for use in a single game
    PlayerSetupFile = list(open('players.txt', 'r')) #Read players.txt and create a list
    NumberOfPlayers = 0
    for LineFromTextFile in PlayerSetupFile:
        if LineFromTextFile[:3] == '***':
            NumberOfPlayers += 1
    return(NumberOfPlayers)


def CreatePlayerList(): # Reads players.txt and makes the main list for use in a single game
    PlayerListToReturn = []
    PlayerID=1
    PlayerSetupFile = list(open('players.txt', 'r')) #Read players.txt and create a list
    PlayerToAdd = ReturnBlankPlayer(1)
    global TownStartingNamesInHat
    global MafiaStartingNamesInHat
    global IndexList
    IndexList = []
    for LineFromTextFile in PlayerSetupFile:
        if LineFromTextFile[:3] != '***':   # If the line is not "***", interpret the line to add it to the PlayerToAdd dictionary
            if (len(LineFromTextFile) > 0) and LineFromTextFile[:1] != '#': #If the line isn't commented or empty
                exec("PlayerToAdd['" + LineFromTextFile.replace("=", "']="))
        else:   # If the line is "***" it's time to add the Player to the List
            PlayerToAdd['Alive']='Yes'    # Default 'Alive' to 'Yes', can change to 'No' during game
            if PlayerToAdd['InnocentChild'] == "Yes":
                PlayerToAdd['NumberOfNamesInHat'] = 1
            else:
                if PlayerToAdd['Alignment'] == 'Mafia':
                    PlayerToAdd['NumberOfNamesInHat'] = MafiaStartingNamesInHat
                elif PlayerToAdd['Alignment'] == 'Town':
                    PlayerToAdd['NumberOfNamesInHat'] = TownStartingNamesInHat
            PlayerListToReturn.append(PlayerToAdd.copy())  # Add PlayerToAdd to the global PlayerList list
            IndexList.append(PlayerID)
            PlayerID += 1
            PlayerToAdd = ReturnBlankPlayer(PlayerID) # Prepare the next player
    return(PlayerListToReturn)

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
    global IndexList
    global PlayerList
    Player = PlayerList[IndexList.index(PlayerID)]
    return(eval("Player['" + Attribute + "']"))


def WriteAttributeToPlayer(PlayerID,Attribute,ValueToWrite): # Change an attribute for a particular player
    global PlayerList
    for Player in PlayerList:
        if Player['PlayerID'] == PlayerID:
            Player[Attribute] = ValueToWrite
            break


def TryToLynch():
    Candidates = SearchPlayersFor('Alive',"==","'Yes'")
    PlayerWhoWillBeLynched = 0

    #If there's been mafia revealed this day.
    global MafiaRevealedToday
    LivingMafiaRevealedToday = ReturnOneListWithCommonItemsFromTwoLists(MafiaRevealedToday,SearchPlayersFor('Alive','==',"'Yes'"))
    while len(LivingMafiaRevealedToday) > 0 and PlayerWhoWillBeLynched == 0:
        CandidatePickedFromHat = PickNameFromHatForLynch(LivingMafiaRevealedToday)
        DebugPrint("Seeing if we can lynch Revealed Mafia, Player " + str(CandidatePickedFromHat))
        GetsEnoughVotes, ActualVoters = WillGetEnoughLynchVotes(CandidatePickedFromHat)
        if GetsEnoughVotes == "Yes":    # See if this candidate gets enough votes
            PlayerWhoWillBeLynched = CandidatePickedFromHat
        else:
            Candidates.remove(CandidatePickedFromHat)
            LivingMafiaRevealedToday.remove(CandidatePickedFromHat)


    #If there's no mafia been revealed this day
    DebugPrint ("The current candidates for the lynch are " + str(Candidates))
    while len(Candidates) > 0 and PlayerWhoWillBeLynched == 0:  # While there are still candidates and no one has been voted for
        CandidatePickedFromHat = PickNameFromHatForLynch(Candidates)
        #DebugPrint ("Going to see if there are enough votes for " + str(CandidatePickedFromHat))
        GetsEnoughVotes, ActualVoters = WillGetEnoughLynchVotes(CandidatePickedFromHat)
        if GetsEnoughVotes == "Yes":    # See if this candidate gets enough votes
            PlayerWhoWillBeLynched = CandidatePickedFromHat
        else:
            DebugPrint ("The players couldn't get enough votes to lynch " + str(CandidatePickedFromHat))
            Candidates.remove(CandidatePickedFromHat)   # If there aren't enough votes for the candidate, knock the candidate off the list
    if PlayerWhoWillBeLynched != 0:
        KillPlayer(ActualVoters,PlayerWhoWillBeLynched,"Lynch")
        if GetAttributeFromPlayer(PlayerWhoWillBeLynched,'Alive') == 'No':  #If the lynch worked
            PunishAndRewardVotersAfterLynch(ActualVoters,PlayerWhoWillBeLynched)


def KillPlayer(Killer,Victim,KillType):
    ResistancesOvercome = "No" #Test resistances first
    if KillType == "Lynch":
        if GetAttributeFromPlayer(Victim,'LynchResistant') != 0:  #If player is lynch resistant
            WriteAttributeToPlayer(Victim,'LynchResistant',int(GetAttributeFromPlayer(Victim,'LynchResistant'))-1)
            DebugPrint("Player was lynch-resistant.")
        else:
            ResistancesOvercome = "Yes"
    elif KillType == "Night":
        if GetAttributeFromPlayer(Victim,'NightKillResistant') != 0:  #If player is NK resistant
            WriteAttributeToPlayer(Victim,'NightKillResistant',int(GetAttributeFromPlayer(Victim,'NightKillResistant'))-1)
            DebugPrint("Player was night-kill-resistant.")
        else:
            ResistancesOvercome = "Yes"
    if KillType == "LynchBomb" or KillType == "NightBomb":
        ResistancesOvercome = "Yes"
    if ResistancesOvercome == "Yes": #Proceed if resistances are overcome
        KillBecomesConvert = "No"   #Check whether kill fails because player is Judas or Saulus
        if GetAttributeFromPlayer(Victim,'Judas') == 'Yes' and GetAttributeFromPlayer(Victim,'Alignment') == 'Town': #If Player is a Judas
            LivingMafiaTeamKillers = ReturnOneListWithCommonItemsFromFourLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor('Alignment','==',"'Mafia'"),SearchPlayersFor('Team','!=',"0"),SearchPlayersFor('TeamNightKill','!=',"'No'"))
            if len(LivingMafiaTeamKillers) > 0:
                RandomMafiaPlayerToFollow = PickRandomItemFromList(LivingMafiaTeamKillers)
                NewTeam = GetAttributeFromPlayer(RandomMafiaPlayerToFollow,'Team')
                NewTeamKill = GetAttributeFromPlayer(RandomMafiaPlayerToFollow,'TeamNightKill')
            else:
                NewTeam = 0
                NewTeamKill = 'No'
            WriteAttributeToPlayer(Victim,'Team',NewTeam)
            WriteAttributeToPlayer(Victim,'TeamNightKill',NewTeamKill)
            WriteAttributeToPlayer(Victim,'Alignment','Mafia')
            KillBecomesConvert = "Yes"
            DebugPrint("Player was a Judas! Player is now Mafia. They are on team " + str(NewTeam) + " and their NightKill is '" + NewTeamKill +"'")
        elif GetAttributeFromPlayer(Victim,'Saulus') == 'Yes' and GetAttributeFromPlayer(Victim,'Alignment') == 'Mafia': #If Player is a Saulus
            WriteAttributeToPlayer(Victim,'Alignment','Town')
            WriteAttributeToPlayer(Victim,'Team',0)
            WriteAttributeToPlayer(Victim,'TeamNightKill',0)
            KillBecomesConvert = "Yes"
            DebugPrint("Player was a Saulus! Player is now Town.")
        if KillBecomesConvert == "No": #Proceed if kill wasn't converted
            if GetAttributeFromPlayer(Victim,'Alive') != 'No':
                WriteAttributeToPlayer(Victim,'Alive','No')   #kill player
                TestForDeputies(Victim)
                BelovedPrincess = GetAttributeFromPlayer(Victim,'BelovedPrincess')
                InkBomb = GetAttributeFromPlayer(Victim,'InkBomb')
                Cop = GetAttributeFromPlayer(Victim,'Cop')
                Alignment = GetAttributeFromPlayer(Victim,'Alignment')
                if Cop != 'No' and Alignment == 'Town' and KillType == 'Lynch':
                    DebugPrint("Player " + str(Victim) + " was a Town Cop, seeing if they have any investigations to reveal before being lynched.")
                    ConsiderRevealingInvestigations(Victim)
                if BelovedPrincess == 'Either' or BelovedPrincess == KillType: # If player is a Beloved Princess
                    DebugPrint("Player " + str(Victim) + " was a Beloved Princess! Day " + str(Day + 1) + " will be skipped.")
                    global DaysThatDoNotHappen
                    DaysThatDoNotHappen.append(Day+1)
                if InkBomb == 'Either' or InkBomb == KillType: # If player is an InkBomb
                    if KillType == "Lynch":
                        NightOnWhichThereWillBeNoKills = Night
                    elif KillType == "Night":
                        NightOnWhichThereWillBeNoKills = Night+1
                    DebugPrint("Player " + str(Victim) + " was a InkBomb! There can be no night kills on " + str(NightOnWhichThereWillBeNoKills) + ".")
                    global NightsOnWhichThereAreNoKills
                    NightsOnWhichThereAreNoKills.append(NightOnWhichThereWillBeNoKills)
                if KillType == 'Lynch' and GetAttributeFromPlayer(Victim,'LynchBomb') == 'Yes':
                    RandomVoterKilled = PickRandomItemFromList(Killer)
                    DebugPrint("Player " + str(Victim) + " was a LynchBomb. Random voter, Player " + str(RandomVoterKilled) + ", is targeted by the bomb.")
                    KillPlayer(Victim,RandomVoterKilled,'LynchBomb')   #Kill random voter
                elif KillType == 'Night' and GetAttributeFromPlayer(Victim,'NightBomb') == 'Yes':
                    DebugPrint("Player " + str(Victim) + " was a NightBomb. Their killer, Player " + str(Killer) + ", is targeted by the bomb.")
                    KillPlayer(Victim,Killer,'NightBomb')   #Kill killer


def PunishAndRewardVotersAfterLynch(Voters,LynchedPlayer):
    global MafiaPunishRewardMultiplier
    global TownPunishRewardMultiplier
    MinimumProbability = 1
    MaximumProbability = 2.5
    CriticalProportion = .6
    ProportionOfPlayers = len(SearchPlayersFor('Alive','==',"'Yes'")) / len(PlayerList)
    Probability = ((MaximumProbability - MinimumProbability) / (CriticalProportion - MaximumProbability) * (ProportionOfPlayers - MaximumProbability)) + MinimumProbability
    Probability = max(Probability, MinimumProbability)
    AlignmentOfDeadPlayer = GetAttributeFromPlayer(LynchedPlayer,'Alignment')
    #Punish and reward the voters
    for Voter in Voters:
        if AlignmentOfDeadPlayer == 'Mafia':
            ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(50,70))
            NewNumber=GetAttributeFromPlayer(Voter,'NumberOfNamesInHat')-ChangeToNumberOfNamesInHat
#            DebugPrint("Player " + str(Voter) + " voted to lynch a mafia.")
        elif AlignmentOfDeadPlayer == 'Town':
            ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(50,70))
            NewNumber=GetAttributeFromPlayer(Voter,'NumberOfNamesInHat')+ChangeToNumberOfNamesInHat
 #           DebugPrint("Player " + str(Voter) + " voted to lynch a town.")
        VoterAlignment = GetAttributeFromPlayer(Voter,'Alignment')
        if VoterAlignment == 'Town':
            NewNumber = int(NewNumber * TownPunishRewardMultiplier)
        elif VoterAlignment == 'Mafia':
            NewNumber = int(NewNumber * MafiaPunishRewardMultiplier)
        if NewNumber<1:
            NewNumber=1
        WriteAttributeToPlayer(Voter,'NumberOfNamesInHat',NewNumber)
        #DebugPrint("Player " + str(Voter) + "'s odds are now " + str(NewNumber))
    #Punish and reward the non-voters
    NonVoters = SearchPlayersFor('Alive','==','"Yes"')
    for NonVoter in NonVoters:
        if NonVoter != LynchedPlayer:
            if NonVoter not in Voters:
                if AlignmentOfDeadPlayer == 'Mafia':
                    ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(5,20))
                    NewNumber = GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')+ChangeToNumberOfNamesInHat
#                    DebugPrint("Player " + str(NonVoter) + " didn't vote to lynch a mafia.")
                elif AlignmentOfDeadPlayer == 'Town':
                    ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(5,20))
                    NewNumber = GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')-ChangeToNumberOfNamesInHat
#                    DebugPrint("Player " + str(NonVoter) + " didn't vote to lynch a town.")
                NonVoterAlignment = GetAttributeFromPlayer(NonVoter,'Alignment')
                if NonVoterAlignment == 'Town':
                    NewNumber = int(NewNumber * TownPunishRewardMultiplier)
                elif NonVoterAlignment == 'Mafia':
                    NewNumber = int(NewNumber * MafiaPunishRewardMultiplier)
                if NewNumber<1:
                    NewNumber=1
                WriteAttributeToPlayer(NonVoter,'NumberOfNamesInHat',NewNumber)
                #DebugPrint("Player " + str(NonVoter) + "'s odds are now " + str(GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')))


def PickNameFromHatForLynch(PlayersToGoInHat):
    Hat = []
    #DebugPrint("PlayersToGoInHat = " + str(PlayersToGoInHat))
    for Player in PlayersToGoInHat:
        i = 0
        #DebugPrint("Player = " + str(Player))
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
    if PlayersTeam != 0:
        PlayersTeamMates = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alive','==',"'Yes'"), SearchPlayersFor('PlayerID','!=',PlayerWhoIsChoosing), SearchPlayersFor('Team','==',PlayersTeam))
    else:
        PlayersTeamMates = []
    global FriendlyNeighbourResults
    global InvestigationResults
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
        if NumberOfNamesFromPlayerList >=1000 and GetAttributeFromPlayer(PlayerInHat,'InnocentChild') != "Yes": #If the candidate is probably mafia, don't add them.
            NumberOfTimesToGoInHat = 0
        else: #If the candidate might not be mafia, figure out how many names to add (reversing polarity)
            if NumberOfNamesFromPlayerList >= 500:
                NumberOfTimesToGoInHat = 500 - (NumberOfNamesFromPlayerList - 500)
            else:
                NumberOfTimesToGoInHat = 500 + (500 - NumberOfNamesFromPlayerList)
            # Increase chances for person who is known to be town through Friendly Neighbour
            if len(FriendlyNeighbourResults) > 0:
                for FriendlyNeighbourResult in FriendlyNeighbourResults:
                    if FriendlyNeighbourResult['Teller'] == PlayerInHat:
                        if PlayerWhoIsChoosing == FriendlyNeighbourResult['Listener']:
                            NumberOfTimesToGoInHat = NumberOfTimesToGoInHat * 3
                        elif FriendlyNeighbourResult['Listener'] in PlayersTeamMates:
                            NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat * 2.5)
                        elif FriendlyNeighbourResult['Revealed'] == 'Yes':
                            NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat * 2.5)
            # Increase chances for person who is known to be town through investigations (either as cops or as targets)
            if len(InvestigationResults) > 0:
                for Investigation in InvestigationResults:
                    if Investigation['Target'] == PlayerInHat:
                        if PlayerWhoIsChoosing == Investigation['Cop']:
                            if Investigation['Alignment'] == 'Town':
                                NumberOfTimesToGoInHat = NumberOfTimesToGoInHat * 3
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat / 3)
                        elif Investigation['Cop'] in PlayersTeamMates:
                            if Investigation['Alignment'] == 'Town':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat * 2.5)
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat / 2)
                        elif Investigation['Revealed'] == 'Yes':
                            if Investigation['Alignment'] == 'Town':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat * 2)
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat / 1.5)
            # Increase chance for Innocent Children
            if GetAttributeFromPlayer(PlayerInHat,'InnocentChild') == "Yes":
                NumberOfTimesToGoInHat = NumberOfTimesToGoInHat * 3
            # Increase chances for person who is on same town team
            if PlayersTeam != 0 and PlayersAlignment == "Town":
                if PlayersTeam == int(GetAttributeFromPlayer(PlayerInHat,"Team")):
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
    if PlayersTeam != 0:
        PlayersTeamMates = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alive','==',"'Yes'"), SearchPlayersFor('PlayerID','!=',PlayerWhoIsChoosing), SearchPlayersFor('Team','==',PlayersTeam))
    else:
        PlayersTeamMates = []
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
            NumberOfNamesFromPlayerList = 0
        else:
            # Decrease chances for person who is known to be town through Friendly Neighbour
            if len(FriendlyNeighbourResults) > 0:
                for FriendlyNeighbourResult in FriendlyNeighbourResults:
                    if FriendlyNeighbourResult['Teller'] == PlayerInHat:
                        if PlayerWhoIsChoosing == FriendlyNeighbourResult['Listener']:
                            NumberOfNamesFromPlayerList = 0
                        elif FriendlyNeighbourResult['Listener'] in PlayersTeamMates:
                            NumberOfNamesFromPlayerList = 10
                        elif FriendlyNeighbourResult['Revealed'] == 'Yes':
                            NumberOfNamesFromPlayerList = 10
            # Decrease chances for person who is known to be town through investigations (either as cops or as targets)
            if len(InvestigationResults) > 0:
                for Investigation in InvestigationResults:
                    if Investigation['Target'] == PlayerInHat:
                        if PlayerWhoIsChoosing == Investigation['Cop']:
                            if Investigation['Alignment'] == 'Town':
                                NumberOfNamesFromPlayerList = int(NumberOfNamesFromPlayerList / 3)
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfNamesFromPlayerList * 3
                        elif Investigation['Cop'] in PlayersTeamMates:
                            if Investigation['Alignment'] == 'Town':
                                NumberOfNamesFromPlayerList = int(NumberOfNamesFromPlayerList / 2)
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfNamesFromPlayerList = int(NumberOfNamesFromPlayerList * 3)
                        elif Investigation['Revealed'] == 'Yes':
                            if Investigation['Alignment'] == 'Town':
                                NumberOfNamesFromPlayerList = int(NumberOfNamesFromPlayerList / 2.5)
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfNamesFromPlayerList = int(NumberOfNamesFromPlayerList * 2.5)
            if PlayersTeam != 0: # if the player is on a team
                if PlayersTeam == int(GetAttributeFromPlayer(PlayerInHat,"Team")): #if the candidate is on the same team
                    if PlayersAlignment == "Town":
                        NumberOfNamesFromPlayerList = 0
                    elif PlayersAlignment == "Mafia":
                        NumberOfNamesFromPlayerList = NumberOfNamesFromPlayerList * 3

            if NumberOfNamesFromPlayerList <= 70: #Exclude anyone who's unlikely to be mafia
                NumberOfNamesFromPlayerList = 0
        #Now populate the hat
        i = 0
        while i < NumberOfNamesFromPlayerList:
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
    #DebugPrint("Going to see if the following players will vote 'yes': " + str(PossibleVoters))
    Votes = 0
    for Player in PossibleVoters:
        #DebugPrint("Going to see if the following player will vote 'yes': " + str(Player))
        if DoesPlayer1VoteForPlayer2(Player,TargetPlayerID) == 'Yes':
            ActualVoters.append(Player)
            Votes += 1
            #DebugPrint("Player " + str(Player) + " will vote yes, bringing the total votes to " + str(Votes))
            if Votes >= NumberOfVotesRequiredToLynch():
                DebugPrint("They're lynching player " + str(TargetPlayerID) + " and the people voting are " + str(ActualVoters))
                return('Yes',ActualVoters)
    return('No',[])


def EffectOfFriendlyNeighbourResults(Player1,Player2,Player1Team,Player1Alignment):
    EffectToReturn = "None"
    EffectStrengthToReturn = "None"
    if Player1Team != 0:
        Player1TeamMates = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alive','==',"'Yes'"), SearchPlayersFor('PlayerID','!=',Player1), SearchPlayersFor('Team','==',Player1Team))
    else:
        Player1TeamMates = []
    global FriendlyNeighbourResults
    if len(FriendlyNeighbourResults) > 0:
        for FriendlyNeighbourResult in FriendlyNeighbourResults:
            if FriendlyNeighbourResult['Teller'] == Player2:
                if Player1 == FriendlyNeighbourResult['Listener']:
                    if Player1Alignment == 'Town':
                        Effect = "No"
                        EffectStrength = 'Definite'
                    elif Player1Alignment == 'Mafia':
                        if FriendlyNeighbourResult['Revealed'] == 'No':
                            Effect = "Yes"
                            EffectStrength = 'Strong'
                        elif FriendlyNeighbourResult['Revealed'] == 'Yes':
                            Effect = "No"
                            EffectStrength = 'Strong'
                if FriendlyNeighbourResult['Listener'] in Player1TeamMates:
                    if Player1Alignment == 'Mafia' and FriendlyNeighbourResult['Revealed'] == 'No':
                        Effect = "Yes"
                        EffectStrength = "Strong"
                    else:
                        Effect = "No"
                        EffectStrength = 'Strong'
                if FriendlyNeighbourResult['Revealed'] == 'Yes' and Player1 != FriendlyNeighbourResult['Listener'] and FriendlyNeighbourResult['Listener'] not in Player1TeamMates:
                    Effect = "No"
                    EffectStrength = 'Strong'
    return(EffectToReturn, EffectStrengthToReturn)


def DoesPlayer1VoteForPlayer2(Player1,Player2):
    AnswerToReturn = 'Yes'    # The default assumption is that the vote will be cast.
    Player1Alignment = GetAttributeFromPlayer(Player1,'Alignment')
    Player1Team = GetAttributeFromPlayer(Player1,'Team')
    Effect, EffectStrength = EffectOfInvestigationsOnLynchVote(Player1, Player2, Player1Team, Player1Alignment)
    if Effect != 'No' and EffectStrength != 'Strong' and EffectStrength != 'Definite': # If the investigations don't mean there's a refusal
        Effect, EffectStrength = EffectOfFriendlyNeighbourResults(Player1, Player2, Player1Team, Player1Alignment)
    if Effect != 'No' and EffectStrength != 'Strong' and EffectStrength != 'Definite': # If the investigations and neighbours don't mean there's a refusal
        # Test to see if the vote will be nullified because of teams
        if (Player1Team != 0) and (Player1Team == GetAttributeFromPlayer(Player2,'Team')):
            if Player1Alignment == 'Mafia':
                if GetAttributeFromPlayer(Player2,'InkBomb') != 'No':
                    Effect = 'No'
                    EffectStrength = 'Strong'
                else:
                    Effect = 'No'
                    EffectStrength = 'Weak'
            elif Player1Team == 'Town':
                Effect = 'No'
                EffectStrength = 'Definite'
    if Effect == 'No' and EffectStrength == 'Definite':
        AnswerToReturn = 'No'
    else:
        if Effect == "None" and EffectStrength == "None":
            Effect = "Yes"
            EffectStrength = "Strong"
        AnswerToReturn = GetYesOrNoFromStableProbability(Effect,EffectStrength)
    return(AnswerToReturn)


def GetYesOrNoFromStableProbability(Effect,EffectStrength):
    if Effect == 'Yes':
        if EffectStrength == 'Strong':
            ProbabilityPercentage = 90
        elif EffectStrength == 'Weak':
            ProbabilityPercentage = 75
    if Effect == 'No':
        if EffectStrength == 'Strong':
            ProbabilityPercentage = 10
        elif EffectStrength == 'Weak':
            ProbabilityPercentage = 25
    RandomNumber = randint(1,100)
    if RandomNumber < ProbabilityPercentage:
#        DebugPrint("Random Number " + str(RandomNumber) + " was lower than " + str(ProbabilityPercentage))
        return('Yes')
    else:
#        DebugPrint("Random Number " + str(RandomNumber) + " was equal to or higher than " + str(ProbabilityPercentage))
        return('No')


def GetYesOrNoFromChangingProbability(Effect,EffectStrength):
    global PlayerList
    MinimumProbability = .5
    MaximumProbability = .95
    CriticalProportion = .6
    ProportionOfPlayers = len(SearchPlayersFor('Alive','==',"'Yes'")) / len(PlayerList)
    Probability = ((MaximumProbability - MinimumProbability) / (CriticalProportion - MaximumProbability) * (ProportionOfPlayers - MaximumProbability)) + MinimumProbability
    Probability = max(Probability, MinimumProbability)
#    DebugPrint("Probability is " + str(Probability))
    if Effect == 'Yes':
        if EffectStrength == 'Strong':
            Probability = Probability * 2
#            DebugPrint("Probability has a Strong Yes modifier and is now " + str(Probability))
        elif EffectStrength == 'Weak':
            Probability = Probability * 1.4
#            DebugPrint("Probability has a Weak Yes modifier and is now " + str(Probability))
    if Effect == 'No':
        if EffectStrength == 'Strong':
            Probability = Probability / 2
#            DebugPrint("Probability has a Strong No modifier and is now " + str(Probability))
        elif EffectStrength == 'Weak':
            Probability = Probability / 1.4
#            DebugPrint("Probability has a Weak No modifier and is now " + str(Probability))
    Probability = min(Probability, 1)
    ProbabilityPercentage = Probability * 100
    ProbabilityPercentage = int(ProbabilityPercentage)
    RandomNumber = randint(1,100)
    if RandomNumber < ProbabilityPercentage:
#        DebugPrint("Random Number " + str(RandomNumber) + " was lower than " + str(ProbabilityPercentage))
        return('Yes')
    else:
#        DebugPrint("Random Number " + str(RandomNumber) + " was equal to or higher than " + str(ProbabilityPercentage))
        return('No')

def EffectOfInvestigationsOnLynchVote(Player1,Player2,Player1TeamNumber,Player1Alignment):
    global InvestigationResults
    EffectToReturn = "None"
    EffectStrengthToReturn = "None"
    Player2Alignment = GetAttributeFromPlayer(Player2,'Alignment')

    #First, build a list of all living players in the team
    Player1Team = [Player1]
    if Player1TeamNumber != 0:
        TeamMembers = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor('Team','==',Player1TeamNumber))
        if len(TeamMembers) != 0:
            for TeamMember in TeamMembers:
                Player1Team.append(TeamMember)

    #Next, check unrevealed investigations
    for Result in InvestigationResults:
        if Result['Revealed'] == 'No' and Result['Cop'] in Player1Team and Result['Target'] == Player2:
            if Player1Alignment == 'Town' and Player2Alignment == 'Town':
                EffectToReturn = 'No'
                EffectStrengthToReturn = 'Strong'
            elif Player1Alignment == 'Town' and Player2Alignment == 'Mafia':
                EffectToReturn = 'Yes'
                EffectStrengthToReturn = 'Strong'
            elif Player1Alignment == 'Mafia' and Player2Alignment == 'Mafia':
                EffectToReturn = 'No'
                EffectStrengthToReturn = 'Weak'

    #Next, check revealed investigations
    for Result in InvestigationResults:
        if Result['Revealed'] == 'Yes' and Result['Target'] == Player2:
            if Player1Alignment == 'Town' and Player2Alignment == 'Town':
                EffectToReturn = 'No'
                EffectStrengthToReturn = 'Strong'
            elif Player1Alignment == 'Town' and Player2Alignment == 'Mafia':
                EffectToReturn = 'Yes'
                EffectStrengthToReturn = 'Strong'
            elif Player1Alignment == 'Mafia' and Player2Alignment == 'Town':
                EffectToReturn = 'None'
                EffectStrengthToReturn = 'None'
            elif Player1Alignment == 'Mafia' and Player2Alignment == 'Mafia':
                EffectToReturn = 'Yes'
                EffectStrengthToReturn = 'Strong'

    return(EffectToReturn, EffectStrengthToReturn)

def NumberOfVotesRequiredToLynch():
    return(math.ceil(float(len(SearchPlayersFor('Alive','==',"'Yes'")))/2))


def ShuffleList(InputList):
    ReturnList = []
    for i in range(len(InputList)):
        element = random.choice(InputList)
        InputList.remove(element)
        ReturnList.append(element)
    return ReturnList


def AssignNightActionsForEachPlayer():
    global Night
    global NightsOnWhichThereAreNoKills
    TonightsTeamKillerActions = []
    TonightsTeamKillers = []
    TonightsFriendlyNeighbours = []
    TonightsCops = []
    TonightsCommuters = []
    TonightsDoctors = []
    TonightsRoleBlockers = []
    TonightsBusDrivers = []
    TonightsVigilantes = []
    TeamsWithLivingPlayers = BuildListOfTeamNumbers("")
    NightSearchVariable = "'Yes' or '" + IsNumberOddOrEven(Night) + "'"

    #If this is not an inkbombed night, assign team night killers
    if Night not in NightsOnWhichThereAreNoKills:
        if len(TeamsWithLivingPlayers) > 0:
            #DebugPrint("The teams to be searched for Team Night Killers are " + str(TeamsWithLivingPlayers))
            for Team in TeamsWithLivingPlayers:
                #DebugPrint("Team being searched for Team Night Killers: " + str(Team))
                LivingActiveTeamKillersInTeam = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor('Team',"==",Team),SearchPlayersFor('TeamNightKill',"!=","'No'"))
                if len(LivingActiveTeamKillersInTeam) > 0:
                    #DebugPrint("Going through the Team Killers for Team " + str(Team) + ", those being " + str(LivingActiveTeamKillersInTeam))
                    ActiveTeamKillersWithNoOtherActions = []
                    for Player in LivingActiveTeamKillersInTeam:
                        TeamNightKillForThisPlayer = GetAttributeFromPlayer(Player,'TeamNightKill')
                        if TeamNightKillForThisPlayer == "Yes" or TeamNightKillForThisPlayer == IsNumberOddOrEven(Night):
                            #DebugPrint("The night is right.")
                            if len(ReturnPlayersNonTeamKillActions(Player,NightSearchVariable)) == 0:
                                ActiveTeamKillersWithNoOtherActions.append(Player)
                    SelectedTeamKiller = 0
                    if len(ActiveTeamKillersWithNoOtherActions) == 0:
                        SelectedTeamKiller = PickRandomItemFromList(LivingActiveTeamKillersInTeam)
                    else:
                        SelectedTeamKiller = PickRandomItemFromList(ActiveTeamKillersWithNoOtherActions)
                    if SelectedTeamKiller != 0:
                        DebugPrint("Team " + str(Team) + " has selected Player " + str(SelectedTeamKiller) + " as the Team Night Killer.")
                        ReturnedPlayer, ReturnedAction, ReturnedAlternatives = PickNightActionForPlayer(SelectedTeamKiller,NightSearchVariable)
                        TonightsTeamKillerActions.append({'Player' : SelectedTeamKiller, 'AlternativeActions' : ReturnedAlternatives})
                        TonightsTeamKillers.append(SelectedTeamKiller)
    #Go through every living player not in TeamKillers and assign them an action
    LivingPlayersNotTeamKilling = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor('PlayerID','not in',str(TonightsTeamKillers)))
    for Player in LivingPlayersNotTeamKilling:
        #print("Finding a night action for Player " + str(Player) + ".")
        ReturnedPlayer, ReturnedAction, ReturnedAlternatives = PickNightActionForPlayer(Player,NightSearchVariable)
        #print("Action returned is " + str(ReturnedAction) + ".")
        if ReturnedAction == 'FriendlyNeighbour':
            TonightsFriendlyNeighbours.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
        elif ReturnedAction == 'Cop':
            TonightsCops.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
        elif ReturnedAction == 'Commuter':
            TonightsCommuters.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
        elif ReturnedAction == 'Doctor':
            TonightsDoctors.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
        elif ReturnedAction == 'RoleBlocker':
            TonightsRoleBlockers.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
        elif ReturnedAction == 'BusDriver':
            TonightsBusDrivers.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
        elif ReturnedAction == 'Vigilante':
            TonightsVigilantes.append({'Player' : ReturnedPlayer, 'AlternativeActions' : ReturnedAlternatives})
    return(TonightsTeamKillerActions, TonightsFriendlyNeighbours, TonightsCops, TonightsCommuters, TonightsDoctors, TonightsRoleBlockers, TonightsBusDrivers, TonightsVigilantes)


def PickNightActionForPlayer(Player,NightSearchVariable):
    ThisPlayersPossibleNightActions = ReturnPlayersNonTeamKillActions(Player,NightSearchVariable)
    #DebugPrint("Player " + str(Player) + "'s possible night actions are " + str(ThisPlayersPossibleNightActions) +".")
    ChosenAction = ""
    AlternativeActions = []
    if len(ThisPlayersPossibleNightActions) > 0: #If the player has possible actions
        PossibleActionsGivenNumberOfShots = []
        for Action in ThisPlayersPossibleNightActions:
            #Work out if the player would choose the action, given the number of shots available
            NumberOfShots = eval("GetAttributeFromPlayer(Player,'" + Action + "Shots')")
            if NumberOfShots < 0 or (NumberOfShots > 0 and (GetYesOrNoFromChangingProbability('Yes','Weak') == 'No')):
                PossibleActionsGivenNumberOfShots.append(Action)
        #Pick a random action from the available options
        ChosenAction = PickRandomItemFromList(PossibleActionsGivenNumberOfShots)
        for Action in PossibleActionsGivenNumberOfShots:
            if Action != ChosenAction:
                AlternativeActions.append(Action)
    return(Player,ChosenAction,AlternativeActions)


def ReturnPlayersNonTeamKillActions(Player,NightSearchVariable):
    global Night
    NonTeamKillActions = []
    #print("Returning non team kill night actions for Player " + str(Player))
    PossibleActions = ['FriendlyNeighbour','Cop','Commuter','Doctor','RoleBlocker','BusDriver','Vigilante']
    for PossibleAction in PossibleActions:
        if not (PossibleAction == 'Vigilante' and Night in NightsOnWhichThereAreNoKills):
            ActionValueIsAppropriate = "No"
            ActionShotsIsAppropriate = "No"
            ActionValue = eval("GetAttributeFromPlayer(Player,'" + PossibleAction + "')")
            if ActionValue == "Yes":
                ActionValueIsAppropriate = "Yes"
            elif ActionValue == IsNumberOddOrEven(Night):
                ActionValueIsAppropriate = "Yes"
            ActionShotsValue = eval("GetAttributeFromPlayer(Player,'" + PossibleAction + "Shots')")
            if ActionShotsValue != 0:
                ActionShotsIsAppropriate = "Yes"
            #DebugPrint("Night is " + IsNumberOddOrEven(Night) + ", ActionValue is " + ActionValue + ", ActionShotsValue is " + str(ActionShotsValue) +", Action is " + PossibleAction + ", ActionValueIsAppropriate = "+ ActionValueIsAppropriate+", ActionShotsValueIsAppropriate = " + ActionShotsIsAppropriate + ".")
            if ActionShotsIsAppropriate == "Yes" and ActionValueIsAppropriate == "Yes":
                #DebugPrint("Adding the " + PossibleAction + " for Player " +str(Player))
                NonTeamKillActions.append(PossibleAction)
    return(NonTeamKillActions)


def BuildListOfTeamNumbers(Alignment):   #Return a list of the numbers of the teams that have living players
    #Alignment = "Mafia", "Town", ""
    LivingPlayersInTeams = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive',"==","'Yes'"),SearchPlayersFor('Team',"!=",0))
    Teams = []
    for Player in LivingPlayersInTeams: #Build a list of the teams
        IsTeamAppropriateToAddToList = "No"
        TeamNumberForThisPlayer = GetAttributeFromPlayer(Player,'Team')
        if (Alignment == "" or GetAttributeFromPlayer(Player,'Alignment') == Alignment) and TeamNumberForThisPlayer not in Teams:
            Teams.append(GetAttributeFromPlayer(Player,'Team'))
    return(Teams)


def SeeIfAnyOneMafiaTeamHasTheMajority():
    LivingPlayers = SearchPlayersFor('Alive',"==","'Yes'")
    Majority = NumberOfVotesRequiredToLynch()
    MafiaTeams = BuildListOfTeamNumbers("Mafia")
    DebugPrint("Seeing if any one MafiaTeam out of Teams " + str(MafiaTeams) + " has " + str(Majority) + " votes.")
    for TeamNumber in MafiaTeams: #See if each scum team has the votes
        ListOfLivingPlayersInTeam = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive',"==","'Yes'"), SearchPlayersFor('Team',"==",TeamNumber))
        #DebugPrint("List of living players in team " + str(TeamNumber) +": " + str(ListOfLivingPlayersInTeam))
        if len(ListOfLivingPlayersInTeam) >= Majority:
            DebugPrint("The mafia team " + str(TeamNumber) + " has a majority of votes. Game over.")
            return('Yes')
    return('No')


def CheckForVictory():
    global WinningTeam
    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    MafiaPlayers = SearchPlayersFor('Alignment','==',"'Mafia'")
    LivingMafiaPlayers = ShuffleList(ReturnOneListWithCommonItemsFromTwoLists(LivingPlayers,MafiaPlayers))
    TownPlayers = SearchPlayersFor('Alignment','==',"'Town'")
    LivingTownPlayers = ShuffleList(ReturnOneListWithCommonItemsFromTwoLists(LivingPlayers,TownPlayers))
    DebugPrint("Living Town Players: " + str(LivingTownPlayers))
    DebugPrint("Living Mafia Players: " + str(LivingMafiaPlayers))
    if len(LivingMafiaPlayers) == 0:
        WinningTeam = "Town"
    elif len(LivingTownPlayers) == 0:
        WinningTeam = "Mafia"
    elif SeeIfAnyOneMafiaTeamHasTheMajority() == 'Yes':
        WinningTeam = "Mafia"
    elif len(LivingPlayers) == 2:
        WinningTeam = "Mafia"

def ConsiderRevealingFriendlyNeighbours():
    global FriendlyNeighbourResults
    for Result in FriendlyNeighbourResults:
        if Result['Revealed'] == 'No' and GetAttributeFromPlayer(Result['Listener'],'Alive') == 'Yes' and GetAttributeFromPlayer(Result['Teller'],'Alive') == 'Yes' and GetAttributeFromPlayer(Result['Listener'],'Alignment') == 'Town':
            if GetYesOrNoFromChangingProbability('Yes','Weak'):
                DebugPrint("Player " + str(Result['Listener']) + " is revealing that Player " + str(Result ['Teller']) + " is a Friendly Neighbour.")
                Result['Revealed'] = 'Yes'

def ConsiderRevealingInvestigations(Cop):
    global InvestigationResults
    global MafiaRevealedToday
    global MafiaRevealedByLynchedCop
    MafiaRevealedToday = []
    for Result in InvestigationResults:
        if Cop == 0:
            WillReveal = 'No'
            if Result['Revealed'] == 'No':
                if GetAttributeFromPlayer(Result['Cop'],'Alive') == "Yes" and GetAttributeFromPlayer(Result['Cop'],'Alignment') == "Town":
                    if Result['Alignment'] == 'Mafia' and GetAttributeFromPlayer(Result['Cop'],'Alignment') == "Town":
                        WillReveal = GetYesOrNoFromChangingProbability('Yes','Strong')
                    elif Result['Alignment'] != 'Mafia' and GetAttributeFromPlayer(Result['Cop'],'Alignment') == "Mafia":
                        WillReveal = GetYesOrNoFromChangingProbability('No','Strong')
                    else:
                        WillReveal = GetYesOrNoFromChangingProbability('No','Weak')
                    if WillReveal == 'Yes':
                        Result['Revealed'] = "Yes"
                        WriteAttributeToPlayer(Result['Cop'],'NumberOfNamesInHat',50)
                        if Result['Alignment'] == "Town":
                            WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',50)
                        if Result['Alignment'] == "Mafia":
                            WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',1500)
                            MafiaRevealedToday.append(Result['Target'])
                        DebugPrint("Player " + str(Result['Cop']) + " just revealed that they investigated Player " + str(Result['Target']) + " and found that they are " + str(Result['Alignment']))
        else:   #If this is a reveal being done on a cop bieng lynched
            if Result['Cop'] == Cop and Result['Revealed'] == 'No' and GetAttributeFromPlayer(Cop,'Alignment') == 'Town':
                Result['Revealed'] = "Yes"
                WriteAttributeToPlayer(Result['Cop'],'NumberOfNamesInHat',50)
                if Result['Alignment'] == "Town":
                    WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',50)
                if Result['Alignment'] == "Mafia":
                    WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',1500)
                    MafiaRevealedByLynchedCop.append(Result['Target'])
                DebugPrint("Before being lynched, player " + str(Result['Cop']) + " just revealed that they investigated Player " + str(Result['Target']) + " and found that they are " + str(Result['Alignment']))
    if Cop == 0:
        #Add in the ones revealed by the cop on being lynched yesterday, and then zero that variable.
        for Reveal in MafiaRevealedByLynchedCop:
            MafiaRevealedToday.append(Reveal)
        MafiaRevealedByLynchedCop = []

def SimulateSingleGame():
    InitiateSingleGameVariables()
    global IndexList
    global PlayerList
    #DebugPrint("PlayerList = " + str(PlayerList))
    #DebugPrint("IndexList = " + str(IndexList))

    global DaysThatDoNotHappen
    global Day
    global Night
    global TimeCounter
    global WinningTeam
    while WinningTeam == '':
        Day += 1
        Night += 1
        TimeCounter += 1
        #Day cycle
        DebugPrint(" ")
        DebugPrint("Day " + str(Day))
        if not Day in DaysThatDoNotHappen:
            ConsiderRevealingInvestigations(0)
            ConsiderRevealingFriendlyNeighbours()
            TryToLynch()
        CheckForVictory()
        LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
        DebugPrint("The remaining living players at the end of Day " + str(Day) + " are " + str(LivingPlayers))
        if WinningTeam != '':
            DayOrNightWhenGameEnded = "D" + str(Day)
        else:   #If no winning team at the end of the day, do the night
            #Night cycle
            TimeCounter += 1
            DebugPrint(" ")
            DebugPrint("Night " + str(Night))
            NightRoutine()
            CheckForVictory()
            if WinningTeam != '':
                DayOrNightWhenGameEnded = "N" + str(Night)
            LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
            DebugPrint("The remaining living players at the end of Night " + str(Night) + " are " + str(LivingPlayers))
    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    EndingMoment = str(TimeCounter) + "(" + str(DayOrNightWhenGameEnded) + ")"
    DebugPrint(" ")
    DebugPrint("Winners = " + WinningTeam)
    DebugPrint("Ending moment = " + str(TimeCounter) + "(" + str(DayOrNightWhenGameEnded) + ")")
    return(EndingMoment,WinningTeam)


def NightRoutine():
    global ThisNightsCommutings
    global ThisNightsRoleBlockings
    global BusDrivings
    global ThisNightsInvestigationActions
    global InvestigationResults
    global TeamNightKillActions
    global VigilanteActions
    global PlayersTargetedByDoctors
    global PlayersProtectedByDoctors
    global ActualNightKills
    global NightsOnWhichThereAreNoKills
    global ThisTurnsFriendlyNeighbourActions
    global ThisNightsPGOKills
    ThisNightsCommutings = []
    ThisNightsRoleBlockings =[]
    ThisNightsPGOKills =[]
    PlayersProtectedByDoctors = []
    ThisNightsInvestigationActions = []
    ThisTurnsFriendlyNeighbourActions = []
    ActualNightKills = []
    TonightsTeamKillerActions, TonightsFriendlyNeighbours, TonightsCops, TonightsCommuters, TonightsDoctors, TonightsRoleBlockers, TonightsBusDrivers, TonightsVigilantes = AssignNightActionsForEachPlayer()
    ReceiveCommuterActions(TonightsCommuters)
    ReceiveRoleBlockingActions(TonightsRoleBlockers)
    ReceiveBusDrivingActions(TonightsBusDrivers)
    ReceiveCopActions(TonightsCops)
    ReceiveDoctorActions(TonightsDoctors)
    ReceiveFriendlyNeighbourActions(TonightsFriendlyNeighbours)
    ReceiveTeamNightKillActions(TonightsTeamKillerActions)
    ReceiveVigilanteKillActions(TonightsVigilantes)
    ProcessCopActions()
    ProcessDoctorActions()
    ProcessFriendlyNeighbourActions()
    ProcessTeamNightKillActions()
    ProcessVigilanteKillActions()
    if not Night in NightsOnWhichThereAreNoKills:
        #DebugPrint("The night kills are not being skipped because this night is not in " + str(NightsOnWhichThereAreNoKills))
        for ActualNightKill in ActualNightKills:
            #DebugPrint("Player " + str(ActualNightKill['Killer']) + " is night killing " + str(ActualNightKill['Victim']))
            KillPlayer(ActualNightKill['Killer'],ActualNightKill['Victim'],'Night')
    else:
        DebugPrint("The night kills are being skipped because this night is in " + str(NightsOnWhichThereAreNoKills))


def ProcessDoctorActions():
    global PlayersTargetedByDoctors
    global PlayersProtectedByDoctors
    global ThisNightsCommutings
    for Target in PlayersTargetedByDoctors:
        ProtectionsResultingFromBusDriving = FindBusDrivingPairs(Target)
        for Protection in ProtectionsResultingFromBusDriving:
            if Protection not in ThisNightsCommutings:
                PlayersProtectedByDoctors.append(Protection)


def ProcessVigilanteKillActions():
    global VigilanteActions
    global ActualNightKills
    global PlayersProtectedByDoctors
    global ThisNightsCommutings
    for VigilanteKill in VigilanteActions:
        DeathsResultingFromBusDriving = FindBusDrivingPairs(VigilanteKill['Victim'])
        for Death in DeathsResultingFromBusDriving:
            if Death not in PlayersProtectedByDoctors:
                if Death not in ThisNightsCommutings:
                    ActualNightKills.append({'Killer': VigilanteKill['Killer'], 'Victim': Death})


def ProcessCopActions(): 
    global InvestigationResults
    global ThisNightsCommutings
    global ThisNightsInvestigationActions
    for Investigation in ThisNightsInvestigationActions:
        ActualTarget = FindBusDrivingPairs(Investigation['Target'])
        if len(ActualTarget) == 1: #Investigation fails if busdriving means there's multiple targets
            if ActualTarget not in ThisNightsCommutings:
                if GetAttributeFromPlayer(ActualTarget[0],'Godfather') != 'Yes':
                    RevealedAlignment = GetAttributeFromPlayer(ActualTarget[0],'Alignment')
                else:
                    RevealedAlignment = 'Town'
                InvestigationResults.append({'Cop':Investigation['Cop'],'Target':Investigation['Target'],'Alignment':RevealedAlignment,'Revealed':'No'})


def ProcessFriendlyNeighbourActions():
    global FriendlyNeighbourResults
    global ThisTurnsFriendlyNeighbourActions
    global ThisNightsCommutings
    for FriendlyNeighbourAction in ThisTurnsFriendlyNeighbourActions:
        #DebugPrint("Processing Friendly Neighour: " + str(FriendlyNeighbourAction))
        ActualTarget = FindBusDrivingPairs(FriendlyNeighbourAction['Target'])
        #DebugPrint("The Friendly Neighbour Actual Target is " + str(ActualTarget))
        for Target in ActualTarget:
            #DebugPrint("adding a target!")
            if Target not in ThisNightsCommutings:
                FriendlyNeighbourResults.append({'Teller':FriendlyNeighbourAction['FriendlyNeighbour'],'Listener':Target,'IntendedListener':FriendlyNeighbourAction['Target'],'Revealed':'No'})
    #DebugPrint("After processing Friendly Neighbours, FriendlyNeighbourResults = " + str(FriendlyNeighbourResults))

def ProcessTeamNightKillActions():
    global TeamNightKillActions
    global ActualNightKills
    global ThisNightsCommutings
    for TeamNightKill in TeamNightKillActions:
        DeathsResultingFromBusDriving = FindBusDrivingPairs(TeamNightKill['Victim'])
        for Death in DeathsResultingFromBusDriving:
            if Death not in PlayersProtectedByDoctors:
                if Death not in ThisNightsCommutings:
                    ActualNightKills.append({'Killer': TeamNightKill['Killer'], 'Victim': Death})


def FindBusDrivingPairs(PlayerID):
    ReturnedPlayerIDs = []
    global BusDrivings
    if BusDrivings == []:
        ReturnedPlayerIDs.append(PlayerID)
    else:
        #DebugPrint("There's a busdriving happening.")
        for BusDriving in BusDrivings:
            if BusDriving['Target1'] == PlayerID:
                ReturnedPlayerIDs.append(BusDriving['Target2'])
            elif BusDriving['Target2'] == PlayerID:
                ReturnedPlayerIDs.append(BusDriving['Target1'])
            else:
                ReturnedPlayerIDs.append(PlayerID)
    #DebugPrint("Accounting for busdrivings (if any), the player actually targeted is " + str(ReturnedPlayerIDs))
    return(ReturnedPlayerIDs)


def ReceiveRoleBlockingActions(TonightsRoleBlockers):
    global ThisNightsRoleBlockings
    global NightsOnWhichThereAreNoKills
    global ThisNightsCommutings
    ThisNightsRoleBlockings = []
    for RoleBlockerEntry in TonightsRoleBlockers:
        RoleBlocker = RoleBlockerEntry['Player']
        if GetAttributeFromPlayer(RoleBlocker,'Alignment') == 'Mafia':
            PlayerToBeRoleBlocked = TryToPickTownPlayer(RoleBlocker,[])
        else:
            PlayerToBeRoleBlocked = TryToPickMafiaPlayer(RoleBlocker,[])
        if PlayerToBeRoleBlocked != 0:
            if GetAttributeFromPlayer(PlayerToBeRoleBlocked,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(PlayerToBeRoleBlocked,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and PlayerToBeRoleBlocked not in ThisNightsCommutings:
                DebugPrint("Player " + str(RoleBlocker) + " tried to roleblock a PGO and is now getting killed.")
                PGOReaction(PlayerToBeRoleBlocked,RoleBlocker)
            else:
                WriteAttributeToPlayer(RoleBlocker, "RoleBlockerShots", GetAttributeFromPlayer(RoleBlocker, "RoleBlockerShots")-1)
                ThisNightsRoleBlockings.append({'RoleBlocker': RoleBlocker, 'Target' : PlayerToBeRoleBlocked})
                DebugPrint("Player " + str(RoleBlocker) + " is roleblocking " + str(PlayerToBeRoleBlocked))


def PGOReaction(Killer,Victim):
    global ActualNightKills
    WriteAttributeToPlayer(Killer, "ParanoidGunOwnerShots", GetAttributeFromPlayer(Killer, "ParanoidGunOwnerShots")-1)
    ActualNightKills.append({'Killer': Killer,'Victim': Victim})

def ReceiveBusDrivingActions(TonightsBusDrivers):
    global BusDrivings
    global NightOnWhichThereAreNoKills
    global ThisNightsCommutings
    BusDrivings = []
    for BusDriverEntry in TonightsBusDrivers:
        BusDriver = BusDriverEntry['Player']
        ExcludedPlayers = []
        BusDrivenPlayer1 = TryToPickMafiaPlayer(BusDriver,ExcludedPlayers)
        ExcludedPlayers.append(BusDrivenPlayer1)
        BusDrivenPlayer2 = TryToPickTownPlayer(BusDriver,ExcludedPlayers)

        if (BusDrivenPlayer1 != 0) and (BusDrivenPlayer2 != 0):
            if BusDrivenPlayer1 > BusDrivenPlayer2:
                InsertSlot1 = BusDrivenPlayer2
                InsertSlot2 = BusDrivenPlayer1
            else:
                InsertSlot1 = BusDrivenPlayer1
                InsertSlot2 = BusDrivenPlayer2
            if [InsertSlot1,InsertSlot2] not in BusDrivings:
                if GetAttributeFromPlayer(BusDrivenPlayer1,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(BusDrivenPlayer1,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and BusDrivenPlayer1 not in ThisNightsCommutings:
                    DebugPrint("Player " + str(BusDriver) + " tried to busdrive a PGO and is now getting killed.")
                    PGOReaction(BusDrivenPlayer1,BusDriver)
                elif GetAttributeFromPlayer(BusDrivenPlayer2,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(BusDrivenPlayer2,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and BusDrivenPlayer2 not in ThisNightsCommutings:
                    DebugPrint("Player " + str(BusDriver) + " tried to busdrive a PGO and is now getting killed.")
                    PGOReaction(BusDrivenPlayer2,BusDriver)
                else:
                    if not (BusDrivenPlayer1 in ThisNightsCommutings or BusDrivenPlayer2 in ThisNightsCommutings):
                        #DebugPrint("Tried to busdrive an active commuter, and so failed.")
                    #else:
                        DebugPrint("Player " + str(BusDriver) + " is busdriving Player " + str(BusDrivenPlayer1) + " and Player " + str(BusDrivenPlayer2))
                        BusDrivings.append({'BusDriver': BusDriver, 'Target1' : BusDrivenPlayer1, 'Target2' : BusDrivenPlayer2})
        else:
            DebugPrint("Player " + str(BusDriver) + " failed to pick two targets to busdrive.")


def ReceiveTeamNightKillActions(TonightsTeamKillerActions):
    global TeamNightKillActions
    global ThisNightsInvestigationActions
    global ThisNightsDoctorActions
    global BusDrivings
    TeamNightKillActions = []
    for TeamKillerEntry in TonightsTeamKillerActions:
        TeamKiller = TeamKillerEntry['Player']
        Team = GetAttributeFromPlayer(TeamKiller,"Team")
        if GetAttributeFromPlayer(TeamKiller,'Alignment') == "Mafia":
            PlayersExcludedBecauseOfTeamActions = []
            for BusDriving in BusDrivings:
                #DebugPrint("Busdriving found.")
                if BusDriving['BusDriver'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                    #DebugPrint("Busdriving was by a team member!")
                    PlayersExcludedBecauseOfTeamActions.append(BusDriving['Target1'])
                    PlayersExcludedBecauseOfTeamActions.append(BusDriving['Target2'])
            Target = TryToPickTownPlayer(TeamKiller,PlayersExcludedBecauseOfTeamActions)
        else:
            #First ensure you don't try to nightkill a person your teammate is investigating, doctoring or busdriving
            PlayersExcludedBecauseOfTeamActions = []
            for Investigation in ThisNightsInvestigationActions:
                if Investigation['Cop'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                    PlayersExcludedBecauseOfTeamActions.append(Investigation['Target'])
            for Doctoring in ThisNightsDoctorActions:
                if Doctoring['Doctor'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                    PlayersExcludedBecauseOfTeamActions.append(Doctoring['Target'])
            #DebugPrint("Checking to see if Player " + str(TeamKiller) + "'s NightKill for Team " + str(Team) + " needs to exclude anyone because of busdriving.")
            for BusDriving in BusDrivings:
                #DebugPrint("Busdriving found.")
                if BusDriving['BusDriver'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                    #DebugPrint("Busdriving was by a team member!")
                    PlayersExcludedBecauseOfTeamActions.append(BusDriving['Target1'])
                    PlayersExcludedBecauseOfTeamActions.append(BusDriving['Target2'])
            Target = TryToPickMafiaPlayer(TeamKiller,PlayersExcludedBecauseOfTeamActions)
        if Target != 0:
            ActualTargets = FindBusDrivingPairs(Target)
            for ActualTarget in ActualTargets:
                global NightsOnWhichThereAreNoKills
                global ThisNightsCommutings
                if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                    DebugPrint("Player " + str(TeamKiller) + " tried to TeamKill a PGO and is now getting killed.")
                    PGOReaction(ActualTarget,TeamKiller)
            TeamNightKillActions.append({'Killer': TeamKiller,'Victim': Target})
            DebugPrint("Player " + str(TeamKiller) + " is NightKilling Player " + str(Target) + " for team " + str(GetAttributeFromPlayer(TeamKiller,'Team')))


def ReceiveCommuterActions(TonightsCommuters):
    global ThisNightsCommutings
    ThisNightsCommutings = []
    for CommuterEntry in TonightsCommuters:
        Commuter = CommuterEntry['Player']
        WriteAttributeToPlayer(Commuter, "CommuterShots", GetAttributeFromPlayer(Commuter, "CommuterShots")-1)
        ThisNightsCommutings.append(Commuter)
        DebugPrint("Player " + str(Commuter) + " is commuting.")


def ReceiveVigilanteKillActions(TonightsVigilantes):
    global VigilanteActions
    global ThisNightsInvestigationActions
    global ThisNightsDoctorActions
    VigilanteActions = []
    for VigilanteEntry in TonightsVigilantes:
        Vigilante = VigilanteEntry['Player']
        if GetAttributeFromPlayer(Vigilante,'Alignment') == "Mafia":
            Target = TryToPickTownPlayer(Vigilante,[])
        else:
            PlayersBeingInvestigatedOrDoctoredByTeammates = []
            if GetAttributeFromPlayer(Vigilante, 'Team') != 0:
                for Investigation in ThisNightsInvestigationActions:
                    if Investigation['Cop'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                        PlayersBeingInvestigatedOrDoctoredByTeammates.append(Investigation['Target'])
                for Doctoring in ThisNightsDoctorActions:
                    if Doctoring['Doctor'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                        PlayersBeingInvestigatedOrDoctoredByTeammates.append(Doctoring['Target'])
            Target = TryToPickMafiaPlayer(Vigilante,PlayersBeingInvestigatedOrDoctoredByTeammates)
        if Target != 0:
            ActualTargets = FindBusDrivingPairs(Target)
            global NightsOnWhichThereAreNoKills
            global ThisNightsCommutings
            for ActualTarget in ActualTargets:
                if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                    DebugPrint("Player " + str(Vigilante) + " tried to VigilanteKill a PGO and is now getting killed.")
                    PGOReaction(ActualTarget,Vigilante)
            WriteAttributeToPlayer(Vigilante, "VigilanteShots", GetAttributeFromPlayer(Vigilante, "VigilanteShots")-1)
            VigilanteActions.append({'Killer': Vigilante,'Victim': Target})
            DebugPrint("Player " + str(Vigilante) + " is NightKilling Player " + str(Target) + " as a Vigilante.")


def ReceiveDoctorActions(TonightsDoctors):
    global PlayersTargetedByDoctors
    global Night
    global ThisNightsDoctorActions
    global NightsOnWhichThereAreNoKills
    global ThisNightsCommutings
    ThisNightsDoctorActions = []
    PlayersTargetedByDoctors = []
    for DoctorEntry in TonightsDoctors:
        Doctor = DoctorEntry['Player']
        if GetAttributeFromPlayer(Doctor,'Alignment') == 'Mafia':
            PlayerToBeDoctored = TryToPickMafiaPlayer(Doctor,[])
        else:
            PlayerToBeDoctored = TryToPickTownPlayer(Doctor,[])
        if PlayerToBeDoctored != 0:
            PGOKilled = 'No'
            ActualTargets = FindBusDrivingPairs(PlayerToBeDoctored)
            for ActualTarget in ActualTargets:
                if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                    DebugPrint("Player " + str(Doctor) + " tried to doctor a PGO and is now getting killed.")
                    PGOReaction(ActualTarget,Doctor)
                    PGOKilled = "Yes"
            if PGOKilled == 'No':
                WriteAttributeToPlayer(Doctor, "DoctorShots", GetAttributeFromPlayer(Doctor, "DoctorShots")-1)
                ThisNightsDoctorActions.append({'Doctor': Doctor, 'Target' : PlayerToBeDoctored})
                PlayersTargetedByDoctors.append(PlayerToBeDoctored)
                DebugPrint("Player " + str(Doctor) + " is Doctoring " + str(PlayerToBeDoctored))


def ReceiveFriendlyNeighbourActions(TonightsFriendlyNeighbours):
    global ThisTurnsFriendlyNeighbourActions
    global FriendlyNeighbourResults
    global NightsOnWhichThereAreNoKills
    global ThisNightsCommutings
    ThisTurnsFriendlyNeighbourActions = []
    for FriendlyNeighbourEntry in TonightsFriendlyNeighbours:
        FriendlyNeighbour = FriendlyNeighbourEntry['Player']
        WillNotTell = []
        #Build a list of people who this neighbour has previously targeted, or who is in their team.
        for FriendlyNeighbourResult in FriendlyNeighbourResults:
            if (FriendlyNeighbourResult['Teller'] == FriendlyNeighbour):
                if FriendlyNeighbourResult['Revealed'] == 'Yes':
                    WillNotTell.append(FriendlyNeighbourResult['Listener'])
                else:
                    WillNotTell.append(FriendlyNeighbourResult['IntendedListener'])
        FriendlyNeighbourTeam = GetAttributeFromPlayer(FriendlyNeighbour,'Team')
        if FriendlyNeighbourTeam != 0:
            WillNotTell += SearchPlayersFor('Team','==',FriendlyNeighbourTeam)
            DebugPrint("Friendly Neighbour, player " + str(FriendlyNeighbour) + " is not going to tell " +str(WillNotTell))
        Target = TryToPickTownPlayer(FriendlyNeighbour,WillNotTell)
        if Target != 0:
            PGOKilled = 'No'
            ActualTargets = FindBusDrivingPairs(Target)
            for ActualTarget in ActualTargets:
                if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                    DebugPrint("Player " + str(FriendlyNeighbour) + " tried to friendly neighbour a PGO and is now getting killed.")
                    PGOReaction(ActualTarget,FriendlyNeighbour)
                    PGOKilled = "Yes"
            if PGOKilled == 'No':
                WriteAttributeToPlayer(FriendlyNeighbour, "FriendlyNeighbourShots", GetAttributeFromPlayer(FriendlyNeighbour, "FriendlyNeighbourShots")-1)
                ThisTurnsFriendlyNeighbourActions.append({'FriendlyNeighbour': FriendlyNeighbour, 'Target' : Target})
                DebugPrint("Player " + str(FriendlyNeighbour) + " is being a Friendly Neighbour and informing Player " + str(Target))


def ReceiveCopActions(TonightsCops):
    global ThisNightsInvestigationActions
    global NightsOnWhichThereAreNoKills
    global ThisNightsCommutings
    ThisNightsInvestigationActions = []
    #Build a list of cops who will be asked for night actions
    for CopEntry in TonightsCops:
        Cop = CopEntry['Player']
        WillNotInvestigate = GetPlayersWhoCopWillNotInvestigate(Cop)
        if GetAttributeFromPlayer(Cop,'Alignment') == "Mafia":
            Target = TryToPickTownPlayer(Cop,WillNotInvestigate)
        else:
            Target = TryToPickMafiaPlayer(Cop,WillNotInvestigate)
        if Target != 0:
            PGOKilled = 'No'
            ActualTargets = FindBusDrivingPairs(Target)
            for ActualTarget in ActualTargets:
                if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                    DebugPrint("Player " + str(Cop) + " tried to investigate a PGO and is now getting killed.")
                    PGOReaction(ActualTarget,Cop)
                    PGOKilled = "Yes"
            if PGOKilled == 'No':
                WriteAttributeToPlayer(Cop, "CopShots", GetAttributeFromPlayer(Cop, "CopShots")-1)
                ThisNightsInvestigationActions.append({'Cop': Cop, 'Target' : Target})
                DebugPrint("Player " + str(Cop) + " is Investigating Player " + str(Target))


def GetPlayersWhoCopWillNotInvestigate(Cop):
    CopTeam = GetAttributeFromPlayer(Cop,"Team") != 0
    if CopTeam != 0:
        CopTeamMates = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alive','==',"'Yes'"), SearchPlayersFor('PlayerID','!=',Cop), SearchPlayersFor('Team','==',CopTeam))
    else:
        CopTeamMates = []
    WillNotInvestigate = []
    #Build a list of people who have been the target of a revealed investigation by anyone or an unrevealed investigation by this cop
    if len(InvestigationResults) > 0:
        for Investigation in InvestigationResults:
            if (Investigation['Cop'] == Cop) or (Investigation['Cop'] in CopTeamMates) or (Investigation['Revealed'] == 'Yes'):
                if GetYesOrNoFromStableProbability('No','Strong') == 'No': #Probably add to list of people not to investigate
                    WillNotInvestigate.append(Investigation['Target'])
    #Exclude Friendly Neighbours
    global FriendlyNeighbourResults
    if len(FriendlyNeighbourResults) > 0:
        for FriendlyNeighbourResult in FriendlyNeighbourResults:
            if (FriendlyNeighbourResult['Listener'] == Cop) or (FriendlyNeighbourResult['Listener'] in CopTeamMates) or (FriendlyNeighbourResult['Revealed'] == 'Yes'):
                if GetYesOrNoFromStableProbability('No','Strong') == 'No': #Probably add to list of people not to investigate
                    WillNotInvestigate.append(FriendlyNeighbourResult['Teller'])
    #Exclude Innocent Children
    for InnocentChild in SearchPlayersFor('InnocentChild','==',"'Yes'"):
        if GetYesOrNoFromStableProbability('No','Strong') == 'No':
            WillNotInvestigate.append(InnocentChild)
    return(WillNotInvestigate)


def DebugPrint(StringToPrint):
    global PrintDebugLines
    if PrintDebugLines == 1:
        print(StringToPrint)

global MafiaPunishRewardMultiplier
global TownPunishRewardMultiplier
global MafiaStartingNamesInHat
global TownStartingNamesInHat
global GlobalPlayerList

NumberOfPlayers = GetNumberOfPlayersFromTextFile()
print("Number Of Players = " +str(NumberOfPlayers))

MafiaPunishRewardMultiplier = max((1.2903451676529 - (0.009457593688363 * NumberOfPlayers)),1)
TownPunishRewardMultiplier = min((0.87159763313609 + (0.0032248520710059 * NumberOfPlayers)),1)
MafiaStartingNamesInHat = int(max((551.73668639053 - (1.9852071005917 * NumberOfPlayers)),500))
TownStartingNamesInHat = int(min((474.31656804734 + (0.92603550295856 * NumberOfPlayers)),500))

#print("MafiaPunishRewardMultiplier = " +str(MafiaPunishRewardMultiplier))
#print("TownPunishRewardMultiplier = " +str(TownPunishRewardMultiplier))
#print("MafiaStartingNamesInHat = " +str(MafiaStartingNamesInHat))
#print("TownStartingNamesInHat = " +str(TownStartingNamesInHat))


GlobalPlayerList = CreatePlayerList()
global IndexList


PrintDebugLines = 0
ResultsFile = open('results.txt','w')
ResultsFile.write('Ending Day,Winning Team\n')
i=0
TownVictories = 0
MafiaVictories = 0
while i<200:
    EndingTime, EndingTeam = SimulateSingleGame()
    ResultsFile.write(EndingTime + "," + EndingTeam + "\n")
    if EndingTeam == "Town":
        TownVictories += 1
    else:
        MafiaVictories +=1
    print("Iteration " + str(i))
    print("Town Victories = " + str(TownVictories))
    print("Mafia Victories = " + str(MafiaVictories))
    i+=1

print("Town Victories = " + str(TownVictories))
print("Mafia Victories = " + str(MafiaVictories))