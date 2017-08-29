import os
import re
import numpy as np


def key(element):
    return re.search(prefix_pattern, element).group(1), int(re.search(number_pattern, element).group(1))

prefix_pattern = re.compile(r'^(.*)\[')
number_pattern = re.compile(r'\[(\d*)-')

files = [file for file in os.listdir('.') if file[-4:] == '.npy']
prefixes = sorted({re.search(prefix_pattern, file).group(1) for file in files})
files.sort(key=key)
files = np.reshape(np.array(files), (len(prefixes), -1))

for prefix, sub_files in zip(prefixes, files):
    np.save(prefix, np.concatenate([np.load(file) for file in sub_files]))
