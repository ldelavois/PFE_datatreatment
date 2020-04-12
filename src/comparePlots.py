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

        self.parsercompare.add_argument("-t","--target", type=float, nargs=2, required = False,
                                                help= "Target position (x,y) and plot it")

        self.args = self.parsercompare.parse_args()
        
        ##check if the two inputs are csv files
        if self.args.files[0][-4:] != '.csv':
            print("Error: File 1 is not a .csv file")
            sys.exit()

        if self.args.files[1][-4:] != '.csv':
            print("Error: File 2 is not a .csv file")
            sys.exit()
            
        #check if input 1 is approach and input 2 is position
        if 'approach' not in self.args.files[0] or 'position' not in self.args.files[1]:
            print("Error: File 1 must be approach file\n File 2 must be position file")
            sys.exit()


    def compareplots(self):
        self.paths=self.args.files
        
        ##initialize the plot figure with labels and fixes axes
        plt.xlabel('x')
        plt.ylabel('y')
        axes = plt.axes()
        axes.set_ylim([-1.5,1.5])
        axes.set_yticks([-1,0,1])
        axes.set_xlim([-0.5,3.5])
        axes.set_xticks([0,1,2,3])
        plt.title('Trajectories')
        
        ##for each file
        for path in self.paths:
            csvfile = open(path,'r')
            plots = csv.reader(csvfile, delimiter=',')
            header =next((plots))
            indexRobotX = header.index("pos_robotX")
            indexRobotY = header.index("pos_robotY")
            
            #check if there are ball positions
            if 'pos_ballX' in header:
                self.indexBallX = header.index("pos_ballX")
                self.indexBallY = header.index("pos_ballY")
                BallX, BallY = [],[]
                
            RobotX, RobotY = [],[]
            lines = [list(map(float, line)) for line in plots]
            
            ##add position for each line in the csv file
            for line in lines:

                RobotX.append(line[indexRobotX])
                RobotY.append(line[indexRobotY])
                if 'pos_ballX' in header:
                    BallX.append(line[self.indexBallX])
                    BallY.append(line[self.indexBallY])
            ##check the current treated file for the associated label
            if 'approach' in path:
                plt.plot(RobotX,RobotY,label='Approach')
            else:
                plt.plot(RobotX,RobotY,label='Vive')
            #if 'pos_ballX' in header:
                #plt.plot(BallX,BallY,'.',label ='Ball')
        if self.args.target:
            plt.plot(self.args.target[0],self.args.target[1],'*', label = 'Target')
            
        plt.legend()
        plt.savefig(str(self.paths[0][:-4])+'-compare.png')
        plt.show()


## main
prgm = ComparePlots()
prgm.compareplots()
