#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 22:40:41 2017

@author: Aretas
"""

import os, re, argparse
import matplotlib.pyplot as plt
import numpy as np
import collections

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',
    help='choose the pdb protein file', required=True)
parser.add_argument('-n', '--normalisation',
    help='performs normalisation on the data', default=False)
parser.add_argument('-lo', '--location',
    help='choose the folder containing the pdb file; it should be in RP1 folder'
        , required=True)
parser.add_argument('-lo1', '--location1',
    help='choose the folder containing the ligand SMILES library', default='Natural_products')
parser.add_argument('-ch', '--chain',
    help='select enzyme chain', default = 'A')
parser.add_argument('-lo2', '--location2',
    help='choose the folder containing the control library docking results; it should be in RP1 folder')

args = parser.parse_args()
protein_file = str(args.file)
norm = args.normalisation
location = args.location
location1 = args.location1
chain = args.chain
control_location = args.location2

m_obj = re.search(r'(.*).pdb', protein_file)
if m_obj:
    protein_name = m_obj.groups()[0]
    print (protein_name)

p_name_chain = protein_name + "_" + chain
folder_name = protein_name + "_final1" + "_" + chain

dictionary = {}
dict_C = {}
dict_norm = {}

directory = "/Users/Aretas/RP1/" + location + "/" + folder_name + "/"  #ADD bornyl!!! #change vina regex
directory2 = "/Users/Aretas/RP1/" + location + "/aff_dis"
directory3 = "/Users/Aretas/RP1/" + location + "/aff_dis_norm"
directory4 = "/Users/Aretas/RP1/" + location + "/aff_dis_norm2"

#Extract the best affinity result
for filename in os.listdir(directory):
    if filename.endswith("_vina.pdbqt"):
        completeName = os.path.join(directory,"{0}".format(filename))
        open_file1 = open(completeName)
        open_file = open_file1.readlines()

        scaffold_number = re.search(r'{0}_scaffold_(.*)_vina.pdbqt'.format(p_name_chain), filename)
        scaffold_number2 = scaffold_number.groups()[0]

        for line in open_file:
            m_obj2 = re.search(r'REMARK VINA RESULT:(.*)',line)
            if m_obj2:
                split = line.split()
                if split[4] == "0.000": #retrieves just the first line
                    #print(split[3], scaffold_number2)
                    dictionary[scaffold_number2] = float(split[3]) #!!!!!!stores result in a dictionary
        # print(os.path.join(directory, filename))
        continue
    else:
        continue

#writes results to a file
scaffold_list = []
value_list = []

if not os.path.exists(directory2):
    os.makedirs(directory2)

completeName2 =  os.path.join(directory2,"{0}_scaffold_aff_dis.txt".format(p_name_chain))
file2 = open(completeName2, "w")

od = collections.OrderedDict(sorted(dictionary.items()))
for k, v in od.items():
    #file2.write(str(k) + " " + str(v) + "\n")
    value = dictionary[k]
    value1 = 0 - float(value)
    value_list.append(float(value1))
    scaffold_list.append(int(k))

for i in sorted(scaffold_list):
    file2.write(str(i) + " " + str(dictionary[str(i)]) + "\n")
'''
for item in dictionary.keys():
    #print (dictionary[item])
    file2.write(str(item) + " " + str(dictionary[item]) + "\n")

    value = dictionary[item]
    value1 = 0 - float(value)
    value_list.append(float(value1))
    scaffold_list.append(int(item))
'''

file2.close()

N = len(scaffold_list)
x_axis = np.arange(0,N,1)

plt.figure(1)
plt.xticks(x_axis, sorted(scaffold_list))
plt.bar(x_axis, value_list)
plt.ylabel ("Best affinity (-ve) results")
plt.xlabel ("Scaffold number")
plt.title('Scaffold affinity measure for {0}'.format(p_name_chain))
#plt.show()
plt.savefig('{1}/{0}_scaffold_aff_dis.png'.format(p_name_chain, directory2))


if norm:
    drctr = "/Users/Aretas/RP1/" + location1 + "/"

    ##opens scaffold smiles and counts C letters; stores info as dictionary
    for filename in os.listdir(drctr):
        if filename.endswith(".smiles"):
            completeName = os.path.join(drctr,"{0}".format(filename))
            open_smiles = open(completeName)
            read_smiles = open_smiles.readline()

            scaffold_number = re.search(r'(.*)_(.*).smiles', filename)
            scaffold_number2 = scaffold_number.groups()[1]


            f = read_smiles.split()
            counter_C = read_smiles.count('C')
            dict_C[scaffold_number2] = counter_C
            #print (read_smiles)
            #print (dict_C[scaffold_number2])
            continue
        else:
            continue

    ## the keys of both dict are the same;  have to divide one value from the other
    norm_list = []
    for i in scaffold_list:
        lets_norm_aff = (0 - float(dictionary[str(i)])) / float(dict_C[str(i)])
        #print (i, dictionary[str(i)], dict_C[str(i)], "%.3f" % lets_norm_aff)
        dict_norm[i] = "%.3f" % lets_norm_aff
        norm_list.append(float("%.3f" % lets_norm_aff))

    ###Writing normalisation data to a file and plotting
    if not os.path.exists(directory3):
        os.makedirs(directory3)

    completeName3 =  os.path.join(directory3,"{0}_scaffold_aff_dis_NORM.txt".format(p_name_chain))
    file3 = open(completeName3, "w")

    for i in sorted(scaffold_list):
        #print (str(i) + " " + dict_norm[i])

        file3.write(str(i) + " " + str(dict_norm[i]) + "\n")


    file3.close()
    print ("NORMALISATION: DONE")

    plt.figure(2)
    plt.xticks(x_axis, sorted(scaffold_list))
    plt.bar(x_axis, norm_list)
    plt.ylabel ("Best affinity (-ve) results")
    plt.xlabel ("Scaffold number")
    plt.title('Scaffold affinity normalisation for {0}'.format(p_name_chain))
    #plt.show()
    plt.savefig('{1}/{0}_scaffold_aff_dis_NORMAL.png'.format(p_name_chain, directory3))

### normalisation2
dictionary2 = {}
dict_norm2 = {}

if control_location:
    drctr = "/Users/Aretas/RP1/" + control_location + "/aff_dis/"


    for filename in os.listdir(drctr):
        if filename.endswith("{0}_{1}_scaffold_aff_dis.txt".format(protein_name, chain)):
            completeName = os.path.join(drctr,"{0}".format(filename))
            open_control = open(completeName)
            read_control = open_control.readlines()

            for line in read_control:
                f = line.split()
                c_count = int(f[0])
                affinity = f[1]
                dictionary2 [c_count] = float(affinity)

    norm_list2 = []
    for i in sorted(scaffold_list):
        lets_norm_aff = float(dictionary[str(i)]) / float(dictionary2[int(dict_C[str(i)])])
        dict_norm2[int(i)] = "%.3f" % lets_norm_aff
        norm_list2.append(float("%.3f" % lets_norm_aff))

    ###Writing normalisation data to a file and plotting
    if not os.path.exists(directory4):
        os.makedirs(directory4)

    completeName4 =  os.path.join(directory4,"{0}_scaffold_aff_dis_NORM2.txt".format(p_name_chain))
    file4 = open(completeName4, "w")

    od = collections.OrderedDict(sorted(dict_norm2.items()))
    for k, v in od.items():
        file4.write(str(k) + " " + str(v) + "\n")

    file4.close()
    print ("NORMALISATION2: DONE")

    plt.figure(3)
    plt.xticks(x_axis, sorted(scaffold_list))
    plt.bar(x_axis, norm_list2)
    plt.ylabel ("Best affinity (-ve) results")
    plt.xlabel ("Scaffold number")
    plt.title('Scaffold affinity normalisation2 for {0}'.format(p_name_chain))
    #plt.show()
    plt.savefig('{1}/{0}_scaffold_aff_dis_NORMAL2.png'.format(p_name_chain, directory4))
