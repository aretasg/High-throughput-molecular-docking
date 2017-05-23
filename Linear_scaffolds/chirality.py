#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 21:04:15 2017

@author: Aretas
"""

#numerate the scaffolds
#find molecules with chiral centres
#connect smiles and chirality information to a dictionary
#bind the chiral C atom number to variable
#replace C with [C@] and C[@@]
#bind both version to variables and add to the respective keys in the final dictionary
#writes enantiomer SMILES to a .txt file together with IUPAC names, scaffold number
#ONLY deals with molecules with carbon atoms as chiral centres
#and only upto 3 chiral centres per a ligand molecule
#the script assumes that one of the covalently bound atoms to tetrahedral carbon is hydrogen
#if a none of the groups around the chiral centre are hydrogen; the script won't work

import sys, re

list_molecules = open (sys.argv[1]).readlines()  #text file with IUPAC names and SMILES
info_chirality = open (sys.argv[2]).readlines()  #chirality info from obchiral chi_info2.txt

dictionary_smiles = {} # ligand number : SMILES
chir_dict = {}         # ligand number : chiral carbon atom(s)
eta1 = "[C@H]"        # string to mark chirality in SMILES
eta2 = "[C@@H]"
enantiomer_dict = {} #enantiomer dicitonary

for line in list_molecules:
    f = line.split()            #!!!!!!! change these according to your preference
    dictionary_smiles[f[0]] = f[4] #modify these numbers depending on the position of SMILES and IUPAC name in the line of the input

for line in info_chirality: #obchiral input
    match1 = re.search(r'Molecule (.*): Atom ([0-9]+) Is Chiral C3',line)
    match2 = re.search(r'Molecule (.*): Atom ([0-9]+) Is Chiral C3; Atom ([0-9]+) Is Chiral C3',line)
    match3 = re.search(r'Molecule (.*): Atom ([0-9]+) Is Chiral C3; Atom ([0-9]+) Is Chiral C3; Atom ([0-9]+) Is Chiral C3',line)

    if match1:
        mol_no1 = match1.groups()[0]  #ligand number
        atom_no1 = match1.groups()[1]   #position of chiral carbon atom
        chir_dict [mol_no1] = atom_no1  #creating a new entry in the dictionary

    if match2:
        mol_no2 = match2.groups()[0]
        atom_no2 = match2.groups()[1]
        atom_no21 = match2.groups()[2]
        chir_dict [mol_no2] = atom_no2 + " " + atom_no21

    if match3:
        mol_no3 = match3.groups()[0]
        atom_no3 = match3.groups()[1]
        atom_no31 = match3.groups()[2]
        atom_no32 = match3.groups()[3]
        #print (mol_no3, atom_no3, atom_no31, atom_no32)
        chir_dict [mol_no3] = atom_no3 + " " + atom_no31 + " " + atom_no32

#print (chir_dict)

for i in chir_dict.keys():
    dictionary_smiles [i] += ", " + chir_dict[i]
    #adds position of chiral atoms to the key (ligand number) value (SMILES)
    #dictionary_smiles now looks like this: dictionary_smiles [1] = SMILES, 3, 5

##creating enantiomers with eta1 and eta2

for i in chir_dict.keys():  #ligand number in the library
    match_a = re.search(r'(.*), (.*)', dictionary_smiles[i]) #search the key value
    if match_a:
        m_obj1 = match_a.groups()[0]  #SMILES
        m_obj2 = match_a.groups()[1]  #chiral information

        f = m_obj2.split()  #splits chiral information

        count1 = len(f)  #count the number of chiral centres

        if count1 == 3:     #if there are three chiral centres
            first_cc = f[0] #set the position of chiral centres as variables
            second_cc = f[1]
            third_cc = f[2]

            new_string1 = "" #empty strings for each enantiomer
            new_string2 = ""
            new_string3 = ""
            new_string4 = ""
            new_string5 = ""
            new_string6 = ""
            new_string7 = ""
            new_string8 = ""
            C_counter = 0   #counting occurance of carbon atoms
            for letter in m_obj1:  # for every element in the SMILES string
                if letter == "C":  # if element is "C"
                    C_counter += 1 # update counter
                    if int(C_counter) == int(first_cc): #if the carbon is chiral
                        new_string1 += eta1   #replaces "C" with "C@H" or "C@@H"
                        new_string2 += eta1
                        new_string3 += eta1
                        new_string4 += eta2
                        new_string5 += eta2
                        new_string6 += eta2
                        new_string7 += eta1
                        new_string8 += eta2
                    elif int(C_counter) == int(second_cc):
                        new_string1 += eta1
                        new_string2 += eta1
                        new_string3 += eta2
                        new_string4 += eta1
                        new_string5 += eta2
                        new_string6 += eta2
                        new_string7 += eta2
                        new_string8 += eta1
                    elif int(C_counter) == int(third_cc):
                        new_string1 += eta1
                        new_string2 += eta2
                        new_string3 += eta2
                        new_string4 += eta1
                        new_string5 += eta1
                        new_string6 += eta2
                        new_string7 += eta1
                        new_string8 += eta2
                    else:
                        new_string1 += letter #if the element is carbon and is not chiral
                        new_string2 += letter #adds an original element back
                        new_string3 += letter
                        new_string4 += letter
                        new_string5 += letter
                        new_string6 += letter
                        new_string7 += letter
                        new_string8 += letter
                else:
                    new_string1 += letter #if the element is not carbon
                    new_string2 += letter #adds an original element back
                    new_string3 += letter
                    new_string4 += letter
                    new_string5 += letter
                    new_string6 += letter
                    new_string7 += letter
                    new_string8 += letter

            #print (new_string1, new_string2, new_string3, new_string4, new_string5, new_string6, new_string7, new_string8)
            enantiomer_dict[i] = (new_string1, new_string2, new_string3, \
                new_string4, new_string5, new_string6, new_string7, new_string8)
                #creates a new entry in the dicionary skeleton number : all enantiomer SMILES

        if count1 == 2:
            first_cc = f[0]
            second_cc = f[1]

            new_string1 = ""
            new_string2 = ""
            new_string3 = ""
            new_string4 = ""
            C_counter = 0
            for letter in m_obj1:
                if letter == "C":
                    C_counter += 1
                    if int(C_counter) == int(first_cc):
                        new_string1 += eta1
                        new_string2 += eta2
                        new_string3 += eta1
                        new_string4 += eta2
                    elif int(C_counter) == int(second_cc):
                        new_string1 += eta1
                        new_string2 += eta2
                        new_string3 += eta2
                        new_string4 += eta1
                    else:
                        new_string1 += letter
                        new_string2 += letter
                        new_string3 += letter
                        new_string4 += letter
                else:
                    new_string1 += letter
                    new_string2 += letter
                    new_string3 += letter
                    new_string4 += letter

            enantiomer_dict[i] = new_string1, new_string2, new_string3, new_string4

        if count1 == 1:
            first_cc = f[0]
            new_string1 = ""
            new_string2 = ""
            C_counter = 0
            for letter in m_obj1:
                if letter == "C":
                    C_counter += 1
                    if int(C_counter) == int(first_cc):
                        new_string1 = new_string1 + eta1
                        new_string2 = new_string2 + eta2
                    else:
                        new_string1 += letter
                        new_string2 += letter
                else:
                    new_string1 += letter
                    new_string2 += letter

            enantiomer_dict[i] = new_string1, new_string2

for i in dictionary_smiles.keys():     #iterate over ligand numbers
    if i not in enantiomer_dict.keys():  #if ligand number not in enantiomer_dict
        enantiomer_dict[i] = dictionary_smiles[i]  #add it
        #these commands copy ligands without chiral centres to make a full ligand list

print (enantiomer_dict)
open_file = open("linear_scaffold_list_ch.txt", "w")
for item in list_molecules:    #iterates over list of ligands (input)
    f = item.split()
    h = enantiomer_dict[f[0]]  #extracts enantiomer SMILES from dictionary
    len_h = len(h)            #the length of dict SMILES
    if len_h > 9:             #if length is more than 9 elements; in this case there is only one SMILES which is split up hence 9 elements
        open_file.write('{:2} | {:37} | {:20} \n'
            .format(f[0], f[2], enantiomer_dict[f[0]])) #number; IUPAC, SMILES
    if len_h == 2:          #if the length is 2; one chiral centre
        open_file.write('{:2} | {:37} | {:20} | {:20} \n'.format(f[0],
            f[2], h[0], h[1]))
    if len_h == 4:  #if the length is 4; two chiral centres
        open_file.write('{:2} | {:37} | {:20} | {:20} | {:20} | {:20} \n'
            .format(f[0], f[2], h[0], h[1], h[2], h[3]))
    if len_h == 8: #if the length is 8; three chiral centres
        open_file.write('{:2} | {:37} | {:20} | {:20} | {:20} | {:20} | {:20} \
        | {:20} | {:20} | {:20} \n'.format(f[0], f[2], h[0], h[1], h[2], h[3], \
            h[4], h[5], h[6], h[7]))
    #h_split = h.split()
    #print (f[0], f[2], enantiomer_dict[f[0]])
    #open_file.write('{:2} | {:37} | {:20} | \n'.format(f[0], f[2], enantiomer_dict[f[0]]))

open_file.close()
print ("DONE")
