# coding: utf-8

import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime

epsilon = 0.03 #3cm
date = datetime.datetime.now()
flag = 0
tmp = []
strDate = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '-' + str(date.hour) + 'h' + str(date.minute) + 'm' + str(date.second) + 's'

with open('/home/ldelavois/Desktop/m2aspic/PFE/approach/nova/approach_status.csv','r') as input:
    with open('/home/ldelavois/Desktop/m2aspic/PFE/approach/nova/approach_status_' + strDate + '.csv','w') as output:
        reader = csv.reader(input, delimiter=',')
        output.write(next(input))
        writer = csv.writer(output)


        for line in reader:
            #print("ligne en cours: "+str(line)+'\n')
            if flag == 0:
                tmp = line
                writer.writeline((line))
                print("ligne au temps t ="+str(line[0])+ " ajoutée." )
            if abs(float(line[1])-float(tmp[1])) >= 0.03:
                writer = csv.writer(output, lineterminator='\n')
                writer.writeline((line))
                print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                tmp = line
            flag = 1


# with open('/home/ldelavois/Desktop/m2aspic/PFE/approach/nova/approach_status.csv','r') as input:
#     with open('/home/ldelavois/Desktop/m2aspic/PFE/approach/nova/approach_status_'+strDate,'w') as output:
#         reader = csv.reader(input, delimiter=',', lineterminator='\n')
#         next(reader, None)  # skip the headers
#         writer = csv.writer(output)
#
#         for line in reader:
#             if flag == 0:
#                 tmp = line
#             if abs(float(line[1])-float(tmp[1])) > 0.03:
#                 writer = csv.writer(output, lineterminator='\n')
#                 writer.writeline((line))
#             flag = 1
#             tmp = line
