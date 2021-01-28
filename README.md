# Mutagenesis_Primer_Maker
Makes primers for mutagenesis work (***Internet Access is required***)

Mutations must be in this format: Original Residue Residue Number Residue to mutate to. E.G. (```R133A```)

Has 3 inputs:

```-file```
The DNA file of your protein (must not contain any tags, the first codon should be your first amino acid). 

```atgagtta```

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
The output for each mutation will indicate which primer is being run, and a forward and reverse primer with the respective Tms. The program runs all 4 possible variations for the forward and reverse primers for the mutation (i.e. all 3 mutant bases on the forward primer, 2 mutant bases on the forward and 1 mutant base on the reverse, etc.). 

Example output (GCG is the mutant bases for the Alanine):
```
Primers for mutation R133A
Forward Primer GCGCACAGCTTTAACGCACTGTTAAAAACC with Tm 72/67
Reverse Primer CGACAGCATGTGCACTTCGTC with Tm 69


Forward Primer CGCACAGCTTTAACGCACTGTTAAAAACCCTT with Tm 73/69
Reverse Primer CCGACAGCATGTGCACTTCGTCG with Tm 73/71


Forward Primer GCACAGCTTTAACGCACTGTTAAAAACCCTT with Tm 71/69
Reverse Primer GCCGACAGCATGTGCACTTCGT with Tm 73/68


Forward Primer CACAGCTTTAACGCACTGTTAAAAACCCTT with Tm 69/69
Reverse Primer CGCCGACAGCATGTGCACTTC with Tm 72/64
```
