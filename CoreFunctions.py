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
    global TimeCounter
    TimeCounter = 0
    global DaysThatDoNotHappen
    DaysThatDoNotHappen = []    #This is needed for the Beloved Princess
    global NightsOnWhichThereAreNoKills
    NightsOnWhichThereAreNoKills = []   #This is needed for the Inkbomb
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
        print("Dying player was a " + RoleType + ". Looking for deputies.")
        PossibleDeputies = []
        LivingDeputiesOfSameAlignmentAndTeam = []
        LivingDeputiesOfSameAlignment = ReturnOneListWithCommonItemsFromThreeLists(SearchPlayersFor('Alignment','==',"'" + GetAttributeFromPlayer(DyingPlayer,'Alignment') + "'"),SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor('Deputy' + RoleType,'==',"'Yes'"))
        if len(LivingDeputiesOfSameAlignment) != 0: # If there are any living deputies of same alignment
            print("There are some deputy "+ RoleType + "s of that alignment.")
            if GetAttributeFromPlayer(DyingPlayer,'Team') != 0: # If the dying player has a team, and there are deputies alive on that team, narrow the list to those on that team
                print("The player had a team, so we're looking for deputies on that team.")
                LivingDeputiesOfSameAlignmentAndTeam = ReturnOneListWithCommonItemsFromTwoLists(LivingDeputiesOfSameAlignment,SearchPlayersFor('Team','==',GetAttributeFromPlayer(DyingPlayer,'Team')))
                if len(LivingDeputiesOfSameAlignmentAndTeam) == 0:
                    print("There were no deputies on that team, so we're looking for any deputies.")
                    LivingDeputiesOfSameAlignmentAndTeam = LivingDeputiesOfSameAlignment
            else: # If the dying player has no team, any deputy of that alignment will do
                print("The player had no team, so we're looking for any deputies.")
                LivingDeputiesOfSameAlignmentAndTeam = LivingDeputiesOfSameAlignment
        if len(LivingDeputiesOfSameAlignmentAndTeam) != 0:
            FoundDeputy = PickRandomItemFromList(LivingDeputiesOfSameAlignmentAndTeam)
            print("We found a living Deputy " + RoleType + "! It was player " + str (FoundDeputy))
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
    PlayerToReturn['Inkbomb'] = 'No'                 # # "No", "Lynch", "Night" or "Either" (if not "No", must be Mafia. Other values refer to triggering type of kill.)
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

    #If there's been mafia revealed this day.
    global MafiaRevealedToday
    LivingMafiaRevealedToday = ReturnOneListWithCommonItemsFromTwoLists(MafiaRevealedToday,SearchPlayersFor('Alive','==',"'Yes'"))
    while len(LivingMafiaRevealedToday) > 0 and PlayerWhoWillBeLynched == 0:
        CandidatePickedFromHat = PickNameFromHatForLynch(LivingMafiaRevealedToday)
        print("Seeing if we can lynch Revealed Mafia, Player " + str(CandidatePickedFromHat))
        GetsEnoughVotes, ActualVoters = WillGetEnoughLynchVotes(CandidatePickedFromHat)
        if GetsEnoughVotes == "Yes":    # See if this candidate gets enough votes
            PlayerWhoWillBeLynched = CandidatePickedFromHat
        else:
            Candidates.remove(CandidatePickedFromHat)
            LivingMafiaRevealedToday.remove(CandidatePickedFromHat)


    #If there's no mafia been revealed this day
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
    ResistancesOvercome = "No" #Test resistances first
    if KillType == "Lynch":
        if GetAttributeFromPlayer(Victim,'LynchResistant') != 0:  #If player is lynch resistant
            WriteAttributeToPlayer(Victim,'LynchResistant',int(GetAttributeFromPlayer(Victim,'LynchResistant'))-1)
            print("Player was lynch-resistant.")
        else:
            ResistancesOvercome = "Yes"
    elif KillType == "Night":
        if GetAttributeFromPlayer(Victim,'NightKillResistant') != 0:  #If player is NK resistant
            WriteAttributeToPlayer(Victim,'NightKillResistant',int(GetAttributeFromPlayer(Victim,'NightKillResistant'))-1)
            print("Player was night-kill-resistant.")
        else:
            ResistancesOvercome = "Yes"
    if KillType == "LynchBomb" or KillType == "NightBomb":
        ResistancesOvercome = "Yes"
    if ResistancesOvercome == "Yes": #Proceed if resistances are overcome
        KillBecomesConvert = "No"   #Check whether kill fails because player is Judas or Saulus
        if GetAttributeFromPlayer(Victim,'Judas') == 'Yes' and GetAttributeFromPlayer(Victim,'Alignment') == 'Town': #If Player is a Judas
            WriteAttributeToPlayer(Victim,'Alignment','Mafia')
            KillBecomesConvert = "Yes"
            print("Player was a Judas! Player is now Mafia.")
        elif GetAttributeFromPlayer(Victim,'Saulus') == 'Yes' and GetAttributeFromPlayer(Victim,'Alignment') == 'Mafia': #If Player is a Saulus
            WriteAttributeToPlayer(Victim,'Alignment','Town')
            KillBecomesConvert = "Yes"
            print("Player was a Saulus! Player is now Town.")
        if KillBecomesConvert == "No": #Proceed if kill wasn't converted
            WriteAttributeToPlayer(Victim,'Alive','No')   #kill player
            TestForDeputies(Victim)
            BelovedPrincess = GetAttributeFromPlayer(Victim,'BelovedPrincess')
            Inkbomb = GetAttributeFromPlayer(Victim,'Inkbomb')
            if BelovedPrincess == 'Either' or BelovedPrincess == KillType: # If player is a Beloved Princess
                print("Player " + str(Victim) + " was a Beloved Princess! Day " + str(Day + 1) + " will be skipped.")
                global DaysThatDoNotHappen
                DaysThatDoNotHappen.append(Day+1)
            if Inkbomb == 'Either' or Inkbomb == KillType: # If player is an Inkbomb
                if KillType == "Lynch":
                    NightOnWhichThereWillBeNoKills = Night
                elif KillType == "Night":
                    NightOnWhichThereWillBeNoKills = Night+1
                print("Player " + str(Victim) + " was a Inkbomb! There can be no night kills on " + str(NightOnWhichThereWillBeNoKills) + ".")
                global NightsOnWhichThereAreNoKills
                NightsOnWhichThereAreNoKills.append(NightOnWhichThereWillBeNoKills)
            if KillType == 'Lynch' and GetAttributeFromPlayer(Victim,'LynchBomb') == 'Yes':
                RandomVoterKilled = PickRandomItemFromList(Killer)
                print("Player " + str(Victim) + " was a LynchBomb. Random voter, Player " + str(RandomVoterKilled) + ", is targeted by the bomb.")
                KillPlayer(Victim,RandomVoterKilled,'LynchBomb')   #Kill random voter
            elif KillType == 'Night' and GetAttributeFromPlayer(Victim,'NightBomb') == 'Yes':
                print("Player " + str(Victim) + " was a NightBomb. Their killer, Player " + str(Killer) + ", is targeted by the bomb.")
                KillPlayer(Victim,Killer,'NightBomb')   #Kill killer


