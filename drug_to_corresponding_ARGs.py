# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 21:15:28 2024

@author: 67535
"""

from owlready2 import *
import pandas as pd
import argparse

def get_ARGs_from_owl(drug_ARO,onto):
    
    #onto=get_ontology("http://purl.obolibrary.org/obo/aro.owl").load()

    target_class=IRIS[f"http://purl.obolibrary.org/obo/ARO_{drug_ARO}"]
    
    # List to hold all the classes that have the given object property pointing to the target class
    related_classes=[]
    related_families=[]
    # Loop through all classes in the ontology
    confers_resistance_to_antibiotic=onto.search_one(iri="*2000000")  
    confers_resistance_to_drug_class=onto.search_one(iri="*2000001")
    
    for cls in onto.classes():
        try:
            if target_class in getattr(cls, confers_resistance_to_antibiotic.name, []):
                related_classes.append(cls.name.strip("ARO_"))
            if target_class in getattr(cls, confers_resistance_to_drug_class.name, []):
                related_families.append(cls.name.strip("ARO_"))
        except AttributeError:
            continue
    return related_classes, related_families

def get_ARGs_from_family(family_ARO,onto):
    
    #onto=get_ontology("http://purl.obolibrary.org/obo/aro.owl").load()

    target_class=IRIS[f"http://purl.obolibrary.org/obo/ARO_{family_ARO}"]
    
    # List to hold all the classes that have the given object property pointing to the target class
    related_classes=[]
    # Loop through all classes in the ontology
    for cls in onto.classes():

        if target_class in cls.is_a:
            related_classes.append(cls.name.strip('ARO_'))

    return related_classes

onto_content=get_ontology("http://purl.obolibrary.org/obo/aro.owl").load()
parser = argparse.ArgumentParser(description='Use the ARO list of antibiotics of interested to search for the sequences of antibiotic resistance genes (ARGs).')

parser.add_argument('-o', '--output', required = False,
                    help='Output fasta file path and name. Default: ./output/output_ARG_seq.fasta',default='./output/output_ARG_seq.fasta')
parser.add_argument('-i', '--input',required = True,
                    help='Input txt file path listing AROs of the drugs of interest.')
parser.add_argument('-c', '--coverage', required = True,
                    help='Input tsv file generated from Samtools coverage containing the ARG mapping information of a given sample.')   
parser.add_argument('-p', '--percent',required = False,
                    help='The coverage percent threashold to determine whether an ARG is detected. Default: 70',default=70)
args = parser.parse_args()


file=open("./ARG_with_NH8B.fasta")  
fasta=file.readlines()
file.close()

file=open(args.input)
drug_list=file.readlines()
file.close()  

for i in range(0,len(drug_list)):
    drug_list[i]=drug_list[i].strip('\n').strip()

map_file=pd.read_csv(args.coverage,sep='\t')   

mapped_ARGs=[]
for i in range(0,len(map_file)):
    if map_file.loc[i,'coverage']>=float(args.percent):
        mapped_ARGs.append(str(map_file.loc[i,'#rname']))

AROs_for_gRNA=[]
for i in range(0,len(fasta),2):
    AROs_for_gRNA.append(fasta[i])

ARG_list=[]
ARG_family_list=[]
for drug in drug_list:
    ARG_list_temp,ARG_family_list_temp=get_ARGs_from_owl(drug,onto_content)
    ARG_list=ARG_list+ARG_list_temp
    ARG_family_list=ARG_family_list+ARG_family_list_temp

for i in range(0,len(ARG_family_list)):
    ARG_list=ARG_list+get_ARGs_from_family(ARG_family_list[i],onto_content)

ARG_list=sorted(set(ARG_list))

output_list=[]
for i in range(0,len(ARG_list)):
    for j in range(0,len(AROs_for_gRNA)):
        if ARG_list[i] in AROs_for_gRNA[j]:
            output_list.append(ARG_list[i])
            break

output_list=list(set(output_list).intersection(set(mapped_ARGs)))

out_file=open(args.output,'w')   
for i in range(0,len(output_list)):
    for j in range(0,len(fasta),2):
        if output_list[i] in fasta[j]:
            print(fasta[j],file=out_file,end='')
            print(fasta[j+1],file=out_file,end='')
            break
out_file.close()   
    
    