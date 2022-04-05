# calculateMobileClientResults.py

# import
import argparse
import os
import os.path
import sys

import numpy as np
import scipy as sp
import scipy.stats

import createBarChart



# filename of all average files
filenameAverageValues = "averageValues.txt"

# all average values from all runs
allAvgIsr10List = list()
allAvgIsr20List = list()
allAvgIsr30List = list()
allAvgIsr40List = list()
allAvgIsr50List = list()
allAvgIsr60List = list()
allAvgIsr70List = list()
allAvgIsr80List = list()
allAvgIsr90List = list()

# average from all average values
avgIsr10List = list()
avgIsr20List = list()
avgIsr30List = list()
avgIsr40List = list()
avgIsr50List = list()
avgIsr60List = list()
avgIsr70List = list()
avgIsr80List = list()
avgIsr90List = list()

# confidence interval from all average values
confIsr10List = list()
confIsr20List = list()
confIsr30List = list()
confIsr40List = list()
confIsr50List = list()
confIsr60List = list()
confIsr70List = list()
confIsr80List = list()
confIsr90List = list()






# ===== Read functions for average files =====

# ===== findAndReadAllAverageFiles() =====
#
# finds and reads all average files with all average values from all runs
def findAndReadAllAverageFiles(directory10, directory20, directory30, directory40, directory50, directory60, directory70, directory80, directory90):

  # find all average files  
  for subdir, dirs, files in os.walk("."):
    for file in files:
    
      if file == filenameAverageValues:
        
        if subdir.find(directory10) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr10List)

        if subdir.find(directory20) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr20List)

        if subdir.find(directory30) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr30List)

        if subdir.find(directory40) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr40List)

        if subdir.find(directory50) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr50List)

        if subdir.find(directory60) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr60List)

        if subdir.find(directory70) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr70List)

        if subdir.find(directory80) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr80List)

        if subdir.find(directory90) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgIsr90List)



# ===== readAverageFile() =====
#
# reads an average file with average values
def readAverageFile(filename, dataList):
  # reads the whole file (averageValues.txt) line by line
  if os.path.isfile(filename):
    with open(filename) as txtFile:
      for line in txtFile:
        
        # split and print line entries
        lineLength = len(line.split("\t"))
        
        if lineLength == 27:
          avgNumberOfPackets, avgNumberOfInterestPacketsOutSum, avgNumberOfInterestPacketsInSum, avgNumberOfSatisfiedInterestPacketsInSum, avgNumberOfDataPacketsOutSum, avgNumberOfDataPacketsInSum, avgInterestPacketBytesOutSum, avgInterestPacketBytesInSum, avgDataPacketBytesOutSum, avgDataPacketBytesInSum, avgRetransmissions, avgDuplicates, avgReceivedPackets, avgMissingPackets, avgLastDelay, avgFullDelay, avgTotalDelay, avgHopCount, avgIpOutOverhead, avgIpInOverhead, avgDpOutOverhead, avgDpInOverhead, avgDpOutBytesOverhead, avgDpInBytesOverhead, avgIsr, avgDpErrorRate, avgMos = line.split("\t")
          
          # add data to tmpList and to the specific trace list
          tmpList = list()
          tmpList.append(avgNumberOfPackets)
          tmpList.append(avgNumberOfInterestPacketsOutSum)
          tmpList.append(avgNumberOfInterestPacketsInSum)
          tmpList.append(avgNumberOfSatisfiedInterestPacketsInSum)
          tmpList.append(avgNumberOfDataPacketsOutSum)
          tmpList.append(avgNumberOfDataPacketsInSum)
          tmpList.append(avgInterestPacketBytesOutSum)
          tmpList.append(avgInterestPacketBytesInSum)
          tmpList.append(avgDataPacketBytesOutSum)
          tmpList.append(avgDataPacketBytesInSum)
          tmpList.append(avgRetransmissions)
          tmpList.append(avgDuplicates)
          tmpList.append(avgReceivedPackets)
          tmpList.append(avgMissingPackets)
          tmpList.append(avgLastDelay)
          tmpList.append(avgFullDelay)
          tmpList.append(avgTotalDelay)
          tmpList.append(avgHopCount)
          tmpList.append(avgIpOutOverhead)
          tmpList.append(avgIpInOverhead)
          tmpList.append(avgDpOutOverhead)
          tmpList.append(avgDpInOverhead)
          tmpList.append(avgDpOutBytesOverhead)
          tmpList.append(avgDpInBytesOverhead)
          tmpList.append(avgIsr)
          tmpList.append(avgDpErrorRate)
          tmpList.append(avgMos)
          dataList.append(tmpList)
          tmpList = []
        
        else:
          print ("Terminated. The file "+filename+" does not exist.")
          sys.exit()






