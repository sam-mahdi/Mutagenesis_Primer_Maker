# Mutagenesis_Primer_Maker
Makes primers for mutagenesis work

Has 3 inputs:
```-file```
The DNA file of your protein (must not contain any tags, the first codon should be your first amino acid). 
```-res_start```
The first starting residue number (i.e. if your construct of an individual domain 200-373, then your starting residue number is 200). 
```-mutations```
Optional: A text file containing the desired mutations. One mutation per line 
I.E.
R133A
F451T
You may also type in -h for the above breakdown. 

Example input
```
python3 primer_maker.py -file gene_sequence.txt -res_start 1 -mutations mutation_list.txt
```
The output for each mutation will be an indication which primer is being run, and a forward and reverse primer with the respective Tms. The mutation will always be aded to the forward primer. 

Example output:
```
Primers for mutation R133A

Forward Primer GCGCACAGCTTTAACGCACTGTTAAAAACC with Tm 72/67
Reverse Primer CGACAGCATGTGCACTTCGTC with Tm 69
```
