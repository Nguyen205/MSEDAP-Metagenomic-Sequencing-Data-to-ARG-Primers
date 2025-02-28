# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:22:28 2025

@author: 67535
"""

import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Use the ARO list of antibiotics of interested to search for the sequences of antibiotic resistance genes (ARGs).')

parser.add_argument('-o', '--output', required = False,
                    help='Output fasta file path and name. Default: ./output/output_ARG_seq_screened.fasta',default='./output/output_ARG_seq_screened.fasta')
parser.add_argument('-i', '--input',required = True,
                    help='Input fasta file path listing all ARGs confers resistance to the drugs in the given sample.')
parser.add_argument('-m', '--mode', required = False,
                    help='Determine the mode for screening ARGs for primer design: A for all ARGs, C for one ARG per cluster, F for one ARG per family. Default: A',default='A')   

args = parser.parse_args()

print('Reading input fasta file......')
file=open(args.input.strip("'"))
input_fasta=file.readlines()
file.close()

cluster=pd.read_csv(r'./ARG_clustering.csv')

print('Analyzing......')

ARO_list=[]
seq_list=[]

for i in range(0,len(input_fasta),2):
    ARO_list.append(input_fasta[i].split('>')[1].split('\n')[0])
    seq_list.append(input_fasta[i+1].strip('\n'))
    
ARG_info=pd.DataFrame(columns=cluster.columns)
ARG_info['Sequence']=seq_list
ARG_info['ARO']=ARO_list

for i in range(0,len(ARG_info)):
    print(i+1,'/',len(ARG_info))
    for j in range(0,len(cluster)):
        if ARG_info.loc[i,'ARO']==str(cluster.loc[j,'ARO']):
            ARG_info.loc[i,'Cluster#']=cluster.loc[j,'Cluster#']
            ARG_info.loc[i,'ARG Name']=cluster.loc[j,'ARG Name']
            ARG_info.loc[i,'ARG Family']=cluster.loc[j,'ARG Family']
            ARG_info.loc[i,'Drug class']=cluster.loc[j,'Drug class']
            break

print('Writing output fasta file......')
if args.mode=='A':
    output_file=open(args.output,'w')
    for i in range(0,len(ARG_info)):
        print('>'+ARG_info.loc[i,'ARO']+'_'+ARG_info.loc[i,'ARG Name'],file=output_file)
        print(ARG_info.loc[i,'Sequence'],file=output_file)
    output_file.close()
elif args.mode=='C':
    ARG_clusters=sorted(set(ARG_info['Cluster#']))
    output_df=pd.DataFrame(columns=ARG_info.columns)
    for i in range(0,len(ARG_clusters)):
        selected_rows=ARG_info[ARG_info['Cluster#']==ARG_clusters[i]]
        selected_rows.Sequence.str.len().sort_values(inplace=True)
        selected_rows.reset_index(inplace=True,drop=True)
        row_df=pd.DataFrame(columns=ARG_info.columns,data=[selected_rows.iloc[0]])
        output_df=pd.concat([output_df,row_df],ignore_index=True)
    output_df.reset_index(inplace=True,drop=True)
    output_file=open(args.output.strip("'"),'w')
    for i in range(0,len(output_df)):
        print('>'+output_df.loc[i,'ARO']+'_'+output_df.loc[i,'ARG Name'],file=output_file)
        print(output_df.loc[i,'Sequence'],file=output_file)
    output_file.close()
elif args.mode=='F':
    ARG_families=sorted(set(ARG_info['ARG Family']))
    output_df=pd.DataFrame(columns=ARG_info.columns)
    for i in range(0,len(ARG_families)):
        selected_rows=ARG_info[ARG_info['ARG Family']==ARG_families[i]]
        selected_rows.Sequence.str.len().sort_values(inplace=True)
        selected_rows.reset_index(inplace=True,drop=True)
        row_df=pd.DataFrame(columns=ARG_info.columns,data=[selected_rows.iloc[0]])
        output_df=pd.concat([output_df,row_df],ignore_index=True)
    output_df.reset_index(inplace=True,drop=True)
    output_file=open(args.output.strip("'"),'w')
    for i in range(0,len(output_df)):
        print('>'+output_df.loc[i,'ARO']+'_'+output_df.loc[i,'ARG Name'],file=output_file)
        print(output_df.loc[i,'Sequence'],file=output_file)
    output_file.close()
else:
    print('Mode not recognized, use default setting to include all ARGs.')
    output_file=open(args.output,'w')
    for i in range(0,len(ARG_info)):
        print('>'+ARG_info.loc[i,'ARO']+'_'+ARG_info.loc[i,'ARG Name'],file=output_file)
        print(ARG_info.loc[i,'Sequence'],file=output_file)
    output_file.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    