def PunishAndRewardVotersAfterLynch(Voters,LynchedPlayer):
    MinimumProbability = 1
    MaximumProbability = 5
    CriticalProportion = .8
    ProportionOfPlayers = len(SearchPlayersFor('Alive','==',"'Yes'")) / len(PlayerList)
    Probability = ((MaximumProbability - MinimumProbability) / (CriticalProportion - MaximumProbability) * (ProportionOfPlayers - MaximumProbability)) + MinimumProbability
    Probability = max(Probability, MinimumProbability)
    AlignmentOfDeadPlayer = GetAttributeFromPlayer(LynchedPlayer,'Alignment')
    #Punish and reward the voters
    for Voter in Voters:
        if AlignmentOfDeadPlayer == 'Mafia':
            ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(10,15))
            NewNumber=GetAttributeFromPlayer(Voter,'NumberOfNamesInHat')-ChangeToNumberOfNamesInHat
#            print("Player " + str(Voter) + " voted to lynch a mafia.")
        elif AlignmentOfDeadPlayer == 'Town':
            ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(10,15))
            NewNumber=GetAttributeFromPlayer(Voter,'NumberOfNamesInHat')+ChangeToNumberOfNamesInHat
 #           print("Player " + str(Voter) + " voted to lynch a town.")
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
                    ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(1,5))
                    NewNumber = GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')+ChangeToNumberOfNamesInHat
#                    print("Player " + str(NonVoter) + " didn't vote to lynch a mafia.")
                elif AlignmentOfDeadPlayer == 'Town':
                    ChangeToNumberOfNamesInHat = math.ceil(Probability * randint(1,5))
                    NewNumber = GetAttributeFromPlayer(NonVoter,'NumberOfNamesInHat')-ChangeToNumberOfNamesInHat
