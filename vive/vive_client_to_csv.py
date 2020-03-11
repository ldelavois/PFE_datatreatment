#!/usr/bin/env python
import csv

from vive_pb2 import *
import socket
from utils import *
from vive_provider import *
import time
from datetime import datetime

vp = Vive_provider(clientMode=True)
pathoutput = 'position'+datetime.now().strftime('-%Y-%m-%d-%H-%M-%S')+'.csv'
#print(pathoutput)
output = open(pathoutput,'w')
writer = csv.writer(output, delimiter=',')
header =['time','pos_robotX','pos_robotY']
writer.writerow(i for i in header)
row=[]
start = time.time()
while True:
  for id in vp.trackers:
      row=[]
      infos = vp.getTrackersInfos()
      trackers = infos['trackers'][id]
      if trackers['device_type'] == 'tracker':
          m = trackers['pose_matrix']
          positions = np.array(m.T[3])[0][:3]
          #print("positions = ",positions)
          #print(trackers['device_type'])
          row.append(float(time.time()-start))
          row.append(positions[0])
          row.append(positions[1])
          print(row)
          writer.writerow((row))



input.close()
output.close()
