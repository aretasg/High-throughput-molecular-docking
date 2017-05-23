#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 01:48:17 2017

@author: Aretas
"""

import re, argparse, os
import xlsxwriter
import collections
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-f1', '--file1',
    help='choose the list of MD ligands', required=True)
parser.add_argument('-f2', '--file2',
    help='choose the list of MD enzymes (should be a .csv file)', required=True)
parser.add_argument('-lo', '--location',
    help='choose aff_dis.txt folder containing folder (should be in RP1)', required=True)

args = parser.parse_args()
input1 = open(args.file1).readlines()
input3 = open(args.file2).readlines()
location = args.location

input1_dict = {}
input1_dict_t = {}
number_of_products = 1

file_path = "/Users/Aretas/RP1/" + location + "/aff_dis/"
#print(file_path)

with open(args.file2) as f:
    csv_dict = [{k: str(v) for k, v in row.items()}
         for row in csv.DictReader(f, skipinitialspace=True)]



for line in input1:
    f = line.split()
    number = f[0]
    name = f[2]
    topology = f[4]
    number_of_products += 1
    input1_dict[int(number)] = name
    input1_dict_t[int(number)] = topology


workbook = xlsxwriter.Workbook("MD_NatPro.xlsx")#####!!!!!!!       
mean_line = ""    

worksheet1 = workbook.add_worksheet('mean')

for txt_aff in os.listdir(file_path):
    
    if txt_aff.endswith("aff_dis.txt"): 
        completeName = os.path.join(file_path,"{0}".format(txt_aff)) 
    
        input2_open = open(completeName)
        input2 = input2_open.readlines()
        input2_dict = {}
    
        for line in input2:
            f = line.split()
            input2_dict[int(f[0])] = 0 - float(f[1])
        
        m_obj = re.search(r'(.*)_NS_(.*)_scaffold_aff_dis.txt', txt_aff)  ###!!!!
        if m_obj:
            enzyme_name = m_obj.groups()[0]
            chain = m_obj.groups()[1]

        sheet_name = enzyme_name.upper() + "_" + chain
        sheet_name2 = "'" + sheet_name + "'" + '!C{0},'
        mean_line += sheet_name2

        worksheet = workbook.add_worksheet(sheet_name)

        bold = workbook.add_format ({'bold' : True})
        italic = workbook.add_format ({'italic' : True})
        chart = workbook.add_chart({'type': 'column'})

        chart.add_series({'values': '={0}!$C$2:$C${1}'.format(sheet_name, number_of_products)})
        chart.set_y_axis({'min': 4.5})
        worksheet.insert_chart('F12', chart)

        worksheet.write('A1', 'Number', bold)
        worksheet.write('B1', 'Name', bold)
        worksheet.write('C1', 'Top score', bold)

        worksheet.set_column('B:B', 18)

        row = 1
        col = 0

        od = collections.OrderedDict(sorted(input2_dict.items()))
        for k, v in od.items():
            worksheet.write(row, col, k)
            worksheet.write(row, col + 2, input2_dict[k])
            worksheet.write_string(row, col + 1, input1_dict[k])
            row += 1
        
        #worksheet.write('F2', enzyme_name.upper())
        worksheet.write('F2', 'Top score')
        worksheet.write('F3', 'min')
        worksheet.write('F4', 'max')
        worksheet.write('F5', 'sd')
        worksheet.write('G3', '=MIN(C2:C{0})'.format(number_of_products))
        worksheet.write('G4', '=MAX(C2:C{0})'.format(number_of_products))
        worksheet.write('G5', '=STDEV(C2:C{0})'.format(number_of_products))
        
        for dictionary in csv_dict:
            if dictionary["PDB_ID"] == enzyme_name or dictionary["PDB_ID"] == enzyme_name.upper():
                worksheet.write('F7', 'Enzyme name')
                worksheet.write('G7', 'PDB ID')
                worksheet.write('H7', 'Native product', bold)
                worksheet.write('I7', 'Chain')
                worksheet.write('J7', 'Ligand in crystal')
                worksheet.write('K7', 'Conformation')
                worksheet.write('L7', 'Resolution (A)')
                worksheet.set_column('L:L', 12)
                worksheet.write('M7', 'Species')
                
                worksheet.write('F8', dictionary["Enzyme_name"])
                worksheet.set_column('F:F', 25)
                worksheet.write('G8', dictionary['PDB_ID'])
                worksheet.write('H8', dictionary['Product'])
                worksheet.set_column('H:H', 20)
                worksheet.write('I8', chain)
                worksheet.write('J8', dictionary['Ligand_crystal'])
                worksheet.set_column('J:J', 18)
                worksheet.write('K8', dictionary['Conformation'])
                worksheet.write('L8', dictionary['Resolution'])
                worksheet.write('M8', dictionary['Species'], italic)
                worksheet.set_column('M:M', 18)

### MEAN SHEET


bold = workbook.add_format ({'bold' : True})
italic = workbook.add_format ({'italic' : True})
chart = workbook.add_chart({'type': 'column'})
chart1 = workbook.add_chart({'type': 'column'})

worksheet1.write('A1', 'Number', bold)
worksheet1.write('B1', 'Name', bold)
worksheet1.write('C1', 'Toplogy', bold)
worksheet1.write('D1', 'mean', bold)
worksheet1.write('E1', 'sd', bold)

worksheet1.set_column('B:B', 18)

row = 1
col = 0

od = collections.OrderedDict(sorted(input1_dict.items()))
for k, v in od.items():
    worksheet1.write(row, col, k)
    worksheet1.write(row, col + 2, input1_dict_t[k])  ####!!!!!
    worksheet1.write_string(row, col + 1, input1_dict[k])
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
    