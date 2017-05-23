#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 19:10:01 2017

@author: Aretas
"""

###removes HETATM rows except for phosphate groups (if there is one), Mg, Mn, waters;
# accepts protein pdb as a CL argument
import sys, os, re

file_name = str(sys.argv[1])
file = open (sys.argv[1]).readlines()


m_obj = re.search(r'(.*).pdb', file_name)
if m_obj:
    protein_name = m_obj.groups()[0]

file_path = "/Users/Aretas/RP1/MD_C_scaff_pho/"
directory = os.path.dirname(file_path)

if not os.path.exists(file_path):
    os.makedirs(file_path)

completeName = os.path.join(file_path,"{0}_NS_pho.pdb".format(protein_name))  
file2 = open(completeName, "w")  
for line in file:
    m_obj2 = re.search(r'^HETATM',line)
    m_obj3 = re.search(r'^HET',line)
    
    if m_obj2 or m_obj3:
   
        m_obj4 = re.search(r'P  $',line)
        m_obj5 = re.search(r'O  $',line)
        m_obj8 = re.search(r'HOH',line)  #water
        m_obj9 = re.search(r'BTB',line)  #buffer HETATM
        m_obj10 = re.search(r'BME',line) #buffer
        m_obj11 = re.search(r'EDO',line)  #buffer

        if m_obj4 or m_obj5 and not m_obj8 and not m_obj9 and not m_obj10 and not m_obj11:
            file2.write(line) 
            
    if not m_obj2 or not m_obj3:
        file2.write(line)

file2.close()
print ("DONE")
