# calculateMetrics.py

# import
import sys
import os.path



# ===== usage =====
# Usage: python calculateMetrics.py <path_to_files> 
# For instance: python calculateMetrics.py "multicast_noAPs_3_xPos_20_yPosNext_-40/run_0/"
# <path_to_files> is optional, use <path_to_files> when the files are not located in the current folder
usage = "Usage: calculateMetrics.py <path_to_files> \nYou can specify the path to the files as the first argument when the files are not located in the current folder."






# ===== filenames for traces =====
fileDir = ""
filenameRateTrace = "rate-trace.txt"
filenameAppDelaysTrace = "app-delays-trace.txt"
filenameCallLengths = "callLengths.txt"
filenameAverageValues = "averageValues.txt"






# ===== scenario parameters =====
scenario = "big-mobile-voice-scenario"
interestsPerSecond = 100
dataPacketPayloadSize = 82
simulationSeconds = 300






# ===== define custom lists =====
# client/consumer
clientNodesList = list()

# server/producer
serverNodesList = list()

# voicemail message duration
callDurationsList = list()

# number of packets and number of total bytes
numberOfInterestOrDataPacketsList = list()
numberOfTotalDataPacketBytesList = list()






# ===== filter data - define lists for data =====
# rateTrace
rateTraceList = list()
rateTraceListInterestPacketsOutC = list() # interest packets OUT at all clients
rateTraceListSatisfiedInterestPacketsOutC = list() # satisfied interest packets OUT at all client
rateTraceListInterestPacketsInS = list() # interest packets IN at all servers
rateTraceListSatisfiedInterestPacketsInS = list() # satisfied interest packets IN at all servers
rateTraceListDataPacketsOutS = list() # data packets OUT at all servers
rateTraceListDataPacketsInC = list() # data packets IN at all clients

#appDelayTrace
appDelayTraceList = list()
appDelayTraceRetransmissions = list()
appDelayTraceAllReceivedSeqNoList = list()

#callLengths
callLengthsList = list()






# ===== calculate data - define variables for calculated data for each client =====

# number of packets
numberOfInterestPacketsOutSumList = list()
#numberOfSatisfiedInterestPacketsOutSumList = list() # TODO: BUG!
numberOfInterestPacketsInSumList = list()
numberOfSatisfiedInterestPacketsInSumList = list()
numberOfDataPacketsOutSumList = list()
numberOfDataPacketsInSumList = list()

# packet bytes
interestPacketBytesOutSumList = list()
interestPacketBytesInSumList = list()
dataPacketBytesOutSumList = list()
dataPacketBytesInSumList = list()

# retransmitted packets
numberOfRetransmissionsSumList = list()

# duplicate packets
duplicatePacketsList = list()

# received data packets
numberOfReceivedPacketsList = list()

# missing data packets
numberOfMissingPacketsList = list()

# delay
averageLastDelayList = list()
averageLastDelayInFormatList = list()
averageFullDelayList = list()
averageFullDelayInFormatList = list()
totalDelayList = list()
totalDelayInFormatList = list()

# hop count
averageHopCountList = list()

# overhead
ipOutOverheadList = list()
ipInOverheadList = list()
dpOutOverheadList = list()
dpInOverheadList = list()
dpOutBytesOverheadList = list()
dpInBytesOverheadList = list()

# ISR
isrList = list()

# error rate
errorRateList = list()

# MOS
mosList = list()






# ===== Print functions =====

# ===== printConfiguration() =====
#
# prints the configuration for the scenario
def printConfiguration():
  print "scenario:"
  print scenario
  print "interestsPerSecond:"
  print interestsPerSecond
  print "dataPacketPayloadSize:"
  print dataPacketPayloadSize
  print "simulationSeconds:"
  print simulationSeconds
  print "numberOfClients:"
  print len(clientNodesList)



# ===== printList() =====
#
# prints a list
def printList(listname, listToPrint):
  print "===== "+listname+" ====="
  for i in listToPrint:
    print i



# ===== printListOfLists() =====
#
# prints a list of lists
def printListOfLists(listname, listToPrint):
  print "===== "+listname+" ====="
  for i in listToPrint:
    for j in i:
      print j
    print " "



# ===== printCustomLists() =====
#
# prints the custom lists
def printCustomLists(isPrintingCallLengthsList):
  if (isPrintingCallLengthsList == False):
    print "len(callLengthsList) "+str(len(callLengthsList))
  else:
    print "len(callLengthsList) "+str(len(callLengthsList))
    printListOfLists("callLengthsList", callLengthsList)



# ===== printTraceLists() =====
#
# prints the trace lists
def printTraceLists(isPrintingTraceList, isPrintingAppDelayList):
  if (isPrintingTraceList == False):
    print "len(rateTraceList) "+str(len(rateTraceList))
  else:
    print "len(rateTraceList) "+str(len(rateTraceList))
    printListOfLists("rateTraceList", rateTraceList)
  
  if (isPrintingAppDelayList == False):
    print "len(appDelayTraceList) "+str(len(appDelayTraceList))
    print "len(appDelayTraceList)/2 "+str(len(appDelayTraceList)/2)+" (# of received data packets)"
  else:
    print "len(appDelayTraceList) "+str(len(appDelayTraceList))
    print "len(appDelayTraceList)/2 "+str(len(appDelayTraceList)/2)+" (# of received data packets)"
    printListOfLists("appDelayTraceList", appDelayTraceList)



# ===== printSpecificCustumLists() =====
#
# prints the specific custom lists - client nodes, server nodes, call durations, number of IPs or DPs, DP bytes
def printSpecificCustumLists(isPrintingClientNodes, isPrintingServerNodes, isPrintingCallDurations, isPrintingNoOfInterestOrDataPackets, isPrintingNoOfTotalDataPacketBytesList):
  if (isPrintingClientNodes == False):
    print "len(clientNodesList) "+str(len(clientNodesList))
  else:
    print "len(clientNodesList) "+str(len(clientNodesList))
    printList("clientNodesList", clientNodesList)
  
  if (isPrintingServerNodes == False):
    print "len(serverNodesList) "+str(len(serverNodesList))
  else:
    print "len(serverNodesList) "+str(len(serverNodesList))
    printList("serverNodesList", serverNodesList)
  
  if (isPrintingCallDurations == False):
    print "len(callDurationsList) "+str(len(callDurationsList))
  else:
    print "len(callDurationsList) "+str(len(callDurationsList))
    printList("callDurationsList", callDurationsList)
  
  if (isPrintingNoOfInterestOrDataPackets == False):
    print "len(numberOfInterestOrDataPacketsList) "+str(len(numberOfInterestOrDataPacketsList))
  else:
    print "len(numberOfInterestOrDataPacketsList) "+str(len(numberOfInterestOrDataPacketsList))
    printList("numberOfInterestOrDataPacketsList", numberOfInterestOrDataPacketsList)
  
  if (isPrintingNoOfTotalDataPacketBytesList == False):
    print "len(numberOfTotalDataPacketBytesList) "+str(len(numberOfTotalDataPacketBytesList))
  else:
    print "len(numberOfTotalDataPacketBytesList) "+str(len(numberOfTotalDataPacketBytesList))
    printList("numberOfTotalDataPacketBytesList", numberOfTotalDataPacketBytesList)



