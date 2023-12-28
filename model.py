import csv
import sys
import json

# defining global constants

SCHOOL_NAME = 1 # col 2 on kenpom
SCHOOL_CONF = 2 # col 3 on kenpom

ADJ_O = 5 # col 6 on kenpom
ADJ_D = 7 # col 7 on kenpom
LUCK = 11 # col 12 on kenpom
SOS = 13 # col 14 on kenpom

EFG = 30 # col 31 on SR
TOV = 31 # col 32 on SR
ORB = 32 # col 33 on SR
FT_FGA = 33 # col 34 on SR

# this is the main function, here is where all the UI processing is done
def main(argv):
    # we start by initializing empty arrays. these will hold all the information from the CSV
    school_stats = []
    opponent_stats = []
    kenpom_stats = []

    # making sure the proper amount of arguments is passed in when calling the script
    # this is 4 (and not 3) because the name of the script itself is counted
    if (len(argv) != 4):
        print("USAGE: python model.py [school-stats] [opponent-stats] [kenpom-stats]")
    else:
    # here, we open each csv file and populate its respective 2D array
        with open(argv[1], mode='r') as school_file:
            arr = [] # creating a temporary array to save the data
            school_temp = csv.reader(school_file)
            for line in school_temp:
                arr.append(line) # populating the temporary array with each line from the csv

            school_stats = arr # assigning it to our "school_stats" array

        
        with open(argv[2], mode='r') as opponent_file:
            arr = [] # creating a temporary array to save the data
            opponent_temp = csv.reader(opponent_file)
            for line in opponent_temp:
                arr.append(line) # populating the temporary array with each line from the csv

            opponent_stats = arr # assigning it to our "opponent_stats" array
        
        with open(argv[3], mode='r') as kenpom_file:
            arr = [] # creating a temporary array to save the data
            kenpom_temp = csv.reader(kenpom_file)
            for line in kenpom_temp:
                arr.append(line) # populating the temporary array with each line from the csv

            kenpom_stats = arr # assigning it to our "kenpom_stats" array

        # here we call the promptScript function, which asks the user the home and away 
        # teams they would like to see a predition for. using those returned values, 
        # we save the strings into "home" and "away".
        home, away = promptScript(False)
        
        # if the user doesn't decite to exit the UI, we start doing the processing & calculations
        while (home != 'exit' and away != 'exit'):
            # these 4 variables represent the index of the home and away team in the kenpom file,
            # and the sports-reference file, respectively. we start by initializing them to -1
            home_k = -1
            away_k = -1
            home_sr = -1
            away_sr = -1

            # this will represent the current index we are at
            i = 0

            # here, our goal is to find which index the home team is located at in the kenpom
            # file. we iterate through every entry in the csv array, and stop once we reach
            # one who shares the same name as the user inputted for home.
            for school in kenpom_stats:
                if school[SCHOOL_NAME] == home:
                    home_k = i # once we find the entry, we save the index into home_k

                    # names are formatted slightly differently in the sports-reference data
                    # 'St.' in kenpom is represented as 'State' in sports-reference.
                    # we check if the name ends with 'St.', and if it does, we replace it
                    # with 'State', so we can find it in the sports-reference file.
                    if home[len(home)-3:len(home)] == 'St.':
                        home = home[0:len(home)-3]
                        home += "State"
                    
                    # so far, LSU is the only outlier that we've found to this
                    # in kenpom, it is represented as 'LSU', in sports-reference,
                    # it is represented as 'Lousiana State'
                    elif home == 'LSU':
                        home = "Louisiana State"

                i += 1 # incrementing i for next iteration


            i = 0 # resetting i before next search

            # here we do the same, just for the away team
            for school in kenpom_stats:
                if school[SCHOOL_NAME] == away:
                    away_k = i

                    # making the same naming adjustments
                    if away[len(away)-3:len(away)] == 'St.':
                        away = away[0:len(away)-3]
                        away += "State"
                    elif away == 'LSU':
                        away = "Louisiana State"
                i += 1 # incrementing i


            i = 0 # resetting i for the next iteration
            
            # now that we've adjusted the name to represent what it should be
            # in the sports reference file, we can search each sports reference
            # array for the according school.
            for school in school_stats:
                if school[SCHOOL_NAME] == home:
                    home_sr = i # saving its index
                i += 1 # incrementing i


            i = 0 # resetting i
            
            # doing the same for the away team
            for school in school_stats:
                if school[SCHOOL_NAME] == away:
                    away_sr = i
                i += 1

            # now that we have located our indicies for the home and away team
            # we can move forward. if no entry was found, home_k and away_k
            # would not have been changed. therefore, -1 represents a user inputted
            # school that hasn't been found. if the school wasn't found, we start the UI
            # over and display a message indicating that we couldn't find the school
            if home_k == -1 or away_k == -1:
                print("Schools not found in kenpom. Please try again with correct school names. Reference the kenpom stats for what to call the school")
                home, away = promptScript(True)
                continue

            if home_sr == -1 or away_sr == -1:
                print("Schools not found in sports-ref. Please try again with correct school names. Reference the kenpom stats for what to call the school")
                home, away = promptScript(True)
                continue

            # here, using the indicies we found, we call the calculation function
            # this will, given the indicies of a home and away team in each file,
            # return a predicted line for that matchup
            result = calculateFinal(home_sr, away_sr, home_k, away_k, 
                                    school_stats, opponent_stats, kenpom_stats)
            
            # we then print that result to the console, rounding it to 2 decimal
            # places
            print("The result is: " + str(round(result, 2)))

            # here we give the user the option to either continue (search another
            # matchup), or to exit the UI.
            response = input("Continue or Exit?: ").lower()
            if response == 'exit':
                break

            # restarting the UI with a new home and away team prompt
            home, away = promptScript(True)

