#!/bin/bash
#delete previous generated csv files and png files in the example approach repository
cd ../data/approach_status_13h13_odom
find . -name "*.png" | xargs rm
find . -name "approach_status_13h13_odom-*.csv" | xargs rm

#delete previous generated csv files and png files in the example position repository
cd ../position-2020-03-13-13-26-05
find . -name "*.png" | xargs rm
find . -name "position-2020-03-13-13-26-05_v2-.csv" | xargs rm

#launch the two functions that divide the two csv files then compare them
cd ../../src
python divisionCsv.py -f ../data/approach_status_13h13_odom/approach_status_13h13_odom.csv -save -line
python divisionCsv.py -f ../data/position-2020-03-13-13-26-05/position-2020-03-13-13-26-05_v2.csv -save -line
python comparePlots.py -ff ../data/approach_status_13h13_odom/approach_status_13h13_odom-1.csv ../data/position-2020-03-13-13-26-05/position-2020-03-13-13-26-05_v2-1.csv -t 3 1