# ===== printSpecificTraceLists() =====
#
# prints the specific trace lists - IPs out at C, satisfied IPs out at C, IPs in at S, satisfied IPs in at S, DPs out at S, DPs in at C, retransmissions
def printSpecificTraceLists(isPrintingIpOutC, isPrintingSatIpOutC, isPrintingIpInS, isPrintingSatIpInS, isPrintingDpOutS, isPrintingDpInC, isPrintingRetransmitted):
  if (isPrintingIpOutC == False):
    print "len(rateTraceListInterestPacketsOutC) "+str(len(rateTraceListInterestPacketsOutC))
  else:
    print "len(rateTraceListInterestPacketsOutC) "+str(len(rateTraceListInterestPacketsOutC))
    printListOfLists("rateTraceListInterestPacketsOutC", rateTraceListInterestPacketsOutC)
  
  if (isPrintingSatIpOutC == False):
    print "len(rateTraceListSatisfiedInterestPacketsOutC) "+str(len(rateTraceListSatisfiedInterestPacketsOutC))
  else:
    print "len(rateTraceListSatisfiedInterestPacketsOutC) "+str(len(rateTraceListSatisfiedInterestPacketsOutC))
    printListOfLists("rateTraceListSatisfiedInterestPacketsOutC", rateTraceListSatisfiedInterestPacketsOutC)
  
  if (isPrintingIpInS == False):
    print "len(rateTraceListInterestPacketsInS) "+str(len(rateTraceListInterestPacketsInS))
  else:
    print "len(rateTraceListInterestPacketsInS) "+str(len(rateTraceListInterestPacketsInS))
    printListOfLists("rateTraceListInterestPacketsInS", rateTraceListInterestPacketsInS)
  
  if (isPrintingSatIpInS == False):
    print "len(rateTraceListSatisfiedInterestPacketsInS) "+str(len(rateTraceListSatisfiedInterestPacketsInS))
  else:
    print "len(rateTraceListSatisfiedInterestPacketsInS) "+str(len(rateTraceListSatisfiedInterestPacketsInS))
    printListOfLists("rateTraceListSatisfiedInterestPacketsInS", rateTraceListSatisfiedInterestPacketsInS)
  
  if (isPrintingDpOutS == False):
    print "len(rateTraceListDataPacketsOutS) "+str(len(rateTraceListDataPacketsOutS))
  else:
    print "len(rateTraceListDataPacketsOutS) "+str(len(rateTraceListDataPacketsOutS))
    printListOfLists("rateTraceListDataPacketsOutS", rateTraceListDataPacketsOutS)
  
  if (isPrintingDpInC == False):
    print "len(rateTraceListDataPacketsInC) "+str(len(rateTraceListDataPacketsInC))
  else:
    print "len(rateTraceListDataPacketsInC) "+str(len(rateTraceListDataPacketsInC))
    printListOfLists("rateTraceListDataPacketsInC", rateTraceListDataPacketsInC)
  
  if (isPrintingRetransmitted == False):
    print "len(appDelayTraceRetransmissions) "+str(len(appDelayTraceRetransmissions))
  else:
    print "len(appDelayTraceRetransmissions) "+str(len(appDelayTraceRetransmissions))
    printListOfLists("appDelayTraceRetransmissions", appDelayTraceRetransmissions)



# ===== printNumberOfPackets() =====
#
# prints the number of specific packets from the rate trace - IPs expected, IPs out at C, satisfied IPs out at C, IPs in at S, satisfied IPs in at S, DPs expected, DPs out at S and DPs in at C
def printNumberOfPackets(i):
  print "# PACKETS:"
  print "Number of === Interest Packets === EXPECTED OUT and IN: "+str(numberOfInterestOrDataPacketsList[i])
  print "Number of === Interest Packets === OUT at all clients: "+str(numberOfInterestPacketsOutSumList[i])
  #print "Number of === Interest Packets === SATISFIED OUT at all clients: "+str(numberOfSatisfiedInterestPacketsOutSumList[i])+" (BUG!)" # TODO: BUG!
  print "Number of === Interest Packets === IN at all servers: "+str(numberOfInterestPacketsInSumList[i])
  print "Number of === Interest Packets === SATISFIED IN at all servers: "+str(numberOfSatisfiedInterestPacketsInSumList[i])
  print "Number of === Data Packets === EXPECTED OUT and IN: "+str(numberOfInterestOrDataPacketsList[i])
  print "Number of === Data Packets === OUT at all servers: "+str(numberOfDataPacketsOutSumList[i])
  print "Number of === Data Packets === IN at all clients: "+str(numberOfDataPacketsInSumList[i])



# ===== printPacketBytes() =====
#
# prints specific packet bytes from the rate trace - IPs expected, IPs out at C, IPs in at S, DPs expected, DPs out at S, DPs in at C
def printPacketBytes(i):
  print "BYTES:"
  print "Bytes === Interest Packet === EXPECTED OUT and IN: X"
  print "Bytes === Interest Packets === OUT at all clients: "+str(interestPacketBytesOutSumList[i])
  print "Bytes === Interest Packets === IN at all servers: "+str(interestPacketBytesInSumList[i])
  print "Bytes === Data Packets === EXPECTED OUT and IN: "+str(numberOfTotalDataPacketBytesList[i])
  print "Bytes === Data Packets === OUT at all servers: "+str(dataPacketBytesOutSumList[i])
  print "Bytes === Data Packets === IN at all clients: "+str(dataPacketBytesInSumList[i])



# ===== printRetransmittedPackets() =====
#
# prints the retransmitted packets
def printRetransmittedPackets(i):
  print "RETRANSMITTED PACKETS:"
  print "Number of === Packets === retransmitted: "+str(numberOfRetransmissionsSumList[i])



# ===== printDuplicatePacketsAndReceivedPackets() =====
#
# prints dupicate packets
def printDuplicatePacketsAndReceivedPackets(i):
  print "DUPLICATE Data Packets and RECEIVED Data Packets:"
  print "Number of === Data Packets === IN at all clients: "+str(numberOfDataPacketsInSumList[i])
  print "Number of === Data Packets === in AppDelayTrace List RECEIVED IN at all clients: "+str(numberOfReceivedPacketsList[i])
  print "Number of === Data Packets === DUPLICATES IN at all clients: "+str(duplicatePacketsList[i])



# ===== printMissingPackets() =====
#
# prints missing packets
def printMissingPackets(i):
  print "Missing packets:"
  print "The number of missing packets: " + str(numberOfMissingPacketsList[i])



