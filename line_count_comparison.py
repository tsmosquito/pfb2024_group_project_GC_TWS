#! /usr/bin/env python3

import sys
import pickle

line_dict = {}

with open(sys.argv[1], 'r') as first_in_fh: # open(sys.argv[2], 'w') as write_fh:
    for line in first_in_fh:
        word_list = line.split()
        line_length = word_list[0:3]
        word_count = len(word_list)
        line_dict[line_length[2]] = word_count

with open('line_dict_all.p', 'wb') as fp:
     pickle.dump(line_dict, fp)
     print('dictionary saved successfully to file')

        
        #write_fh.write(f"{line_length[2]} {word_count}\n")
