#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 01:48:17 2017

@author: Aretas
"""

#Outputs MD_C_scaff_pho and MD_C_scaff (results) screening and conversion to the
#Excel sheets for furhter analysis
import re
import argparse
import os
import xlsxwriter
import collections
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file1',
    help='choose the list of MD enzymes (should be a .csv file)', required=True)
parser.add_argument('-f2', '--file2',
    help='choose the TXT file with the list of ligands', required=True)
parser.add_argument('-lo', '--location',
    help='choose the MD results folder', required=True)

args = parser.parse_args()
ligand_input = args.file2
location = args.location

workbook = xlsxwriter.Workbook("MD_Cyclic_pho.xlsx") #the name of the excel file
#Iteration over ligand list e.g. cyclic_list.txt
ligand_dict = {} #skeleton number in the lib : type of the skeleton
ligand_counter = 0
with open(ligand_input) as f:
    for line in f:
        k = line.split("|")
        ligand_dict [int(k[0])] = k[2]
        ligand_counter += 1

input1_dict = {}
number_of_products = ligand_counter + 1

results_loc = os.path.realpath(args.location)
file_path = results_loc + "/aff_dis/"
file_path2 = results_loc + "/aff_dis_norm/"
file_path3 = results_loc + "/aff_dis_norm2/"

#Extracting relavent information from protein CSV file
with open(args.file1) as f:
    csv_dict = [{k: str(v) for k, v in row.items()}
         for row in csv.DictReader(f, skipinitialspace=True)]

mean_line = ""   #create a excel formula to calculate the mean
mean_line2 = ""
mean_line3 = ""

worksheet1 = workbook.add_worksheet('mean')

for txt_aff in os.listdir(file_path):
    if txt_aff.endswith("aff_dis.txt"):
        completeName = os.path.join(file_path,"{0}".format(txt_aff))
        with open(completeName) as input2:
            input2_dict = {}
            for line in input2:
                f = line.split()
                input2_dict[int(f[0])] = 0 - float(f[1])

        m_obj = re.search(r'(.*)_NS_pho_(.*)_scaffold_aff_dis.txt', txt_aff)
        m_obj1 = re.search(r'(.*)_NS_(.*)_scaffold_aff_dis.txt', txt_aff)
        if m_obj:
            enzyme_name = m_obj.groups()[0]
            chain = m_obj.groups()[1]
        if m_obj1:
            enzyme_name = m_obj1.groups()[0]
            chain = m_obj.groups()[1]

        sheet_name = enzyme_name.upper() + "_" + chain   #strings to calclate mean for mean sheet
        sheet_name2 = "'" + sheet_name + "'" + '!B{0},'
        sheet_name3 = "'" + sheet_name + "'" + '!C{0},'
        sheet_name4 = "'" + sheet_name + "'" + '!D{0},'
        mean_line += sheet_name2
        mean_line2 += sheet_name3
        mean_line3 += sheet_name4

#normalisation
        norm_file_name = txt_aff[:-4] + "_NORM.txt"
        completeName2 = os.path.join(file_path2,"{0}".format(norm_file_name))
        input3_dict = {}
        with open(completeName2) as input3:
            for line in input3:
                f = line.split()
                input3_dict[int(f[0])] = float(f[1]) # skeleton number : affinity

#normalisation2
        norm_file_name2 = txt_aff[:-4] + "_NORM2.txt"
        completeName3 = os.path.join(file_path3,"{0}".format(norm_file_name2))
        input4_dict = {}
        with open(completeName3) as input4:
            for line in input4:
                f = line.split()
                input4_dict[int(f[0])] = float(f[1]) #skeleton number : affinity

        worksheet = workbook.add_worksheet(sheet_name)

        bold = workbook.add_format ({'bold' : True})
        italic = workbook.add_format ({'italic' : True})
        chart = workbook.add_chart({'type': 'column'})
        chart1 = workbook.add_chart({'type': 'column'})
        chart2 = workbook.add_chart({'type': 'column'})


        chart.add_series({'values': '={0}!$B$2:$B${1}'.format(sheet_name, number_of_products)})
        #chart.set_y_axis({'min': 2.5})
        worksheet.insert_chart('H12', chart)

        chart1.add_series({'values': '={0}!$C$2:$C${1}'.format(sheet_name, number_of_products)})
        #chart1.set_y_axis({'min': 0.4})

        worksheet.insert_chart('H33', chart1)

        chart2.add_series({'values': '={0}!$D$2:$D${1}'.format(sheet_name, number_of_products)})
        worksheet.insert_chart('N12',chart2)

        worksheet.write('C1', 'Normalisation score', bold)
        worksheet.set_column('C:C', 18)

        worksheet.write('A1', 'Scaffold Number', bold)
        worksheet.set_column('A:A', 14)

        worksheet.write('B1', 'Top Score', bold)
        worksheet.write('D1', 'Normalisation2', bold)
        worksheet.set_column('D:D', 14)
        worksheet.write('E1', 'Carbons', bold)
        worksheet.write('F1', 'Toplogy', bold)
        worksheet.set_column('F:F', 20)


        row = 1
        col = 0

        od = collections.OrderedDict(sorted(input2_dict.items()))
        for k, v in od.items():
            worksheet.write(row, col, k)
            worksheet.write(row, col + 1, input2_dict[k])
            worksheet.write(row, col + 2, input3_dict[k])
            worksheet.write(row, col + 3, input4_dict[k])
            worksheet.write(row, col + 4, input2_dict[k]/input3_dict[k])
            worksheet.write(row, col + 5, ligand_dict[k])
            row += 1


        #worksheet.write('F2', enzyme_name.upper())
        worksheet.write('H2', 'Top score')
        worksheet.write('H3', 'min')
        worksheet.write('H4', 'max')
        worksheet.write('H5', 'sd')
        worksheet.write('I3', '=MIN(B2:B{0})'.format(number_of_products))
        worksheet.write('I4', '=MAX(B2:B{0})'.format(number_of_products))
        worksheet.write('I5', '=STDEV(B2:B{0})'.format(number_of_products))

        worksheet.write('H28', 'Top score normalisation')
        worksheet.write('H29', 'min')
        worksheet.write('H30', 'max')
        worksheet.write('H31', 'sd')
        worksheet.write('I29', '=MIN(C2:C{0})'.format(number_of_products))
        worksheet.write('I30', '=MAX(C2:C{0})'.format(number_of_products))
        worksheet.write('I31', '=STDEV(C2:C{0})'.format(number_of_products))

        for dictionary in csv_dict:
            if dictionary["PDB_ID"] == enzyme_name or dictionary["PDB_ID"] == enzyme_name.upper():
                worksheet.write('H7', 'Enzyme name')
                worksheet.write('I7', 'PDB ID')
                worksheet.write('J7', 'Native product', bold)
                worksheet.write('K7', 'Chain')
                worksheet.write('L7', 'Ligand in crystal')
                worksheet.write('M7', 'Conformation')
                worksheet.write('N7', 'Resolution (A)')
                worksheet.set_column('N:N', 12)
                worksheet.write('O7', 'Species')

                worksheet.write('H8', dictionary["Enzyme_name"])
                worksheet.set_column('G:G', 25)
                worksheet.write('I8', dictionary['PDB_ID'])
                worksheet.write('J8', dictionary['Product'])
                worksheet.set_column('J:J', 20)
                worksheet.write('K8', chain)
                worksheet.write('L8', dictionary['Ligand_crystal'])
                worksheet.set_column('L:L', 18)
                worksheet.write('M8', dictionary['Conformation'])
                worksheet.write('N8', dictionary['Resolution'])
                worksheet.write('O8', dictionary['Species'], italic)
                worksheet.set_column('O:O', 18)

### MEAN SHEET


bold = workbook.add_format ({'bold' : True})
italic = workbook.add_format ({'italic' : True})
chart = workbook.add_chart({'type': 'column'})
chart1 = workbook.add_chart({'type': 'column'})
chart2 = workbook.add_chart({'type': 'column'})
chart3 = workbook.add_chart({'type': 'column'})
chart4 = workbook.add_chart({'type': 'column'})


worksheet1.write('A1', 'Scaffold Number', bold)
worksheet1.set_column('A:A', 14)
worksheet1.write('B1', 'Topology', bold)
worksheet1.write('C1', 'mean', bold)
worksheet1.write('D1', 'sd', bold)
worksheet1.write('F1', 'mean_norm', bold)
worksheet1.set_column('F:F', 12)
worksheet1.write('G1', 'sd_norm', bold)
worksheet1.write('I1', 'mean_norm2', bold)
worksheet1.write('J1', 'sd_norm2', bold)


row = 1
col = 0

od = collections.OrderedDict(sorted(input1_dict.items()))
for i in range(1, number_of_products):
    worksheet1.write(row, col, i)
    worksheet1.write(row, col + 1, ligand_dict[i])
    row += 1

mean_line = mean_line[:-1]
a_mean_line = "=AVERAGE(" + mean_line + ")"
std_mean_line = "=STDEV(" + mean_line + ")"

mean_line2 = mean_line2[:-1]
a_mean_line2 = "=AVERAGE(" + mean_line2 + ")"
std_mean_line2 = "=STDEV(" + mean_line2 + ")"

mean_line3 = mean_line3[:-1]
a_mean_line3 = "=AVERAGE(" + mean_line3 + ")"
std_mean_line3 = "=STDEV(" + mean_line3 + ")"


for i in range(2, number_of_products + 1):
    worksheet1.write('C{0}'.format(i), a_mean_line.format(i))
    worksheet1.write('D{0}'.format(i), std_mean_line.format(i))
    worksheet1.write('F{0}'.format(i), a_mean_line2.format(i))
    worksheet1.write('G{0}'.format(i), std_mean_line2.format(i))
    worksheet1.write('I{0}'.format(i), a_mean_line3.format(i))
    worksheet1.write('J{0}'.format(i), std_mean_line3.format(i))



worksheet1.write('L2', 'mean')
worksheet1.write('L3', 'min')
worksheet1.write('L4', 'max')
worksheet1.write('L5', 'sd')
worksheet1.write('M3', '=MIN(C2:C{0})'.format(number_of_products))
worksheet1.write('M4', '=MAX(C2:C{0})'.format(number_of_products))
worksheet1.write('M5', '=STDEV(C2:C{0})'.format(number_of_products))

worksheet1.write('T2', 'mean_norm')
worksheet1.write('T3', 'min')
worksheet1.write('T4', 'max')
worksheet1.write('T5', 'sd')
worksheet1.write('U3', '=MIN(F2:F{0})'.format(number_of_products))
worksheet1.write('U4', '=MAX(F2:F{0})'.format(number_of_products))
worksheet1.write('U5', '=STDEV(F2:F{0})'.format(number_of_products))

chart.add_series({
                  'values': '={0}!$C$2:$C${1}'.format("mean", number_of_products),
                  'y_error_bars': {'type': 'standard_error'},
})
chart.set_y_axis({'min': 2.4})

worksheet1.insert_chart('K8', chart)

##########
chart1.add_series({'values': '={0}!$D$2:$D${1}'.format("mean", number_of_products)})
#chart1.set_y_axis({'min': 0.03})
worksheet1.insert_chart('K23', chart1)
#########
#normalisation
chart2.add_series({
                  'values': '={0}!$F$2:$F${1}'.format("mean", number_of_products),
                  'y_error_bars': {'type': 'standard_error'},
})

#chart2.set_y_axis({'min': 0.5})

worksheet1.insert_chart('S8', chart2)

##########
chart3.add_series({'values': '={0}!$G$2:$G${1}'.format("mean", number_of_products)})
#chart3.set_y_axis({'min': 0.03})

worksheet1.insert_chart('S23', chart3)
#########
chart4.add_series({'values': '={0}!$I$2:$I${1}'.format("mean", number_of_products)})
worksheet1.insert_chart('K39', chart4)

workbook.close()
