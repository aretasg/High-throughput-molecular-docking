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

import re
import argparse
import xlsxwriter
import collections

parser = argparse.ArgumentParser()
parser.add_argument('-f2', '--file2',
    help='choose aff_dis.txt', required=True)

workbook = xlsxwriter.Workbook("MD_control_scaff_pho.xlsx")

args = parser.parse_args()
input2 = open(args.file2).readlines()

input1_dict = {}
input2_dict = {}
number_of_products = 1

with open(args.file2) as f:
    for line in f:
        k = line.split()
        input2_dict[int(k[0])] = 0 - float(k[1])

m_obj = re.search(r'(.*)_NS_pho_(.*)_scaffold_aff_dis.txt', txt_aff)
m_obj1 = re.search(r'(.*)_NS_(.*)_scaffold_aff_dis.txt', txt_aff)
if m_obj:
    enzyme_name = m_obj.groups()[0]
    chain = m_obj.groups()[1]
if m_obj1:
    enzyme_name = m_obj1.groups()[0]
    chain = m_obj.groups()[1]

worksheet = workbook.add_worksheet(enzyme_name.upper())

bold = workbook.add_format ({'bold' : True})
chart = workbook.add_chart({'type': 'column'})

chart.add_series({'values': '={0}!$C$2:$C${1}'.format(enzyme_name.upper(), number_of_products)})
chart.set_y_axis({'min': 4.5})
worksheet.insert_chart('F8', chart)

worksheet.write('A1', 'Number', bold)
worksheet.write('C1', 'Top score', bold)

row = 1
col = 0

od = collections.OrderedDict(sorted(input2_dict.items()))
for k, v in od.items():
    #print (k,v)
    worksheet.write(row, col, k)
    worksheet.write(row, col + 1, input2_dict[k])
    row += 1

worksheet.write('F2', enzyme_name.upper())
worksheet.write('F3', 'min')
worksheet.write('F4', 'max')
worksheet.write('F5', 'sd')
worksheet.write('G3', '=MIN(C2:C{0})'.format(number_of_products))
worksheet.write('G4', '=MAX(C2:C{0})'.format(number_of_products))
worksheet.write('G5', '=STDEV(C2:C{0})'.format(number_of_products))

### MEAN SHEET

bold = workbook.add_format ({'bold' : True})
italic = workbook.add_format ({'italic' : True})
chart = workbook.add_chart({'type': 'column'})
chart1 = workbook.add_chart({'type': 'column'})

worksheet1.write('A1', 'Number', bold)
worksheet1.write('D1', 'mean', bold)
worksheet1.write('E1', 'sd', bold)

row = 1
col = 0

od = collections.OrderedDict(sorted(input2_dict.items()))
for k, v in od.items():
    worksheet1.write(row, col, k)
    row += 1

mean_line = mean_line[:-1]
a_mean_line = "=AVERAGE(" + mean_line + ")"
std_mean_line = "=STDEV(" + mean_line + ")"
#print (a_mean_line)
for i in range(2, number_of_products + 1):
    worksheet1.write('D{0}'.format(i), a_mean_line.format(i))
    worksheet1.write('E{0}'.format(i), std_mean_line.format(i))
    #worksheet.write('D{0}'.format(i), "=AVERAGE('1N1Z_A'!C{0},'1N1Z_B'!C{0},'1N20_A'!C{0},'1N20_B'!C{0},'1N21_A'!C{0},'1N22_A'!C{0},'1N22_B'!C{0},'1N23_A'!C{0},'1N23_B'!C{0},'1N24_A'!C{0},'1N24_B'!C{0},'2ONG_A'!C{0},'2ONG_B'!C{0},'2ONH_A'!C{0},'2ONH_B'!C{0},'5UV1_A'!C{0},'5UV2_A'!C{0},BCINS_A!C{0},BCINS_B!C{0})".format(i))
    #worksheet.write('E{0}'.format(i), "=STDEV('1N1Z_A'!C{0},'1N1Z_B'!C{0},'1N20_A'!C{0},'1N20_B'!C{0},'1N21_A'!C{0},'1N22_A'!C{0},'1N22_B'!C{0},'1N23_A'!C{0},'1N23_B'!C{0},'1N24_A'!C{0},'1N24_B'!C{0},'2ONG_A'!C{0},'2ONG_B'!C{0},'2ONH_A'!C{0},'2ONH_B'!C{0},'5UV1_A'!C{0},'5UV2_A'!C{0},BCINS_A!C{0},BCINS_B!C{0})".format(i))

worksheet1.write('G2', 'mean')
worksheet1.write('G3', 'min')
worksheet1.write('G4', 'max')
worksheet1.write('G5', 'sd')
worksheet1.write('H3', '=MIN(D2:D{0})'.format(number_of_products))
worksheet1.write('H4', '=MAX(D2:D{0})'.format(number_of_products))
worksheet1.write('H5', '=STDEV(D2:D{0})'.format(number_of_products))

chart.add_series({
                  'values': '={0}!$D$2:$D${1}'.format("mean", number_of_products),
                  'y_error_bars': {'type': 'standard_error'},
})
chart.set_y_axis({'min': 4.5})
worksheet1.insert_chart('G8', chart)


chart1.add_series({'values': '={0}!$E$2:$E${1}'.format("mean", number_of_products)})
worksheet1.insert_chart('G23', chart1)

workbook.close()
