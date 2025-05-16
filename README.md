# MSEDAP: Metagenomic Sequencing Data to ARG Primers
Metagenomic sequencing results can guide the design of qPCR primers and probes. This is a pipeline for designing qPCR primers and probes targeting the ARGs of interest based on metagenomic sequencing results and a list of antibiotics of interest. 

## Description
Metagenomic sequencing and qPCR are two mainstream methods for detecting antibiotic resistance genes (ARGs) in complex DNA samples (e.g., wastewater, stool, etc.). Metagenomic sequencing can detect a wide range of ARGs without targeting them, while qPCR requires primer and probe design for each ARG. However, metagenomic sequencing is more expensive, harder to perform, and less sensitive than qPCR. Therefore, for routine ARG surveillance, it is more practical to use metagenomic sequencing at the beginning to determine the range of target ARGs and design qPCR primers and probes accordingly. In addition, metagenomic sequencing can detect the mutated sites in ARGs. To achieve better qPCR efficiencies, these mutated sites should be avoided in primer and probe design. Hundreds to thousands of ARGs may be found in metagenomic sequencing, but not all ARGs should be included in routine qPCR surveillance. This pipeline fills the gap between metagenomic sequencing and qPCR primer design for routine surveillance. With a drug list of interest and the fastq file from metagenomic sequencing, this pipeline generates qPCR primers and probes targeting the ARGs of most concern in the sample while avoiding the mutated sites.

## Package Requirements
### Python Packages  
* [Owlready2](https://github.com/pwin/owlready2)  
* [PyVCF](https://github.com/jamescasbon/PyVCF)
* [Pandas](https://anaconda.org/anaconda/pandas) 
* [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/index.html)
### Bioinformatic Tools  
* [Samtools](https://www.htslib.org/) (v1.10 or above)  
* [FreeBayes](https://github.com/freebayes/freebayes)  
* [Bowtie2](https://github.com/BenLangmead/bowtie2)
* [Primer3](https://github.com/primer3-org/primer3) (Primer3 installation is included in the "Installing" part below)
* [IGV](https://igv.org/)

## Installing 
```
sudo apt-get install -y build-essential g++ cmake git-all
```
```
git clone https://github.com/Nguyen205/MSEDAP-Metagenomic-Sequencing-Data-to-ARG-Primers.git msedap
```
```
cd msedap
```
```
git clone https://github.com/primer3-org/primer3.git primer3
```
```
cd primer3/src
```
```
make
```
```
make test
```

## Database Update
Before the first use, to access the latest version of the Comprehensive Antibiotic Resistance Database (CARD), run the commands below. It will take around 30 minutes to update all files needed for MSEDAP. For future database updates, delete the `card` and `ARG_fasta_separated` directories generated in previous updates before running the commands.
```
cd msedap
```
```
./latest_database.sh
```

## Usage 
Before you start, it is recommended to use sequencing quality filtering tools (e.g., [PriceSeqFilter](https://vcru.wisc.edu/simonlab/bioinformatics/programs/price/PriceDocumentation140408/independentQualityFilter.html)) to remove low-quality reads from the fastq files.
```
cd msedap
```
For single-read fastq input (See `example/drug_name_example.txt` for the format of the drug list. See `example/single_fastq_list_example.txt` for the format of the single-read fastq path list.):
```
./msedap.sh -1 single_read_fastq_path_list.txt -d drug_list.txt
```
For paired-read fastq input (See `example/drug_name_example.txt` for the format of the drug list. See `example/paired_fastq_list_example.txt` for the format of the paired-read fastq path list.):
```
./msedap.sh -2 paired_read_fastq_path_list.txt -d drug_list.txt
```
Other optional parameters (Type `./msedap.sh -h` for detailed usage information):
```
-t INT     Number of threads used for running the code. (default: 1)
-p INT     The coverage percentage cutoff for determining the presence of a gene. (default: 70)
-m STR     The mode for ARG screening. A: all ARGs are included. C: select one ARG from each cluster of ARGs that share highly similar sequences. F: select one ARG from each ARG family that share highly similar functions. (default: A)
-s STR     The range of the PCR amplicon size. (default: 75-250)
-n INT     Number of primers designed for each ARG. (default: 5)
-f         Run FreeBayes to exclude primers that bind to mutated sites of the ARGs in the given sample.
-o STR     Name the output directory. (default: the current time stamp)
```

## Output Files
All output files of each individual run can be found in the corresponding directory in the `output` directory.<br />
<br />
**map#.bam**<br />
The individual ARG mapping file generated for each input fastq file by Bowtie2. <br />
<br />
**merge.bam**<br />
The merged ARG mapping file for all fastq files. <br />
<br />
**merge.bam.bai**<br />
The merged ARG mapping index file. <br />
<br />
**ARG_coverage.tsv**<br />
The file including the ARG coverage information of the given sample.<br />
<br />
**drug_AROs.txt**<br />
The AROs of the drugs provided by the user.<br />
<br />
**drugs_not_found_try_other_synonyms.txt**<br />
The names of the drugs whose AROs cannot be found in the database. Users may want to try other synonyms of these drugs.<br />
<br />
**ARG_seq.fasta**<br />
The file containing the sequences of the ARGs conferring resistance to the given drugs which are also present in the given metagenomic sample.<br />
<br />
**ARG_seq_screened.fasta**<br />
The file containing reduced number of the sequences of the ARGs conferring resistance to the given drugs. See `-m` for screening criteria.<br />
<br />
**primer3_input**<br />
The directory containing all primer3 input files for each individual ARG after screening.<br />
<br />
**primer3_output**<br />
The directory containing all primer3 designing results for each individual ARG after screening.<br />
<br />
**designed_primers.xlsx**<br />
The file containing all PCR primers designed for the ARGs conferring resistance to the given drugs without considering gene mutations.<br />
<br />
**merge_cleaned.bam**<br />
The ARG mapping file removing all secondary flags as the input of FreeBayes for detecting ARG mutations.<br />
<br />
**mutations.vcf**<br />
The file containing all mutated sites of the ARGs detected in the given sample.<br />
<br />
**designed_primers_mutation_screened.xlsx**<br />
The file containing all PCR primers with perfect matching to the ARGs conferring resistance to the given drugs in the given sample.<br />
<br />
