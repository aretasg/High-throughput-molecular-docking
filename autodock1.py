#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 03:51:37 2017

@author: Aretas
"""

###Accepts vina config file and location of vina as input
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--vina_config_file',
    help='choose a vina configuration file', required=True)
parser.add_argument('-vina', '--vina_location',
    help='choose the vina directory', required=True)

args = parser.parse_args()
file_name = str(args.vina_config_file)
home_dir = args.vina_location

m_obj = re.search(r'config_vina_(.*)_(.*)_(.*).txt', file_name)
if m_obj:
    protein_name = m_obj.groups()[0]
    scaffold_number = m_obj.groups()[1]
    print (protein_name + " scaffold " + scaffold_number)

if home_dir.endswith("/"):
    home_dir.strip("/")

command1 = home_dir + " --config {2} > \
    {0}_vina_scaffold_{1}_out.txt".format(protein_name,scaffold_number,file_name)

os.system(command1)
