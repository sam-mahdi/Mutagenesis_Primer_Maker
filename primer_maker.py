import math

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import time

import re

import sys

import argparse

import os



parser = argparse.ArgumentParser()

parser.add_argument('-file',help='Upload your file with the DNA sequence, make sure it only contains the DNA of your protein, no tags')

parser.add_argument('-res_start',help='Indicate the residue number of your first amino acid')

parser.add_argument('-mutations',help='A list of mutations. Ensure mutations are listed one mutation per line')

args = parser.parse_args()

chromedriver_directory=(os.getcwd()+'/chromedriver')

try:
  os.system(f"chmod +x {chromedriver_directory}")
except:
  pass


starting_residue_number=int(args.res_start)

dna_file=args.file



dna_codon_dict={'TTT':'F','TTC':'F',

                'TTA':'L','TTG':'L',

                'CTT':'L','CTC':'L',

                'CTA':'L','CTG':'L',

                'ATT':'I','ATC':'I',

                'ATA':'I','ATG':'M',

                'GTT':'V','GTC':'V',

                'GTA':'V','GTG':'V',

                'TCT':'S','TCC':'S',

                'TCA':'S','TCG':'S',

                'CCT':'P','CCC':'P',

                'CCA':'P','CCG':'P',

                'ACT':'T','ACC':'T',

                'ACA':'T','ACG':'T',

                'GCT':'A','GCC':'A',

                'GCA':'A','GCG':'A',

                'TAT':'Y','TAC':'Y',

                'CAT':'H','CAC':'H',

                'CAA':'Q','CAG':'Q',

                'AAT':'N','AAC':'N',

                'AAA':'K','AAG':'K',

                'GAT':'D','GAC':'D',

                'GAA':'E','GAG':'E',

                'TGT':'C','TGC':'C',

                'TGG':'W','CGT':'R',

                'CGC':'R','CGA':'R',

                'CGG':'R','AGT':'S',

                'AGC':'S','AGA':'R',

                'AGG':'R','GGT':'G',

                'GGC':'G','GGA':'G',

                'GGG':'G','TAA':'X',

                'TAG':'X','TGA':'X'}

DNA_complement_dict={'A':'T',

                     'T':'A',

                     'G':'C',

                     'C':'G',

                     'N':'N'}

Codons_to_use={'F':'TTT','L':'CTG','Y':'TAT','H':'CAT','Q':'CAG','I':'ATT','M':'ATG','N':'AAC','K':'AAA','V':'GTG','D':'GAT','E':'GAA','S':'AGC','C':'TGC','P':'CCG','R':'CGT','T':'ACC','A':'GCG','G':'GGC'}



def create_sequence_lists(mutation):

    sequence=[]

    dna_sequence=[]

    counter=0

    codon=[]

    with open(dna_file,'rU') as file:

        for lines in file:

            for letters in lines:

                if letters == '\n' or letters == '':

                    continue

                codon.append(letters.upper())

                dna_sequence.append(letters.upper())

                counter+=1

                if counter == 3:

                    sequence.append(dna_codon_dict[''.join(codon)])

                    counter=0

                    codon.clear()

    return dna_sequence,sequence

def create_primers(mutation):

    counter=0

    codon=[]

    residue_number=0+starting_residue_number-1

    counter2=0+starting_residue_number-1

    primer_for=[]

    primer_rev=[]

    if list(mutation)[-1] == '\n':

        mutation=(list(mutation))

        mutation.pop(-1)

        mutation=''.join(mutation)

    mutant_number=int(''.join((list(mutation))[1:-1]))

    dna_sequence,sequence=create_sequence_lists(mutation)

    for bases in dna_sequence:

        codon.append(bases)

        counter+=1

        if counter == 3:

            residue_number+=1

            for residues in sequence:

                counter2+=1

                if counter2 == residue_number and counter2 <= mutant_number+10:

                    if counter2 >= mutant_number-10:

                        if counter2 == mutant_number and residues == ((list(mutation)[0])).upper():

                            primer_for.append(Codons_to_use[((list(mutation)[-1])).upper()])

                            continue

                        if counter2 > mutant_number:

                            for letters in codon:

                                primer_for.append(letters)

                            continue

                        for letters in codon:

                            primer_rev.append(DNA_complement_dict[letters])

                        continue

            codon.clear()

            counter=0

            counter2=0+starting_residue_number-1

    primer_rev_reverse=((''.join(primer_rev))[::-1]).split()

    return primer_for,primer_rev_reverse



