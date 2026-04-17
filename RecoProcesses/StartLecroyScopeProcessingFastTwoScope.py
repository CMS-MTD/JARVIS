from ProcessExec import *
import ProcessRuns as pr
import argparse

# -------- Argument parsing --------
parser = argparse.ArgumentParser(description="Run data processing with configurable scope number")
parser.add_argument("--scope", type=int, default=1, help="Scope number (default: 1)")
args = parser.parse_args()

ScopeNum = args.scope
if not(ScopeNum ==1 or ScopeNum == 2):sys.exit("Scoper number is 1 or 1")
# -------- Config --------
ExecutionOrder = 0  # descending Run number order
if ScopeNum == 1: PID = 2             # 9 means TimingdaqFast
else: PID = 12
#PID = 3             # means no tracking
GetRunListEachTime = True

SaveWaveForms = True
ConfigVersion = "v1"
DigitizerKey = 6    # key=3 for KeySightScope

# -------- Get Key --------
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
    condor=False,
    ScopeNum=ScopeNum
)

print("\n##############################")
print("## Completed Data processing ##")
print("##############################\n")
