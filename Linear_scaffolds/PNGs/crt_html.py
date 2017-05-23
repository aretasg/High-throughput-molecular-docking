#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 02:22:55 2017

@author: Aretas
"""

#create a html file with a basic list of linear images including 2D sketch;
#IUPAC name; chiral info and SMILES
#input linear_enantiomer_list.txt

import sys

dict1 = {}

with open("linear_list_images.html", "w") as html_open:

    html_open.write("<html>\n")
    html_open.write(" <head>\n")
    html_open.write("  <title></title>\n")
    html_open.write(" </head>\n")
    html_open.write("<body>\n")
    html_open.write("<table>\n")

    with open(sys.argv[1]) as file_in:
        for line in file_in:
            f = line.split()
            number = int(f[0])
            number_old = str(f[2])
            name = str(f[4])
            smiles = str(f[6])

            png_name = "scaffold_{}.svg.png".format(number_old)

            dict1[number] = "Scaffold number: " + str(number) + '''; Isomeric \
                number: ''' + number_old + "; SMILES: " + smiles

            html_open.write('''<tr><img src="{0}" style="width: 16%; height: 16%" \
                alt="text"> <p>{1}; {2}</p> </tr>\n'''.format(png_name, name, dict1[number]))

    html_open.write("</table>")
    html_open.write(" </body>")
    html_open.write("</html>")
