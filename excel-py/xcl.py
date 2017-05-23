#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 23:38:36 2017

@author: Aretas
"""

##a script to create .xlsx file with a separate sheet for each enzyme

## input1: a file with a list of substrates used for docking;
## input2: a folder with .txt files for each enzyme docking results
## from input2 list all the scaffold/product numbers in colA and score in colC
## from input1 list the names of the products in colB
## write fields for min/max/sd values; name of the enzyme (get it from input2 file name)
## trends

import re, argparse
import xlsxwriter
import collections

#input1 = open (sys.argv[1]).readlines()
#input2 = open (sys.argv[2]).readlines()

parser = argparse.ArgumentParser()
parser.add_argument('-f1', '--file1',
    help='choose the list of MD ligands', required=True)
parser.add_argument('-f2', '--file2',
    help='choose aff_dis.txt', required=True)

args = parser.parse_args()
input1 = open(args.file1).readlines()
input2 = open(args.file2).readlines()

input1_dict = {}
input2_dict = {}
number_of_products = 1

for line in input1:
    f = line.split()
    number = f[0]
    name = f[2]
    number_of_products += 1
    input1_dict[int(number)] = name
    
    
for line in input2:
    f = line.split()
    input2_dict[int(f[0])] = 0 - float(f[1])

m_obj = re.search(r'(.*)_NS_(.*).txt', args.file2)
if m_obj:
    enzyme_name = m_obj.groups()[0]


workbook = xlsxwriter.Workbook("MD_NatPro.xlsx")
worksheet = workbook.add_worksheet(enzyme_name.upper())

bold = workbook.add_format ({'bold' : True})
chart = workbook.add_chart({'type': 'column'})

chart.add_series({'values': '={0}!$C$2:$C${1}'.format(enzyme_name.upper(), number_of_products)})
chart.set_y_axis({'min': 4.5})
worksheet.insert_chart('F8', chart)

worksheet.write('A1', 'Number', bold)
worksheet.write('B1', 'Name', bold)
worksheet.write('C1', 'Top score', bold)

worksheet.set_column('B:B', 18)

row = 1
col = 0

od = collections.OrderedDict(sorted(input2_dict.items()))
for k, v in od.items():
    #print (k,v)
    worksheet.write(row, col, k)
    worksheet.write(row, col + 2, input2_dict[k])
    worksheet.write_string(row, col + 1, input1_dict[k])
    row += 1
    
worksheet.write('F2', enzyme_name.upper())
worksheet.write('F3', 'min')
worksheet.write('F4', 'max')
worksheet.write('F5', 'sd')
worksheet.write('G3', '=MIN(C2:C{0})'.format(number_of_products))
worksheet.write('G4', '=MAX(C2:C{0})'.format(number_of_products))
worksheet.write('G5', '=STDEV(C2:C{0})'.format(number_of_products))

workbook.close()