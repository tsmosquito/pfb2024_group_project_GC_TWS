#!/usr/bin/env python3

"""This script takes an ensemble fasta file with human CDS chromosomal CDS sequences: 
> .... chromosome:GRCh38:17:67739553:67744203:1 .... gene:ENSG00000211592.8 ....
where each header line starts with '>'
where .... indicates additional characters/sequence identifiers
where 17 is the chromosome, the following numbers are gene coordinates
and where gene:ENSG... gives a unique gene identifier.

This script then parses out the sequences and concatenates them according to chromosome, 
creating one long CDS DNA sequence.

Output: is a corrupted fasta file with 24 (X/Y are separately stored) headers and 24 
        concatenated chromosomal sequences. Lines are not necessarily 60 characters but 
        are terminatd by a newline character. Only the first transcript of a gene is
        kept, not all coding sequences with the same gene identifier.
        Non-chromosmal CDS sequences on other scaffolds are not saved."""


###Final code that works as stated above

import re
import sys

chrom_dict = {}
gene_id_dict = {}

with open(sys.argv[1], 'r') as fasta_in_fh, open(sys.argv[2], 'w') as fasta_out_fh:
    current_gene_id = None  # Store the current gene ID
    header = ''
    
    for line in fasta_in_fh:
        if line.startswith('>'):
            # Check for "protein_coding" in the header line
            if 'protein_coding' in line:
                # Extract chromosome and gene ID from the header
                chrom_match = re.search(r'^>.*:([\dXY]\d?):.*gene:(ENSG\S*)\s', line)
                if chrom_match:
                    chrom_id = chrom_match.group(1)
                    current_gene_id = chrom_match.group(2)

                    # Initialize if this gene ID hasn't been seen before
                    if current_gene_id not in gene_id_dict:
                        gene_id_dict[current_gene_id] = True  # Mark it as seen
                        chrom_dict.setdefault(chrom_id, '')  # Initialize if not present
                    else:
                        current_gene_id = None  # Reset to avoid duplicates
            else:
                # Skip lines that don't contain "protein_coding"
                current_gene_id = None
                
        else:
            # Only append if we have a valid gene ID and it's the first occurrence
            if current_gene_id is not None:
                chrom_dict[chrom_id] += line  # Append sequence lines

    # Write output
    for key in chrom_dict:
        fasta_out_fh.write(f">{key}\n{chrom_dict[key]}")


######Archived versions of the code that weren't quite working but were close:

###MY CODE THAT WASN'T QUITE WORKING

# chrom_dict = {}
# gene_id_dict = {}
# gene_id_counter = 0

# with open(sys.argv[1], 'r') as fasta_in_fh, open(sys.argv[2], 'w') as fasta_out_fh:
#     header = ''
#     gene_id = ''
#     for line in fasta_in_fh:
#         if '>' in line:
#             #print(gene_id_dict) #This dictionary has only the first gene id one in the line
#             if gene_id not in gene_id_dict: 
#                 gene_id_counter = 0 
#                 #print(gene_id_dict) #And here it becomes an empty dictionary
#                 if 'protein_coding' in line:
#                     chrom_name = re.search(r'^>.*:([\dXY]\d?):.*(ENSG\S*)\s', line) 
#                     #fasta_out_fh.write(f"{line}")
#                     if chrom_name != None:
#                         if chrom_name.group(2) not in gene_id_dict: 
#                             gene_id_dict[chrom_name.group(2)] = ''
#                             gene_id = chrom_name.group(2)
#                             #print(gene_id)
#                             if chrom_name.group(1) not in chrom_dict:
#                                 chrom_dict[chrom_name.group(1)] = ''
#                                 header = chrom_name.group(1)
#                                 #gene_id_dict[chrom_name.group(2)] = ''
#                                 #gene_id = chrom_name.group(2)
#                                 #print(header)
#                                 #print(gene_id)
#                             else:
#                                 header = chrom_name.group(1)
#                     else:
#                         header = 'scaffold'
#                 else:
#                     header = 'scaffold' 
#             else:
#                 continue ####Not sure if I need this if else statement, goes with gene id in gene id dict
#         else :
#             gene_id_counter += 1 
#             #gene_id_counter += 1 ###This might need to be one up with the gene id in gene id dict
#             if header != 'scaffold' :
#                 #print(line) #gets to here just fine
#                 #print(gene_id) #Fixed, has geneIDs
#                 #print(gene_id_dict) #EMPTY!!!
#                 #print(gene_id_counter) This looks okay
#                 if ((gene_id in gene_id_dict) and (gene_id_counter != 0)): 
#                     chrom_dict[header] += line 
#                 else:
#                       continue
#             else:
#                 header = 'scaffold'
#                 #gene_id_dict[gene_id] = '' This takes all of the lines
#                 continue
#     for key in chrom_dict:
#         fasta_out_fh.write(f">{key}\n{chrom_dict[key]}")



