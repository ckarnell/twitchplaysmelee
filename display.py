import itertools
import random
import time

NUM_SPACES = 80
spacing = ' ' * NUM_SPACES

def main():
    while True:
        print('\033[2J')
        print('\033[H')
        print(f'P1{spacing}P2')

        info_file = open('info.txt', 'r')
        player_one_usernames = []
        player_two_usernames = []

        found_p2 = False
        for raw_line in info_file:
            line = raw_line.strip()

            if line == 'P2':
                found_p2 = True
                continue

            if found_p2:
                player_two_usernames.append(line)
            else:
                player_one_usernames.append(line)

        
        combos = itertools.zip_longest(player_one_usernames, player_two_usernames, fillvalue='')
        for combo in combos:
            spaces_needed = ' ' * (NUM_SPACES - len(combo[0]) + 2)
            print(f'{combo[0]}{spaces_needed}{combo[1]}')
            
        time.sleep(1)

        info_file.close()


if __name__ == "__main__":
    main()