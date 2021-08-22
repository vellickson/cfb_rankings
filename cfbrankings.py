import sys
import getopt
from games import GameResults


def main(argv):
    week = 0
    season = 0

    try:
        opts, args = getopt.getopt(argv, "hs:w:", ["season=", "week="])
    except getopt.GetoptError:
        print('games.py -s <season as int> -w <week as int>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('games.py -s <season as int> -w <week as int>')
            sys.exit()
        elif opt in ("-s", "--season"):
            season = arg
        elif opt in ("-w", "--week"):
            week = arg
    print('Season is ', season)
    print('Week is ', week)
    g = GameResults(season, week)
    g.get_weekly_game_results()


if __name__ == "__main__":
    main(sys.argv[1:])