# ===== printDelay() =====
#
# prints the average delay in milliseconds, the average delay in format (h, m, s, ms, micros), the total delay in seconds and the total delay in format (h, m, s, ms, micros)
def printDelay(i):
  print "DELAY:"
  print "Average last Delay in milliseconds: "+str(averageLastDelayList[i])
  print "Average last Delay in format: "+averageLastDelayInFormatList[i]
  print "Average full Delay in milliseconds: "+str(averageFullDelayList[i])
  print "Average full Delay in format: "+averageFullDelayInFormatList[i]
  print "Total Delay in seconds: "+str(totalDelayList[i])
  print "Total Delay in format: "+totalDelayInFormatList[i]



# ===== printHopCount() =====
#
# prints the average hop count
def printHopCount(i):
  print "HOP COUNT:"
  print "Average hop count between client and server: "+str(averageHopCountList[i])



# ===== printAllPacketsOverheads() =====
#
# prints the overhead in percentage, the overhead of IPs out, IPs in, DPs out and DPs in
def printAllPacketsOverheads(i):
  print "OVERHEAD (# Packets):"
  print "Number of === Interest Packets Out === Overhead: "+str(ipOutOverheadList[i])+"%"
  print "Number of === Interest Packets In === Overhead: "+str(ipInOverheadList[i])+"%"
  print "Number of === Data Packets Out === Overhead: "+str(dpOutOverheadList[i])+"%"
  print "Number of === Data Packets In === Overhead: "+str(dpInOverheadList[i])+"%"



# ===== printAllPacketBytesOverheads() =====
#
# prints the overhead in percentage, the overhead of DP bytes out and DP bytes in
def printAllPacketBytesOverheads(i):
  print "OVERHEAD (Bytes):"
  print "Bytes === Data Packets Out === Overhead: "+str(dpOutBytesOverheadList[i])+"%"
  print "Bytes === Data Packets In === Overhead: "+str(dpInBytesOverheadList[i])+"%"



# ===== printISR() =====
#
# prints the interest satisfaction ratio (ISR)
def printISR(i):
  print "ISR:"
  print "Number of === Interest Packets === which are satisfied through a Data Packet: "+str(isrList[i])+"%"



# ===== printErrorRate() =====
#
# prints the error rate for the MOS
def printErrorRate(i):
  print "Error rate:"
  print "The error rate is: " + str(errorRateList[i])



# ===== printMOS() =====
#
# prints the mean opinion score (MOS)
def printMOS(i):
  print "MOS:"
  print "The MOS is: "+str(mosList[i])






# ===== Read functions for custom files and trace files =====

# ===== readCustomFiles() =====
#
# reads the custom files
def readCustomFiles():
  readCallLengthsFile(fileDir+filenameCallLengths, callLengthsList)



# ===== custom - readCallLengthsFile() =====
#
# reads the file and stores the data into a list
def readCallLengthsFile(filename, dataList):
  # reads the whole file (callLengths.txt) line by line
  if os.path.isfile(filename):
    with open(filename) as txtFile:
      for line in txtFile:
        
        # split and print line entries
        lineLength = len(line.split("\t"))
        if lineLength == 3:
          
          # split line into vars     
          mobileClient, fixedClient, callDuration = line.split("\t")
          callDuration = callDuration.replace('\n','')
          
          # add data to tmpList and to the specific trace list
          tmpList = list()
          tmpList.append(mobileClient)
          tmpList.append(fixedClient)
          tmpList.append(callDuration)
          dataList.append(tmpList)
          tmpList = []
  else:
    print "Terminated. The file "+filename+" does not exist."
    print usage
    sys.exit()



# ===== readTraceFiles() =====
#
# reads the trace files
def readTraceFiles():
  readRateTraceFile(fileDir+filenameRateTrace, rateTraceList)
  readAppDelayTraceListFile(fileDir+filenameAppDelaysTrace, appDelayTraceList)



# ===== trace - readRateTraceFile() =====
#
# reads the file and stores the data into a list
def readRateTraceFile(filename, dataList):
  # reads the whole file (rate-trace.txt) line by line
  if os.path.isfile(filename):
    with open(filename) as txtFile:
      for line in txtFile:
        
        # split and print line entries
        lineLength = len(line.split("\t"))
        if lineLength == 9:
          
          # split line into vars     
          time, node, faceId, faceDescr, dataType, packets, kilobytes, packetRaw, kilobytesRaw = line.split("\t")
          kilobytesRaw = kilobytesRaw.replace('\n','')
          
          # add data to tmpList and to the specific trace list
          tmpList = list()
          tmpList.append(time)
          tmpList.append(node)
          tmpList.append(faceId)
          tmpList.append(faceDescr)
          tmpList.append(dataType)
          tmpList.append(packets)
          tmpList.append(kilobytes)
          tmpList.append(packetRaw)
          tmpList.append(kilobytesRaw)
          dataList.append(tmpList)
          tmpList = []
  else:
    print "Terminated. The file "+filename+" does not exist."
    print usage
    sys.exit()



# ===== trace - readAppDelayTraceListFile() =====
#
# reads the file and stores the data into a list
def readAppDelayTraceListFile(filename, dataList):
  # reads the whole file (app-delays-trace.txt) line by line
  if os.path.isfile(filename):
    with open(filename) as txtFile:
      for line in txtFile:
        
        # split and print line entries
        lineLength = len(line.split("\t"))
        if lineLength == 9:
          
          # split line into vars     
          time, node, appId, seqNo, dataType, delayS, delayUS, retxCount, hopCount = line.split("\t")
          hopCount = hopCount.replace('\n','')
          
          # add data to tmpList and to the specific trace list
          tmpList = list()
          tmpList.append(time)
          tmpList.append(node)
          tmpList.append(appId)
          tmpList.append(seqNo)
          tmpList.append(dataType)
          tmpList.append(delayS)
          tmpList.append(delayUS)
          tmpList.append(retxCount)
          tmpList.append(hopCount)
          dataList.append(tmpList)
          tmpList = []
  else:
    print "Terminated. The file "+filename+" does not exist."
    print usage
    sys.exit()






# ===== Filter functions for custom files and trace files =====

# ===== custom - setSpecificCustomLists() =====
#
# sets specific lists - client nodes , server nodes, call durations, number of IPs or DPs and number of total DP bytes
def setSpecificCustomLists():
  for i in callLengthsList:
    clientNodesList.append(i[0])
    serverNodesList.append(i[1])
    callDurationsList.append(i[2])
    noOfPackets = interestsPerSecond * int(i[2])
    numberOfInterestOrDataPacketsList.append(noOfPackets)
    numberOfTotalDataPacketBytesList.append(noOfPackets * dataPacketPayloadSize)



# ===== rateTrace - setRateTraceListPackets() =====
#
# sets specific packets (Data Packets, Interest Packets, ...)
def setRateTraceListPackets(traceList, specificTraceList, node, face, packetType):
  for i in traceList: # List of Lists (lines)
    if (i[1] == node and i[3].startswith(face) and i[4] == packetType and i[7] != "0"):
      specificTraceList.append(i)



