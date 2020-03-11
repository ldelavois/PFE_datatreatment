#!/usr/bin/env python

from vive_pb2 import *
import socket
from utils import *
from vive_provider import *

vp = Vive_provider(clientMode=True)

input = open(self.path,'w')
writer = csv.writer(output, delimiter=',')

while True:

    trackers = vp.getTrackersInfos()
    positions = trackers["pose"]
    print("positions = ",positions)
    writer.writerow((positions))

input.close()
