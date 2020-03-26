# PFE_datatreatment
Data treatment of csv files from robot during PFE course

## Script script.sh
You can run the script script.sh in the src folder to test the fonctions explained below.

## divisionCsv.py
The first program will delete close positions and then will divide the csv source file for each trajectory in several csv files. It can also save and show trajectories png graphs. Your csv file should come from approach or vive test.

### Command:
``` python
python divisionCsv.py -f csvfile.csv -save -show -line -all
```

### Options:
```-save``` : save the png graphs in the same csv file folder

``` -show ``` : show the png graph for each trajectory

``` line ```: draw line between dots in the graphs (simple dots by default)

``` -all ```: don't delete lines with too close position (do it by default)

## comparePlots.py

The second program will compare an approach trajectory from a csv file with a vive trajectory from another csv file. You have to specify the target.

### Command:
```python
python comparePlots.py -ff approachfile.csv vivefile.csv -target float float
```