# ===== rateTrace - setRateTraceListPacketsMoreNodes() =====
#
# sets specific packets (Data Packets, Interest Packets, ...)
def setRateTraceListPacketsMoreNodes(traceList, specificTraceList, nodes, face, packetType):
  for i in nodes: # list of nodes
    setRateTraceListPackets(traceList, specificTraceList, i, face, packetType)



# ===== setSpecificTraceLists() =====
#
# sets specific lists - IPs out at C, satisfied IPs out at C, IPs in at S, satisfied IPs in at S, DPs out at S, DPs in at C and retransmissions
def setSpecificTraceLists():
  setRateTraceListPacketsMoreNodes(rateTraceList, rateTraceListInterestPacketsOutC, clientNodesList, "netdev", "OutInterests")
  setRateTraceListPacketsMoreNodes(rateTraceList, rateTraceListSatisfiedInterestPacketsOutC, clientNodesList, "netdev", "OutSatisfiedInterests")
  setRateTraceListPacketsMoreNodes(rateTraceList, rateTraceListInterestPacketsInS, serverNodesList, "netdev", "InInterests")
  setRateTraceListPacketsMoreNodes(rateTraceList, rateTraceListSatisfiedInterestPacketsInS, serverNodesList, "netdev", "InSatisfiedInterests") 
  setRateTraceListPacketsMoreNodes(rateTraceList, rateTraceListDataPacketsOutS, serverNodesList, "netdev", "OutData")
  setRateTraceListPacketsMoreNodes(rateTraceList, rateTraceListDataPacketsInC, clientNodesList, "netdev", "InData")
  setAppDelayTraceRetransmissions(appDelayTraceList, appDelayTraceRetransmissions)



# ===== app delay trace - setAppDelayTraceRetransmissions() =====
#
# sets retransmissions
def setAppDelayTraceRetransmissions(traceList, specificTraceList):
  for i in traceList:
    if (i[7] != "RetxCount" and int(i[7]) > 1):
      specificTraceList.append(i)






# ===== Calculation functions - for specific clients =====

# ===== rateTrace - calcRateTraceListNumberOfPackets() =====
#
# calculates the number of packets (Data Packets or Interest Packets)
def calcRateTraceListNumberOfPackets(specificTraceList, nodeName):
  numberOfPacketsSum = 0  
  for i in specificTraceList:
   if (i[1] == nodeName):
     numberOfPacketsSum = numberOfPacketsSum + int(i[7])
  return numberOfPacketsSum



# ===== calculateNumberOfPackets() =====
#
# calculates the number of specific packets from the rate trace - IPs out at C, satisfied IPs out at C, IPs in at S, satisfied IPs in at S, DPs out at S and DPs in at C
def calculateNumberOfPackets(clientNodeName, serverNodeName):
  numberOfInterestPacketsOutSumList.append(calcRateTraceListNumberOfPackets(rateTraceListInterestPacketsOutC, clientNodeName))
  #numberOfSatisfiedInterestPacketsOutSumList.append(calcRateTraceListNumberOfPackets(rateTraceListSatisfiedInterestPacketsOutC, clientNodeName)) # TODO: BUG!
  numberOfInterestPacketsInSumList.append(calcRateTraceListNumberOfPackets(rateTraceListInterestPacketsInS, serverNodeName))
  numberOfSatisfiedInterestPacketsInSumList.append(calcRateTraceListNumberOfPackets(rateTraceListSatisfiedInterestPacketsInS, serverNodeName))
  numberOfDataPacketsOutSumList.append(calcRateTraceListNumberOfPackets(rateTraceListDataPacketsOutS, serverNodeName))
  numberOfDataPacketsInSumList.append(calcRateTraceListNumberOfPackets(rateTraceListDataPacketsInC, clientNodeName))



# ===== rateTrace - calcRateTraceListPacketBytes() =====
#
# calculates the bytes for all packets (Data Packets or Interest Packets)
def calcRateTraceListPacketBytes(specificTraceList, nodeName):
  packetBytesSum = 0.0  
  for i in specificTraceList:
   if (i[1] == nodeName):
     packetBytesSum = packetBytesSum + (float(i[8])*1024.0) # convert kilobytes to bytes (TODO: 1000 or 1024)
  return packetBytesSum



# ===== calculatePacketBytes() =====
#
# calculates specific packet bytes from the rate trace - IPs out at C, IPs in at S, DP out at S, DP in at C
def calculatePacketBytes(clientNodeName, serverNodeName):
  interestPacketBytesOutSumList.append(calcRateTraceListPacketBytes(rateTraceListInterestPacketsOutC, clientNodeName))
  interestPacketBytesInSumList.append(calcRateTraceListPacketBytes(rateTraceListInterestPacketsInS, serverNodeName))
  dataPacketBytesOutSumList.append(calcRateTraceListPacketBytes(rateTraceListDataPacketsOutS, serverNodeName))
  dataPacketBytesInSumList.append(calcRateTraceListPacketBytes(rateTraceListDataPacketsInC, clientNodeName))



# ===== app delay trace - calcAppDelayTraceListNumberOfRetransmissions() =====
#
# calculates the number of retransmissions
def calcAppDelayTraceListNumberOfRetransmissions(specificTraceList, nodeName):
  numberOfRetransmissionsSum = 0
  for i in specificTraceList:
    if (i[1] == nodeName):
      if (int(i[7]) > 1):
        numberOfRetransmissionsSum = numberOfRetransmissionsSum + (int(i[7])-1)
  return numberOfRetransmissionsSum



# ===== calculateRetransmittedPackets() =====
#
# calculates the retransmitted packets
def calculateRetransmittedPackets(clientNodeName):
  numberOfRetransmissionsSumList.append(calcAppDelayTraceListNumberOfRetransmissions(appDelayTraceRetransmissions, clientNodeName))



# ===== app delay trace - calcAppDelayTraceListNumberOfReceivedPackets() =====
#
# calculates the number of received packets at the clients for instance for calculating the duplicate packets
def calcAppDelayTraceListNumberOfReceivedPackets(specificTraceList, nodeName):
  counter = 0
  for i in specificTraceList:
    if (i[1] == nodeName):
      if (i[4] == "FullDelay"):
        counter = counter + 1
  return counter



# ===== app delay trace - calcAppDelayTraceListAllReceivedSeqNo() =====
#
# calculates the sequence numbers of received packets at the clients for instance for calculating the MOS
def calcAppDelayTraceListAllReceivedSeqNo(specificTraceList, nodeName):
  receivedSeqNoList = list()
  for i in specificTraceList:
    if (i[1] == nodeName):
      if (i[4] == "FullDelay"):
        receivedSeqNoList.append(int(i[3]))
  receivedSeqNoList.sort()
  return receivedSeqNoList



