#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  20 15:47:08 2017

@author: Aretas
"""
## input: text file with enantiomers in the format of linear_scaffold_list_ch.txt
## output: enantiomer list and 2D sketeches of each ligand
import sys
import os

file_name = "linear_enantiomer_list.txt"
open_file = open(file_name, "w")
#open_file.write("Number Isomer number IUPAC SMILES")

with open (sys.argv[1]) as f:
    counter = 1
    for line in f:
        f = line.split()
        len_f = len(f)

        if len_f == 5:
            scaffold_name = "scaffold_" + f[0]
            smiles_comma = '"' + f[4] + '"'
            command1 = "obabel -:{0} -O {1}.svg".format(smiles_comma, scaffold_name)
            os.system(command1)
            open_file.write("{:2} | {:4} | {:37} | {:20} \n".format(counter,
                f[0], f[2], f[4]))
            counter += 1

        if len_f == 11 or len_f == 19 or len_f == 7:
            n = 1
            for i in f:
                if i.startswith("C"):
                    smiles_comma = '"' + i + '"'
                    scaff_number = f[0] + "_"  + str(n)
                    scaffold_name = '"scaffold_' + scaff_number + '"'
                    command1 = "obabel -:{0} -O {1}.svg".format(smiles_comma,
                        scaffold_name)
                    os.system(command1)
                    n += 1
                    open_file.write("{:2} | {:4} | {:37} | {:20} \n".format(counter,
                        scaff_number, f[2], i))
                    counter += 1

    open_file.close()
    print ('DONE')
