#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 01:47:08 2017

@author: Aretas
"""

#input linear_scaffold_list_ch.txt
#print scaffold number; IUPAC name; smiles and number of enantiomers

import sys

file1 = open (sys.argv[1]).readlines()
file2 = open (sys.argv[2]).readlines()

dict1 = {}

for line in file1:
    f = line.split("|")
    #print (f[0], f[1])
    count = 0
    for item in f:
        count += 1
    count_1 = count - 2
    dict1[int(f[0])] = count_1

file_open = open("linear_scaffold_list2.txt", "w")
for line in file2:
    f = line.split("|")
    number = int(f[0])

    #print(f[0], "|" , f[1] , "|" , dict1[number],  "|" , f[2])
    file_open.write(str(f[0]) + " | " + str(f[1]) + " | " + str(dict1[number]) + " | " + str(f[2]) + "\n")

file_open.close()