# ===== app delay trace - calculateMissingPackets() =====
#
# calculates the number of missing packets at the clients for instance for calculating the error rate for the MOS
def calculateMissingPackets(i):
  noOfReceivedDataPackets = numberOfReceivedPacketsList[i]
  noOfExpectedDataPackets = numberOfInterestOrDataPacketsList[i]
  missing = noOfExpectedDataPackets - noOfReceivedDataPackets
  numberOfMissingPacketsList.append(missing)



# ===== calculateDuplicatePacketsAndReceivedPackets() =====
#
# calculates dupicate packets
def calculateDuplicatePacketsAndReceivedPackets(clientNodeName, i):
  received = calcAppDelayTraceListNumberOfReceivedPackets(appDelayTraceList, clientNodeName)
  numberOfReceivedPacketsList.append(received)
  duplicatePacketsList.append(numberOfDataPacketsInSumList[i] - received)



# ===== app delay trace - calcAppDelayTraceListAverageDelay() =====
#
# calculates the average delay in milliseconds
def calcAppDelayTraceListAverageDelay(specificTraceList, nodeName, delayName):
  delayInSecondsSum = 0.0
  counter = 0
  for i in specificTraceList:
    if (i[1] == nodeName):
      if (i[4] == delayName):
        delayInSecondsSum = delayInSecondsSum + float(i[5])
        counter = counter + 1
  if (counter != 0):
    delayInSecondsSum = delayInSecondsSum / counter
  delayInMillisecondsSum = delayInSecondsSum * 1000
  return delayInMillisecondsSum



# ===== app delay trace - calcAppDelayTraceListTotalDelay() =====
#
# calculates the total delay in seconds
def calcAppDelayTraceListTotalDelay(specificTraceList, nodeName):
  delayInSecondsSum = 0.0
  for i in specificTraceList:
    if (i[1] == nodeName):
      if (i[4] == "FullDelay"):
        delayInSecondsSum = delayInSecondsSum + float(i[5])
  return delayInSecondsSum



# ===== calculateDelay() =====
#
# calculates the average delay in milliseconds, the average delay in format (h, m, s, ms, micros), the total delay in seconds and the total delay in format (h, m, s, ms, micros)
def calculateDelay(clientNodeName):
  avgLastDelay = calcAppDelayTraceListAverageDelay(appDelayTraceList, clientNodeName, "LastDelay")
  averageLastDelayList.append(avgLastDelay)
  averageLastDelayInFormatList.append(calcSecondsInFormat(avgLastDelay/1000))
  avgFullDelay = calcAppDelayTraceListAverageDelay(appDelayTraceList, clientNodeName, "FullDelay")
  averageFullDelayList.append(avgFullDelay)
  averageFullDelayInFormatList.append(calcSecondsInFormat(avgFullDelay/1000))
  totDelay = calcAppDelayTraceListTotalDelay(appDelayTraceList, clientNodeName)
  totalDelayList.append(totDelay)
  totalDelayInFormatList.append(calcSecondsInFormat(totDelay))



# ===== app delay trace - calcSecondsInFormat() =====
#
# converts seconds into hours, minutes, seconds, milliseconds and microseconds
def calcSecondsInFormat(totalSeconds):
  hours = int(totalSeconds / 60 / 60)
  minutes = int(totalSeconds / 60) - (hours * 60)
  seconds = int (totalSeconds) - (hours * 60 * 60) - (minutes *60)
  milliseconds = int((totalSeconds - (hours * 60 * 60) - (minutes * 60) - seconds) * 1000)
  microseconds = int((((totalSeconds - (hours * 60 * 60) - (minutes * 60) - seconds) * 1000) - milliseconds) * 1000)
  # return format as string
  return str(hours)+"h "+str(minutes)+"m "+str(seconds)+"s "+str(milliseconds)+"ms "+str(microseconds)+"micros"



# ===== calculateHopCount() =====
#
# calculates the average hop count
def calculateHopCount(clientNodeName):
  hopCount = calcAppDelayTraceListHopCount(appDelayTraceList, clientNodeName)
  averageHopCountList.append(hopCount)



# ===== app delay trace - calcAppDelayTraceListHopCount() =====
#
# calculates the hop count between clients and servers
def calcAppDelayTraceListHopCount(specificTraceList, nodeName):
  hopCountSum = 0
  numberOfEntries = 0
  averageHopCount = 0
  for i in specificTraceList:
    if (i[1] == nodeName):
      hopCountSum = hopCountSum + (int(i[8]))
      numberOfEntries = numberOfEntries + 1
  if (numberOfEntries != 0):
    averageHopCount = hopCountSum / numberOfEntries
  return averageHopCount



# ===== metrics - calculateOverhead() =====
#
# calculates the overhead in percentage
def calculateOverhead(expected, received):
  overhead100Percent = float(expected) # 100% overhead  
  overhead1Percent = float(overhead100Percent / 100)	# 1% overhead
  totalOverhead = float(received / overhead1Percent)
  return totalOverhead



# ===== metrics - calculateAllPacketsOverheads() =====
#
# calculates the overhead in percentage - the overhead of IPs out, IPs in, DPs out and DPs in
def calculateAllPacketsOverheads(numberOfPackets, numberOfIpOutSum, numberOfIpInSum, numberOfDpOutSum, numberOfDpInSum):
  ipOutOverheadList.append(calculateOverhead(numberOfPackets, numberOfIpOutSum))
  ipInOverheadList.append(calculateOverhead(numberOfPackets, numberOfIpInSum))
  dpOutOverheadList.append(calculateOverhead(numberOfPackets, numberOfDpOutSum))
  dpInOverheadList.append(calculateOverhead(numberOfPackets, numberOfDpInSum))



# ===== metrics - calculateAllBytesOverheads() =====
#
# calculates the overhead in percentage - the overhead of DP bytes out and DP bytes in
def calculateAllBytesOverheads(numberOfBytes, dpBytesOutSum, dpBytesInSum):
  dpOutBytesOverheadList.append(calculateOverhead(numberOfBytes, dpBytesOutSum))
  dpInBytesOverheadList.append(calculateOverhead(numberOfBytes, dpBytesInSum))



# ===== metrics - calculateISR() =====
#
# calculates the interest satisfaction ratio (ISR)
def calculateISR(numberOfInterests, numberOfSatisfiedInterests):
  isrList.append(float(float(numberOfSatisfiedInterests) / float(numberOfInterests)) * 100.0)



# ===== metrics - calculateReceivedSeqNos() =====
#
# calculates all sequence numbers of the received packets
def calculateReceivedSeqNos(clientNodeName):
  receivedSeqNoList = calcAppDelayTraceListAllReceivedSeqNo(appDelayTraceList, clientNodeName)
  appDelayTraceAllReceivedSeqNoList.append(receivedSeqNoList)



# ===== metrics - calculateErrorRate() =====
#
# calculates the error rate for the MOS (error rate = missing packets / total packets)
def calculateErrorRate(i):
  errorRate = float(float(numberOfMissingPacketsList[i]) / float(numberOfInterestOrDataPacketsList[i]))
  errorRateList.append(errorRate)



# ===== metrics - calculateMOS() =====
#
# calculates the mean opinion score (MOS)
def calculateMOS(noOfRequiredSeqNos, receivedSeqNoList, averageDelay, errorRate):
  # burstR
  burstR = calculateBurstRWith2StateMarkovModel(noOfRequiredSeqNos, receivedSeqNoList)
  
  # R
  R = calculateRValue(averageDelay, errorRate, burstR)

  # MOS
  meanOpinionScore = -1
  if R <= 0:
    meanOpinionScore = 1.0
  elif 0 < R < 100:
    meanOpinionScore = 1.0 + 0.035 * R + R * (R - 60.0) * (100.0 - R) * 7.0 * 10 ** -6 # 10^-6
  else:
    meanOpinionScore = 4.5
  
  mosList.append(meanOpinionScore)



# ===== metrics - calculateRValue() =====
#
# calculates the R value for the mean opinion score (MOS)
def calculateRValue(avgDelay, errorRate, burstR):
  # calculate d
  delayNetwork = avgDelay
  delayCodec = 0.25
  delayJitterBuffer = 50.0
  d = delayNetwork + delayCodec + delayJitterBuffer

  # calculate h(x) for I_d
  h = 0.0
  if (d - 177.3) >= 0:
    h = 1.0
  
  # calculate I_d
  I_d = 0.024 * d + 0.11 * (d - 177.3) * h

  # calculate I_e_eff
  I_e = 0.0
  P_pl = errorRate * 100.0
  B_pl = 34.0
  I_e_eff = I_e + (95.0 - I_e) * (P_pl / ((P_pl / burstR) + B_pl))

  # calculate R
  R = 93.2 - I_d - I_e_eff
  return R



# ===== metrics - calculateBurstRWith2StateMarkovModel() =====
#
# calculates the burstR for the mean opinion score (MOS)
def calculateBurstRWith2StateMarkovModel(noOfRequiredSeqNos, receivedSeqNoList):
  # counter variables to calculate the burstR
  noLossAfterNoLoss = 0
  lossAfterNoLoss = 0
  noLossAfterLoss = 0
  lossAfterLoss = 0
  
  # stores True if the last packet gets lost
  lastPacketIsLost = False
  
  # set of sequencenumbers of all received packets
  receivedSeqNoSet = set(receivedSeqNoList)
  
  for reqSeqNo in range(0, noOfRequiredSeqNos):
    if not lastPacketIsLost and reqSeqNo in receivedSeqNoSet:
      noLossAfterNoLoss = noLossAfterNoLoss + 1
    elif not lastPacketIsLost and reqSeqNo not in receivedSeqNoSet:
      lossAfterNoLoss = lossAfterNoLoss + 1
    elif lastPacketIsLost and reqSeqNo in receivedSeqNoSet:
      noLossAfterLoss = noLossAfterLoss + 1
    elif lastPacketIsLost and reqSeqNo not in receivedSeqNoSet:
      lossAfterLoss = lossAfterLoss + 1
    
    lastPacketIsLost = reqSeqNo not in receivedSeqNoSet
  
  # calculate burstR
  try:
    p = float(noLossAfterLoss / float(noLossAfterLoss + lossAfterLoss))
    q = float(lossAfterNoLoss / float(lossAfterNoLoss + noLossAfterNoLoss))
    burstR = float(1.0 / (p + q))
  except ZeroDivisionError:
    burstR = float(1)
  
  return burstR



# ===== calculateAllMetrics() =====
#
# calculates all relevant metrics for each client
def calculateAllMetrics(isPrintingAllMetrics):
  for i in range(0, len(clientNodesList)):
    print "== Voicemail message "+str(i)+" =="
    # calculate all metrics here
    
    # calculate number of packets
    calculateNumberOfPackets(clientNodesList[i], serverNodesList[i])
    if (isPrintingAllMetrics == True):
      printNumberOfPackets(i)
      print " "
    
    # calculate number of packet bytes
    calculatePacketBytes(clientNodesList[i], serverNodesList[i])
    if (isPrintingAllMetrics == True):
      printPacketBytes(i)
      print " "
    
    # calculate retransmitted packets
    calculateRetransmittedPackets(clientNodesList[i])
    if (isPrintingAllMetrics == True):
      printRetransmittedPackets(i)
      print " "
    
    # calculate duplicate packets and received packets
    calculateDuplicatePacketsAndReceivedPackets(clientNodesList[i], i)
    if (isPrintingAllMetrics == True):
      printDuplicatePacketsAndReceivedPackets(i)
      print " "
    
    # calculate missing packets for error rate of MOS
    calculateMissingPackets(i)
    if (isPrintingAllMetrics == True):
      printMissingPackets(i)
      print " "
    
    # calculate delay
    calculateDelay(clientNodesList[i])
    if (isPrintingAllMetrics == True):
      printDelay(i)
      print " "
    
    # calculate average hopcount or hop count
    calculateHopCount(clientNodesList[i])
    if (isPrintingAllMetrics == True):
      printHopCount(i)
      print " "
    
    # calculate overhead
    calculateAllPacketsOverheads(numberOfInterestOrDataPacketsList[i], numberOfInterestPacketsOutSumList[i], numberOfInterestPacketsInSumList[i], numberOfDataPacketsOutSumList[i], numberOfDataPacketsInSumList[i])
    calculateAllBytesOverheads(numberOfTotalDataPacketBytesList[i], dataPacketBytesOutSumList[i], dataPacketBytesInSumList[i])
    if (isPrintingAllMetrics == True):
      printAllPacketsOverheads(i)
      print " "
      printAllPacketBytesOverheads(i)
      print " "
    
    # calculate ISR
    calculateISR(numberOfInterestOrDataPacketsList[i], numberOfReceivedPacketsList[i])
    if (isPrintingAllMetrics == True):
      printISR(i)
      print " "
    
    # calculate received sequence numbers for MOS 
    calculateReceivedSeqNos(clientNodesList[i])
    
    # calculate error rate (missing packets + delayed packets / total packets)
    calculateErrorRate(i)
    if (isPrintingAllMetrics == True):
      printErrorRate(i)
      print " "
    
    # calculate MOS # TODO: use last-delay or full-delay
    calculateMOS(numberOfInterestOrDataPacketsList[i], appDelayTraceAllReceivedSeqNoList[i], averageFullDelayList[i], errorRateList[i])
    if (isPrintingAllMetrics == True):
      printMOS(i)
      print " "



# ===== Average functions - for all clients =====

# ===== calculateAverageValue() =====
#
# calculates the average value for some values
def calculateAverageValue(valueList):
  avgValue = 0
  for i in range(0, len(valueList)):
    avgValue = avgValue + valueList[i]
  avgValue = avgValue / len(valueList)
  return avgValue



# ===== calculateAveragesOfMetrics() =====
#
# calculates averages of metrics
def calculateAveragesOfMetrics(isPrintingMetrics):
  
  # expected number of packets
  avgNumberOfPackets = calculateAverageValue(numberOfInterestOrDataPacketsList)
  
  # number of packets
  avgNumberOfInterestPacketsOutSum = calculateAverageValue(numberOfInterestPacketsOutSumList)
  #avgNumberOfSatisfiedInterestPacketsOutSum = calculateAverageValue(numberOfSatisfiedInterestPacketsOutSumList) # TODO: BUG!
  avgNumberOfInterestPacketsInSum = calculateAverageValue(numberOfInterestPacketsInSumList)
  avgNumberOfSatisfiedInterestPacketsInSum = calculateAverageValue(numberOfSatisfiedInterestPacketsInSumList)
  avgNumberOfDataPacketsOutSum = calculateAverageValue(numberOfDataPacketsOutSumList)
  avgNumberOfDataPacketsInSum = calculateAverageValue(numberOfDataPacketsInSumList)
  
  # packet bytes
  avgInterestPacketBytesOutSum = calculateAverageValue(interestPacketBytesOutSumList)
  avgInterestPacketBytesInSum = calculateAverageValue(interestPacketBytesInSumList)
  avgDataPacketBytesOutSum = calculateAverageValue(dataPacketBytesOutSumList)
  avgDataPacketBytesInSum = calculateAverageValue(dataPacketBytesInSumList)
  
  # retransmitted packets
  avgRetransmissions = calculateAverageValue(numberOfRetransmissionsSumList)
  
  # duplicate packets
  avgDuplicates = calculateAverageValue(duplicatePacketsList)
  
  # received packets
  avgReceivedPackets = calculateAverageValue(numberOfReceivedPacketsList)
  
  # missing packets
  avgMissingPackets = calculateAverageValue(numberOfMissingPacketsList)
  
  # delay
  avgLastDelay = calculateAverageValue(averageLastDelayList)
  avgFullDelay = calculateAverageValue(averageFullDelayList)
  avgTotalDelay = calculateAverageValue(totalDelayList)
  
  # hop count
  avgHopCount = calculateAverageValue(averageHopCountList)
  
  # overhead
  avgIpOutOverhead = calculateAverageValue(ipOutOverheadList)
  avgIpInOverhead = calculateAverageValue(ipInOverheadList)
  avgDpOutOverhead = calculateAverageValue(dpOutOverheadList)
  avgDpInOverhead = calculateAverageValue(dpInOverheadList)
  avgDpOutBytesOverhead = calculateAverageValue(dpOutBytesOverheadList)
  avgDpInBytesOverhead = calculateAverageValue(dpInBytesOverheadList)
  
  # ISR
  avgIsr = calculateAverageValue(isrList)

  # error rate
  avgErrorRate = calculateAverageValue(errorRateList)
  
  # MOS
  avgMos = calculateAverageValue(mosList)
  
  
  
  # print averages of metrics
  if (isPrintingMetrics == True):
    print "avgNumberOfPackets " + str(avgNumberOfPackets)
    print "avgNumberOfInterestPacketsOutSum " + str(avgNumberOfInterestPacketsOutSum)
    #print "avgNumberOfSatisfiedInterestPacketsOutSum " + str(avgNumberOfSatisfiedInterestPacketsOutSum) # TODO: BUG!
    print "avgNumberOfInterestPacketsInSum " + str(avgNumberOfInterestPacketsInSum)
    print "avgNumberOfSatisfiedInterestPacketsInSum " + str(avgNumberOfSatisfiedInterestPacketsInSum)
    print "avgNumberOfDataPacketsOutSum " + str(avgNumberOfDataPacketsOutSum)
    print "avgNumberOfDataPacketsInSum " + str(avgNumberOfDataPacketsInSum)
    print "avgInterestPacketBytesOutSum " + str(avgInterestPacketBytesOutSum)
    print "avgInterestPacketBytesInSum " + str(avgInterestPacketBytesInSum)
    print "avgDataPacketBytesOutSum " + str(avgDataPacketBytesOutSum)
    print "avgDataPacketBytesInSum " + str(avgDataPacketBytesInSum)
    print "avgRetransmissions " + str(avgRetransmissions)
    print "avgDuplicates " + str(avgDuplicates)
    print "avgReceivedPackets " + str(avgReceivedPackets)
    print "avgMissingPackets " + str(avgMissingPackets)
    print "avgLastDelay " + str(avgLastDelay)
    print "avgFullDelay " + str(avgFullDelay)
    print "avgTotalDelay " + str(avgTotalDelay)
    print "avgHopCount " + str(avgHopCount)
    print "avgIpOutOverhead " + str(avgIpOutOverhead)
    print "avgIpInOverhead " + str(avgIpInOverhead)
    print "avgDpOutOverhead " + str(avgDpOutOverhead)
    print "avgDpInOverhead " + str(avgDpInOverhead)
    print "avgDpOutBytesOverhead " + str(avgDpOutBytesOverhead)
    print "avgDpInBytesOverhead " + str(avgDpInBytesOverhead)
    print "avgIsr " + str(avgIsr)
    print "avgErrorRate " + str(avgErrorRate)
    print "avgMos " + str(avgMos)
  
  
  
  # write average values into a file
  outputFile = open(fileDir+filenameAverageValues,"w")

  outputFile.write(str(avgNumberOfPackets)+"\t")
  
  outputFile.write(str(avgNumberOfInterestPacketsOutSum)+"\t")
  outputFile.write(str(avgNumberOfInterestPacketsInSum)+"\t")
  outputFile.write(str(avgNumberOfSatisfiedInterestPacketsInSum)+"\t")
  outputFile.write(str(avgNumberOfDataPacketsOutSum)+"\t")
  outputFile.write(str(avgNumberOfDataPacketsInSum)+"\t")
  
  outputFile.write(str(avgInterestPacketBytesOutSum)+"\t")
  outputFile.write(str(avgInterestPacketBytesInSum)+"\t")
  outputFile.write(str(avgDataPacketBytesOutSum)+"\t")
  outputFile.write(str(avgDataPacketBytesInSum)+"\t")
  
  outputFile.write(str(avgRetransmissions)+"\t")
  
  outputFile.write(str(avgDuplicates)+"\t")
  
  outputFile.write(str(avgReceivedPackets)+"\t")
  
  outputFile.write(str(avgMissingPackets)+"\t")
  
  outputFile.write(str(avgLastDelay)+"\t")
  outputFile.write(str(avgFullDelay)+"\t")
  outputFile.write(str(avgTotalDelay)+"\t")
  
  outputFile.write(str(avgHopCount)+"\t")
  
  outputFile.write(str(avgIpOutOverhead)+"\t")
  outputFile.write(str(avgIpInOverhead)+"\t")
  outputFile.write(str(avgDpOutOverhead)+"\t")
  outputFile.write(str(avgDpInOverhead)+"\t")
  outputFile.write(str(avgDpOutBytesOverhead)+"\t")
  outputFile.write(str(avgDpInBytesOverhead)+"\t")
  
  outputFile.write(str(avgIsr)+"\t")
  
  outputFile.write(str(avgErrorRate)+"\t")
  
  outputFile.write(str(avgMos))
  
  outputFile.close()






# ===== Other functions =====

# ===== setDirAndFiles() =====
#
# sets the direcotry and files
def setDirAndFiles(argv):
  # set file directory
  global fileDir
  if len(argv) == 2:
    fileDir = argv[1]



# ===== resetGlobalVariables() =====
#
# resets the global variables
def resetGlobalVariables():
  global clientNodesList
  clientNodesList = list()
  global serverNodesList
  serverNodesList = list()
  global callDurationsList
  callDurationsList = list()
  global numberOfInterestOrDataPacketsList
  numberOfInterestOrDataPacketsList = list()
  global numberOfTotalDataPacketBytesList
  numberOfTotalDataPacketBytesList = list()
  global rateTraceList
  rateTraceList = list()
  global rateTraceListInterestPacketsOutC
  rateTraceListInterestPacketsOutC = list()
  global rateTraceListSatisfiedInterestPacketsOutC
  rateTraceListSatisfiedInterestPacketsOutC = list()
  global rateTraceListInterestPacketsInS
  rateTraceListInterestPacketsInS = list()
  global rateTraceListSatisfiedInterestPacketsInS
  rateTraceListSatisfiedInterestPacketsInS = list()
  global rateTraceListDataPacketsOutS
  rateTraceListDataPacketsOutS = list()
  global rateTraceListDataPacketsInC
  rateTraceListDataPacketsInC = list()
  global appDelayTraceList
  appDelayTraceList = list()
  global appDelayTraceRetransmissions
  appDelayTraceRetransmissions = list()
  global appDelayTraceAllReceivedSeqNoList
  appDelayTraceAllReceivedSeqNoList = list()
  global callLengthsList
  callLengthsList = list()
  global numberOfInterestPacketsOutSumList
  numberOfInterestPacketsOutSumList = list()
  #global numberOfSatisfiedInterestPacketsOutSumList # TODO: BUG!
  #numberOfSatisfiedInterestPacketsOutSumList = list() # TODO: BUG!
  global numberOfInterestPacketsInSumList
  numberOfInterestPacketsInSumList = list()
  global numberOfSatisfiedInterestPacketsInSumList
  numberOfSatisfiedInterestPacketsInSumList = list()
  global numberOfDataPacketsOutSumList
  numberOfDataPacketsOutSumList = list()
  global numberOfDataPacketsInSumList
  numberOfDataPacketsInSumList = list()
  global interestPacketBytesOutSumList
  interestPacketBytesOutSumList = list()
  global interestPacketBytesInSumList
  interestPacketBytesInSumList = list()
  global dataPacketBytesOutSumList
  dataPacketBytesOutSumList = list()
  global dataPacketBytesInSumList
  dataPacketBytesInSumList = list()
  global numberOfRetransmissionsSumList
  numberOfRetransmissionsSumList = list()
  global duplicatePacketsList
  duplicatePacketsList = list()
  global numberOfReceivedPacketsList
  numberOfReceivedPacketsList = list()
  global numberOfMissingPacketsList
  numberOfMissingPacketsList = list()
  global averageLastDelayList
  averageLastDelayList = list()
  global averageLastDelayInFormatList
  averageLastDelayInFormatList = list()
  global averageFullDelayList
  averageFullDelayList = list()
  global averageFullDelayInFormatList
  averageFullDelayInFormatList = list()
  global totalDelayList
  totalDelayList = list()
  global totalDelayInFormatList
  totalDelayInFormatList = list()
  global averageHopCountList
  averageHopCountList = list()
  global ipOutOverheadList
  ipOutOverheadList = list()
  global ipInOverheadList
  ipInOverheadList = list()
  global dpOutOverheadList
  dpOutOverheadList = list()
  global dpInOverheadList
  dpInOverheadList = list()
  global dpOutBytesOverheadList
  dpOutBytesOverheadList = list()
  global dpInBytesOverheadList
  dpInBytesOverheadList = list()
  global isrList
  isrList = list()
  global errorRateList
  errorRateList = list()
  global mosList
  mosList = list()






# ===== MAIN function =====
#
# this is the main function
def main(argv):
  
  # set director and files
  setDirAndFiles(argv)
  
  
  
  print "===== Read (and print) trace files and custom files ====="
  readTraceFiles()
  isPrintingTraceList = False
  isPrintingAppDelayList = False
  printTraceLists(isPrintingTraceList, isPrintingAppDelayList)
  readCustomFiles()
  isPrintingCallLengthsList = False
  printCustomLists(isPrintingCallLengthsList)
  print " "
  
  
  
  print "===== Filter data (Interest Packets, Data Packets, Retransmissions ...) ====="
  setSpecificCustomLists()
  isPrintingClientNodes = False
  isPrintingServerNodes = False
  isPrintingCallDurations = False
  isPrintingNoOfInterestOrDataPackets = False
  isPrintingNoOfTotalDataPacketBytesList = False
  printSpecificCustumLists(isPrintingClientNodes, isPrintingServerNodes, isPrintingCallDurations, isPrintingNoOfInterestOrDataPackets, isPrintingNoOfTotalDataPacketBytesList)
  setSpecificTraceLists()
  isPrintingIpOutC = False
  isPrintingSatIpOutC = False
  isPrintingIpInS = False
  isPrintingSatIpInS = False
  isPrintingDpOutS = False
  isPrintingDpInC = False
  isPrintingRetransmitted = False
  printSpecificTraceLists(isPrintingIpOutC, isPrintingSatIpOutC, isPrintingIpInS, isPrintingSatIpInS, isPrintingDpOutS, isPrintingDpInC, isPrintingRetransmitted)
  print " "
  
  
  
  print "\n===== Configuration ====="
  printConfiguration()
  print " "
  
  
  
  print "===== Calculation of metrics (# of packets, bytes, retransmissions, duplicate packets, delay, overhead, ISR) ====="
  isPrintingAllMetrics = False
  calculateAllMetrics(isPrintingAllMetrics)
  print " "
  
  
  
  print "===== Calculation of averages (# of packets, bytes, retransmissions, duplicate packets, delay, hop count overhead, ISR) ====="
  isPrintingMetrics = True
  calculateAveragesOfMetrics(isPrintingMetrics)
  print " "
  
  
  
  # reset all global variables for the next runs
  resetGlobalVariables()






# ========== MAIN PROGRAM ==========
if __name__== "__main__":
  main(sys.argv)






