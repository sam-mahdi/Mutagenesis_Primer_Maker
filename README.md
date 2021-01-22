# Mutagenesis_Primer_Maker
Makes primers for mutagenesis work

Has 3 inputs:

The DNA file of your protein (must not contain any tags, the first codon should be your first amino acid). 

The first starting residue number (i.e. if your construct of an individual domain 200-373, then your starting residue number is 200). 

Optional: A text file containing the desired mutations. One mutation per line 
I.E.
R133A
F451T

Example input
```
python3 primer_maker.py -file gene_sequence.txt -res_start 1 -mutations mutation_list.txt
```