#                    print("Player " + str(NonVoter) + " didn't vote to lynch a town.")
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
        if NumberOfNamesFromPlayerList >=130 and GetAttributeFromPlayer(PlayerInHat,'InnocentChild') != "Yes": #If the candidate is probably mafia, don't add them.
            NumberOfTimesToGoInHat = 0
        else: #If the candidate might not be mafia, figure out how many names to add (reversing polarity)
            if NumberOfNamesFromPlayerList >= 100:
                NumberOfTimesToGoInHat = 100 - (NumberOfNamesFromPlayerList - 100)
            else:
                NumberOfTimesToGoInHat = 100 + (100 - NumberOfNamesFromPlayerList)
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
                        elif FriendlyNeighbourResult['Revealed'] == 'Yes':
                            if Investigation['Alignment'] == 'Town':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat * 2)
                            elif Investigation['Alignment'] == 'Mafia':
                                NumberOfTimesToGoInHat = int(NumberOfTimesToGoInHat / 1.5)
            # Increase chance for Innocent Children
            if GetAttributeFromPlayer(PlayerInHat,'InnocentChild') == "Yes":
                NumberOfTimesToGoInHat = NumberOfTimesToGoInHat * 3
            # Increase chances for person who is on same town team
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
                        elif FriendlyNeighbourResult['Revealed'] == 'Yes':
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
                if GetAttributeFromPlayer(Player2,'Inkbomb') == 'Yes':
                    Effect = 'No'
                    EffectStrength = 'Weak'
                else:
                    Effect = 'No'
                    EffectStrength = 'Strong'
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
#        print("Random Number " + str(RandomNumber) + " was lower than " + str(ProbabilityPercentage))
        return('Yes')
    else:
#        print("Random Number " + str(RandomNumber) + " was equal to or higher than " + str(ProbabilityPercentage))
        return('No')


def GetYesOrNoFromChangingProbability(Effect,EffectStrength):
    global PlayerList
    MinimumProbability = .5
    MaximumProbability = .95
    CriticalProportion = .6
    ProportionOfPlayers = len(SearchPlayersFor('Alive','==',"'Yes'")) / len(PlayerList)
    Probability = ((MaximumProbability - MinimumProbability) / (CriticalProportion - MaximumProbability) * (ProportionOfPlayers - MaximumProbability)) + MinimumProbability
    Probability = max(Probability, MinimumProbability)
#    print("Probability is " + str(Probability))
    if Effect == 'Yes':
        if EffectStrength == 'Strong':
            Probability = Probability * 2
#            print("Probability has a Strong Yes modifier and is now " + str(Probability))
        elif EffectStrength == 'Weak':
            Probability = Probability * 1.4
#            print("Probability has a Weak Yes modifier and is now " + str(Probability))
    if Effect == 'No':
        if EffectStrength == 'Strong':
            Probability = Probability / 2
#            print("Probability has a Strong No modifier and is now " + str(Probability))
        elif EffectStrength == 'Weak':
            Probability = Probability / 1.4
#            print("Probability has a Weak No modifier and is now " + str(Probability))
    Probability = min(Probability, 1)
    ProbabilityPercentage = Probability * 100
    ProbabilityPercentage = int(ProbabilityPercentage)
    RandomNumber = randint(1,100)
    if RandomNumber < ProbabilityPercentage:
#        print("Random Number " + str(RandomNumber) + " was lower than " + str(ProbabilityPercentage))
        return('Yes')
    else:
#        print("Random Number " + str(RandomNumber) + " was equal to or higher than " + str(ProbabilityPercentage))
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
    print("Living Town Players: " + str(LivingTownPlayers))
    print("Living Mafia Players: " + str(LivingMafiaPlayers))
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
                print("Player " + str(Result['Listener']) + " is revealing that Player " + str(Result ['Teller']) + " is a Friendly Neighbour.")
                Result['Revealed'] = 'Yes'

def ConsiderRevealingInvestigations():
    global InvestigationResults
    global MafiaRevealedToday
    MafiaRevealedToday = []
    for Result in InvestigationResults:
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
                    WriteAttributeToPlayer(Result['Cop'],'NumberOfNamesInHat',10)
                    if Result['Alignment'] == "Town":
                        WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',10)
                    if Result['Alignment'] == "Mafia":
                        WriteAttributeToPlayer(Result['Target'],'NumberOfNamesInHat',300)
                        MafiaRevealedToday.append(Result['Target'])
                    print("Player " + str(Result['Cop']) + " just revealed that they investigated Player " + str(Result['Target']) + " and found that they are " + str(Result['Alignment']))

