# coding: utf-8

import argparse
import matplotlib.pyplot as plt
import csv
import sys
import os
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

        if 'approach' not in self.args.files[0] or 'position' not in self.args.files[1]:
            print("Error: File 1 must be approach file\n File 2 must be position file")


    def compareplots(self):
        self.paths=self.args.files
        numFile = 1
        plt.xlabel('x')
        plt.ylabel('y')
        axes = plt.axes()
        axes.set_ylim([-1.5,1.5])
        axes.set_yticks([-1,0,1])
        axes.set_xlim([-0.5,3.5])
        axes.set_xticks([0,1,2,3])
        plt.title('Trajectories')

        for path in self.paths:
            csvfile = open(path,'r')
            plots = csv.reader(csvfile, delimiter=',')
            header =next((plots))
            indexRobotX = header.index("pos_robotX")
            indexRobotY = header.index("pos_robotY")
            if 'pos_ballX' in header:
                self.indexBallX = header.index("pos_ballX")
                self.indexBallY = header.index("pos_ballY")
                BallX, BallY = [],[]
            RobotX, RobotY = [],[]
            lines = [list(map(float, line)) for line in plots]

            for line in lines:

                RobotX.append(line[indexRobotX])
                RobotY.append(line[indexRobotY])
                if 'pos_ballX' in header:
                    print(line[self.indexBallX])
                    print(line[self.indexBallY])
                    BallX.append(line[self.indexBallX])
                    BallY.append(line[self.indexBallY])
            plt.plot(RobotX,RobotY,label =os.path.basename(path))
            if 'pos_ballX' in header:
                plt.plot(BallX,BallY,'.',label ='Ball')





            numFile+=1
        plt.legend()
        plt.savefig(str(self.paths[0][:-4])+'-compare.png')
        plt.show()


















prgm = ComparePlots()
prgm.compareplots()
