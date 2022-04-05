# calculateResults.py

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
allAvgMobileClientList = list()
allAvgBestRouteList = list()
allAvgMulticastList = list()

# average from all average values
avgMobileClientList = list()
avgBestRouteList = list()
avgMulticastList = list()

# confidence interval from all average values
confMobileClientList = list()
confBestRouteList = list()
confMulticastList = list()






# ===== Read functions for average files =====

# ===== findAndReadAllAverageFiles() =====
#
# finds and reads all average files with all average values from all runs
def findAndReadAllAverageFiles(bestRouteDir, multicastDir, mobileClientDir):

  # find all average files  
  for subdir, dirs, files in os.walk("."):
    for file in files:
    
      if file == filenameAverageValues:
        
        if subdir.find(bestRouteDir) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgBestRouteList)
          
        if subdir.find(multicastDir) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgMulticastList)
        
        if subdir.find(mobileClientDir) != -1:
          filePath = os.path.join(subdir, file)
          readAverageFile(filePath, allAvgMobileClientList)



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
  calculateAverages(allAvgMobileClientList, avgMobileClientList)
  calculateAverages(allAvgBestRouteList, avgBestRouteList)
  calculateAverages(allAvgMulticastList, avgMulticastList)



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
  calculateAllConfidenceIntervall(allAvgBestRouteList, confBestRouteList)
  calculateAllConfidenceIntervall(allAvgMulticastList, confMulticastList)
  calculateAllConfidenceIntervall(allAvgMobileClientList, confMobileClientList)






