# -*- coding: utf-8 -*-
"""
Created on Thu May 15 17:19:57 2025

@author: 67535
"""

import pandas as pd
from collections import deque 
import argparse

parser = argparse.ArgumentParser(description='Summarize all Primer3 output files into one single Excel file.')

parser.add_argument('-i', '--input', required = True,
                    help='Input FastANI summary.')
parser.add_argument('-o', '--output', required = True,
                    help='Output clustering based on ANI.')
args = parser.parse_args()

weight_threshold=90     #Threshold for creating an edge
weight_column='ANI'     #Use which parameter to determine edge weight

df_raw=pd.read_csv(args.input,header=None,sep='\t')
df_raw.columns=['target','source','ANI','query','subject']
df_raw_2=df_raw[df_raw[weight_column]>weight_threshold]   #Screen qualified edges, may have multiple thresholds
df_raw_2['coverage']=df_raw_2['query']/df_raw_2['subject']
df=df_raw_2[df_raw_2['coverage']>0.9]

raw_target_list=sorted(set(df_raw['target']))
raw_source_list=sorted(set(df_raw['source']))
raw_node_list=sorted(set(raw_target_list+raw_source_list))

target_list=sorted(set(df['target']))
source_list=sorted(set(df['source']))
node_list=sorted(set(target_list+source_list))

output_df=pd.DataFrame(columns=['Sample','Class'])
all_visited=[]
class_value=1
for i in range(0,len(node_list)):
    print(i,'/',len(node_list))
    if node_list[i] in all_visited:
        continue
    current_cluster=[]
    que=deque([node_list[i]])
    visited=set([node_list[i]])
    while len(que)>0:
        node=que.popleft()
        current_cluster.append(node)
        search_df_1=df[df['target']==node]
        search_df_2=df[df['source']==node]
        search_df=pd.concat([search_df_1,search_df_2],ignore_index=True)
        for j in range(0,len(search_df)):
            if node==search_df.loc[j,'target']:
                if search_df.loc[j,'source'] in visited:
                    continue
                que.append(search_df.loc[j,'source'])
                visited.add(search_df.loc[j,'source'])
            if node==search_df.loc[j,'source']:
                if search_df.loc[j,'target'] in visited:
                    continue
                que.append(search_df.loc[j,'target'])
                visited.add(search_df.loc[j,'target'])
    all_visited=all_visited+list(visited)
    current_cluster=sorted(set(current_cluster))
    temp_df=pd.DataFrame(columns=output_df.columns)
    temp_df['Sample']=current_cluster
    temp_df['Class']=class_value
    output_df=pd.concat([output_df,temp_df],ignore_index=True)
    class_value+=1
    
unclustered_nodes=list(set(raw_node_list).difference(set(node_list)))    
additional_df=pd.DataFrame(columns=output_df.columns)
additional_df['Sample']=unclustered_nodes
for i in range(0,len(additional_df)):
    additional_df.loc[i,'Class']=class_value
    class_value+=1
output_df=pd.concat([output_df,additional_df],ignore_index=True)   

output_df.to_csv(args.output,index=None)