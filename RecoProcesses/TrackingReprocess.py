from ProcessExec import *
import ProcessRuns as pr

ExecutionOrder = 1 #This is Ascending Run number order, Refer to the dictionary in all modules
PID = 0 #0 means Tracking, Refer to the dictionary in all modules
GetRunListEachTime = False #Could be true also for this case.

#Give the range of run numbers to process
StartRunNumber = 63001
StopRunNumber = 65141

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v12"
DigitizerKey = 3 #key=0 for VME, Refer Allmodules

########### Get Key ###########
key = am.GetKey()

print "\n##############################"
print "## Starting Data processing ##"
print "##############################\n"

for run in range (StartRunNumber, StopRunNumber + 1):	
        ProcessExec(ExecutionOrder,PID, SaveWaveForms, ConfigVersion,run,DigitizerKey,key,GetRunListEachTime)

print "\n##############################"
print "## Completed Data processing ##"
print "##############################\n"
