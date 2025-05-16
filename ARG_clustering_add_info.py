# -*- coding: utf-8 -*-
"""
Created on Thu May 15 18:09:04 2025

@author: 67535
"""

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Summarize all Primer3 output files into one single Excel file.')

parser.add_argument('-i', '--input', required = True,
                    help='Input raw clustering csv file path.')
parser.add_argument('-a', '--aro', required = True,
                    help='Input ARO index csv file path.')
parser.add_argument('-o', '--output', required = True,
                    help='Output ARG clustering csv file path.')
args = parser.parse_args()

ARO_index=pd.read_csv(args.aro)
ARG_cluster=pd.read_csv(args.input)
ARG_cluster.rename(columns={'Sample':'ARO','Class':'Cluster#'},inplace=True)
ARG_cluster['ARG Name']=''       #ARG Name	ARG Family	Drug class
ARG_cluster['ARG Family']=''
ARG_cluster['Drug class']=''
for i in range(0,len(ARG_cluster)):
    ARG_cluster.loc[i,'ARO']=ARG_cluster.loc[i,'ARO'].split('.fasta')[0]
    print(i,'/',len(ARG_cluster))
    for j in range(0,len(ARO_index)):
        if ARG_cluster.loc[i,'ARO']==str(ARO_index.loc[j,'ARO Accession']):
            ARG_cluster.loc[i,'ARG Name']=ARO_index.loc[j,'ARO Name']
            ARG_cluster.loc[i,'ARG Family']=ARO_index.loc[j,'AMR Gene Family']
            ARG_cluster.loc[i,'Drug class']=ARO_index.loc[j,'Drug Class']
            break
ARG_cluster.to_csv(args.output,index=None)