def SimulateSingleGame():
    InitiateSingleGameVariables()
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
        print()
        print("Day " + str(Day))
        if not Day in DaysThatDoNotHappen:
            ConsiderRevealingInvestigations()
            ConsiderRevealingFriendlyNeighbours()
            TryToLynch()
        CheckForVictory()
        LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
        print("The remaining living players at the end of Day " + str(Day) + " are " + str(LivingPlayers))
        if WinningTeam != '':
            DayOrNightWhenGameEnded = "D" + str(Day)
        else:   #If no winning team at the end of the day, do the night
            #Night cycle
            TimeCounter += 1
            print()
            print("Night " + str(Night))
            NightRoutine()
            CheckForVictory()
            if WinningTeam != '':
                DayOrNightWhenGameEnded = "N" + str(Night)
            LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
            print("The remaining living players at the end of Night " + str(Night) + " are " + str(LivingPlayers))
    LivingPlayers = SearchPlayersFor('Alive','==',"'Yes'")
    EndingMoment = str(TimeCounter) + "(" + str(DayOrNightWhenGameEnded) + ")"
    print()
    print("Winners = " + WinningTeam)
    print("Ending moment = " + str(TimeCounter) + "(" + str(DayOrNightWhenGameEnded) + ")")
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
    ReceiveCommuterActions()
    ReceiveRoleBlockingActions()
    ReceiveBusDrivingActions()
    ReceiveCopActions()
    ReceiveDoctorActions()
    ReceiveFriendlyNeighbourActions()
    ReceiveTeamNightKillActions()
    ReceiveVigilanteKillActions()
    ProcessCopActions()
    ProcessDoctorActions()
    ProcessFriendlyNeighbourActions()
    ProcessTeamNightKillActions()
    ProcessVigilanteKillActions()
    if Night not in NightsOnWhichThereAreNoKills:
        print("The night kills are not being skipped because this night is not in " + str(NightsOnWhichThereAreNoKills))
        for ActualNightKill in ActualNightKills:
            print("Player " + str(ActualNightKill['Killer']) + " is night killing " + str(ActualNightKill['Victim']))
            KillPlayer(ActualNightKill['Killer'],ActualNightKill['Victim'],'Night')
    else:
        print("The night kills are being skipped because this night is in " + str(NightsOnWhichThereAreNoKills))


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
        #print("Processing Friendly Neighour: " + str(FriendlyNeighbourAction))
        ActualTarget = FindBusDrivingPairs(FriendlyNeighbourAction['Target'])
        #print("The Friendly Neighbour Actual Target is " + str(ActualTarget))
        for Target in ActualTarget:
            #print("adding a target!")
            if Target not in ThisNightsCommutings:
                FriendlyNeighbourResults.append({'Teller':FriendlyNeighbourAction['FriendlyNeighbour'],'Listener':Target,'IntendedListener':FriendlyNeighbourAction['Target'],'Revealed':'No'})
    #print("After processing Friendly Neighbours, FriendlyNeighbourResults = " + str(FriendlyNeighbourResults))

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
    #print("BusDrivings = " + str(BusDrivings))
    if BusDrivings == []:
        #print("No Busdrivings.")
        ReturnedPlayerIDs.append(PlayerID)
    else:
        #print("Some Busdrivings.")
        for BusDriving in BusDrivings:
            if BusDriving[0] == PlayerID:
                ReturnedPlayerIDs.append(BusDriving[1])
            elif BusDriving[1] == PlayerID:
                ReturnedPlayerIDs.append(BusDriving[0])
            else:
                ReturnedPlayerIDs.append(PlayerID)
    #print("Returning " + str(ReturnedPlayerIDs))
    return(ReturnedPlayerIDs)


