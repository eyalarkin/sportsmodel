import csv
import sys
import json

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

def main(argv):
    school_stats = []
    opponent_stats = []
    kenpom_stats = []

    if (len(argv) != 4):
        print("USAGE: python model.py [school-stats] [opponent-stats] [kenpom-stats]")
    else:
        with open(argv[1], mode='r') as school_file:
            arr = []
            school_temp = csv.reader(school_file)
            for line in school_temp:
                arr.append(line)

            school_stats = arr

        
        with open(argv[2], mode='r') as opponent_file:
            arr = []
            opponent_temp = csv.reader(opponent_file)
            for line in opponent_temp:
                arr.append(line)

            opponent_stats = arr
        
        with open(argv[3], mode='r') as kenpom_file:
            arr = []
            kenpom_temp = csv.reader(kenpom_file)
            for line in kenpom_temp:
                arr.append(line)

            kenpom_stats = arr

        home, away = promptScript(False)
        while (home != 'exit' and away != 'exit'):
            home_k = -1
            away_k = -1
            home_sr = -1
            away_sr = -1
            i = 0

            for school in kenpom_stats:
                if school[SCHOOL_NAME] == home:
                    home_k = i
                    if home[len(home)-3:len(home)] == 'St.':
                        home = home[0:len(home)-3]
                        home += "State"
                    elif home == 'LSU':
                        home = "Louisiana State"
                i += 1
            i = 0

            for school in kenpom_stats:
                if school[SCHOOL_NAME] == away:
                    away_k = i
                    if away[len(away)-3:len(away)] == 'St.':
                        away = away[0:len(away)-3]
                        away += "State"
                    elif away == 'LSU':
                        away = "Louisiana State"
                i += 1
            i = 0
            
            for school in school_stats:
                if school[SCHOOL_NAME] == home:
                    home_sr = i
                i += 1
            i = 0
            
            for school in school_stats:
                if school[SCHOOL_NAME] == away:
                    away_sr = i
                i += 1

            if home_k == -1 or away_k == -1:
                print("Schools not found in kenpom. Please try again with correct school names. Reference the kenpom stats for what to call the school")
                home, away = promptScript(True)
                continue

            if home_sr == -1 or away_sr == -1:
                print("Schools not found in sports-ref. Please try again with correct school names. Reference the kenpom stats for what to call the school")
                home, away = promptScript(True)
                continue

            result = calculateFinal(home_sr, away_sr, home_k, away_k, 
                                    school_stats, opponent_stats, kenpom_stats)

            print("The result is: " + str(round(result, 2)))
            response = input("Continue or Exit?: ").lower()
            if response == 'exit':
                break
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
