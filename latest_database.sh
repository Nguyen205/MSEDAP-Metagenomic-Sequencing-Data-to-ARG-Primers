mkdir card
cd card
wget -c https://card.mcmaster.ca/latest/data -O card_data.tar.bz2
tar -xvjf card_data.tar.bz2
python3 ../card_fasta_trim.py -f nucleotide_fasta_protein_homolog_model.fasta -o ../ARG_with_NH8B.fasta
cd ..
samtools faidx ARG_with_NH8B.fasta
bowtie2-build ARG_with_NH8B.fasta ARG_with_NH8B
python3 ARO_index_convert.py -i ./card/aro_index.tsv -o ARO_index.csv
python3 separate_to_multiple_fasta.py -i ARG_with_NH8B.fasta -o ARG_fasta_separated
cd ARG_fasta_separated
ls | while read i; do echo ${i} >> ARG_fasta_list_for_ANI.txt; done
fastANI --rl ARG_fasta_list_for_ANI.txt --ql ARG_fasta_list_for_ANI.txt -t 40 --fragLen 100 --minFraction 0.9 -o ARG_ANI_output.txt
cd ..
python3 ARG_clustering_by_ANI.py -i ./ARG_fasta_separated/ARG_ANI_output.txt -o ./ARG_fasta_separated/ARG_clustering_raw.csv
python3 ARG_clustering_add_info.py -i ./ARG_fasta_separated/ARG_clustering_raw.csv -a ARO_index.csv -o ARG_clustering.csv