# executeSimulations.py

# Usage - has to be started from the scenario (voicemail_scenario) folder
# python ./results/executeSimulations.py -t=<numberOfThreads> -r=<numberOfRuns> -s=<startNumberOfRuns> 

# import
import threading
import argparse
import os
from subprocess import call
import time
import subprocess
import glob
import shutil






noOfActiveThreads = 0
noOfInvalidRuns = 0



# ===== class Thread =====
#
# the class thread extends the class threading.Thread
class Thread(threading.Thread):



  # ===== __init__() =====
  #
  # initializes a thread
  def __init__(self, job_number, sys_cal, callback_method, src, dst):
    super(Thread, self).__init__()
    self.sysCall = sys_cal
    self.jobNumber = job_number
    self.callback = callback_method
    self.src = src
    self.dst = dst



  # ===== run() =====
  #
  # overwriting the run method of threading.Thread, this method is called by thread.start()
  def run(self):

    print "Job " + str(self.jobNumber) + " started..."

    if not os.path.exists(self.src):
      os.makedirs(self.src)

    # output file
    fpOut = open(self.src + "t_" + str(self.jobNumber) + ".stdout.txt", "w")

    # start subprocess and wait until it is finished
    proc = subprocess.Popen(self.sysCall, stdout=fpOut, cwd=self.src)
    proc.communicate()

    # sleep 0.5 seconds to be sure the OS really has finished the process
    time.sleep(0.5)

    # close file
    fpOut.close()

    # return code of subprocess
    returnCode = proc.returncode

    # callback method
    print "Job " + str(self.jobNumber) + " finished."
    self.callback(self.jobNumber, self.src, self.dst, returnCode)



# ===== threadFinished() =====
#
# the callback method is called when a thread has finished
def threadFinished(job_number, src, dst, returnCode):

  global noOfActiveThreads, noOfInvalidRuns

  if (returnCode != 0):
    noOfInvalidRuns = noOfInvalidRuns + 1

  # copy the output files
  textFiles = glob.glob(src + "*.txt")

  # no error occured
  if returnCode == 0:
    if not os.path.exists(dst):
      os.makedirs(dst)

    # move results to dst folder
    for f in textFiles:
      shutil.move(f, dst + "/" + os.path.basename(f))

  # delete results from src folder
  shutil.rmtree(src)
  print "Job " + str(job_number) + " results moved."

  noOfActiveThreads = noOfActiveThreads - 1






# ========== MAIN PROGRAM ==========

# parse command line arguments
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("-t", "--threads", type = int, help = "Number of threads for parallel executions", default = 10)
argumentParser.add_argument("-r", "--runs", type = int, help = "Number of runs for each setting", default = 20)
argumentParser.add_argument("-s", "--skip", type = int, help = "Start number of runs for skipping a certain number of runs", default = 0)
args = argumentParser.parse_args()

# current working directory
simulationDir = os.getcwd()

# command line arguments
noOfThreads = args.threads
noOfRuns = args.runs
startNoOfRuns = args.skip

# scenario
scenario = "big-mobile-voicemail"

# output directories
simulationOutputDir = simulationDir + "/results/"
simulationOutputDirRam = "/run/shm/scenarioResults/"

# argument with path to brite configuration file
briteConfig = "--briteConfig=" + simulationDir + "/brite_configs/brite_3_as.conf"

# set options for forwarding strategies
bestRoute = "--fwStrategy=best-route"
multicast = "--fwStrategy=multicast"
mobileClient = "--fwStrategy=mobile-client"
forwardingStrategies = [bestRoute, multicast, mobileClient]

# set options for the number of AP nodes for each WiFi network
numberOfAPs = [
  "--noAPs=1",
  "--noAPs=2",
  "--noAPs=3"
]

# set the ISR threshold
isrThresholds = [
  "--isrT=90"
]

# set xPos
xPos = [
  "--xPos=15",
  "--xPos=20"
]

# set yPos
yPos = [
  "--yPos=-150"
]

# set yNextPos
yPosNext = [
  "--yPosNext=-30",
  "--yPosNext=-40"
]

# scenario dictionary stores parameters for executing the simulations
scenarioDictionary = {}

# number of actuall job
jobNumber = 0


# save all possible configurations into the dictionary
for strategy in forwardingStrategies:
  for noAPs in numberOfAPs:
    for isrT in isrThresholds:
      for xP in xPos:
        for yPN in yPosNext:
          name = strategy + noAPs + isrT + xP + yPN
          scenarioDictionary.update({name: {"executeable": scenario, "numRuns": noOfRuns, "params": [briteConfig, strategy, noAPs, isrT, xP, yPN]}})



# build project
call([simulationDir + "/waf"])

# sleep for 3 seconds
time.sleep(3)




for scenarioName in scenarioDictionary.keys():
    
  runs = scenarioDictionary[scenarioName]['numRuns']

  executeable = scenarioDictionary[scenarioName]['executeable']
  executeable = "build/" + executeable


  print "Starting simulations..."
  for i in range(startNoOfRuns, startNoOfRuns + runs):
        
    # wait until a thread is available for a job
    while noOfActiveThreads >= noOfThreads:
      time.sleep(1)

    src = simulationOutputDirRam + scenarioName[13:].replace("--", "_").replace("=", "_") + "/run_" + str(i) + "/"
    dst = simulationOutputDir + scenarioName[13:].replace("--", "_").replace("=", "_") + "/run_" + str(i) + "/"

    # sys call for the scenario configuration
    sysCall = [simulationDir + "/" + executeable] + scenarioDictionary[scenarioName]['params'] + ["--RngRun=" + str(i)] + ["--logDir=" + src]

    # initialize thread, pass callback method which is called when thread is done
    thread = Thread(jobNumber, sysCall, threadFinished, src, dst)

    # if a configuration folder exists, skip this folder
    if(os.path.exists(dst)):
      jobNumber = jobNumber + 1
      continue

    # start thread and count the number of threads and jobs
    thread.start()
    noOfActiveThreads = noOfActiveThreads + 1
    jobNumber = jobNumber + 1



while noOfActiveThreads != 0:
  time.sleep(15)



print "------------------------------------------------------------------------"
print "Number of invalid runs: " + str(noOfInvalidRuns)
print "Simulations finished."
