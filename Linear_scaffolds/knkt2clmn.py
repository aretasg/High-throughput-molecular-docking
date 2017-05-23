#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 18:32:30 2017

@author: Aretas
"""
## a script to create a .txt file with 2 columns; IUPAC and smiles 
import sys

file1 = open(sys.argv[1]).readlines() #SMILES file
file2 = open(sys.argv[2]).readlines() #IUPAC file; both should list compounds in the same order

smiles_list = []
IUPAC_list = []
dictionary = {}

for line in file1:
    smiles_list.append(line.strip("\n"))
    
for line in file2:
    IUPAC_list.append(line.strip("\n"))
    
#print (smiles_list)

dictionary = dict(zip(IUPAC_list, smiles_list))
#print (dictionary)

open_file = open("linear_scaffold_list.txt", "w")
n = 1
for i in IUPAC_list:
    smiles = dictionary[i]
    open_file.write('{:2} | {:37} | {:20} | \n'.format(n, i, smiles))
    n += 1

open_file.close()
print ("DONE")