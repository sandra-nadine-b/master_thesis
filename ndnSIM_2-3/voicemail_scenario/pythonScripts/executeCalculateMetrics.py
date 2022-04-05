# executeCalculateMetrics.py

# import
import argparse
import calculateMetrics



# ===== MAIN function =====
#
# this is the main function
def main():
  
  # parse command line arguments
  argumentParser = argparse.ArgumentParser()
  argumentParser.add_argument("-noRuns", "--numberOfRuns", type = int, help = "Number of runs", default = 0)
  argumentParser.add_argument("-dir", "--directory", type = str, help = "The directory with the results for a configuration", default = "")
  args = argumentParser.parse_args()


  # python script which should be executed
  pythonScript = "calculateMetrics.py"
  dirSep = "/"
  
  # number of runs
  noOfRuns = args.numberOfRuns
  
  # directory
  if not (args.directory.endswith("/")):
    directoryToFiles = args.directory + dirSep + "run_"
  else:
    directoryToFiles = args.directory + "run_"
  
  # calculetes metrics for a configuration
  for i in range(0, noOfRuns):
    fileDir = directoryToFiles + str(i) + dirSep
    
    argsList = list()
    argsList.append(pythonScript)
    argsList.append(fileDir)
    
    # calculate metrics
    calculateMetrics.main(argsList)



# ========== MAIN PROGRAM ==========
if __name__== "__main__":
  main()