# ===== Calculation functions - for average value and confidence interval =====

# ===== calculateAverages() =====
#
# calculates average from all average values from all runs
def calculateAverages(allAvgList, avgList):
  # initializes all average values with zero
  avgNumberOfPackets = 0
  avgList.append(avgNumberOfPackets)
  avgNumberOfInterestPacketsOutSum = 0
  avgList.append(avgNumberOfInterestPacketsOutSum)
  avgNumberOfInterestPacketsInSum = 0
  avgList.append(avgNumberOfInterestPacketsInSum)
  avgNumberOfSatisfiedInterestPacketsInSum = 0
  avgList.append(avgNumberOfSatisfiedInterestPacketsInSum)
  avgNumberOfDataPacketsOutSum = 0
  avgList.append(avgNumberOfDataPacketsOutSum)
  avgNumberOfDataPacketsInSum = 0
  avgList.append(avgNumberOfDataPacketsInSum)
  avgInterestPacketBytesOutSum = 0
  avgList.append(avgInterestPacketBytesOutSum)
  avgInterestPacketBytesInSum = 0
  avgList.append(avgInterestPacketBytesInSum)
  avgDataPacketBytesOutSum = 0
  avgList.append(avgDataPacketBytesOutSum)
  avgDataPacketBytesInSum = 0
  avgList.append(avgDataPacketBytesInSum)
  avgRetransmissions = 0
  avgList.append(avgRetransmissions)
  avgDuplicates = 0
  avgList.append(avgDuplicates)
  avgReceivedPackets = 0
  avgList.append(avgReceivedPackets)
  avgMissingPackets = 0
  avgList.append(avgMissingPackets)
  avgLastDelay = 0
  avgList.append(avgLastDelay)
  avgFullDelay = 0
  avgList.append(avgFullDelay)
  avgTotalDelay = 0
  avgList.append(avgTotalDelay)
  avgHopCount = 0
  avgList.append(avgHopCount)
  avgIpOutOverhead = 0
  avgList.append(avgIpOutOverhead)
  avgIpInOverhead = 0
  avgList.append(avgIpInOverhead)
  avgDpOutOverhead = 0
  avgList.append(avgDpOutOverhead)
  avgDpInOverhead = 0
  avgList.append(avgDpInOverhead)
  avgDpOutBytesOverhead = 0
  avgList.append(avgDpOutBytesOverhead)
  avgDpInBytesOverhead = 0
  avgList.append(avgDpInBytesOverhead)
  avgIsr = 0
  avgList.append(avgIsr)
  avgDpErrorRate = 0
  avgList.append(avgDpErrorRate)
  avgMos = 0
  avgList.append(avgMos)
  
  
  index = 0
  # sum up all values
  for i in allAvgList:
    
    for j in i:
      avgList[index] = avgList[index] + float(j)
      index = index + 1
    index = 0
  
  # calculate average
  for k in range(0,len(avgList)):
    avgList[k] = avgList[k] / len(allAvgList)



