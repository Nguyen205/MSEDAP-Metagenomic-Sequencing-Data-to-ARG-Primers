# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 02:08:51 2025

@author: 67535
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:53:36 2025

@author: 67535
"""

import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='Summarize all Primer3 output files into one single Excel file.')

parser.add_argument('-o', '--output', required = False,
                    help='Output fasta file path and name. Default: ./output/primers_output.xlsx',default='./output/primers_output.xlsx')
parser.add_argument('-i', '--input',required = True,
                    help='Input folder path containing all primer3 output files')
parser.add_argument('-n', '--number', required = False,
                    help='Number of primers designed for each ARG. Default: 5',default=5)

args = parser.parse_args()

dir_path=args.input.strip("'")
file_list=[]
dir_list=os.listdir(dir_path)

for cur_file in dir_list:
    if os.path.splitext(cur_file)[1]=='.txt':
        file=os.path.join(dir_path,cur_file)
        file_list.append(file)

output_df=pd.DataFrame(columns=['AssaySet','Type','Sequence','Start','Length','Tm','GC Percent','Amplicon'])

for file_path in file_list:
    p3_file=open(file_path)
    p3_file_content=p3_file.readlines()
    p3_file.close()
    if len(p3_file_content)<50:
        continue
    else:
        temp_df=pd.DataFrame(columns=output_df.columns)
        gene_id=p3_file_content[0].split('SEQUENCE_ID=')[1].strip('\n')
        assay_set_list=[]
        type_list=[]
        for num in range(0,int(args.number)):
            assay_set_item=['Batch Item ('+gene_id+'), Assay Set '+str(num)]
            assay_set_list+=assay_set_item*4
            type_list+=['Forward Primer','Probe','Reverse Primer','Product']
        temp_df['AssaySet']=assay_set_list
        temp_df['Type']=type_list
        for i in range(0,int(args.number)):
            temp_df.loc[i*4,'Sequence']=p3_file_content[19+i*31+5].split('PRIMER_LEFT_'+str(int(i))+'_SEQUENCE=')[1].strip('\n')
            temp_df.loc[i*4+1,'Sequence']=p3_file_content[19+i*31+7].split('PRIMER_INTERNAL_'+str(int(i))+'_SEQUENCE=')[1].strip('\n')
            temp_df.loc[i*4+2,'Sequence']=p3_file_content[19+i*31+6].split('PRIMER_RIGHT_'+str(int(i))+'_SEQUENCE=')[1].strip('\n')
            temp_df.loc[i*4,'Start']=p3_file_content[19+i*31+8].split('PRIMER_LEFT_'+str(int(i))+'=')[1].split(',')[0]
            temp_df.loc[i*4+1,'Start']=p3_file_content[19+i*31+10].split('PRIMER_INTERNAL_'+str(int(i))+'=')[1].split(',')[0]
            temp_df.loc[i*4+2,'Start']=p3_file_content[19+i*31+9].split('PRIMER_RIGHT_'+str(int(i))+'=')[1].split(',')[0]
            temp_df.loc[i*4,'Length']=p3_file_content[19+i*31+8].split(',')[1].strip('\n')
            temp_df.loc[i*4+1,'Length']=p3_file_content[19+i*31+10].split(',')[1].strip('\n')
            temp_df.loc[i*4+2,'Length']=p3_file_content[19+i*31+9].split(',')[1].strip('\n')
            temp_df.loc[i*4,'Tm']=p3_file_content[19+i*31+11].split('PRIMER_LEFT_'+str(int(i))+'_TM=')[1].strip('\n')
            temp_df.loc[i*4+1,'Tm']=p3_file_content[19+i*31+13].split('PRIMER_INTERNAL_'+str(int(i))+'_TM=')[1].strip('\n')
            temp_df.loc[i*4+2,'Tm']=p3_file_content[19+i*31+12].split('PRIMER_RIGHT_'+str(int(i))+'_TM=')[1].strip('\n')
            temp_df.loc[i*4,'GC Percent']=p3_file_content[19+i*31+14].split('PRIMER_LEFT_'+str(int(i))+'_GC_PERCENT=')[1].strip('\n')
            temp_df.loc[i*4+1,'GC Percent']=p3_file_content[19+i*31+16].split('PRIMER_INTERNAL_'+str(int(i))+'_GC_PERCENT=')[1].strip('\n')
            temp_df.loc[i*4+2,'GC Percent']=p3_file_content[19+i*31+15].split('PRIMER_RIGHT_'+str(int(i))+'_GC_PERCENT=')[1].strip('\n')
            temp_df.loc[i*4+3,'Amplicon']=p3_file_content[19+i*31+30].split('PRIMER_PAIR_'+str(int(i))+'_PRODUCT_SIZE=')[1].strip('\n')
        output_df=pd.concat([output_df,temp_df],ignore_index=True)
    
output_df.to_excel(args.output,index=None)
    
    