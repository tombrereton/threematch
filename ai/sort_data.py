# read in file
# read last line and determine if winning game
# move file to win or loss folder

import os

from ai.state_parser import StateParser


def move_to_win_folder(file_name, is_winner, is_finished):
    folder = 'win' if is_winner else 'loss'
    folder = folder if is_finished else ''
    new_full_file_name = file_name.split('/')
    new_full_file_name.insert(len(new_full_file_name) - 1, folder)
    new_full_file_name = '/'.join(new_full_file_name)
    os.rename(file_name, new_full_file_name)


state_parser = StateParser()

current_dir = os.getcwd() + '/data/'
files = os.listdir(current_dir)

# remove non training files
files.remove('win')
files.remove('loss')

# start loop
while files:

    file_name = files.pop(0)
    full_file_name = current_dir + file_name

    is_file_winner = False
    with open(full_file_name, mode='r') as file:
        total_medals = None
        medals_uncovered = 0
        line_count = 0
        game_finished = None

        for line in file:
            if line_count == 16:
                total_medals = line.split('\t')[1]

            if line_count > 24 and line_count % 2 == 0:
                medals_uncovered = line.split('\t')[1]

            if line_count > 24 and line_count % 2 == 1:
                game_finished = True if line == '-1--1--1--1\n' else False

            if medals_uncovered == total_medals:
                is_file_winner = True

            line_count += 1

    move_to_win_folder(full_file_name, is_file_winner, game_finished)
