#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 04:38:30 2017

@author: Aretas
"""

#creates a smiles file for each molecule in the list
import sys

list_file = open (sys.argv[1]).readlines()

for line in list_file:
    f = line.split()
    number = f[0]
    smiles = f[6]
    file_name = "scaffold_" + number + ".smiles"
    open_file = open(file_name, "w")
    open_file.write(smiles)
    open_file.close()
