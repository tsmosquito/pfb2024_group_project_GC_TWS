#! /usr/bin/env python3

# import sys

# line_length_dict = {}
# line_length = ''

# with open(sys.argv[1], 'r') as fasta_in_fh, open(sys.argv[2], 'w') as fasta_out_fh:
#     for line in fasta_in_fh:
#         if line.startswith('>'):
#             continue
#         else:
#             line = line.strip()
#             line_length = len(line)
#             if line_length not in line_length_dict:
#                 line_length_dict[line_length] = line
#             else:
#                 line_length_dict[line_length] += line
#     for key in line_length_dict:
#         fasta_out_fh.write(f"Line length {key}: {line_length_dict[key]}\n")


import sys

line_length_dict = {}

with open(sys.argv[1], 'r') as fasta_in_fh:
    for line in fasta_in_fh:
        if line.startswith('>'):
            continue
        line = line.strip()
        line_length = len(line)
        
        # Initialize an empty list if this length is not in the dictionary
        if line_length not in line_length_dict:
            line_length_dict[line_length] = []
        
        # Append the line to the list for this length
        line_length_dict[line_length].append(line)

# Writing the results to the output file
with open(sys.argv[2], 'w') as fasta_out_fh:
    for key in line_length_dict:
        # Join the lines into a single string for each length, if desired
        fasta_out_fh.write(f"Line length {key}: {', '.join(line_length_dict[key])}\n")

