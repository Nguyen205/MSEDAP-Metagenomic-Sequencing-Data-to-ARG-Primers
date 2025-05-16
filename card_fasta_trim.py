# -*- coding: utf-8 -*-
"""
Created on Thu May 15 16:46:38 2025

@author: 67535
"""

import argparse

parser = argparse.ArgumentParser(description='Summarize all Primer3 output files into one single Excel file.')

parser.add_argument('-f', '--file', required = True,
                    help='Input nucleotide protein homolog fasta file path.')
parser.add_argument('-o', '--output', required = True,
                    help='Output trimmed fasta file path.')
args = parser.parse_args()

file=open(args.file)
fasta=file.readlines()
file.close()

for i in range(0,len(fasta),2):
    fasta[i]='>'+fasta[i].split('ARO:')[1].split('|')[0]
    
out_file=open(args.output,'w')
for i in range(0,len(fasta)):
    print(fasta[i].strip('\n'),file=out_file)
out_file.close()