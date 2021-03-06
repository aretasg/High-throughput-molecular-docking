#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 01:48:17 2017

@author: Aretas
"""
#Export Linear MD results to xlsx
import re
import argparse
import os
import xlsxwriter
import collections
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',
    help='choose the list of MD enzymes (should be a .csv file)', required=True)
parser.add_argument('-f2', '--file2',
    help='choose the TXT file with the list of ligands', required=True)
parser.add_argument('-lo', '--location',
    help='choose MD results containing folder', required=True)

args = parser.parse_args()
location = args.location

workbook = xlsxwriter.Workbook("MD_Linear_pho.xlsx")#####!!!!!!!

ligand_dict = {} #skeleton number in the lib : type of the skeleton
ligand_counter = 0
with open(args.file2) as f:
    for line in f:
        k = line.split()
        ligand_dict[int(k[0])] = k[2]
        ligand_counter += 1

input1_dict = {}
number_of_products = ligand_counter + 1

results_loc = os.path.realpath(args.location)
file_path = results_loc + "/aff_dis/"

with open(args.file) as f:
    csv_dict = [{k: str(v) for k, v in row.items()}
         for row in csv.DictReader(f, skipinitialspace=True)]

mean_line = ""

worksheet1 = workbook.add_worksheet('mean')
input2_dict = {}

for txt_aff in os.listdir(file_path):

    if txt_aff.endswith("aff_dis.txt"):
        completeName = os.path.join(file_path,"{0}".format(txt_aff))

        with open(completeName) as input2:
            for line in input2:
                f = line.split()
                input2_dict[f[0]] = 0 - float(f[1])

        m_obj = re.search(r'(.*)_NS_pho_(.*)_scaffold_aff_dis.txt', txt_aff)
        m_obj1 = re.search(r'(.*)_NS_(.*)_scaffold_aff_dis.txt', txt_aff)
        if m_obj:
            enzyme_name = m_obj.groups()[0]
            chain = m_obj.groups()[1]
        if m_obj1:
            enzyme_name = m_obj1.groups()[0]
            chain = m_obj.groups()[1]

        sheet_name = enzyme_name.upper() + "_" + chain
        sheet_name2 = "'" + sheet_name + "'" + '!C{0},'
        mean_line += sheet_name2

        worksheet = workbook.add_worksheet(sheet_name)

        bold = workbook.add_format ({'bold' : True})
        italic = workbook.add_format ({'italic' : True})
        chart = workbook.add_chart({'type': 'column'})
        chart1 = workbook.add_chart({'type': 'column'})


        chart.add_series({'values': '={0}!$C$2:$C${1}'.format(sheet_name, number_of_products)})
        chart.set_y_axis({'min': 4.0})
        worksheet.insert_chart('F12', chart)


        worksheet.write('A1', 'Scaffold Number', bold)
        worksheet.set_column('A:A', 14)

        worksheet.write('B1', 'Library number', bold)
        worksheet.write('C1', 'Top Score', bold)


        row = 1
        col = 0

        od = collections.OrderedDict(sorted(ligand_dict.items()))
        for k, v in od.items():
            worksheet.write(row, col, k)
            worksheet.write(row, col + 1, v)
            worksheet.write(row, col + 2, input2_dict[v])
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
            if dictionary["PDB_ID"] == enzyme_name or dictionary["PDB_ID"] == enzyme_name.upper() :
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
chart2 = workbook.add_chart({'type': 'column'})
chart3 = workbook.add_chart({'type': 'column'})

worksheet1.write('A1', 'Scaffold Number', bold)
worksheet1.set_column('A:A', 14)
worksheet1.write('B1', 'Library number', bold)
worksheet1.write('C1', 'Topology', bold)
worksheet1.write('D1', 'mean', bold)
worksheet1.write('E1', 'sd', bold)

row = 1
col = 0

od = collections.OrderedDict(sorted(ligand_dict.items()))
for k, v in od.items():
    worksheet1.write(row, col, k)
    worksheet1.write(row, col + 1, v)
    worksheet1.write(row, col + 2, "linear")
    row += 1

mean_line = mean_line[:-1]
a_mean_line = "=AVERAGE(" + mean_line + ")"
std_mean_line = "=STDEV(" + mean_line + ")"

#print (a_mean_line)
for i in range(2, number_of_products + 1):
    worksheet1.write('D{0}'.format(i), a_mean_line.format(i))
    worksheet1.write('E{0}'.format(i), std_mean_line.format(i))


worksheet1.write('I2', 'mean')
worksheet1.write('I3', 'min')
worksheet1.write('I4', 'max')
worksheet1.write('I5', 'sd')
worksheet1.write('J3', '=MIN(D2:D{0})'.format(number_of_products))
worksheet1.write('J4', '=MAX(D2:D{0})'.format(number_of_products))
worksheet1.write('J5', '=STDEV(D2:D{0})'.format(number_of_products))

chart.add_series({
                  'values': '={0}!$D$2:$D${1}'.format("mean", number_of_products),
                  'y_error_bars': {'type': 'standard_error'},
})
chart.set_y_axis({'min': 5.0})

worksheet1.insert_chart('I8', chart)


chart1.add_series({'values': '={0}!$C$2:$C${1}'.format("mean", number_of_products)})
chart1.set_y_axis({'min': 0.15})
worksheet1.insert_chart('I23', chart1)

workbook.close()
