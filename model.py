import csv
import sys

ADJ_O = 5 # col 6 on kenpom
ADJ_D = 6 # col 7 on kenpom
LUCK = 11 # col 12 on kenpom
SOS = 13 # col 14 on kenpom

EFG = 30 # col 31 on SR
TOV = 31 # col 32 on SR
ORB = 32 # col 33 on SR
FT_FGA = 33 # col 34 on SR

school_stats = []
opponent_stats = []
kenpom_stats = []

def main(argv):
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
        

def calculateSR(home, away, stat):
    if stat == EFG:
        factor = 50
    elif stat == TOV:
        factor = 15
    elif stat == ORB:
        factor = 30
    elif stat == FT_FGA:
        factor = 5

    if stat == TOV:
        home_diff = opponent_stats[stat][home] - school_stats[stat][home]
        away_diff = opponent_stats[stat][away] - school_stats[stat][away]
    else:
        home_diff = school_stats[stat][home] - opponent_stats[stat][home]
        away_diff = school_stats[stat][away] - opponent_stats[stat][away]

    difference = home_diff - away_diff
    finalValue = difference * factor

    return finalValue

def calculateKenpom(home, away, stat):
    if stat == LUCK:
        finalValue = -(kenpom_stats[stat][home] - kenpom_stats[stat][away])/3
    else:
        finalValue = (kenpom_stats[stat][home] - kenpom_stats[stat][away])/3
    
    return finalValue


if __name__ == "__main__":
    main(sys.argv)
