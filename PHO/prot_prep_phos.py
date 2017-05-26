#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 19:10:01 2017

@author: Aretas
"""

#removes HETATM rows except for phosphate groups (if there is one);
#accepts protein pdb as a CL argument
import sys
import os
import re

file_name = str(sys.argv[1])
m_obj = re.search(r'(.*).pdb', file_name)
if m_obj:
    protein_name = m_obj.groups()[0]

file_path = os.path.realpath(sys.argv[1])
directory = file_path.strip("{0}/".format(file_name))

completeName = "/" + directory + "/{0}_NS_pho.pdb".format(protein_name)
with open(sys.argv[1]) as file1:
    with open(completeName, "w") as file2:
        for line in file1:
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
print ("DONE")