# import re
# import sys

# ### Reading in the fasta file based on command line arguments, open as read, open new file for writing.

# chrom_dict = {}
# gene_id_dict = {}

# with open(sys.argv[1], 'r') as fasta_in_fh, open(sys.argv[2], 'w') as fasta_out_fh:
#     header = ''
#     gene_id = ''
#     for line in fasta_in_fh:
#         line = line.upper()
#         if '>' in line:
#             if 'PROTEIN_CODING' in line:
#                 chrom_name = re.search(r'^>.*:([\dXY]\d?):.*(ENSG\S*)\s', line) 
#                 #fasta_out_fh.write(f"{line}")
#                 if chrom_name != None: 
#                     if chrom_name.group(1) not in chrom_dict:
#                         chrom_dict[chrom_name.group(1)] = ''
#                         header = chrom_name.group(1)
#                         # gene_id_dict[chrom_name.group(2)] = ''
#                         # gene_id = chrom_name.group(2)
#                         #print(header)
#                         #print(gene_id)
#                     else:
#                         header = chrom_name.group(1)
#                 else:
#                     header = 'scaffold'
#                 continue
#             else:
#                 header = 'scaffold'
#                 continue
#         else :
#             if ((header != 'scaffold') and (header in chrom_dict)) :
#                 chrom_dict[header] += line   
#             else:
#                 header = 'scaffold'
#                 continue
#     for key in chrom_dict:
#         fasta_out_fh.write(f">{key}\n{chrom_dict[key]}")

#### Just saving another version: I added a bit of bloat with the whole gene_id_counter stuff, but basically this code returns the first line of every 
####gene id transcript along with the chromosome numbers. 

# chrom_dict = {}
# gene_id_dict = {}
# gene_id_counter = 0

# with open(sys.argv[1], 'r') as fasta_in_fh, open(sys.argv[2], 'w') as fasta_out_fh:
#     header = ''
#     gene_id = ''
#     for line in fasta_in_fh:
#         if '>' in line:
#             gene_id_counter = 0
#             if 'protein_coding' in line:
#                 chrom_name = re.search(r'^>.*:([\dXY]\d?):.*(ENSG\S*)\s', line) 
#                 #fasta_out_fh.write(f"{line}")
#                 if chrom_name != None:
#                     if chrom_name.group(2) not in gene_id_dict: 
#                         #gene_id_dict[chrom_name.group(2)] = ''
#                         gene_id = chrom_name.group(2)
#                         #print(gene_id)
#                         if chrom_name.group(1) not in chrom_dict:
#                             chrom_dict[chrom_name.group(1)] = ''
#                             header = chrom_name.group(1)
#                             #gene_id_dict[chrom_name.group(2)] = ''
#                             #gene_id = chrom_name.group(2)
#                             #print(header)
#                             #print(gene_id)
#                         else:
#                             header = chrom_name.group(1)
#                 else:
#                     header = 'scaffold'
#             else:
#                 header = 'scaffold'
#         else :
#             gene_id_counter += 1
#             if header != 'scaffold' :
#                 #print(line) gets to here just fine
#                 #print(gene_id) it succeeds in hanging on to the gene id
#                 #print(gene_id_dict) it's got the dictionary tooo!!!!
#                 if gene_id not in gene_id_dict: 
                    
#                     chrom_dict[header] += line 
#                     gene_id_dict[chrom_name.group(2)] = '' ##This only takes the first line
#                 else:
#                       continue
#             else:
#                 header = 'scaffold'
#                 #gene_id_dict[gene_id] = '' This takes all of the lines
#                 continue
#     for key in chrom_dict:
#         fasta_out_fh.write(f">{key}\n{chrom_dict[key]}")
    