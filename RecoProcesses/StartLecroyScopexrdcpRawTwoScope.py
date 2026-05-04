import argparse

from ProcessExec import *
import ProcessRuns as pr

parser = argparse.ArgumentParser()
parser.add_argument(
    "--scope",
    type=int,
    choices=[1, 2],
    required=True,
    help="Scope number: 1 or 2",
)
args = parser.parse_args()

ExecutionOrder = 0   # descending Run number order
GetRunListEachTime = True

############ Doesn't matter for tracking ###########
SaveWaveForms = True
ConfigVersion = "v10"
DigitizerKey = 6

if args.scope == 1:
    PID = 6          # xrdcp raw
    ScopeNum = 1
elif args.scope == 2:
    PID = 10         # xrdcp raw2
    ScopeNum = 2

########### Get Key ###########
key = am.GetKey()

print("\n##############################")
print("## Starting Data processing ##")
print("##############################\n")

ProcessExec(
    ExecutionOrder,
    PID,
    SaveWaveForms,
    ConfigVersion,
    -1,
    DigitizerKey,
    key,
    GetRunListEachTime,
    True,
    ScopeNum=ScopeNum,
)

print("\n##############################")
print("## Completed Data processing ##")
print("##############################\n")
