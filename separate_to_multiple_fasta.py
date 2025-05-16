# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:03:42 2022

@author: 67535
"""
import os
import argparse

parser = argparse.ArgumentParser(description='Separate single fasta into multiple fasta')

parser.add_argument('-o', '--output', required = True)
parser.add_argument('-i', '--input',required = True)
args = parser.parse_args()

file=open(args.input)
original_file=file.readlines()
file.close()

path=args.output

if not(os.path.exists(path)):
    os.mkdir(path)

marker='>'
marker_loc=[]

for i in range(0,len(original_file)):
    if marker in original_file[i]:
        marker_loc.append(i)
        
#print(marker_loc, len(marker_loc), len(original_file))

for i in range(0,len(marker_loc)):
    name_with_marker=original_file[marker_loc[i]].split(' ')[0]
    name_wo_marker=name_with_marker.split('>')[1].strip('\n\t')
    current_loc=marker_loc[i]
    if i==len(marker_loc)-1:
        next_loc=len(original_file)
    else:
        next_loc=marker_loc[i+1]
    output=open(path+"/"+name_wo_marker+".fasta", 'a+')
    title=original_file[current_loc].replace('\n','').replace('\r','')
    print(title, file=output)
    sequence=''
    for j in range(current_loc+1, next_loc):
        sequence+=original_file[j].replace('\n','').replace('\r','')
    print(sequence, file=output)
    output.close()