def promptScript(restarting: bool):
    if restarting:
        print("Restarting\n")
    print("Hello, welcome to the model. To quit, type 'exit' for one of the team names")
    home = input("Choose home team: ")
    if home == "exit":
        print("Goodbye.")
        return 'exit', 'exit'
    away = input("Choose away team: ")
    if away == "exit":
        print("Goodbye.")
        return 'exit', 'exit'

    return home, away


def calculateFinal(home_sr: int, away_sr: int, home_k: int, away_k: int, 
                   school_stats: list, opponent_stats: list, kenpom_stats: list) -> float:
    total: float = 0.0

    efg_total = calculateSR(home_sr, away_sr, EFG, school_stats, opponent_stats)
    # print("EFG TOTAL: ", efg_total)

    tov_total = calculateSR(home_sr, away_sr, TOV, school_stats, opponent_stats)
    # print("TOV TOTAL: ", tov_total)

    orb_total = calculateSR(home_sr, away_sr, ORB, school_stats, opponent_stats)
    # print("ORB TOTAL: ", orb_total)

    ft_total = calculateSR(home_sr, away_sr, FT_FGA, school_stats, opponent_stats)
    # print("FT TOTAL: ", ft_total)

    total += efg_total + tov_total + orb_total + ft_total

    adjo_total = calculateKenpom(home_k, away_k, ADJ_O, kenpom_stats)
    # print("ADJ_O TOTAL: ", adjo_total)

    adjd_total = calculateKenpom(home_k, away_k, ADJ_D, kenpom_stats)
    # print("ADJ_D TOTAL: ", adjd_total)

    luck_total = calculateKenpom(home_k, away_k, LUCK, kenpom_stats)
    # print("LUCK TOTAL: ", luck_total)

    sos_total = calculateKenpom(home_k, away_k, SOS, kenpom_stats)
    # print("SOS TOTAL: ", sos_total)

    total += adjo_total + adjd_total + luck_total + sos_total

    f = open('hca.json')
    all_hca = json.load(f)
    home_name = kenpom_stats[home_k][SCHOOL_NAME]
    home_conf = kenpom_stats[home_k][SCHOOL_CONF]

    if home_name in all_hca['schools'].keys():
        hca = all_hca['schools'][home_name]
    elif home_conf in all_hca['conferences'].keys():
        hca = all_hca['conferences'][home_conf]
    else:
        hca = all_hca['general']
    
    total += hca

    print("\n" + kenpom_stats[home_k][SCHOOL_NAME] + " (HOME) vs. " + kenpom_stats[away_k][SCHOOL_NAME] + " (AWAY)")

    return total

def calculateSR(home: int, away: int, stat: int, 
                school_stats: list, opponent_stats: list) -> float:
    if stat == EFG:
        factor = 50
    elif stat == TOV:
        factor = 15
    elif stat == ORB:
        factor = 30
    elif stat == FT_FGA:
        factor = 5

    if stat == TOV:
        home_diff = float(opponent_stats[home][stat])/100 - float(school_stats[home][stat])/100
        away_diff = float(opponent_stats[away][stat])/100 - float(school_stats[away][stat])/100
    elif stat == ORB:
        home_diff = float(school_stats[home][stat])/100 - float(opponent_stats[home][stat])/100
        away_diff = float(school_stats[away][stat])/100 - float(opponent_stats[away][stat])/100
    else:
        home_diff = float(school_stats[home][stat]) - float(opponent_stats[home][stat])
        away_diff = float(school_stats[away][stat]) - float(opponent_stats[away][stat])

    difference = home_diff - away_diff
    finalValue = difference * factor

    return float(finalValue)

def calculateKenpom(home: int, away: int, stat: int, kenpom_stats: list) -> float:
    if stat == LUCK:
        finalValue = -(float(kenpom_stats[home][stat]) - float(kenpom_stats[away][stat]))/3
    elif stat == ADJ_D:
        away_adj_d = float(kenpom_stats[away][stat])
        # print(kenpom_stats[away][SCHOOL_NAME] + " (AWAY) ADJ_D: " + str(away_adj_d))
        home_adj_d = float(kenpom_stats[home][stat])
        # print(kenpom_stats[home][SCHOOL_NAME] + " (HOME) ADJ_D: " + str(home_adj_d))
        finalValue = (away_adj_d - home_adj_d)/3
    else:
        finalValue = (float(kenpom_stats[home][stat]) - float(kenpom_stats[away][stat]))/3
    
    return float(finalValue)


if __name__ == "__main__":
    main(sys.argv)
