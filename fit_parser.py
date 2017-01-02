# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 09:20:05 2016

@author: Rowan

The main method of the Activity class is csvParse. This should return two
dictionaries, each with the same keys. The first contains the synchronised
data, the second contains the units.
"""

from itertools import zip_longest
import csv
import numpy as np
import subprocess as sp

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
    
def num(s):
    "Convert strings to floats when possible, default to nan"
    try:
        return float(s)
    except ValueError:
        return float('nan')

class Activity:
    ''' A simple class containing a single activity and methods to analyse it '''
    
    def __init__(self):
        self.dataDict = {}
        self.unitsDict = {}
        self.indexDict = {}
        self.fitPath = ''
        self.csvPath = ''
        print('Generated activity object.')
        
    def fit2csv(self,srcePath,destPath):
        self.fitPath = srcePath
        self.csvPath = destPath
        cmmnd = 'java -jar FitCSVTool.jar -b ' + srcePath + ' ' + destPath
        sp.run(cmmnd, stdout=sp.PIPE)
        print('Finished converting file')
    
    def csv_parse(self,FilePath):
        # Function to read in the data from a csv file
        self.csvPath = FilePath
        
        with open(FilePath, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            print('Parsing file...')
            
            ridx = -1   # Start at -1 so first row has index 0
            # Loop over the rows in the file
            for row in filereader:
                # if type=='Data' and LocalNumber>=6 and Message=='Record' then proceed
                if row[0]=='Data' and int(row[1])>=6 and row[2]=='record':
                    
                    # Increment the row number and append a nan to all data columns
                    ridx = ridx + 1
                    for k in self.dataDict:
                        self.dataDict[k] = np.append(self.dataDict[k],np.nan)
                    
                    # Read groups of three values at a time.
                    for cidx,cells in enumerate(grouper(row,3)):
                        if cidx>0:  # Skip the first three
                            # If the field does not exist:
                            if not cells[0] in self.dataDict:
                                self.dataDict[cells[0]] = np.empty(ridx+1)*np.nan # Add field to dict
                                self.unitsDict[cells[0]] = cells[2] # Add units
                                self.indexDict[cells[0]] = ridx # Record idx for sync
                            
                            # Convert strings to floats or nan
                            if isinstance(cells[1], str):
                                tmp = num(cells[1].replace('"',''))
                            else:
                                tmp = np.nan
                            
                            self.dataDict[cells[0]][ridx] = tmp

        # All data arrays should now be the same length as the time array
        print('Finished parsing file.')
        
    def alt_corr(self):
        self.dataDict['altitudeC'] = self.dataDict['altitude']
        print('Corrected altitude data')
        