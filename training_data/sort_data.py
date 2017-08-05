# read in file
# read last line and determine if winning game
# move file to win or loss folder

import os

from ai.state_parser import StateParser

current_dir = os.getcwd()
print(current_dir)

files = os.listdir(current_dir)

# remove non training files
files.remove('sort_data.py')
files.remove('win')
files.remove('loss')

print(files)

file_name = 'game-20170803-170103.txt'

state_parser = StateParser()
full_file_name = state_parser.get_full_filename(file_name)

state_4 = state_parser.get_state(full_file_name, 4)

screen_cell_list = state_4.split('\t')

screen_cell_list.pop(0)
screen_cell_list.pop(0)
screen_cell_list.remove('\n')
print('screen list: ', screen_cell_list)
