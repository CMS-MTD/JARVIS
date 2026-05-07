from AllModules import *
import ParseFunctions as pf
import json
#### Look at these parameters before running the listener
UsingAutoPilot = True

numEvents = 10000 #28000 ## not used in Long mode #Max with math mode off is 32000 for Lecroy

master_ip = "192.168.0.1"
slave_ip = "192.168.0.173"

###################### Enable Slave ############################
enableSlave = 0 
print("Slave enabled:", enableSlave)
with open(f"{BaseTestbeamDir}/JARVIS/AutoPilot/scope_config.json", "w") as f:
    json.dump({"enable_slave": enableSlave}, f)



####################### Trigger  ###############################
master_trigCh, master_trig, master_trigSlope = 1, 0.05, "POS" # threshold in V
slave_trigCh, slave_trig, slave_trigSlope = "EX", 0.1, "POS" #dont need to change, threshold when splitting the external trigger from Lecroy scope

master_aux_mode, master_aux_pulse_width = "triggerout", 400 #ns
holdoff = 400  # trigger hold off time in ns, when holdoff= 0, hold off is turned off
####################### Horizontal ###############################

timeoffset = 0 #100 ##75 scintillator trigger
numPoints = 25 ##MSa, only used in Long mode
sampleRate = 10 #GSa/s
horizontalWindow = 200 #ns, full window, 10 divisions
### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.

###################### Vertical #################################
display = 1
vScale = {
    1: 0.02,
    2: 0.15,
    3: 0.25,
    4: 0.35,
    5: 0.05,
    6: 0.05,
    7: 0.05,
    8: 0.05,
    9: 0.02, # slave ch 1
    10: 0.05, # slave ch 2
    11: 0.1, # slave ch 3
    12: 0.15, # slave ch 4
    13: 0.25, # slave ch 5
    14: 0.05, # slave ch 6
    15: 0.05, # slave ch 7
    16: 0.05, # slave ch 8
}
vPos = {
    1: -3.,
    2: 0.,
    3: 0.,
    4: 0.,
    5: 0.,
    6: 0.,
    7: 0.,
    8: 0.,
    9: -3., #slave ch 1
    10: 0., #slave ch 2
    11: 0., #slave ch 3
    12: 0., #slave ch 4
    13: 0., #slave ch 5
    14: 0., #slave ch 6
    15: 0., #slave ch 7
    16: 0., #slave ch 8
}


############### Remember to source the otsdaq environment
############### Assuming the directory structure in the KeySightScope repository is the same as on this computer

AutoPilotStatusFile = LecroyScopeCommFileName
#print AgilentScopeCommand
print("####################################")
print("## Starting Loop: Waiting for run ##")
print("####################################")

while True:

    inFile = open(AutoPilotStatusFile,"r")
    runNumber = inFile.readline().strip()
    time.sleep(1)

    if (runNumber != str(0)):

        ScopeStateHandle = open(ScopeStateFileName, "r")
        ScopeState = str(ScopeStateHandle.read().strip())

        if UsingAutoPilot:

            ############### checking the status for the next runs #################  
            with open(AutoPilotStatusFile,'w') as file:
                file.write(str(0))
            print("\n ####################### Running the scope acquisition ##################################\n")
            
            pos_args = " ".join([str(vPos[ch]) for ch in sorted(vPos)])
            scale_args = " ".join([str(vScale[ch]) for ch in sorted(vScale)])
            ScopeCommand = (
            f"python3 {LecroyScopeControlDir}/Acquisition/acquisition_twoscope.py "
            f"--master-scope-ip {master_ip} "
            f"--slave-scope-ip {slave_ip} "
            f"--master-trigCh {master_trigCh} "
            f"--master-trig {master_trig} "
            f"--master-trigSlope {master_trigSlope} "
            f"--slave-trigCh {slave_trigCh} "
            f"--slave-trig {slave_trig} "
            f"--slave-trigSlope {slave_trigSlope} "
            f"--master-aux-mode {master_aux_mode} "
            f"--master-aux-out-pulse-width {master_aux_pulse_width} "
            f"--master-holdoff {holdoff} "
            f"--horizontalWindow {horizontalWindow} "
            f"--runNumber {runNumber} "
            f"--display {display} "
            f"--enableSlave {enableSlave} "
            f"--numEvents {numEvents} "
            f"--sampleRate {sampleRate} "
            f"--vScale {scale_args} "
            f"--vPos {pos_args} "
            )

            print(ScopeCommand)
            #### Starting the acquisition script ####
            os.system(ScopeCommand)
            
            print("\n ####################### Done with the scope acquisition ##################################\n")


        elif ScopeState == "ready":
            print('Change the RunLog.txt file to ready')     
