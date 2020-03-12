import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
import sys

class AbsValue:
    def __init__(self):
        #create arguments

        self.parsercompare = argparse.ArgumentParser()

        self.commandType = self.parsercompare.add_mutually_exclusive_group(required=True)

        self.commandType.add_argument("-f", "--file", type=str, nargs=1,
                                 help="Select csv file")

        self.args = self.parsercompare.parse_args()

        if self.args.file[-4:] != '.csv':
            print("Error: File is not a .csv file")
            sys.exit()

    def absvalue(self):
        self.path= self.args.file[0]
        input = open(self.path,'r')
        reader = csv.reader(input, delimiter=',')
        header = (next(reader))
        output = open(self.path[:-4]+'-signed.csv','w')
        writer = csv.writer(output, delimiter=',')
        writer.writerow((header))
        self.indexRobotX = header.index("pos_robotX")
        self.indexRobotY = header.index("pos_robotY")

        for line in reader:
