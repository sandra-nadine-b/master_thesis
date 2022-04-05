# createBarChart.py

# import
import os
import os.path

import numpy as np
import matplotlib.pyplot as plt



# used colors
colorBestRoute = "white"
colorMulticast = "lightgrey"
colorMobileClient = "grey"

colorExpected = "whitesmoke"

colorConf = "black"

colorLine = "crimson" # "cornflowerblue"

colorInvisibleLine = "white"

# used linestyle
line = "-"
pausedLine= "--"

# used hatch
# '/' - '' - '|' - '-' - '+' - 'x' - 'o' - 'O' - '.' - '*'
hatchBestRoute = "/"
hatchMulticast = "\\"
hatchMobileClient = "x"
hatchExpected = "-"

# legend
legendBestRoute = "Best-Route"
legendMulticast = "Multicast"
legendMobileClient = "Mobile-Client"
legendExpected = "Expected Number of Packets"

legendIsr10 = "ISR Threshold 10%"
legendIsr20 = "ISR Threshold 20%"
legendIsr30 = "ISR Threshold 30%"
legendIsr40 = "ISR Threshold 40%"
legendIsr50 = "ISR Threshold 50%"
legendIsr60 = "ISR Threshold 60%"
legendIsr70 = "ISR Threshold 70%"
legendIsr80 = "ISR Threshold 80%"
legendIsr90 = "ISR Threshold 90%"

# legend location
legendLocBest = "best"

# rotation
rotationVertical = "vertical"
# names
mos = "MOS"
meanOpinionScore = "Mean Opinion Score"
overhead = "Overhead"
isr = "ISR"
interestSatisfactionRatio = "Interest Satisfaction Ratio"









# ===== calculateMaxMOS() =====
#
# calculates the maximal Mean Opinion Score (MOS)
def calculateMaxMOS():
  R = 93.2 - 2.6406 - 0.0
  maxMos = float(1.0 + 0.035 * R + R * (R - 60.0) * (100.0 - R) * 7.0 * 10 ** -6)
  return maxMos






# ===== Bar chart functions =====

# ===== createBarChartCompareOneMetric9Bars() =====
#
# creates a bar chart which compares one metric with different settings for the forwarding strategy mobile-client
def createBarChartCompareOneMetric9Bars(chartName, xName, yName, filename, avgIsr10, avgIsr20, avgIsr30, avgIsr40, avgIsr50, avgIsr60, avgIsr70, avgIsr80, avgIsr90, confIsr10, confIsr20, confIsr30, confIsr40, confIsr50, confIsr60, confIsr70, confIsr80, confIsr90):
  
  # number of metrics
  N = 1
  
  # the x locations for the groups
  index = np.arange(N)
  
  # the width of the bars
  #width = 0.2
  leftMargin = 0.1
  numberOfBars = 9
  width = (1 - 2 * leftMargin) / numberOfBars
  
  # set title
  plt.title(chartName)

  # set bars
  isr10Bar = plt.bar(leftMargin + index, avgIsr10, width, color = colorBestRoute, hatch = hatchBestRoute, yerr = confIsr10, ecolor = colorConf, label = legendIsr10)
  isr20Bar = plt.bar(leftMargin + index + width, avgIsr20, width, color = colorMulticast, hatch = hatchBestRoute, yerr = confIsr20, ecolor = colorConf, label = legendIsr20)
  isr30Bar = plt.bar(leftMargin + index + width * 2, avgIsr30, width, color = colorMobileClient, hatch = hatchBestRoute, yerr = confIsr30, ecolor = colorConf, label = legendIsr30)
  isr40Bar = plt.bar(leftMargin + index + width * 3, avgIsr40, width, color = colorBestRoute, hatch = hatchMulticast, yerr = confIsr40, ecolor = colorConf, label = legendIsr40)
  isr50Bar = plt.bar(leftMargin + index + width * 4, avgIsr50, width, color = colorMulticast, hatch = hatchMulticast, yerr = confIsr50, ecolor = colorConf, label = legendIsr50)
  isr60Bar = plt.bar(leftMargin + index + width * 5, avgIsr60, width, color = colorMobileClient, hatch = hatchMulticast, yerr = confIsr60, ecolor = colorConf, label = legendIsr60)
  isr70Bar = plt.bar(leftMargin + index + width * 6, avgIsr70, width, color = colorBestRoute, hatch = hatchMobileClient, yerr = confIsr70, ecolor = colorConf, label = legendIsr70)
  isr80Bar = plt.bar(leftMargin + index + width * 7, avgIsr80, width, color = colorMulticast, hatch = hatchMobileClient, yerr = confIsr80, ecolor = colorConf, label = legendIsr80)
  isr90Bar = plt.bar(leftMargin + index + width * 8, avgIsr90, width, color = colorMobileClient, hatch = hatchMobileClient, yerr = confIsr90, ecolor = colorConf, label = legendIsr90)
  
  # set legend
  plt.legend((isr10Bar[0], isr20Bar[0], isr30Bar[0], isr40Bar[0], isr50Bar[0], isr60Bar[0], isr70Bar[0], isr80Bar[0], isr90Bar[0]), (legendIsr10, legendIsr20, legendIsr30, legendIsr40, legendIsr50, legendIsr60, legendIsr70, legendIsr80, legendIsr90), loc = legendLocBest)
  
  # add a vertical line across the axes for better display
  plt.axvline(x = 0.0, linestyle = line, color = colorInvisibleLine)
  plt.axvline(x = 1.0, linestyle = line, color = colorInvisibleLine)
  
  # add a horizontal line at max MOS value
  if (chartName.find(meanOpinionScore) != -1 or chartName.find(mos) != -1):
    maxMos = calculateMaxMOS()
    fairMos = 3.6
    poorMos = 2.6
    plt.axhline(y = maxMos, linestyle = line, color = colorLine)
    plt.axhline(y = fairMos, linestyle = pausedLine, color = colorLine)
    plt.axhline(y = poorMos, linestyle = pausedLine, color = colorLine)
  
  # add a horizontal line at 100% Overhead
  if (chartName.find(overhead) != -1):
    totalOverhead = 100
    plt.axhline(y = totalOverhead, linestyle = line, color = colorLine)
  
  # add a horizontal line at 100% ISR
  if (chartName.find(interestSatisfactionRatio) != -1 or chartName.find(isr) != -1):
    totalISR = 100
    plt.axhline(y = totalISR, linestyle = line, color = colorLine)
  
  # x
  plt.xlabel(xName)
  plt.xticks(index)

  # y
  plt.ylabel(yName)
  
  # displays a figure (note: show and save is not possible at the same time)
  #plt.show()
  
  #  gets the current figure (a reference)
  fig = plt.gcf()
  
  # saves the current figure
  fig.savefig(filename, bbox_inches = 'tight')
  
  # clears the current axes
  plt.cla()
  
  # clears the current figure
  plt.clf()






# ===== Bar chart functions =====

# ===== createBarChartCompareOneMetric3Bars() =====
#
# creates a bar chart which compares one metric with the three forwarding strategies (best-route, multicast and mobile-client)
def createBarChartCompareOneMetric3Bars(chartName, xName, yName, filename, avgBestRoute, avgMulticast, avgMobileClient, confBestRoute, confMulticast, confMobileClient):
  
  # number of metrics
  N = 1
  
  # the x locations for the groups
  index = np.arange(N)
  
  # the width of the bars
  #width = 0.2
  leftMargin = 0.1
  numberOfBars = 3
  width = (1 - 2 * leftMargin) / numberOfBars
  
  # set title
  plt.title(chartName)

  # set bars
  bestRouteBar = plt.bar(leftMargin + index, avgBestRoute, width, color = colorBestRoute, hatch = hatchBestRoute, yerr = confBestRoute, ecolor = colorConf, label = legendBestRoute)
  multicastBar = plt.bar(leftMargin + index + width, avgMulticast, width, color = colorMulticast, hatch = hatchMulticast, yerr = confMulticast, ecolor = colorConf, label = legendMulticast)
  mobileClientBar = plt.bar(leftMargin + index + width * 2, avgMobileClient, width, color = colorMobileClient, hatch = hatchMobileClient, yerr = confMobileClient, ecolor = colorConf, label = legendMobileClient)
  
  # set legend
  plt.legend((bestRouteBar[0], multicastBar[0], mobileClientBar[0]), (legendBestRoute, legendMulticast, legendMobileClient), loc = legendLocBest)
  
  # add a vertical line across the axes for better display
  plt.axvline(x = 0.0, linestyle = line, color = colorInvisibleLine)
  plt.axvline(x = 1.0, linestyle = line, color = colorInvisibleLine)
  
  # add a horizontal line at max MOS value
  if (chartName.find(meanOpinionScore) != -1 or chartName.find(mos) != -1):
    maxMos = calculateMaxMOS()
    fairMos = 3.6
    poorMos = 2.6
    plt.axhline(y = maxMos, linestyle = line, color = colorLine)
    plt.axhline(y = fairMos, linestyle = pausedLine, color = colorLine)
    plt.axhline(y = poorMos, linestyle = pausedLine, color = colorLine)
  
  # add a horizontal line at 100% Overhead
  if (chartName.find(overhead) != -1):
    totalOverhead = 100
    plt.axhline(y = totalOverhead, linestyle = line, color = colorLine)
  
  # add a horizontal line at 100% ISR
  if (chartName.find(interestSatisfactionRatio) != -1 or chartName.find(isr) != -1):
    totalISR = 100
    plt.axhline(y = totalISR, linestyle = line, color = colorLine)
  
  # x
  plt.xlabel(xName)
  plt.xticks(index)

  # y
  plt.ylabel(yName)



  # displays a figure (note: show and save is not possible at the same time)
  #plt.show()
  
  #  gets the current figure (a reference)
  fig = plt.gcf()
  
  # saves the current figure
  fig.savefig(filename, bbox_inches = 'tight')
  
  # clears the current axes
  plt.cla()
  
  # clears the current figure
  plt.clf()








# ===== createBarChartComparePacketsOneMetric4Bars() =====
#
# creates a bar chart which compares one metric with the three forwarding strategies (best-route, multicast and mobile-client)
def createBarChartComparePacketsOneMetric4Bars(chartName, xName, yName, filename, avgBestRoute, avgMulticast, avgMobileClient, avgExpected, confBestRoute, confMulticast, confMobileClient, confExpected):
  
  # number of metrics
  N = 1
  
  # the x locations for the groups
  index = np.arange(N)
  
  # the width of the bars
  #width = 0.2
  leftMargin = 0.1
  numberOfBars = 4
  width = (1 - 2 * leftMargin) / numberOfBars
  
  # set title
  plt.title(chartName)

  # set bars
  bestRouteBar = plt.bar(leftMargin + index, avgBestRoute, width, color = colorBestRoute, hatch = hatchBestRoute, yerr = confBestRoute, ecolor = colorConf, label = legendBestRoute)
  multicastBar = plt.bar(leftMargin + index + width, avgMulticast, width, color = colorMulticast, hatch = hatchMulticast, yerr = confMulticast, ecolor = colorConf, label = legendMulticast)
  mobileClientBar = plt.bar(leftMargin + index + width * 2, avgMobileClient, width, color = colorMobileClient, hatch = hatchMobileClient, yerr = confMobileClient, ecolor = colorConf, label = legendMobileClient)
  expectedBar = plt.bar(leftMargin + index + width * 3, avgExpected, width, color = colorExpected, hatch = hatchExpected, yerr = confExpected, ecolor = colorConf, label = legendExpected)
  
  # set legend
  plt.legend((bestRouteBar[0], multicastBar[0], mobileClientBar[0], expectedBar[0]), (legendBestRoute, legendMulticast, legendMobileClient, legendExpected), loc = legendLocBest)
  
  # add a vertical line across the axes for better display
  plt.axvline(x = 0.0, linestyle = line, color = colorInvisibleLine)
  plt.axvline(x = 1.0, linestyle = line, color = colorInvisibleLine)
  
  # x
  plt.xlabel(xName)
  plt.xticks(index)

  # y
  plt.ylabel(yName)
 
  # displays a figure (note: show and save is not possible at the same time)
  #plt.show()
  
  #  gets the current figure (a reference)
  fig = plt.gcf()
  
  # saves the current figure
  fig.savefig(filename, bbox_inches = 'tight')
  
  # clears the current axes
  plt.cla()
  
  # clears the current figure
  plt.clf()






# ===== createAndSaveBarChartTwoMetrics3Bars() =====
#
# creates a bar chart which compares two metrics with the three forwarding strategies (best-route, multicast and mobile-client)
def createAndSaveBarChartTwoMetrics3Bars(chartName, xName, yName, filename, avgBestRoute1, avgMulticast1, avgMobileClient1, confBestRoute1, confMulticast1, confMobileClient1, avgBestRoute2, avgMulticast2, avgMobileClient2, confBestRoute2, confMulticast2, confMobileClient2, metric1, metric2):
  
  # number of metrics
  N = 2
  
  # the x locations for the groups
  index = np.arange(N)
  
  # the width of the bars
  leftMargin = 0.1
  numberOfBars = 3
  width = (1 - 2 * leftMargin) / numberOfBars
  
  # set title
  plt.title(chartName)
  
  # set means for all metrics
  bestRouteMeans = (avgBestRoute1, avgBestRoute2)
  multicastMeans = (avgMulticast1, avgMulticast2)
  mobileClientMeans = (avgMobileClient1, avgMobileClient2)
  
  # set confidence intervalls for all metrics
  bestRouteConf = (confBestRoute1, confBestRoute2)
  multicastConf = (confMulticast1, confMulticast2)
  mobileClientConf = (confMobileClient1, confMobileClient2)
  
  # set bars
  bestRouteBar = plt.bar(leftMargin + index, bestRouteMeans, width, color = colorBestRoute, hatch = hatchBestRoute, yerr = bestRouteConf, ecolor = colorConf, label = legendBestRoute)
  multicastBar = plt.bar(leftMargin + index + width, multicastMeans, width, color = colorMulticast, hatch = hatchMulticast, yerr = multicastConf, ecolor = colorConf, label = legendMulticast)
  mobileClientBar = plt.bar(leftMargin + index + width * 2, mobileClientMeans, width, color = colorMobileClient, hatch = hatchMobileClient, yerr = mobileClientConf, ecolor = colorConf, label = legendMobileClient)
  
  # set legend
  plt.legend((bestRouteBar[0], multicastBar[0], mobileClientBar[0]), (legendBestRoute, legendMulticast, legendMobileClient), loc = legendLocBest)
  
  # add a horizontal line at 100% Overhead
  if (chartName.find(overhead) != -1):
    totalOverhead = 100
    plt.axhline(y = totalOverhead, linestyle = line, color = colorLine)
  
  # x
  plt.xlabel(xName)
  plt.xticks(index + 0.5, (metric1, metric2), rotation = rotationVertical)
  
  # y
  plt.ylabel(yName)
  
  # displays a figure (note: show and save is not possible at the same time)
  #plt.show()

  #  gets the current figure (a reference)
  fig = plt.gcf()
  
  # saves the current figure
  fig.savefig(filename, bbox_inches = 'tight')

  # clears the current axes
  plt.cla()
  
  # clears the current figure
  plt.clf()






# ===== createAndSaveBarChartThreeMetrics3Bars() =====
#
# creates a bar chart which compares three metrics with the three forwarding strategies (best-route, multicast and mobile-client)
def createAndSaveBarChartThreeMetrics3Bars(chartName, xName, yName, filename, avgBestRoute1, avgMulticast1, avgMobileClient1, confBestRoute1, confMulticast1, confMobileClient1, avgBestRoute2, avgMulticast2, avgMobileClient2, confBestRoute2, confMulticast2, confMobileClient2, avgBestRoute3, avgMulticast3, avgMobileClient3, confBestRoute3, confMulticast3, confMobileClient3, metric1, metric2, metric3):
  
  # number of metrics
  N = 3
  
  # the x locations for the groups
  index = np.arange(N)
  
  # the width of the bars
  leftMargin = 0.1
  numberOfBars = 3
  width = (1 - 2 * leftMargin) / numberOfBars
  
  # set title
  plt.title(chartName)
  
  # set means for all metrics
  bestRouteMeans = (avgBestRoute1, avgBestRoute2, avgBestRoute3)
  multicastMeans = (avgMulticast1, avgMulticast2, avgMulticast3)
  mobileClientMeans = (avgMobileClient1, avgMobileClient2, avgMobileClient3)
  
  # set confidence intervalls for all metrics
  bestRouteConf = (confBestRoute1, confBestRoute2, confBestRoute3)
  multicastConf = (confMulticast1, confMulticast2, confMulticast3)
  mobileClientConf = (confMobileClient1, confMobileClient2, confMobileClient3)
  
  # set bars
  bestRouteBar = plt.bar(leftMargin + index, bestRouteMeans, width, color = colorBestRoute, hatch = hatchBestRoute, yerr = bestRouteConf, ecolor = colorConf, label = legendBestRoute)
  multicastBar = plt.bar(leftMargin + index + width, multicastMeans, width, color = colorMulticast, hatch = hatchMulticast, yerr = multicastConf, ecolor = colorConf, label = legendMulticast)
  mobileClientBar = plt.bar(leftMargin + index + width * 2, mobileClientMeans, width, color = colorMobileClient, hatch = hatchMobileClient, yerr = mobileClientConf, ecolor = colorConf, label = legendMobileClient)
  
  # set legend
  plt.legend((bestRouteBar[0], multicastBar[0], mobileClientBar[0]), (legendBestRoute, legendMulticast, legendMobileClient), loc = legendLocBest)
  
  # add a horizontal line at 100% Overhead
  if (chartName.find(overhead) != -1):
    totalOverhead = 100
    plt.axhline(y=totalOverhead, linestyle=line, color=colorLine)
  
  # x
  plt.xlabel(xName)
  plt.xticks(index + 0.5, (metric1, metric2, metric3), rotation = rotationVertical)
  
  # y
  plt.ylabel(yName)
  
  # displays a figure (note: show and save is not possible at the same time)
  #plt.show()

  #  gets the current figure (a reference)
  fig = plt.gcf()
  
  # saves the current figure
  fig.savefig(filename, bbox_inches = 'tight')

  # clears the current axes
  plt.cla()
  
  # clears the current figure
  plt.clf()






