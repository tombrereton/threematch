import os

from ai.state_parser import StateParser

# split into list with newline
# sort list by first element

state_parser = StateParser()

current_dir = os.getcwd() + '/data/'
files = os.listdir(current_dir)

# remove non training files
files.remove('win')
files.remove('loss')

while files:
    file_name = files.pop(0)
    full_file_name = current_dir + file_name

    line_list = []
    with open(full_file_name, mode='r') as file:
        for line in file:
            line_list.append(line)

    if len(line_list) > 26:
        # sort states according to line number
        preamble_list = line_list[:26]
        states_list = line_list[26:]
        states_list.sort(key=lambda x: int(x.split('\t')[0]))

        for i in range(len(states_list)):
            # remove line number for beginning of line
            remove_first_element = states_list[i].split('\t')[1:]
            states_list[i] = '\t'.join(remove_first_element)

        # join list and write into file again
        new_line_list = preamble_list + states_list
        print(new_line_list)
        with open('test.txt', mode='w') as file:
            for line in new_line_list:
                file.write(line)
