# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:53:32 2025

@author: 67535
"""

from owlready2 import *
import argparse

def get_antibiotics_from_owl(drug_ARO,onto):
    
    #onto=get_ontology("http://purl.obolibrary.org/obo/aro.owl").load()

    target_class=IRIS[f"http://purl.obolibrary.org/obo/ARO_{drug_ARO}"]
    
    # List to hold all the classes that have the given object property pointing to the target class
    related_classes = []
    
    # Loop through all classes in the ontology
    for cls in onto.classes():

        if target_class in cls.is_a:
            related_classes.append(cls.name.strip('ARO_'))

    return related_classes

parser = argparse.ArgumentParser(description='Use a list of drug names to search for the drug AROs')

parser.add_argument('-o', '--output', required = False,
                    help='Output file path and name containing all available AROs, suffix not needed. Default: ./output/drug_AROs',default='./output/drug_AROs')
parser.add_argument('-i', '--input',required = True,
                    help='Input txt file path listing the drugs of interest.')

args = parser.parse_args()

onto=get_ontology("http://purl.obolibrary.org/obo/aro.owl").load()

file=open(args.input)
drug_list=file.readlines()
file.close()

drugs_not_found=[]
drug_AROs=[]
drugs_found=[]

for i in range(0,len(drug_list)):
    drug_list[i]=drug_list[i].strip('\n')
    a=str(onto.search(label=drug_list[i],_case_sensitive=False))
    if len(a)>2:
        a=a.split('ARO_')[1].split(']')[0]
        drug_AROs.append(a)
        drugs_found.append(drug_list[i])
    else:
        drugs_not_found.append(drug_list[i])

drug_AROs_out=drug_AROs    #Append more AROs from sub-class antibiotics
for i in range(0,len(drug_AROs)):
    drug_AROs_out=drug_AROs_out+get_antibiotics_from_owl(drug_AROs[i],onto)

print('The AROs of the drugs listed below were not found, please check the spelling or change to other synonyms and try again:')        
print(drugs_not_found)
print('\n')
print('The AROs of the following drugs were found:')
print(drugs_found)
print(drug_AROs_out)

ARO_output=open(args.output+'.txt','w')
for i in range(0,len(drug_AROs_out)):
    print(drug_AROs_out[i],file=ARO_output)
ARO_output.close()

drug_not_found_output=open(args.output.split('drug_AROs')[0]+'drugs_not_found_try_other_synonyms.txt','w')
for i in range(0,len(drugs_not_found)):
    print(drugs_not_found[i],file=drug_not_found_output)
drug_not_found_output.close()