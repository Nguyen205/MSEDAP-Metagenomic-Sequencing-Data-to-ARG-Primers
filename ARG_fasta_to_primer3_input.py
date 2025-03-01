# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:23:28 2025

@author: 67535
"""

import argparse
import os

parser = argparse.ArgumentParser(description='Transfer the fasta files of targeted ARGs into Primer3 input format.')

parser.add_argument('-o', '--output', required = False,
                    help='Output fasta file path and name. Default: ./output/primer3_input',default='./output/primer3_input')
parser.add_argument('-i', '--input',required = True,
                    help='Input fasta file path after screening')
parser.add_argument('-s', '--size',required = False,
                    help='PCR amplicon size range (bp), default: 75-250',default='75-250')
parser.add_argument('-n', '--number',required = False,
                    help='Number of primers designed for each ARG, default: 5',default=5)

args = parser.parse_args()

if not(os.path.exists(args.output)):
    os.mkdir(args.output)
    
file=open(args.input.strip("'"))
fasta=file.readlines()
file.close()

for i in range(0,len(fasta),2):
    print('Writing',int((i+2)/2),'of',int(len(fasta)/2),'......')
    output_file=open(args.output+'/'+fasta[i].split('>')[1].split('\n')[0]+'.txt','w')
    print('SEQUENCE_ID='+fasta[i].split('>')[1].split('\n')[0],file=output_file)
    print('SEQUENCE_TEMPLATE='+fasta[i+1].strip('\n'),file=output_file)
    print('PRIMER_TASK=generic',file=output_file)
    print('PRIMER_PICK_LEFT_PRIMER=1',file=output_file)
    print('PRIMER_PICK_INTERNAL_OLIGO=1',file=output_file)
    print('PRIMER_PICK_RIGHT_PRIMER=1',file=output_file)
    print('PRIMER_NUM_RETURN='+str(args.number),file=output_file)
    print('PRIMER_OPT_SIZE=20',file=output_file)
    print('PRIMER_MIN_SIZE=18',file=output_file)
    print('PRIMER_MAX_SIZE=22',file=output_file)
    print('PRIMER_PRODUCT_SIZE_RANGE='+args.size,file=output_file)
    print('PRIMER_EXPLAIN_FLAG=1',file=output_file)
    print('=',file=output_file)
    output_file.close()