# ===== calculateAllAverages() =====
#
# calculates average from all average values from all runs
def calculateAllAverages():
  calculateAverages(allAvgIsr10List, avgIsr10List)
  calculateAverages(allAvgIsr20List, avgIsr20List)
  calculateAverages(allAvgIsr30List, avgIsr30List)
  calculateAverages(allAvgIsr40List, avgIsr40List)
  calculateAverages(allAvgIsr50List, avgIsr50List)
  calculateAverages(allAvgIsr60List, avgIsr60List)
  calculateAverages(allAvgIsr70List, avgIsr70List)
  calculateAverages(allAvgIsr80List, avgIsr80List)
  calculateAverages(allAvgIsr90List, avgIsr90List)



# ===== calculateConfidenceInterval() =====
#
# calculates confidence intervall for a specific data
def calculateConfidenceInterval(data):
    confidence = 0.95
    
    arrayData = 1.0 * np.array(data)
    n = len(arrayData)
    
    standardError = scipy.stats.sem(arrayData)
    criticalValue = sp.stats.t._ppf((1+confidence)/2., n-1)
    
    # confidence interval
    confidenceInterval = standardError * criticalValue
    return confidenceInterval



# ===== calculateAllConfidenceIntervall() =====
#
# calculates confidence intervall from all average values from all runs
def calculateAllConfidenceIntervall(allAvgList, confList):
  numberOfMetrics = len(allAvgList[0])
  
  # initialize confList with zero
  for i in range(0, numberOfMetrics):
    confList.append(0)
  
  # preparing for calculating the confidence interval for each metric
  for i in range(0, numberOfMetrics):
    
    tmpList = list()
    for j in allAvgList:
      tmpList.append(float(j[i]))
    
    # calculate confidence interval
    confInterval = calculateConfidenceInterval(tmpList)
    confList[i] = confInterval



# ===== calculateAllConfidenceIntervallLists() =====
#
# calculates average from all average values from all runs
def calculateAllConfidenceIntervallLists():
  calculateAllConfidenceIntervall(allAvgIsr10List, confIsr10List)
  calculateAllConfidenceIntervall(allAvgIsr20List, confIsr20List)
  calculateAllConfidenceIntervall(allAvgIsr30List, confIsr30List)
  calculateAllConfidenceIntervall(allAvgIsr40List, confIsr40List)
  calculateAllConfidenceIntervall(allAvgIsr50List, confIsr50List)
  calculateAllConfidenceIntervall(allAvgIsr60List, confIsr60List)
  calculateAllConfidenceIntervall(allAvgIsr70List, confIsr70List)
  calculateAllConfidenceIntervall(allAvgIsr80List, confIsr80List)
  calculateAllConfidenceIntervall(allAvgIsr90List, confIsr90List)



