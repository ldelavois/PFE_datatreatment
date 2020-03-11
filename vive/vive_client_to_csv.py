#!/usr/bin/env python
import csv

from vive_pb2 import *
import socket
from utils import *
from vive_provider import *

vp = Vive_provider(clientMode=True)

output = open("position.csv",'w')
writer = csv.writer(output, delimiter=',')

while True:
  for id in vp.trackers:
      infos = vp.getTrackersInfos()
      trackers = infos['trackers'][id]
      m = trackers['pose_matrix']
      positions = np.array(m.T[3])[0][:3]
      print("positions = ",positions)
      writer.writerow((positions))

input.close()