def tm_calculator(mutation):

    primer_for,primer_rev_reverse=create_primers(mutation)

    options = Options()

    options.add_argument("--window-size=1920,1080")

    options.add_argument("--start-maximized")

    options.add_argument("--disable-gpu")

    options.add_argument('--disable-extensions')

    options.add_argument('--no-sandbox')

    options.add_argument("--headless")

    options.add_argument('log-level=3')

    options.add_argument('--proxy-server="direct://"')

    options.add_argument('--proxy-bypass-list=*')

    driver = webdriver.Chrome(executable_path=chromedriver_directory,options=options)

    driver.get('https://tmcalculator.neb.com/#!/main')

    fill_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="p1"]')))

    fill_box.clear()

    fill_box.send_keys(''.join(primer_for))

    fill_box = driver.find_element_by_xpath('//*[@id="p2"]')

    fill_box.clear()

    fill_box.send_keys((''.join(primer_for)[3:]))

    tm_1=driver.find_element_by_xpath('//*[@id="tm1"]/div[2]/strong[3]')

    tm_2=driver.find_element_by_xpath('//*[@id="tm2"]/div[2]/strong[3]')

    tm_value1=int((''.join(list(tm_1.text.split()[-1])[0:2])))

    tm_value2=int((''.join(list(tm_2.text.split()[-1])[0:2])))

    tm_forward_value_1=0

    tm_forward_value_2=0

    print(f'\nPrimers for mutation {mutation}')

    if tm_value1 <= 73 and (tm_value1-tm_value2) <= 12:

        print(f'Forward Primer {"".join(primer_for)} with Tm {tm_value1}/{tm_value2}')

    else:

        count=0

        while tm_value1 >= 74:

            count-=1

            fill_box = driver.find_element_by_xpath('//*[@id="p1"]')

            fill_box.clear()

            fill_box.send_keys(''.join(primer_for)[0:count])

            fill_box = driver.find_element_by_xpath('//*[@id="p2"]')

            fill_box.clear()

            fill_box.send_keys((''.join(primer_for)[3:count]))

            tm_1=driver.find_element_by_xpath('//*[@id="tm1"]/div[2]/strong[3]')

            tm_2=driver.find_element_by_xpath('//*[@id="tm2"]/div[2]/strong[3]')

            tm_value1=int((''.join(list(tm_1.text.split()[-1])[0:2])))

            tm_value2=int((''.join(list(tm_2.text.split()[-1])[0:2])))

        tm_forward_value_1+=tm_value1

        tm_forward_value_2+=tm_value2

        print(f'Forward Primer {"".join(primer_for)[0:count]} with Tm {tm_value1}/{tm_value2}')



    fill_box = driver.find_element_by_xpath('//*[@id="p1"]')

    fill_box.clear()

    fill_box.send_keys(''.join(primer_rev_reverse))

    fill_box = driver.find_element_by_xpath('//*[@id="p2"]')

    fill_box.clear()

    fill_box.send_keys((''.join(primer_rev_reverse)))

    tm_1=driver.find_element_by_xpath('//*[@id="tm1"]/div[2]/strong[3]')

    tm_2=driver.find_element_by_xpath('//*[@id="tm2"]/div[2]/strong[3]')

    tm_value1=int((''.join(list(tm_1.text.split()[-1])[0:2])))

    tm_value2=int((''.join(list(tm_2.text.split()[-1])[0:2])))

    if tm_value1 < (tm_forward_value_1-1) and tm_value1 > (tm_forward_value_2+1):

        print(f'Reverse Primer {"".join(primer_rev_reverse)} with Tm {tm_value1}')

    else:

        count=0

        while tm_value1 >= (tm_forward_value_1-1):

            count-=1

            fill_box = driver.find_element_by_xpath('//*[@id="p1"]')

            fill_box.clear()

            fill_box.send_keys(''.join(primer_rev_reverse)[0:count])

            fill_box = driver.find_element_by_xpath('//*[@id="p2"]')

            fill_box.clear()

            fill_box.send_keys(''.join(primer_rev_reverse)[0:count])

            tm_1=driver.find_element_by_xpath('//*[@id="tm1"]/div[2]/strong[3]')

            tm_2=driver.find_element_by_xpath('//*[@id="tm2"]/div[2]/strong[3]')

            tm_value1=int((''.join(list(tm_1.text.split()[-1])[0:2])))

            tm_value2=int((''.join(list(tm_2.text.split()[-1])[0:2])))

        print(f'Reverse Primer {"".join(primer_rev_reverse)[0:count]} with Tm {tm_value1}')



def main_loop():

    if args.mutations is not None:

        with open(args.mutations,'rU') as mutation_file:

            for lines in mutation_file:

                tm_calculator(lines)

    else:

        while True:

            question=input('enter mutation: ')

            tm_calculator(question)

main_loop()