# ===== MAIN function =====
#
# this is the main function
def main():

  # parse command line arguments
  argumentParser = argparse.ArgumentParser()
  argumentParser.add_argument("-dir10", "--directory10", type = str, help = "Results directory 10", default = "")
  argumentParser.add_argument("-dir20", "--directory20", type = str, help = "Results directory 20", default = "")
  argumentParser.add_argument("-dir30", "--directory30", type = str, help = "Results directory 30", default = "")
  argumentParser.add_argument("-dir40", "--directory40", type = str, help = "Results directory 40", default = "")
  argumentParser.add_argument("-dir50", "--directory50", type = str, help = "Results directory 50", default = "")
  argumentParser.add_argument("-dir60", "--directory60", type = str, help = "Results directory 60", default = "")
  argumentParser.add_argument("-dir70", "--directory70", type = str, help = "Results directory 70", default = "")
  argumentParser.add_argument("-dir80", "--directory80", type = str, help = "Results directory 80", default = "")
  argumentParser.add_argument("-dir90", "--directory90", type = str, help = "Results directory 90", default = "")
  argumentParser.add_argument("-dstDir", "--destinationDir", type = str, help = "Bar charts results directory", default = "./")
  args = argumentParser.parse_args()
  
  # set command line arguments
  directory10 = args.directory10
  directory20 = args.directory20
  directory30 = args.directory30
  directory40 = args.directory40
  directory50 = args.directory50
  directory60 = args.directory60
  directory70 = args.directory70
  directory80 = args.directory80
  directory90 = args.directory90
  dstDirectory = args.destinationDir

  # set and create destination directory
  dirSep = "/"
  if not (args.destinationDir.endswith(dirSep)):
    dstDirectory = dstDirectory + dirSep
  if not os.path.exists(dstDirectory):
    os.makedirs(dstDirectory)

  # find and read files (all average values from all runs)
  findAndReadAllAverageFiles(directory10, directory20, directory30, directory40, directory50, directory60, directory70, directory80, directory90)
  
  # check if average files are created before
  if (len(allAvgIsr10List) == 0 or len(allAvgIsr20List) == 0 or len(allAvgIsr30List) == 0 or len(allAvgIsr40List) == 0 or len(allAvgIsr50List) == 0 or len(allAvgIsr60List) == 0 or len(allAvgIsr70List) == 0 or len(allAvgIsr80List) == 0 or len(allAvgIsr90List) == 0):
    print("Average files are missing. Create average files before.")
    sys.exit()
  
  # average from all average values
  calculateAllAverages()
  
  # confidence interval from all average values
  calculateAllConfidenceIntervallLists()
  
  
  
  
  
  
  
  # index variables
  indExpP = 0
  indIpOut = 1
  indIpIn = 2
  indSatIpOut = 3
  indDpOut = 4
  indDpIn = 5
  indIpByOut = 6
  indIpByIn = 7
  indDpByOut = 8
  indDPByIn = 9
  indRetrDP = 10
  indDupDp = 11
  indRecDp = 12
  indMissDp = 13
  indLastDel = 14
  indFullDel = 15
  indTotDel = 16
  indHopC = 17
  indIpOutOv = 18
  indIpInOv = 19
  indDpOutOv = 20
  indDpInOv = 21
  indDpOutByOv = 22
  indDpInByOv = 23
  indIsr = 24
  indErrR = 25
  indMos = 26
  
  
  
  #---------------------------------------------------------------
  # create bar charts one metric - for all metrics (9 bars)
  #---------------------------------------------------------------

  # avgNumberOfPackets (expected)
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of expected Interest Packets or Data Packets", "", "The number of packets", dstDirectory + "comp_no_expP.pdf", avgIsr10List[indExpP], avgIsr20List[indExpP], avgIsr30List[indExpP], avgIsr40List[indExpP], avgIsr50List[indExpP], avgIsr60List[indExpP], avgIsr70List[indExpP], avgIsr80List[indExpP], avgIsr90List[indExpP], confIsr10List[indExpP], confIsr20List[indExpP], confIsr30List[indExpP], confIsr40List[indExpP], confIsr50List[indExpP], confIsr60List[indExpP], confIsr70List[indExpP], confIsr80List[indExpP], confIsr90List[indExpP])
  
  # avgNumberOfInterestPacketsOutSum
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Interest Packets out at Consumer", "", "The number of packets", dstDirectory + "comp_no_IPoutC.pdf", avgIsr10List[indIpOut], avgIsr20List[indIpOut], avgIsr30List[indIpOut], avgIsr40List[indIpOut], avgIsr50List[indIpOut], avgIsr60List[indIpOut], avgIsr70List[indIpOut], avgIsr80List[indIpOut], avgIsr90List[indIpOut], confIsr10List[indIpOut], confIsr20List[indIpOut], confIsr30List[indIpOut], confIsr40List[indIpOut], confIsr50List[indIpOut], confIsr60List[indIpOut], confIsr70List[indIpOut], confIsr80List[indIpOut], confIsr90List[indIpOut])
  
  # avgNumberOfInterestPacketsInSum
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Interest Packets in at Producer", "", "The number of packets", dstDirectory + "comp_no_IPinP.pdf", avgIsr10List[indIpIn], avgIsr20List[indIpIn], avgIsr30List[indIpIn], avgIsr40List[indIpIn], avgIsr50List[indIpIn], avgIsr60List[indIpIn], avgIsr70List[indIpIn], avgIsr80List[indIpIn], avgIsr90List[indIpIn], confIsr10List[indIpIn], confIsr20List[indIpIn], confIsr30List[indIpIn], confIsr40List[indIpIn], confIsr50List[indIpIn], confIsr60List[indIpIn], confIsr70List[indIpIn], confIsr80List[indIpIn], confIsr90List[indIpIn])
  
  # avgNumberOfSatisfiedInterestPacketsInSum (not relevant)
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Satisfied Interest Packets out at Consumer", "", "The number of packets", dstDirectory + "comp_no_satIPoutC.pdf", avgIsr10List[indSatIpOut], avgIsr20List[indSatIpOut], avgIsr30List[indSatIpOut], avgIsr40List[indSatIpOut], avgIsr50List[indSatIpOut], avgIsr60List[indSatIpOut], avgIsr70List[indSatIpOut], avgIsr80List[indSatIpOut], avgIsr90List[indSatIpOut], confIsr10List[indSatIpOut], confIsr20List[indSatIpOut], confIsr30List[indSatIpOut], confIsr40List[indSatIpOut], confIsr50List[indSatIpOut], confIsr60List[indSatIpOut], confIsr70List[indSatIpOut], confIsr80List[indSatIpOut], confIsr90List[indSatIpOut])
  
  # avgNumberOfDataPacketsOutSum
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Data Packets out at Producer", "", "The number of packets", dstDirectory + "comp_no_DPoutP.pdf", avgIsr10List[indDpOut], avgIsr20List[indDpOut], avgIsr30List[indDpOut], avgIsr40List[indDpOut], avgIsr50List[indDpOut], avgIsr60List[indDpOut], avgIsr70List[indDpOut], avgIsr80List[indDpOut], avgIsr90List[indDpOut], confIsr10List[indDpOut], confIsr20List[indDpOut], confIsr30List[indDpOut], confIsr40List[indDpOut], confIsr50List[indDpOut], confIsr60List[indDpOut], confIsr70List[indDpOut], confIsr80List[indDpOut], confIsr90List[indDpOut])
  
  # avgNumberOfDataPacketsInSum
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Data Packets in at Consumer", "", "The number of packets", dstDirectory + "comp_no_DPinC.pdf", avgIsr10List[indDpIn], avgIsr20List[indDpIn], avgIsr30List[indDpIn], avgIsr40List[indDpIn], avgIsr50List[indDpIn], avgIsr60List[indDpIn], avgIsr70List[indDpIn], avgIsr80List[indDpIn], avgIsr90List[indDpIn], confIsr10List[indDpIn], confIsr20List[indDpIn], confIsr30List[indDpIn], confIsr40List[indDpIn], confIsr50List[indDpIn], confIsr60List[indDpIn], confIsr70List[indDpIn], confIsr80List[indDpIn], confIsr90List[indDpIn])
  
  # avgRetransmissions
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Retransmitted Data Packets", "", "The number of packets", dstDirectory + "comp_no_RetrDP.pdf", avgIsr10List[indRetrDP], avgIsr20List[indRetrDP], avgIsr30List[indRetrDP], avgIsr40List[indRetrDP], avgIsr50List[indRetrDP], avgIsr60List[indRetrDP], avgIsr70List[indRetrDP], avgIsr80List[indRetrDP], avgIsr90List[indRetrDP], confIsr10List[indRetrDP], confIsr20List[indRetrDP], confIsr30List[indRetrDP], confIsr40List[indRetrDP], confIsr50List[indRetrDP], confIsr60List[indRetrDP], confIsr70List[indRetrDP], confIsr80List[indRetrDP], confIsr90List[indRetrDP])
  
  # avgDuplicates
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Duplicate Data Packets", "", "The number of packets", dstDirectory + "comp_no_dupDP.pdf", avgIsr10List[indDupDp], avgIsr20List[indDupDp], avgIsr30List[indDupDp], avgIsr40List[indDupDp], avgIsr50List[indDupDp], avgIsr60List[indDupDp], avgIsr70List[indDupDp], avgIsr80List[indDupDp], avgIsr90List[indDupDp], confIsr10List[indDupDp], confIsr20List[indDupDp], confIsr30List[indDupDp], confIsr40List[indDupDp], confIsr50List[indDupDp], confIsr60List[indDupDp], confIsr70List[indDupDp], confIsr80List[indDupDp], confIsr90List[indDupDp])
  
  # avgReceivedPackets
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Received Data Packets without Duplicates", "", "The number of packets", dstDirectory + "comp_no_recDP.pdf", avgIsr10List[indRecDp], avgIsr20List[indRecDp], avgIsr30List[indRecDp], avgIsr40List[indRecDp], avgIsr50List[indRecDp], avgIsr60List[indRecDp], avgIsr70List[indRecDp], avgIsr80List[indRecDp], avgIsr90List[indRecDp], confIsr10List[indRecDp], confIsr20List[indRecDp], confIsr30List[indRecDp], confIsr40List[indRecDp], confIsr50List[indRecDp], confIsr60List[indRecDp], confIsr70List[indRecDp], confIsr80List[indRecDp], confIsr90List[indRecDp])
  
  # avgMissingPackets
  createBarChart.createBarChartCompareOneMetric9Bars("The Number of Missed Data Packets", "", "The number of packets", dstDirectory + "comp_no_missDP.pdf", avgIsr10List[indMissDp], avgIsr20List[indMissDp], avgIsr30List[indMissDp], avgIsr40List[indMissDp], avgIsr50List[indMissDp], avgIsr60List[indMissDp], avgIsr70List[indMissDp], avgIsr80List[indMissDp], avgIsr90List[indMissDp], confIsr10List[indMissDp], confIsr20List[indMissDp], confIsr30List[indMissDp], confIsr40List[indMissDp], confIsr50List[indMissDp], confIsr60List[indMissDp], confIsr70List[indMissDp], confIsr80List[indMissDp], confIsr90List[indMissDp])
  
  # avgLastDelay
  createBarChart.createBarChartCompareOneMetric9Bars("The Last Delay", "", "The delay in milliseconds (ms)", dstDirectory + "comp_ms_lastDelay.pdf", avgIsr10List[indLastDel], avgIsr20List[indLastDel], avgIsr30List[indLastDel], avgIsr40List[indLastDel], avgIsr50List[indLastDel], avgIsr60List[indLastDel], avgIsr70List[indLastDel], avgIsr80List[indLastDel], avgIsr90List[indLastDel], confIsr10List[indLastDel], confIsr20List[indLastDel], confIsr30List[indLastDel], confIsr40List[indLastDel], confIsr50List[indLastDel], confIsr60List[indLastDel], confIsr70List[indLastDel], confIsr80List[indLastDel], confIsr90List[indLastDel])
  
  # avgFullDelay
  createBarChart.createBarChartCompareOneMetric9Bars("The Full Delay", "", "The delay in milliseconds (ms)", dstDirectory + "comp_ms_fullDelay.pdf", avgIsr10List[indFullDel], avgIsr20List[indFullDel], avgIsr30List[indFullDel], avgIsr40List[indFullDel], avgIsr50List[indFullDel], avgIsr60List[indFullDel], avgIsr70List[indFullDel], avgIsr80List[indFullDel], avgIsr90List[indFullDel], confIsr10List[indFullDel], confIsr20List[indFullDel], confIsr30List[indFullDel], confIsr40List[indFullDel], confIsr50List[indFullDel], confIsr60List[indFullDel], confIsr70List[indFullDel], confIsr80List[indFullDel], confIsr90List[indFullDel])
  
  # avgTotalDelay (not relevant)
  createBarChart.createBarChartCompareOneMetric9Bars("The Total Delay", "", "The delay in seconds (sec)", dstDirectory + "comp_sec_totalDelay.pdf", avgIsr10List[indTotDel], avgIsr20List[indTotDel], avgIsr30List[indTotDel], avgIsr40List[indTotDel], avgIsr50List[indTotDel], avgIsr60List[indTotDel], avgIsr70List[indTotDel], avgIsr80List[indTotDel], avgIsr90List[indTotDel], confIsr10List[indTotDel], confIsr20List[indTotDel], confIsr30List[indTotDel], confIsr40List[indTotDel], confIsr50List[indTotDel], confIsr60List[indTotDel], confIsr70List[indTotDel], confIsr80List[indTotDel], confIsr90List[indTotDel])
  
  # avgHopCount
  createBarChart.createBarChartCompareOneMetric9Bars("The Hop Count between Sending and Receiving a Packet", "", "The number of network hops", dstDirectory + "comp_val_HopCount.pdf", avgIsr10List[indHopC], avgIsr20List[indHopC], avgIsr30List[indHopC], avgIsr40List[indHopC], avgIsr50List[indHopC], avgIsr60List[indHopC], avgIsr70List[indHopC], avgIsr80List[indHopC], avgIsr90List[indHopC], confIsr10List[indHopC], confIsr20List[indHopC], confIsr30List[indHopC], confIsr40List[indHopC], confIsr50List[indHopC], confIsr60List[indHopC], confIsr70List[indHopC], confIsr80List[indHopC], confIsr90List[indHopC])
  
  # avgIpOutOverhead
  createBarChart.createBarChartCompareOneMetric9Bars("Interest Packet Success Percentage of sent Interest Packets", "", "Interest Packet Success Percentage in %", dstDirectory + "comp_ov_no_IPoutC.pdf", avgIsr10List[indIpOutOv], avgIsr20List[indIpOutOv], avgIsr30List[indIpOutOv], avgIsr40List[indIpOutOv], avgIsr50List[indIpOutOv], avgIsr60List[indIpOutOv], avgIsr70List[indIpOutOv], avgIsr80List[indIpOutOv], avgIsr90List[indIpOutOv], confIsr10List[indIpOutOv], confIsr20List[indIpOutOv], confIsr30List[indIpOutOv], confIsr40List[indIpOutOv], confIsr50List[indIpOutOv], confIsr60List[indIpOutOv], confIsr70List[indIpOutOv], confIsr80List[indIpOutOv], confIsr90List[indIpOutOv])
  
  # avgIpInOverhead
  createBarChart.createBarChartCompareOneMetric9Bars("Interest Packet Success Percentage of received Interest Packets", "", "Interest Packet Success Percentage in %", dstDirectory + "comp_ov_no_IPinP.pdf", avgIsr10List[indIpInOv], avgIsr20List[indIpInOv], avgIsr30List[indIpInOv], avgIsr40List[indIpInOv], avgIsr50List[indIpInOv], avgIsr60List[indIpInOv], avgIsr70List[indIpInOv], avgIsr80List[indIpInOv], avgIsr90List[indIpInOv], confIsr10List[indIpInOv], confIsr20List[indIpInOv], confIsr30List[indIpInOv], confIsr40List[indIpInOv], confIsr50List[indIpInOv], confIsr60List[indIpInOv], confIsr70List[indIpInOv], confIsr80List[indIpInOv], confIsr90List[indIpInOv])
  
  # avgDpOutOverhead
  createBarChart.createBarChartCompareOneMetric9Bars("Data Packet Success Percentage of sent Data Packets", "", "Data Packet Success Percentage in %", dstDirectory + "comp_ov_no_DPoutP.pdf", avgIsr10List[indDpOutOv], avgIsr20List[indDpOutOv], avgIsr30List[indDpOutOv], avgIsr40List[indDpOutOv], avgIsr50List[indDpOutOv], avgIsr60List[indDpOutOv], avgIsr70List[indDpOutOv], avgIsr80List[indDpOutOv], avgIsr90List[indDpOutOv], confIsr10List[indDpOutOv], confIsr20List[indDpOutOv], confIsr30List[indDpOutOv], confIsr40List[indDpOutOv], confIsr50List[indDpOutOv], confIsr60List[indDpOutOv], confIsr70List[indDpOutOv], confIsr80List[indDpOutOv], confIsr90List[indDpOutOv])
  
  # avgDpInOverhead
  createBarChart.createBarChartCompareOneMetric9Bars("Data Packet Success Percentage of received Data Packets", "", "Data Packet Success Percentage in %", dstDirectory + "comp_ov_no_DPinC.pdf", avgIsr10List[indDpInOv], avgIsr20List[indDpInOv], avgIsr30List[indDpInOv], avgIsr40List[indDpInOv], avgIsr50List[indDpInOv], avgIsr60List[indDpInOv], avgIsr70List[indDpInOv], avgIsr80List[indDpInOv], avgIsr90List[indDpInOv], confIsr10List[indDpInOv], confIsr20List[indDpInOv], confIsr30List[indDpInOv], confIsr40List[indDpInOv], confIsr50List[indDpInOv], confIsr60List[indDpInOv], confIsr70List[indDpInOv], confIsr80List[indDpInOv], confIsr90List[indDpInOv])
  
  # avgIsr
  createBarChart.createBarChartCompareOneMetric9Bars("Interest Satisfaction Ratio (ISR)", "", "ISR in %", dstDirectory + "comp_perc_ISR.pdf", avgIsr10List[indIsr], avgIsr20List[indIsr], avgIsr30List[indIsr], avgIsr40List[indIsr], avgIsr50List[indIsr], avgIsr60List[indIsr], avgIsr70List[indIsr], avgIsr80List[indIsr], avgIsr90List[indIsr], confIsr10List[indIsr], confIsr20List[indIsr], confIsr30List[indIsr], confIsr40List[indIsr], confIsr50List[indIsr], confIsr60List[indIsr], confIsr70List[indIsr], confIsr80List[indIsr], confIsr90List[indIsr])
  
  # avgDpErrorRate
  createBarChart.createBarChartCompareOneMetric9Bars("Data Packet Error Rate", "", "Data Packet Error Rate [0, 1]", dstDirectory + "comp_val_DPErrorRate.pdf", avgIsr10List[indErrR], avgIsr20List[indErrR], avgIsr30List[indErrR], avgIsr40List[indErrR], avgIsr50List[indErrR], avgIsr60List[indErrR], avgIsr70List[indErrR], avgIsr80List[indErrR], avgIsr90List[indErrR], confIsr10List[indErrR], confIsr20List[indErrR], confIsr30List[indErrR], confIsr40List[indErrR], confIsr50List[indErrR], confIsr60List[indErrR], confIsr70List[indErrR], confIsr80List[indErrR], confIsr90List[indErrR])
  
  # avgMos
  createBarChart.createBarChartCompareOneMetric9Bars("Estimated Mean Opinion Score (MOS-CQE)", "", "MOS-CQE [1, 4.35]", dstDirectory + "comp_val_MOS.pdf", avgIsr10List[indMos], avgIsr20List[indMos], avgIsr30List[indMos], avgIsr40List[indMos], avgIsr50List[indMos], avgIsr60List[indMos], avgIsr70List[indMos], avgIsr80List[indMos], avgIsr90List[indMos], confIsr10List[indMos], confIsr20List[indMos], confIsr30List[indMos], confIsr40List[indMos], confIsr50List[indMos], confIsr60List[indMos], confIsr70List[indMos], confIsr80List[indMos], confIsr90List[indMos])






# ========== MAIN PROGRAM ==========
if __name__== "__main__":
  main()