def ReceiveRoleBlockingActions():
    global ThisNightsRoleBlockings
    global Night
    ThisNightsRoleBlockings = []
    LivingRoleBlockers = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("RoleBlocker","!=","'No'"))
    if LivingRoleBlockers != []: #If there are any roleblockers
        for RoleBlocker in LivingRoleBlockers:
            RoleBlockerActiveTonight = "No"
            #See if this roleblocker is to be active on this particular night
            RoleBlockerValueFromPlayerlist = GetAttributeFromPlayer(RoleBlocker,"RoleBlocker")
            if RoleBlockerValueFromPlayerlist == "Yes":
                RoleBlockerActiveTonight = "Yes"
            elif RoleBlockerValueFromPlayerlist == IsNumberOddOrEven(Night):
                RoleBlockerActiveTonight = "Yes"
            if GetAttributeFromPlayer(RoleBlocker, "RoleBlockerShots") == 0:
                RoleBlockerActiveTonight = "No"
            if GetAttributeFromPlayer(RoleBlocker, "RoleBlockerShots") > 0:
                if GetYesOrNoFromChangingProbability('Yes','Weak') == 'No':
                    RoleBlockerActiveTonight = "No"
            if RoleBlockerActiveTonight == "Yes":
                if GetAttributeFromPlayer(RoleBlocker,'Alignment') == 'Mafia':
                    PlayerToBeRoleBlocked = TryToPickTownPlayer(RoleBlocker,[])
                else:
                    PlayerToBeRoleBlocked = TryToPickMafiaPlayer(RoleBlocker,[])
                if ThisNightsRoleBlockings != 0:
                    global NightsOnWhichThereAreNoKills
                    global ThisNightsCommutings
                    if GetAttributeFromPlayer(PlayerToBeRoleBlocked,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(PlayerToBeRoleBlocked,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and PlayerToBeRoleBlocked not in ThisNightsCommutings:
                        print("Player " + str(RoleBlocker) + " tried to roleblock a PGO and is now getting killed.")
                        PGOReaction(PlayerToBeRoleBlocked,RoleBlocker)
                    else:
                        WriteAttributeToPlayer(RoleBlocker, "RoleBlockerShots", GetAttributeFromPlayer(RoleBlocker, "RoleBlockerShots")-1)
                        ThisNightsRoleBlockings.append({'RoleBlocker': RoleBlocker, 'Target' : PlayerToBeRoleBlocked})
                        print("Player " + str(RoleBlocker) + " is roleblocking " + str(PlayerToBeRoleBlocked))


def PGOReaction(Killer,Victim):
    global ActualNightKills
    WriteAttributeToPlayer(Killer, "ParanoidGunOwnerShots", GetAttributeFromPlayer(Killer, "ParanoidGunOwnerShots")-1)
    ActualNightKills.append({'Killer': Killer,'Victim': Victim})

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
            for RoleBlocking in ThisNightsRoleBlockings:
                if BusDriver == RoleBlocking['Target']: #BusDriver is inactive if roleblocked
                    BusDriverActiveTonight = "No"
            if BusDriverActiveTonight == "Yes":
                BusDrivenPlayer1 = TryToPickMafiaPlayer(BusDriver,[])
                ExcludedPlayers = []
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
                        global NightOnWhichThereAreNoKills
                        global ThisNightsCommutings
                        if GetAttributeFromPlayer(BusDrivenPlayer1,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(BusDrivenPlayer1,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and BusDrivenPlayer1 not in ThisNightsCommutings:
                            print("Player " + str(BusDriver) + " tried to busdrive a PGO and is now getting killed.")
                            PGOReaction(BusDrivenPlayer1,BusDriver)
                        elif GetAttributeFromPlayer(BusDrivenPlayer2,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(BusDrivenPlayer2,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and BusDrivenPlayer2 not in ThisNightsCommutings:
                            print("Player " + str(BusDriver) + " tried to busdrive a PGO and is now getting killed.")
                            PGOReaction(BusDrivenPlayer2,BusDriver)
                        else:
                            if BusDrivenPlayer1 in ThisNightsCommutings or BusDrivenPlayer2 in ThisNightsCommutings:
                                print("Tried to busdrive an active commuter, and so failed.")
                            else:
                                print("On this night, Player " + str(BusDriver) + " is busdriving Player " + str(BusDrivenPlayer1) + " and Player " + str(BusDrivenPlayer2))
                                BusDrivings.append([BusDrivenPlayer1,BusDrivenPlayer2])


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
            for RoleBlocking in ThisNightsRoleBlockings:
                if ChosenTeamKiller == RoleBlocking['Target']: #Teamkiller is inactive if roleblocked
                    TeamKillerActiveTonight = "No"
            if TeamKillerActiveTonight == "Yes":
                if GetAttributeFromPlayer(ChosenTeamKiller,'Alignment') == "Mafia":
                    Target = TryToPickTownPlayer(ChosenTeamKiller,[])
                else:
                    #First ensure you don't try to nightkill a person your teammate is investigating
                    PlayersBeingInvestigatedOrDoctoredByTeammates = []
                    global ThisNightsInvestigationActions
                    global ThisNightsDoctorActions
                    for Investigation in ThisNightsInvestigationActions:
                        if Investigation['Cop'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                            PlayersBeingInvestigatedOrDoctoredByTeammates.append(Investigation['Target'])
                    for Doctoring in ThisNightsDoctorActions:
                        if Doctoring['Doctor'] in ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Team","==",Team)):
                            PlayersBeingInvestigatedOrDoctoredByTeammates.append(Doctoring['Target'])
                    Target = TryToPickMafiaPlayer(ChosenTeamKiller,PlayersBeingInvestigatedOrDoctoredByTeammates)
                if Target != 0:
                    ActualTargets = FindBusDrivingPairs(Target)
                    for ActualTarget in ActualTargets:
                        global NightsOnWhichThereAreNoKills
                        global ThisNightsCommutings
                        if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                            print("Player " + str(ChosenTeamKiller) + " tried to TeamKill a PGO and is now getting killed.")
                            PGOReaction(ActualTarget,ChosenTeamKiller)
                    TeamNightKillActions.append({'Killer': ChosenTeamKiller,'Victim': Target})
                    print("On this night, Player " + str(ChosenTeamKiller) + " is NightKilling Player " + str(Target) + " for team " + str(Team))


def ReceiveCommuterActions():
    global ThisNightsCommutings
    global Night
    ThisNightsCommutings = []
    LivingCommuters = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("Commuter","!=","'No'"))
    if LivingCommuters != []: #If there are any living Commuters
        for Commuter in LivingCommuters:
            CommuterActiveTonight = "No"
            #See if this Commuter is to be active on this particular night
            CommuterValueFromPlayerlist = GetAttributeFromPlayer(Commuter,"Commuter")
            if CommuterValueFromPlayerlist == "Yes":
                CommuterActiveTonight = "Yes"
            elif CommuterValueFromPlayerlist == IsNumberOddOrEven(Night):
                CommuterActiveTonight = "Yes"
            if GetAttributeFromPlayer(Commuter, "CommuterShots") == 0:
                CommuterActiveTonight = "No"
            if GetAttributeFromPlayer(Commuter, "CommuterShots") > 0:
                if GetYesOrNoFromChangingProbability('Yes','Weak') == 'No':
                    CommuterActiveTonight = "No"
            if CommuterActiveTonight == "Yes":
                WriteAttributeToPlayer(Commuter, "CommuterShots", GetAttributeFromPlayer(Commuter, "CommuterShots")-1)
                ThisNightsCommutings.append(Commuter)
                print("Player " + str(Commuter) + " is commuting.")


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
            for RoleBlocking in ThisNightsRoleBlockings:
                if Vigilante == RoleBlocking['Target']: #Vigilante is inactive if roleblocked
                    VigilanteActiveTonight = "No"
            if GetAttributeFromPlayer(Vigilante, "VigilanteShots") == 0:
                VigilanteActiveTonight = "No"
            if GetAttributeFromPlayer(Vigilante, "VigilanteShots") > 0:
                if GetYesOrNoFromChangingProbability('Yes','Weak') == 'No':
                    VigilanteActiveTonight = "No"
            if VigilanteActiveTonight == "Yes":
                if GetAttributeFromPlayer(Vigilante,'Alignment') == "Mafia":
                    Target = TryToPickTownPlayer(Vigilante,[])
                else:
                    PlayersBeingInvestigatedOrDoctoredByTeammates = []
                    global ThisNightsInvestigationActions
                    global ThisNightsDoctorActions
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
                            print("Player " + str(Vigilante) + " tried to VigilanteKill a PGO and is now getting killed.")
                            PGOReaction(ActualTarget,Vigilante)
                    WriteAttributeToPlayer(Vigilante, "VigilanteShots", GetAttributeFromPlayer(Vigilante, "VigilanteShots")-1)
                    VigilanteActions.append({'Killer': Vigilante,'Victim': Target})
                    print("On this night, Player " + str(Vigilante) + " is NightKilling Player " + str(Target) + " as a Vigilante.")


def ReceiveDoctorActions():
    global PlayersTargetedByDoctors
    global Night
    global ThisNightsDoctorActions
    ThisNightsDoctorActions = []
    PlayersTargetedByDoctors = []
    LivingDoctors = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor('Alive','==',"'Yes'"),SearchPlayersFor("Doctor","!=","'No'"))
    if LivingDoctors != []: #If there are any Doctors
        for Doctor in LivingDoctors:
            DoctorActiveTonight = "No"
            #See if this Doctor is to be active on this particular night
            DoctorValueFromPlayerList = GetAttributeFromPlayer(Doctor,"Doctor")
            if DoctorValueFromPlayerList == "Yes":
                DoctorActiveTonight = "Yes"
            elif DoctorValueFromPlayerList == IsNumberOddOrEven(Night):
                DoctorActiveTonight = "Yes"
            for RoleBlocking in ThisNightsRoleBlockings:
                if Doctor == RoleBlocking['Target']: #Doctor is inactive if roleblocked
                    DoctorActiveTonight = "No"
            if GetAttributeFromPlayer(Doctor, "DoctorShots") == 0:
                DoctorActiveTonight = "No"
            if GetAttributeFromPlayer(Doctor, "DoctorShots") > 0:
                if GetYesOrNoFromChangingProbability('Yes','Weak') == 'No':
                    DoctorActiveTonight = "No"
            if DoctorActiveTonight == "Yes":
                if GetAttributeFromPlayer(Doctor,'Alignment') == 'Mafia':
                    PlayerToBeDoctored = TryToPickMafiaPlayer(Doctor,[])
                else:
                    PlayerToBeDoctored = TryToPickTownPlayer(Doctor,[])
                if PlayerToBeDoctored != 0:
                    PGOKilled = 'No'
                    ActualTargets = FindBusDrivingPairs(PlayerToBeDoctored)
                    global NightsOnWhichThereAreNoKills
                    global ThisNightsCommutings
                    for ActualTarget in ActualTargets:
                        if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                            print("Player " + str(Doctor) + " tried to doctor a PGO and is now getting killed.")
                            PGOReaction(ActualTarget,Doctor)
                            PGOKilled = "Yes"
                    if PGOKilled == 'No':
                        WriteAttributeToPlayer(Doctor, "DoctorShots", GetAttributeFromPlayer(Doctor, "DoctorShots")-1)
                        ThisNightsDoctorActions.append({'Doctor': Doctor, 'Target' : PlayerToBeDoctored})
                        PlayersTargetedByDoctors.append(PlayerToBeDoctored)
                        print("On this night, Player " + str(Doctor) + " is Doctoring " + str(PlayerToBeDoctored))


def ReceiveFriendlyNeighbourActions():
    global ThisTurnsFriendlyNeighbourActions
    global FriendlyNeighbourResults
    ThisTurnsFriendlyNeighbourActions = []
    #Build a list of Friendly Neighbours who will be asked for night actions
    FriendlyNeighbours = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("FriendlyNeighbour","!=","'No'"))
    if FriendlyNeighbours != []:
        for FriendlyNeighbour in FriendlyNeighbours:
            WillNotTell = []
            FriendlyNeighbourActiveTonight = "No"
            #See if this FriendlyNeighbour is to be active on this particular night
            FriendlyNeighbourValueFromPlayerList = GetAttributeFromPlayer(FriendlyNeighbour,"FriendlyNeighbour")
            if FriendlyNeighbourValueFromPlayerList == "Yes":
                FriendlyNeighbourActiveTonight = "Yes"
            elif FriendlyNeighbourValueFromPlayerList == IsNumberOddOrEven(Night):
                FriendlyNeighbourActiveTonight = "Yes"
            for RoleBlocking in ThisNightsRoleBlockings:
                if FriendlyNeighbour == RoleBlocking['Target']: #FriendlyNeighbour is inactive if roleblocked
                    FriendlyNeighbourActiveTonight = "No"
            if GetAttributeFromPlayer(FriendlyNeighbour, "FriendlyNeighbourShots") == 0:
                FriendlyNeighbourActiveTonight = "No"
            if GetAttributeFromPlayer(FriendlyNeighbour, "FriendlyNeighbourShots") > 0:
                if GetYesOrNoFromChangingProbability('Yes','Weak') == 'No':
                    FriendlyNeighbourActiveTonight = "No"
            if FriendlyNeighbourActiveTonight == "Yes":
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
                    print("Friendly Neighbour, player " + str(FriendlyNeighbour) + " is not going to tell " +str(WillNotTell))
                Target = TryToPickTownPlayer(FriendlyNeighbour,WillNotTell)
                if Target != 0:
                    PGOKilled = 'No'
                    ActualTargets = FindBusDrivingPairs(Target)
                    global NightsOnWhichThereAreNoKills
                    global ThisNightsCommutings
                    for ActualTarget in ActualTargets:
                        if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                            print("Player " + str(FriendlyNeighbour) + " tried to friendly neighbour a PGO and is now getting killed.")
                            PGOReaction(ActualTarget,FriendlyNeighbour)
                            PGOKilled = "Yes"
                    if PGOKilled == 'No':
                        WriteAttributeToPlayer(FriendlyNeighbour, "FriendlyNeighbourShots", GetAttributeFromPlayer(FriendlyNeighbour, "FriendlyNeighbourShots")-1)
                        ThisTurnsFriendlyNeighbourActions.append({'FriendlyNeighbour': FriendlyNeighbour, 'Target' : Target})
                        print("On this night, Player " + str(FriendlyNeighbour) + " is being a Friendly Neighbour and informing Player " + str(Target))


def ReceiveCopActions():
    global ThisNightsInvestigationActions
    ThisNightsInvestigationActions = []
    #Build a list of cops who will be asked for night actions
    Cops = ReturnOneListWithCommonItemsFromTwoLists(SearchPlayersFor("Alive","==","'Yes'"),SearchPlayersFor("Cop","!=","'No'"))
    if Cops != []:
        for Cop in Cops:
            CopActiveTonight = "No"
            #See if this Cop is to be active on this particular night
            CopValueFromPlayerList = GetAttributeFromPlayer(Cop,"Cop")
            if CopValueFromPlayerList == "Yes":
                CopActiveTonight = "Yes"
            elif CopValueFromPlayerList == IsNumberOddOrEven(Night):
                CopActiveTonight = "Yes"
            for RoleBlocking in ThisNightsRoleBlockings:
                if Cop == RoleBlocking['Target']: #Cop is inactive if roleblocked
                    CopActiveTonight = "No"
            if GetAttributeFromPlayer(Cop, "CopShots") == 0:
                CopActiveTonight = "No"
            if GetAttributeFromPlayer(Cop, "CopShots") > 0:
                if GetYesOrNoFromChangingProbability('Yes','Weak') == 'No':
                    CopActiveTonight = "No"
            if CopActiveTonight == "Yes":
                WillNotInvestigate = GetPlayersWhoCopWillNotInvestigate(Cop)
                if GetAttributeFromPlayer(Cop,'Alignment') == "Mafia":
                    Target = TryToPickTownPlayer(Cop,WillNotInvestigate)
                else:
                    Target = TryToPickMafiaPlayer(Cop,WillNotInvestigate)
                if Target != 0:
                    global NightsOnWhichThereAreNoKills
                    global ThisNightsCommutings
                    PGOKilled = 'No'
                    ActualTargets = FindBusDrivingPairs(Target)
                    for ActualTarget in ActualTargets:
                        if GetAttributeFromPlayer(ActualTarget,'ParanoidGunOwner') == 'Yes' and GetAttributeFromPlayer(Target,'ParanoidGunOwnerShots') != 0 and Night not in NightsOnWhichThereAreNoKills and ActualTarget not in ThisNightsCommutings:
                            print("Player " + str(Cop) + " tried to investigate a PGO and is now getting killed.")
                            PGOReaction(ActualTarget,Cop)
                            PGOKilled = "Yes"
                    if PGOKilled == 'No':
                        WriteAttributeToPlayer(Cop, "CopShots", GetAttributeFromPlayer(Cop, "CopShots")-1)
                        ThisNightsInvestigationActions.append({'Cop': Cop, 'Target' : Target})
                        print("On this night, Player " + str(Cop) + " is Investigating Player " + str(Target))


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

ResultsFile = open('results.txt','w')
i=0
TownVictories = 0
MafiaVictories = 0
while i<100:
    InitiateGlobalVariables()
    EndingTime, EndingTeam = SimulateSingleGame()
    ResultsFile .write(EndingTime + ", " + EndingTeam + "\n")
    if EndingTeam == "Town":
        TownVictories += 1
    else:
        MafiaVictories +=1
    i+=1

print("Town Victories = " + str(TownVictories))
print("Mafia Victories = " + str(MafiaVictories))