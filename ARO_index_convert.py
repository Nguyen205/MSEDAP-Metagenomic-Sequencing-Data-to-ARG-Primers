# -*- coding: utf-8 -*-
"""
Created on Thu May 15 17:02:27 2025

@author: 67535
"""

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Summarize all Primer3 output files into one single Excel file.')

parser.add_argument('-i', '--input', required = True,
                    help='Input ARO index tsv file path.')
parser.add_argument('-o', '--output', required = True, help='Output ARO index csv file path.')
args = parser.parse_args()

ARO_index=pd.read_csv(args.input,sep='\t')

for i in range(0,len(ARO_index)):
    ARO_index.loc[i,'ARO Accession']=ARO_index.loc[i,'ARO Accession'].split('ARO:')[1]

ARO_index.drop(columns=['CVTERM ID','Model Sequence ID','Model ID'],inplace=True)
ARO_index.to_csv(args.output,index=None)