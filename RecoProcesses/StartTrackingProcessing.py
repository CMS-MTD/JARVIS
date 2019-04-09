from ProcessExec import *
import ProcessRuns as pr

ExecutionOrder = 1 #This is Ascending Run number order, Refer to the dictionary in all modules
PID = 0 #0 means Tracking, Refer to the dictionary in all modules
RunNumber = -1 #-1 means do all runs

########### If want to do processing for specific run range (Both run numbers are included) ##########
StartRunNumber = None
StopRunNumber = None

############ Doesn't matter for tracking ###########
SaveWaveForms = False
ConfigVersion = "v1"
DigitizerKey = 0 #key=0 for VME, Refer Allmodules

#You need to make a file called "key" that sits inside the RecoProcesses directory and contains the key password for the database.
keyFile = open("key", "r")
key = str(keyFile.read().strip())

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"

if RunNumber != -1:
	for run in range (StartRunNumber, StopRunNumber + 1):	
		ProcessExec(ExecutionOrder,TimingPID, SaveWaveForms, ConfigVersion,run,DigitizerKey,key)
else:
	ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,RunNumber,DigitizerKey,key)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"