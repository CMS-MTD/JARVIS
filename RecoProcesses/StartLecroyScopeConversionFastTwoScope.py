from ProcessExec import *
import ProcessRuns as pr
import argparse

# -------- Argument parsing --------
parser = argparse.ArgumentParser(description="Run data processing")
parser.add_argument("--scope", type=int, required=True,
                    help="Scope number (1 or 2)")
args = parser.parse_args()

ScopeNum = args.scope

# -------- Map Scope → PID --------
if ScopeNum == 1:
    PID = 1
elif ScopeNum == 2:
    PID = 11
else:
    raise ValueError(f"Unsupported ScopeNum: {ScopeNum} (expected 1 or 2)")

# -------- Config --------
ExecutionOrder = 0
GetRunListEachTime = True

SaveWaveForms = True
ConfigVersion = "v11"
DigitizerKey = 6

# -------- Get Key --------
key = am.GetKey()

print("\n##############################")
print("## Starting Data processing ##")
print(f"## ScopeNum = {ScopeNum}, PID = {PID}")
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
