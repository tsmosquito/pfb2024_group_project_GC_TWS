#! /usr/bin/env python3

import sys

total_line_count = 0
header_line_count = 0
genes_with_protein_coding = 0
mitochondrial_genes = 0

with open(sys.argv[1], 'r') as fasta_in_fh, open(sys.argv[2], 'w') as fasta_out_fh:
    for line in fasta_in_fh:
        total_line_count += 1
        if line.startswith('>'):
            header_line_count += 1
            if 'protein_coding' in line:
                genes_with_protein_coding += 1
            if ':MT:' in line:
                 mitochondrial_genes +=1

    
    genes_excluded = header_line_count - (genes_with_protein_coding + mitochondrial_genes)
    genes_included = header_line_count - genes_excluded
    fasta_out_fh.write(f"""The total number of lines in the cds file is {total_line_count:,}
The total number of header lines (cds genes) is {header_line_count:,}
The total number of cds genes with the keyword "protein coding" is {genes_with_protein_coding:,}
The total number of mitochondrial cds genes is {mitochondrial_genes:,}
The total number of mitochondrial cds genes that we included before transcript ID filtering are {genes_included:,} 
The total number of genes that we excluded are before transcript ID filtering {genes_excluded:,}""")