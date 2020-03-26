# coding: utf-8

import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np
import sys


class Csv:
    def __init__(self):

        #create arguments

        self.parser = argparse.ArgumentParser()

        self.commandType = self.parser.add_mutually_exclusive_group(required=True)

        self.commandType.add_argument("-f", "--file", type=str, nargs=1,
                                 help="Select a csv file")

        self.parser.add_argument("-show", action="store_true", required = False,
                            help= "Show the plots figure")

        self.parser.add_argument("-save", action="store_true", required = False,
                                help= "Save the plot figure in a .png file in the current path")

        self.parser.add_argument("-all", action="store_true", required = False,
                                help= "Plot the entire file")

        self.parser.add_argument("-line", action="store_true", required = False,
                                        help= "Plot lines between dots")

        self.parser.add_argument("-t","--target", type=float, nargs=2, required = False,
                                        help= "Target position (x,y) and plot it")


        self.args = self.parser.parse_args()

        if self.args.file[0][-4:] != '.csv' :
            print("Error: Not a .csv file")
            sys.exit()



    def divisioncsv(self):
        global isBall
        global isState

        ##initialized variables
        if self.args.file:
            self.path= self.args.file[0]
            #print(self.path)


        flag = 0
        tmp = []
        self.nbTrajectories = 1
        totalLine = 0
        lineNumber = 0
        newTrajectorie = True
        header = ''
        timeShoot = 0.0
        newBallPos = False

        ##open the csv file to be treated

        input = open(self.path,'r')
        reader = csv.reader(input, delimiter=',')
        header = (next(reader)) #memorize the header and go the next line

        if "pos_robotX" in header and "pos_robotY" in header :
            self.indexRobotX = header.index("pos_robotX")
            self.indexRobotY = header.index("pos_robotY")
        else :
            print("Error: Wrong header")
            sys.exit()

        if 'state' in header:
            isState = True
            self.indexApprochState = header.index("state")
        if 'approach_state' in header:
            isState = True
            self.indexApprochState = header.index("approach_state")
        if 'pos_ballX' in header:
            isBall = True
            self.indexBallX = header.index("pos_ballX")
            self.indexBallY = header.index("pos_ballY")


        ##loop for each line in the csv file
        for line in reader:
            lineNumber+=1
            if float(line[self.indexRobotX]) < 0.0 :
                line[self.indexRobotX] = str(abs(float(line[self.indexRobotX])))
            if 'position' in self.path:
                #print(line)
                line[self.indexRobotY] = str(-1.0*float(line[self.indexRobotY]))

            if newBallPos == False :

                #change approach_state strings to integer
                if 'approach_state' in header:
                    if line[self.indexApprochState] == 'stopping':
                        line[self.indexApprochState] = float(0)
                    if line[self.indexApprochState] == 'place':
                        line[self.indexApprochState] = float(1)
                    if line[self.indexApprochState] == 'shoot':
                        line[self.indexApprochState] = float(2)

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
                            #print("ligne au temps t ="+str(tmp[0])+ " ajoutée." )
                        else:
                            tmp = line
                            writer.writerow((line))
                            #print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                        flag = 1

                # if  isBall == True:
                #     if float(line[self.indexBallX]) != float(tmp[self.indexBallX]) or float(line[self.indexBallY])!= float(tmp[self.indexBallY]):
                #         newBallPos = True


                ##copy the current line in the new csv file if diff posX > 0.03 and < 2
                if self.args.all:
                    writer = csv.writer(output, lineterminator='\n')
                    writer.writerow((line))
                    #print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                    tmp = line
                else:
                    if abs(float(line[self.indexRobotX])-float(tmp[self.indexRobotX])) >= 0.03 and abs(float(line[self.indexRobotX])-float(tmp[self.indexRobotX])) < 2 or newBallPos == True:
                        writer = csv.writer(output, lineterminator='\n')
                        writer.writerow((line))
                        #print("ligne au temps t ="+str(line[0])+ " ajoutée." )
                        tmp = line
                print ("")
                ##if diff PosX > 2, condition is ok to create a new csv file and copy the current line
                if abs(float(line[self.indexRobotX])-float(tmp[self.indexRobotX])) >= 2 :
                    print("new")
                    tmp = line
                    self.nbTrajectories+=1
                    newTrajectorie = True
                    flag=0




        input.close()
        output.close()
        if lineNumber <= 20 :
            print("Warning: The csv file contains just "+ str(lineNumber) + " lines of data.")


    def plots(self):
        global isBall
        global isState
    ### plots
        if self.args.save or self.args.show:


            maxX, minX, maxY, minY = [], [], [], []
            i=1


            while i <= self.nbTrajectories:
                if isBall == True:
                    BallX,BallY = [],[]
                RobotX,RobotY = [],[]
                if isState == True:
                    RobotXStop, RobotXPlace, RobotXShoot = [],[],[]
                    RobotYStop, RobotYPlace, RobotYShoot = [],[],[]
                csvfile = open(self.path[:-4]+'-'+ str(i) +'.csv','r')
                plots = csv.reader(csvfile, delimiter=',')
                next((plots))

                lines = [list(map(float, line)) for line in plots]
                for line in lines:
                    if isState == True :
                        if line[self.indexApprochState] == 0:
                            RobotXStop.append(line[self.indexRobotX])
                            RobotYStop.append(line[self.indexRobotY])

                        if line[self.indexApprochState] == 1:
                            RobotXPlace.append(line[self.indexRobotX])
                            RobotYPlace.append(line[self.indexRobotY])
                            #print (RobotXPlace)

                        if line[self.indexApprochState] == 2:
                            RobotXShoot.append(line[self.indexRobotX])
                            RobotYShoot.append(line[self.indexRobotY])

                    RobotX.append(line[self.indexRobotX])
                    RobotY.append(line[self.indexRobotY])
                    #print (str(line[self.indexRobotX])+' , '+str(line[self.indexRobotX]))

                    if isBall == True:
                        BallX.append(abs(line[self.indexBallX]))
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
                    else:
                        maxX.append(line[self.indexRobotX])
                        maxY.append(line[self.indexRobotY])
                        minX.append(line[self.indexRobotX])
                        minY.append(line[self.indexRobotY])

                plt.figure()
                plt.xlabel('x')
                plt.ylabel('y')
                axes = plt.axes()
                axes.set_ylim([-1.5,1.5])
                axes.set_yticks([-1,0,1])
                axes.set_xlim([-0.5,3.5])

                axes.set_xticks([0,1,2,3])
                plt.title('Trajectories')


                if self.args.line:
                    plt.plot(RobotX,RobotY,label ='Robot')
                else:
                    plt.plot(RobotX,RobotY,'r.',label ='Robot')

                if isBall == True:
                    plt.plot(BallX,BallY,'.', label = 'Ball')

                if self.args.target :
                    plt.plot(self.args.target[0],self.args.target[1],'b*', label = 'Target')

                plt.legend()

                if self.args.save:
                    plt.savefig(self.path[:-4]+'-'+ str(i) +'.png')

                if self.args.show:
                    plt.show()

                i+=1


            # print('borne en x: [' + str(min(minX)) + ' , ' + str(max(maxX)) + ']')
            # print('borne en y: [' + str(min(minY)) + ' , ' + str(max(maxY)) + ']')


            # axes.set_ylim([min(minY)-0.2,max(maxY)+0.2])
            # axes.set_yticks([min(minY),0,max(maxY)])
            # axes.set_xlim([min(minX)-0.2,max(maxX)+0.2])
            # axes.set_xticks([min(minX),min(minX)/2,max(maxX)/2,max(maxX)])

            # axes.set_ylim([-5,5])
            # axes.set_yticks([-4,0,4])
            # axes.set_xlim([-5,5])
            # axes.set_xticks([-4,0,4])




            #plt.plot(RobotXStop,RobotYStop,'g.',label ='Robot Stop')
            # if isState == True :
            #     plt.plot(RobotXPlace,RobotYPlace,'y.',label ='Robot Place')
            #     plt.plot(RobotXShoot,RobotYShoot,'r.',label ='Robot Shoot')
            # else :
            # if self.args.line:
            #     plt.plot(RobotX,RobotY,'r',label ='Robot')
            # else:
            #     plt.plot(RobotX,RobotY,'r.',label ='Robot')
            #
            # if isBall == True:
            #     plt.plot(BallX,BallY,'k.', label = 'Ball')
            # plt.legend()
        #
        # if self.args.save:
        #
        #     plt.savefig(self.path[:-4]+'.png')
        #
        # if self.args.show:
        #     plt.show()

isBall = False
isState = False
prgm = Csv()
prgm.divisioncsv()
prgm.plots()

    ############
    ##debugger
    #
    # if __name__ == "__main__":
    #     main()
