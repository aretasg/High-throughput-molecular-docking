#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 03:51:37 2017

@author: Aretas
"""

#creates a config files(s) for vina; accepts enzyme PDB as input
#uses default settings
#accepts and xyz coordinate and xyz box size as input
#default search parameters work with all bornyl synthases except for 1n21
#Results folder -lo
#lo1 flag is for specifting folder directory with the ligand PDBQT library
#ligands must be in name_number format e.g. skeleton_12.pdbqt
#Please use with enyzme library as PWD! Otherwise the script won't work

import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',
    help='choose the PDB protein file', required=True)
parser.add_argument('-xc', '--x_center',
    help='choose x center coordinate', default=45)
parser.add_argument('-yc', '--y_center',
    help='choose the y center coordinate:', default=50)
parser.add_argument('-zc', '--z_center',
    help='choose the z center coordinate:', default=50)
parser.add_argument('-xs', '--x_size',
    help='choose the x size', default=20)
parser.add_argument('-ys', '--y_size',
    help='choose the y size', default=20)
parser.add_argument('-zs', '--z_size',
    help='choose the z size', default=16)
parser.add_argument('-lo', '--location',
    help='choose the folder to save the file to', required=True)
parser.add_argument('-lo1', '--location1',
    help='choose the folder of the ligand PDBQT library', default="Linear_structures/PDBQT_EMM")
parser.add_argument('-ch', '--chain',
    help='specify the enzyme chain (A/B) to perform MD with', default="A")

parser.add_argument('-m', '--num_modes',
    help='choose num_modes', default=15)
parser.add_argument('-e', '--exhaustiveness',
    help='choose exhaustiveness', default=15)
parser.add_argument('-s', '--seed',
    help='choose seed value', default=314159)

args = parser.parse_args()
x_center = float(args.x_center)
y_center = float(args.y_center)
z_center = float(args.z_center)
x_size = float(args.x_size)
y_size = float(args.y_size)
z_size = float(args.z_size)
location = args.location    #MD results folder
location1 = args.location1  #Ligand library location
chain = args.chain

file_name = str(args.file)
pdb_location = os.path.realpath(args.file)
MD_folder = os.path.realpath(args.location)
if not os.path.exists(MD_folder):
    os.makedirs(MD_folder)
ligand_location = os.path.realpath(args.location1)

#print (pdb_location, MD_folder, ligand_location)
m_obj = re.search(r'(.*)_NS(.*).pdbqt', args.file)
if m_obj:
    protein_name = m_obj.groups()[0]
    misc_name = m_obj.groups()[1]
    protein_name = protein_name + "_NS" + misc_name

folder_name = protein_name + "_{0}_final1".format(chain)
file_path = MD_folder + "/" + folder_name + "/"
file_path3 = MD_folder + "/"
file_path4 = ligand_location + "/"

if not os.path.exists(file_path):
    os.makedirs(file_path)

for filename in os.listdir(file_path4):
    scaffold_number = re.search(r'(.*)_(.*)_min.pdbqt',filename)
    if scaffold_number:
        scaffold_number_hit = scaffold_number.groups()[1]
        scaffold_name = scaffold_number.groups()[0]

        completeName = os.path.join(file_path,"config_vina_{0}_{2}_{1}.txt"
            .format(protein_name, scaffold_number_hit, chain))
        with open(completeName, "w") as file2:

            file2.write("receptor = {0}{1}.pdbqt\n".format(file_path3, protein_name))
            file2.write("ligand = {1}{2}_{0}_min.pdbqt\n".format(scaffold_number_hit, file_path4, scaffold_name))
            file2.write("\n")
            file2.write("out = {2}{0}_{3}_{4}_{1}_vina.pdbqt\n".format(
                protein_name,scaffold_number_hit,file_path, chain, scaffold_name))
            file2.write("\n")
            file2.write("center_x = {0}\n".format(x_center))
            file2.write("center_y = {0}\n".format(y_center))
            file2.write("center_z = {0}\n".format(z_center))
            file2.write("\n")
            file2.write("size_x = {0}\n".format(x_size))
            file2.write("size_y = {0}\n".format(y_size))
            file2.write("size_z = {0}\n".format(z_size))
            file2.write("\n")
            file2.write("exhaustiveness = {0}\n".format(args.exhaustiveness))
            file2.write("\n")
            file2.write("num_modes = {0}\n".format(args.num_modes))
            file2.write("\n")
            file2.write("seed = {0}\n".format(args.seed))

print("DONE")
