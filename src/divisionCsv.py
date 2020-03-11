# coding: utf-8

import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
import sys

class Csv:
    isBall = False
    def __init__(self):

        #create arguments

        self.parser = argparse.ArgumentParser()

        self.commandType = self.parser.add_mutually_exclusive_group(required=True)

        self.commandType.add_argument("-f", "--file", type=str, nargs=1,
                                 help="Select a file")

        self.parser.add_argument("-show", action="store_true", required = False,
                            help= "Show the plots figure")

        self.parser.add_argument("-save", action="store_true", required = False,
                                help= "Save the plot figure in a .png file in the current path")

        self.args = self.parser.parse_args()

        if self.args.file[0][-4:] == '.csv':
            print("File selected: " + self.args.file[0])
        else :
            print("Error: Not a .csv file")
            sys.exit()


    def divisioncsv(self):

        ##initialized variables
        self.path = self.args.file[0]
        date = datetime.datetime.now()
        flag = 0
        tmp = []
        self.nbTrajectories = 1
        totalLine = 0
        lineNumber = 1
        newTrajectorie = True
        header = ''
        timeShoot = 0.0
        strDate = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '-' + str(date.hour) + 'h' + str(date.minute) + 'm' + str(date.second) + 's'
        newBallPos = False
        ##open the csv file to be treated
        input = open(self.path,'r')
        reader = csv.reader(input, delimiter=',')
        header = (next(reader)) #memorize the header and go the next line

        self.indexRobotX = header.index("pos_robotX")
        self.indexRobotY = header.index("pos_robotY")
        self.indexApprochState = header.index("state")
        if 'pos_ballX' in header:
            isBall = True
            self.indexBallX = header.index("pos_ballX")
            self.indexBallY = header.index("pos_ballY")


        ##loop for each line in the csv file
        for line in reader:

            if newBallPos == False :

                # #change approach_state strings to integer
                # if line[self.indexApprochState] == 'stopping':
                #     line[self.indexApprochState] = float(0)
                # if line[self.indexApprochState] == 'place':
                #     line[self.indexApprochState] = float(1)
                # if line[self.indexApprochState] == 'shoot':
                #     line[self.indexApprochState] = float(2)

                ##condition to create a new csv file
                if newTrajectorie == True:
                    output = open(self.path[:-4]+'-'+ str(self.nbTrajectories) +'.csv','w')
                    writer = csv.writer(output, delimiter=',')
                    writer.writerow((header))
                    newTrajectorie = False
                    ##condition for memorize the first line to initialize the comparision
                    if flag == 0:
                        if self.nbTrajectories > 1:
                            writer.writerow((tmp))
                            print("ligne au temps t ="+str(tmp[0])+ " ajoutée." )
                        else:
                            tmp = line
                            writer.writerow((line))
                            print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                        flag = 1

                if float(line[self.indexBallX]) != float(tmp[self.indexBallX]) or float(line[self.indexBallY])!= float(tmp[self.indexBallY]):
                    newBallPos = True


                ##copy the current line in the new csv file if diff posX > 0.03 and < 2
                if abs(float(line[self.indexRobotX])-float(tmp[self.indexRobotX])) >= 0.03 and abs(float(line[1])-float(tmp[1])) < 2 or newBallPos == True:
                    writer = csv.writer(output, lineterminator='\n')
                    writer.writerow((line))
                    print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                    tmp = line

                ##if diff PosX > 2, condition is ok to create a new csv file and copy the current line
                if abs(float(line[self.indexRobotX])-float(tmp[self.indexRobotX])) >= 2 :
                    tmp = line
                    self.nbTrajectories+=1
                    newTrajectorie = True
                    flag=0



        input.close()
        output.close()


    def plots(self):

        if self.args.save or self.args.show:
            ### plots

            RobotX,RobotY,BallX,BallY = [],[],[],[]
            RobotXStop, RobotXPlace, RobotXShoot = [],[],[]
            RobotYStop, RobotYPlace, RobotYShoot = [],[],[]

            maxX, minX, maxY, minY = [], [], [], []
            i=1


            while i <= self.nbTrajectories:
                csvfile = open(self.path[:-4]+'-'+ str(i) +'.csv','r')
                plots = csv.reader(csvfile, delimiter=',')
                next((plots))

                lines = [list(map(float, line)) for line in plots]
                for line in lines:
                    print(line)
                    print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                    if line[self.indexApprochState] == 0:
                        RobotXStop.append(line[self.indexRobotX])
                        RobotYStop.append(line[self.indexRobotY])

                    if line[self.indexApprochState] == 1:
                        RobotXPlace.append(line[self.indexRobotX])
                        RobotYPlace.append(line[self.indexRobotY])

                    if line[self.indexApprochState] == 2:
                        RobotXShoot.append(line[self.indexRobotX])
                        RobotYShoot.append(line[self.indexRobotY])

                    RobotX.append(line[self.indexRobotX])
                    RobotY.append(line[self.indexRobotY])
                    BallX.append(line[self.indexBallX])
                    BallY.append(line[self.indexBallY])

                    if line[self.indexRobotX] > line[self.indexBallX] :
                        maxX.append(line[self.indexRobotX])
                        minX.append(line[self.indexBallX])
                    else:
                        maxX.append(line[self.indexBallX])
                        minX.append(line[self.indexRobotX])

                    if line[self.indexRobotY] > line[self.indexBallY] :
                        maxY.append(line[self.indexRobotY])
                        minY.append(line[self.indexBallY])
                    else:
                        maxY.append(line[self.indexBallY])
                        minY.append(line[self.indexRobotY])
                i+=1


            # print('borne en x: [' + str(min(minX)) + ' , ' + str(max(maxX)) + ']')
            # print('borne en y: [' + str(min(minY)) + ' , ' + str(max(maxY)) + ']')

            plt.xlabel('x')
            plt.ylabel('y')
            axes = plt.axes()
            axes.set_ylim([min(minY)-0.2,max(maxY)+0.2])
            axes.set_yticks([min(minY),0,max(maxY)])
            axes.set_xlim([min(minX)-0.2,max(maxX)+0.2])
            axes.set_xticks([min(minX),min(minX)/2,max(maxX)/2,max(maxX)])

            # axes.set_ylim([-5,5])
            # axes.set_yticks([-4,0,4])
            # axes.set_xlim([-5,5])
            # axes.set_xticks([-4,0,4])

            plt.title('Trajectories')


            #plt.plot(RobotXStop,RobotYStop,'g.',label ='Robot Stop')
            plt.plot(RobotXPlace,RobotYPlace,'y.',label ='Robot Place')
            plt.plot(RobotXShoot,RobotYShoot,'r.',label ='Robot Shoot')
            plt.plot(BallX,BallY,'k.', label = 'Ball')
            plt.legend()

        if self.args.save:

            plt.savefig(self.path[:-4]+'.png')



        if self.args.show:
            plt.show()


programme = Csv()
programme.divisioncsv()
programme.plots()

    ############
    ##debugger
    #
    # if __name__ == "__main__":
    #     main()
