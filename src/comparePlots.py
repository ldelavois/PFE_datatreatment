# coding: utf-8

import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
import sys
#import divisionCsv

class ComparePlots:
    def __init__(self):
        #create arguments

        self.parsercompare = argparse.ArgumentParser()

        self.commandType = self.parsercompare.add_mutually_exclusive_group(required=True)

        self.commandType.add_argument("-ff", "--files", type=str, nargs=2,
                                 help="Select two csv files")

        self.parsercompare.add_argument("-line", action="store_true", required = False,
                                        help= "Plot lines between dots")

        self.args = self.parsercompare.parse_args()

        if self.args.files[0][-4:] != '.csv':
            print("Error: File 1 is not a .csv file")
            sys.exit()

        if self.args.files[1][-4:] != '.csv':
            print("Error: File 2 is not a .csv file")
            sys.exit()

    def compareplots(self):
        self.paths=self.args.files
        numFile = 1
        plt.xlabel('x')
        plt.ylabel('y')
        axes = plt.axes()
        plt.title('Trajectories')

        for path in self.paths:
            csvfile = open(path,'r')
            plots = csv.reader(csvfile, delimiter=',')
            header =next((plots))
            indexRobotX = header.index("pos_robotX")
            indexRobotY = header.index("pos_robotY")
            RobotX, RobotY = [],[]
            lines = [list(map(float, line)) for line in plots]

            for line in lines:

                RobotX.append(line[indexRobotX])
                RobotY.append(line[indexRobotY])

            plt.plot(RobotX,RobotY,label ='File ' + str(numFile))
            numFile+=1
        plt.legend()
        plt.savefig('compare.png')
        plt.show()


















prgm = ComparePlots()
prgm.compareplots()