# ===== MAIN function =====
#
# this is the main function
def main():
    
  # parse command line arguments
  argumentParser = argparse.ArgumentParser()
  argumentParser.add_argument("-bDir", "--bestRouteDir", type = str, help = "Best-Route forwarding strategy results directory", default = "")
  argumentParser.add_argument("-mDir", "--multicastDir", type = str, help = "Multicast forwarding strategy results directory", default = "")
  argumentParser.add_argument("-cDir", "--mobileClientDir", type = str, help = "Mobile-Client forwarding strategy results directory", default = "")
  argumentParser.add_argument("-dstDir", "--destinationDir", type = str, help = "Bar charts results directory", default = "./")
  args = argumentParser.parse_args()
  
  # set command line arguments
  bestRouteDirectory = args.bestRouteDir
  multicastDirectory = args.multicastDir
  mobileClientDirectory = args.mobileClientDir
  dstDirectory = args.destinationDir

  # set and create destination directory
  dirSep = "/"
  if not (args.destinationDir.endswith(dirSep)):
    dstDirectory = dstDirectory + dirSep
  if not os.path.exists(dstDirectory):
    os.makedirs(dstDirectory)

  # find and read files (all average values from all runs)
  findAndReadAllAverageFiles(bestRouteDirectory, multicastDirectory, mobileClientDirectory)
  
  # check if average files are created before
  if (len(allAvgBestRouteList) == 0 or len(allAvgMulticastList) == 0 or len(allAvgMobileClientList) == 0):
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
  # create bar charts three metrics - for some metrics (3 bars)
  #---------------------------------------------------------------
  
  # number of IPs in at Producer, received duplicate DPs and  received DPs without duplicates
  createBarChart.createAndSaveBarChartThreeMetrics3Bars("The Number of Interest Packets in at Producer, the Number of Duplicate Data Packets and the Number of Received Data Packets without Duplicates", "", "The number of packets", dstDirectory + "no_IPinP_dupDP_recDP.pdf", avgBestRouteList[indIpIn], avgMulticastList[indIpIn], avgMobileClientList[indIpIn], confBestRouteList[indIpIn], confMulticastList[indIpIn], confMobileClientList[indIpIn], avgBestRouteList[indDupDp], avgMulticastList[indDupDp], avgMobileClientList[indDupDp], confBestRouteList[indDupDp], confMulticastList[indDupDp], confMobileClientList[indDupDp], avgBestRouteList[indRecDp], avgMulticastList[indRecDp], avgMobileClientList[indRecDp], confBestRouteList[indRecDp], confMulticastList[indRecDp], confMobileClientList[indRecDp], "Number of Interest Packets in at Producer", "Number of received duplicate Data Packets", "Number of received Data Packets")
  
  # IPs out at Consumer, IPs in at Producer and DPs in at Consumer overhead
  createBarChart.createAndSaveBarChartThreeMetrics3Bars("The Interest Packets and Data Packets Overhead", "", "The packet overhead in %", dstDirectory + "ov_no_IPoutC_IPinP_DPinC.pdf", avgBestRouteList[indIpOutOv], avgMulticastList[indIpOutOv], avgMobileClientList[indIpOutOv], confBestRouteList[indIpOutOv], confMulticastList[indIpOutOv], confMobileClientList[indIpOutOv], avgBestRouteList[indIpInOv], avgMulticastList[indIpInOv], avgMobileClientList[indIpInOv], confBestRouteList[indIpInOv], confMulticastList[indIpInOv], confMobileClientList[indIpInOv], avgBestRouteList[indDpOutOv], avgMulticastList[indDpOutOv], avgMobileClientList[indDpOutOv], confBestRouteList[indDpOutOv], confMulticastList[indDpOutOv], confMobileClientList[indDpOutOv], "The Interest Packets Overhead out at Consumer", "The Interest Packets Overhead in at Producer", "The Data Packets Overhead in at Consumer")
  
  # number of retransmissions, duplicate DPs, missed DPs
  createBarChart.createAndSaveBarChartThreeMetrics3Bars("The Number of Retransmitted Data Packets, Duplicate Data Packets and Missed Data Packets", "", "The number of packets", dstDirectory + "no_RetrDP_dupDP_missDP.pdf", avgBestRouteList[indRetrDP], avgMulticastList[indRetrDP], avgMobileClientList[indRetrDP], confBestRouteList[indRetrDP], confMulticastList[indRetrDP], confMobileClientList[indRetrDP], avgBestRouteList[indDupDp], avgMulticastList[indDupDp], avgMobileClientList[indDupDp], confBestRouteList[indDupDp], confMulticastList[indDupDp], confMobileClientList[indDupDp], avgBestRouteList[indMissDp], avgMulticastList[indMissDp], avgMobileClientList[indMissDp], confBestRouteList[indMissDp], confMulticastList[indMissDp], confMobileClientList[indMissDp], "Number of Retransmissions", "Number of duplicate Data Packets", "Number of missed Data Packets")
  
  
  
  #---------------------------------------------------------------
  # create bar charts two metrics (3 bars)
  #---------------------------------------------------------------
  
  # IPs out at Consumer and IPs in at Producer overhead
  createBarChart.createAndSaveBarChartTwoMetrics3Bars("The Interest Packets Overhead out at Consumer and the Data Packets Overhead in at Consumer", "", "The packet overhead in %", dstDirectory + "ov_no_IPoutC_DPinC.pdf", avgBestRouteList[indIpOutOv], avgMulticastList[indIpOutOv], avgMobileClientList[indIpOutOv], confBestRouteList[indIpOutOv], confMulticastList[indIpOutOv], confMobileClientList[indIpOutOv], avgBestRouteList[indIpInOv], avgMulticastList[indIpInOv], avgMobileClientList[indIpInOv], confBestRouteList[indIpInOv], confMulticastList[indIpInOv], confMobileClientList[indIpInOv], "Interest Packets Overhead out at Consumer", "Interest Packets Overhead in at Producer")
  
  # number of IPs out at Consumer and IPs in at Producer
  createBarChart.createAndSaveBarChartTwoMetrics3Bars("The Number of Interest Packets out at Consumer and in at Producer", "", "The number of packets", dstDirectory + "no_IPoutC_IPinP.pdf", avgBestRouteList[indIpOut], avgMulticastList[indIpOut], avgMobileClientList[indIpOut], confBestRouteList[indIpOut], confMulticastList[indIpOut], confMobileClientList[indIpOut], avgBestRouteList[indIpIn], avgMulticastList[indIpIn], avgMobileClientList[indIpIn], confBestRouteList[indIpIn], confMulticastList[indIpIn], confMobileClientList[indIpIn], "Interest Packetss out at Consumer", "Interest Packets in at Producer")
  
  
  
  #---------------------------------------------------------------
  # create bar charts one metric - for number of packets (4 bars)
  #---------------------------------------------------------------
  
  # avgNumberOfInterestPacketsOutSum with expected packets
  createBarChart.createBarChartComparePacketsOneMetric4Bars("The Number of Interest Packets out at Consumer", "", "The number of packets", dstDirectory + "no_IPoutC_exp.pdf", avgBestRouteList[indIpOut], avgMulticastList[indIpOut], avgMobileClientList[indIpOut], avgMobileClientList[indExpP], confBestRouteList[indIpOut], confMulticastList[indIpOut], confMobileClientList[indIpOut], confMobileClientList[indExpP])  
  
  # avgNumberOfInterestPacketsInSum with expected packets
  createBarChart.createBarChartComparePacketsOneMetric4Bars("The Number of Interest Packets in at Producer", "", "The number of packets", dstDirectory + "no_IPinP_exp.pdf", avgBestRouteList[indIpIn], avgMulticastList[indIpIn], avgMobileClientList[indIpIn], avgMobileClientList[indExpP], confBestRouteList[indIpIn], confMulticastList[indIpIn], confMobileClientList[indIpIn], confMobileClientList[indExpP])
  
  # avgNumberOfSatisfiedInterestPacketsInSum with expected packets (not relevant)
  createBarChart.createBarChartComparePacketsOneMetric4Bars("The Number of Satisfied Interest Packets out at Consumer", "", "The number of packets", dstDirectory + "no_satIPoutC_exp.pdf", avgBestRouteList[indSatIpOut], avgMulticastList[indSatIpOut], avgMobileClientList[indSatIpOut], avgMobileClientList[indExpP], confBestRouteList[indSatIpOut], confMulticastList[indSatIpOut], confMobileClientList[indSatIpOut], confMobileClientList[indExpP])
  
  # avgNumberOfDataPacketsOutSum with expected packets
  createBarChart.createBarChartComparePacketsOneMetric4Bars("The Number of Data Packets out at Producer", "", "The number of packets", dstDirectory + "no_DPoutP_exp.pdf", avgBestRouteList[indDpOut], avgMulticastList[indDpOut], avgMobileClientList[indDpOut], avgMobileClientList[indExpP], confBestRouteList[indDpOut], confMulticastList[indDpOut], confMobileClientList[indDpOut], confMobileClientList[indExpP])
  
  # avgNumberOfDataPacketsInSum with expected packets
  createBarChart.createBarChartComparePacketsOneMetric4Bars("The Number of Data Packets in at Consumer", "", "The number of packets", dstDirectory + "no_DPinC_exp.pdf", avgBestRouteList[indDpIn], avgMulticastList[indDpIn], avgMobileClientList[indDpIn], avgMobileClientList[indExpP], confBestRouteList[indDpIn], confMulticastList[indDpIn], confMobileClientList[indDpIn], confMobileClientList[indExpP])
  
  
  
  #---------------------------------------------------------------
  # create bar charts one metric - for all metrics (3 bars)
  #---------------------------------------------------------------
  
  # avgNumberOfPackets (expected)
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of expected Interest Packets or Data Packets", "", "The number of packets", dstDirectory + "no_expP.pdf", avgBestRouteList[indExpP], avgMulticastList[indExpP], avgMobileClientList[indExpP], confBestRouteList[indExpP], confMulticastList[indExpP], confMobileClientList[indExpP])
  
  # avgNumberOfInterestPacketsOutSum
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Interest Packets out at Consumer", "", "The number of packets", dstDirectory + "no_IPoutC.pdf", avgBestRouteList[indIpOut], avgMulticastList[indIpOut], avgMobileClientList[indIpOut], confBestRouteList[indIpOut], confMulticastList[indIpOut], confMobileClientList[indIpOut])
  
  # avgNumberOfInterestPacketsInSum
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Interest Packets in at Producer", "", "The number of packets", dstDirectory + "no_IPinP.pdf", avgBestRouteList[indIpIn], avgMulticastList[indIpIn], avgMobileClientList[indIpIn], confBestRouteList[indIpIn], confMulticastList[indIpIn], confMobileClientList[indIpIn])
  
  # avgNumberOfSatisfiedInterestPacketsInSum (not relevant)
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Satisfied Interest Packets out at Consumer", "", "The number of packets", dstDirectory + "no_satIPoutC.pdf", avgBestRouteList[indSatIpOut], avgMulticastList[indSatIpOut], avgMobileClientList[indSatIpOut], confBestRouteList[indSatIpOut], confMulticastList[indSatIpOut], confMobileClientList[indSatIpOut])
  
  # avgNumberOfDataPacketsOutSum
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Data Packets out at Producer", "", "The number of packets", dstDirectory + "no_DPoutP.pdf", avgBestRouteList[indDpOut], avgMulticastList[indDpOut], avgMobileClientList[indDpOut], confBestRouteList[indDpOut], confMulticastList[indDpOut], confMobileClientList[indDpOut])
  
  # avgNumberOfDataPacketsInSum
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Data Packets in at Consumer", "", "The number of packets", dstDirectory + "no_DPinC.pdf", avgBestRouteList[indDpIn], avgMulticastList[indDpIn], avgMobileClientList[indDpIn], confBestRouteList[indDpIn], confMulticastList[indDpIn], confMobileClientList[indDpIn]) 
  
  # avgRetransmissions
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Retransmitted Data Packets", "", "The number of packets", dstDirectory + "no_RetrDP.pdf", avgBestRouteList[indRetrDP], avgMulticastList[indRetrDP], avgMobileClientList[indRetrDP], confBestRouteList[indRetrDP], confMulticastList[indRetrDP], confMobileClientList[indRetrDP])
  
  # avgDuplicates
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Duplicate Data Packets", "", "The number of packets", dstDirectory + "no_dupDP.pdf", avgBestRouteList[indDupDp], avgMulticastList[indDupDp], avgMobileClientList[indDupDp], confBestRouteList[indDupDp], confMulticastList[indDupDp], confMobileClientList[indDupDp])
  
  # avgReceivedPackets
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Received Data Packets without Duplicates", "", "The number of packets", dstDirectory + "no_recDP.pdf", avgBestRouteList[indRecDp], avgMulticastList[indRecDp], avgMobileClientList[indRecDp], confBestRouteList[indRecDp], confMulticastList[indRecDp], confMobileClientList[indRecDp])
  
  # avgMissingPackets
  createBarChart.createBarChartCompareOneMetric3Bars("The Number of Missed Data Packets", "", "The number of packets", dstDirectory + "no_missDP.pdf", avgBestRouteList[indMissDp], avgMulticastList[indMissDp], avgMobileClientList[indMissDp], confBestRouteList[indMissDp], confMulticastList[indMissDp], confMobileClientList[indMissDp])
  
  # avgLastDelay
  createBarChart.createBarChartCompareOneMetric3Bars("The Last Delay", "", "The delay in milliseconds (ms)", dstDirectory + "ms_lastDelay.pdf", avgBestRouteList[indLastDel], avgMulticastList[indLastDel], avgMobileClientList[indLastDel], confBestRouteList[indLastDel], confMulticastList[indLastDel], confMobileClientList[indLastDel])
  
  # avgFullDelay
  createBarChart.createBarChartCompareOneMetric3Bars("The Full Delay", "", "The delay in milliseconds (ms)", dstDirectory + "ms_fullDelay.pdf", avgBestRouteList[indFullDel], avgMulticastList[indFullDel], avgMobileClientList[indFullDel], confBestRouteList[indFullDel], confMulticastList[indFullDel], confMobileClientList[indFullDel])
  
  # avgTotalDelay (not relevant)
  createBarChart.createBarChartCompareOneMetric3Bars("The Total Delay", "", "The delay in seconds (sec)", dstDirectory + "sec_totalDelay.pdf", avgBestRouteList[indTotDel], avgMulticastList[indTotDel], avgMobileClientList[indTotDel], confBestRouteList[indTotDel], confMulticastList[indTotDel], confMobileClientList[indTotDel])
  
  # avgHopCount
  createBarChart.createBarChartCompareOneMetric3Bars("The Hop Count between Sending and Receiving a Packet", "", "The number of network hops", dstDirectory + "val_HopCount.pdf", avgBestRouteList[indHopC], avgMulticastList[indHopC], avgMobileClientList[indHopC], confBestRouteList[indHopC], confMulticastList[indHopC], confMobileClientList[indHopC])
  
  # avgIpOutOverhead
  createBarChart.createBarChartCompareOneMetric3Bars("Interest Packet Success Percentage of sent Interest Packets", "", "Interest Packet Success Percentage in %", dstDirectory + "ov_no_IPoutC.pdf", avgBestRouteList[indIpOutOv], avgMulticastList[indIpOutOv], avgMobileClientList[indIpOutOv], confBestRouteList[indIpOutOv], confMulticastList[indIpOutOv], confMobileClientList[indIpOutOv])
  
  # avgIpInOverhead
  createBarChart.createBarChartCompareOneMetric3Bars("Interest Packet Success Percentage of received Interest Packets", "", "Interest Packet Success Percentage in %", dstDirectory + "ov_no_IPinP.pdf", avgBestRouteList[indIpInOv], avgMulticastList[indIpInOv], avgMobileClientList[indIpInOv], confBestRouteList[indIpInOv], confMulticastList[indIpInOv], confMobileClientList[indIpInOv])
  
  # avgDpOutOverhead
  createBarChart.createBarChartCompareOneMetric3Bars("Data Packet Success Percentage of sent Data Packets", "", "Data Packet Success Percentage in %", dstDirectory + "ov_no_DPoutP.pdf", avgBestRouteList[indDpOutOv], avgMulticastList[indDpOutOv], avgMobileClientList[indDpOutOv], confBestRouteList[indDpOutOv], confMulticastList[indDpOutOv], confMobileClientList[indDpOutOv])
  
  # avgDpInOverhead
  createBarChart.createBarChartCompareOneMetric3Bars("Data Packet Success Percentage of received Data Packets", "", "Data Packet Success Percentage in %", dstDirectory + "ov_no_DPinC.pdf", avgBestRouteList[indDpOutByOv], avgMulticastList[indDpOutByOv], avgMobileClientList[indDpOutByOv], confBestRouteList[indDpOutByOv], confMulticastList[indDpOutByOv], confMobileClientList[indDpOutByOv])
  
  # avgIsr
  createBarChart.createBarChartCompareOneMetric3Bars("Interest Satisfaction Ratio (ISR)", "", "ISR in %", dstDirectory + "perc_ISR.pdf", avgBestRouteList[indIsr], avgMulticastList[indIsr], avgMobileClientList[indIsr], confBestRouteList[indIsr], confMulticastList[indIsr], confMobileClientList[indIsr])
  
  # avgDpErrorRate
  createBarChart.createBarChartCompareOneMetric3Bars("Data Packet Error Rate", "", "Data Packet Error Rate [0, 1]", dstDirectory + "val_DPErrorRate.pdf", avgBestRouteList[indErrR], avgMulticastList[indErrR], avgMobileClientList[indErrR], confBestRouteList[indErrR], confMulticastList[indErrR], confMobileClientList[indErrR])
  
  # avgMos
  createBarChart.createBarChartCompareOneMetric3Bars("Estimated Mean Opinion Score (MOS-CQE)", "", "MOS-CQE [1, 4.35]", dstDirectory + "val_MOS.pdf", avgBestRouteList[indMos], avgMulticastList[indMos], avgMobileClientList[indMos], confBestRouteList[indMos], confMulticastList[indMos], confMobileClientList[indMos])






# ========== MAIN PROGRAM ==========
if __name__== "__main__":
  main()



