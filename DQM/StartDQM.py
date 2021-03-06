import os
import ROOT as rt
import DQMPlots as dqm
import time

#Change to webserver location
WebServerDirectory = "/var/www/html/"

#Change to the location disk location
LocalDataLocation = "/data2/"

#change to name of the testbeam campaign directory
CampaignDirectoryName = "2019_04_April_CMSTiming"

VME_RECO_Version = "v3"
DT_RECO_Version = "v1"
KeySightScope_RECO_Version = "v1"

VME_RECO_DIR = LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/" + VME_RECO_Version + "/"
DT_RECO_DIR = LocalDataLocation+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/" + DT_RECO_Version + "/"
KeySightScope_RECO_DIR = LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/"+ KeySightScope_RECO_Version+"/"


#Define lists for runs and channels
VMEChannelAmpThresholdDict = {
  0 : 30,
  1 : 400,
  2 : 400,
  3 : 400,
  4 : 400,
  5 : 400, 
  6 : 400,
  19: 200,
  20: 200  
}
DTChannelAmpThresholdDict = {
  0 : 15,
  1 : 15,
  2 : 15,
  3 : 15,
  4 : 15,
  5 : 15,
  6 : 15,
  7 : 15,
  9 : 15,
  10 : 15,
  11 : 15,
  12 : 15,
  13 : 15,
  14 : 15,
  15 : 15,
  16 : 15,
}
KeySightScopeChannelAmpThresholdDict = {
  2 : 150
}


#Define Run Lists
VMERunList = []
DTRunList = []
KeySightScopeRunList = []

# Get VME Run List
for f in os.listdir(VME_RECO_DIR):
    run = (f.split("_")[1])[3:]
    VMERunList.append(run)
VMERunList.sort()

# Get DT Run List
for f in os.listdir(DT_RECO_DIR):
    run = ((f.split("_")[2]).split(".")[0])[3:]
    DTRunList.append(run)
DTRunList.sort()

# Get KeysightScope Run List
for f in os.listdir(KeySightScope_RECO_DIR):
    run = (f.split("_")[0])[5:]
    KeySightScopeRunList.append(run)

KeySightScopeRunList.sort()


continueLoop = True
while continueLoop : 


    #########################################
    # VME DQM Plots
    #########################################
    for run in VMERunList :

 
        # open the file
        if os.path.isfile(LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/"+VME_RECO_Version+"/RawDataSaver0CMSVMETiming_Run"+str(run)+"_0_Raw.root"):

            outputDir = WebServerDirectory+"/DQM/Run"+str(run)
            if os.path.exists(outputDir+"/DQMDone_VME.txt"):
                print "DQM (VME) for Run " + str(run) + " already done"
            else :
                myfile = rt.TFile(LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/"+VME_RECO_Version+"/RawDataSaver0CMSVMETiming_Run"+str(run)+"_0_Raw.root")
                # retrieve the tree
                mytree = myfile.Get('pulse')

                #make output run directory if it doesn't exist
                if not os.path.exists(outputDir):
                    os.makedirs(outputDir)

                #Make XYEff Plots
                if myfile.GetListOfKeys().Contains('pulse')==True:
                    dqm.MakeXYEffPlots(mytree, VMEChannelAmpThresholdDict, outputDir, "VME")
                else:
                    print "Run "+str(run)+" missing pulse tree. Skipping DQM"

                f = open(outputDir+"/DQMDone_VME.txt", "w")
                f.write("DONE")
                f.close()

        else :
            print "Data File " + LocalDataLocation+CampaignDirectoryName+"/VME/RecoData/RecoWithTracks/"+VME_RECO_Version+"/RawDataSaver0CMSVMETiming_Run"+str(run)+"_0_Raw.root " + "not found."


    #########################################
    # KeySightScope DQM Plots
    #########################################
    for run in KeySightScopeRunList :
 
        # open the file
        if os.path.isfile(LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/RecoWithTracks/"+KeySightScope_RECO_Version+"/run_scope"+str(run)+"_converted.root"):

            outputDir = WebServerDirectory+"/DQM/Run"+str(run)
            if os.path.exists(outputDir+"/DQMDone_KeySightScope.txt"):
                print "DQM (KeySightScope) for Run " + str(run) + " already done"
            else :
                myfile = rt.TFile(LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/RecoWithTracks/"+KeySightScope_RECO_Version+"/run_scope"+str(run)+"_converted.root")
                # retrieve the tree
                mytree = myfile.Get('pulse')

                #make output run directory if it doesn't exist
                if not os.path.exists(outputDir):
                    os.makedirs(outputDir)

                #Make XYEff Plots
                if myfile.GetListOfKeys().Contains('pulse')==True:
                    dqm.MakeXYEffPlots(mytree, KeySightScopeChannelAmpThresholdDict, outputDir, "KeySightScope")
                else:
                    print "Run "+str(run)+" missing pulse tree. Skipping DQM"

                f = open(outputDir+"/DQMDone_KeySightScope.txt", "w")
                f.write("DONE")
                f.close()

        else :
            print "Data File " + LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RecoData/RecoWithTracks/"+KeySightScope_RECO_Version+"/run_scope"+str(run)+"_converted.root " + "not found."

    
    #########################################
    # DT DQM Plots
    #########################################
    for run in DTRunList :

        # open the file
        if os.path.isfile(LocalDataLocation+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/"+DT_RECO_Version+"/DT5742_RAW_Run"+str(run)+".root"):

            outputDir = WebServerDirectory+"/DQM/Run"+str(run)

            if os.path.exists(outputDir+"/DQMDone_DT.txt"):
                print "DQM (DT5742 )for Run " + str(run) + " already done"
            else :
            
                myfile = rt.TFile(LocalDataLocation+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/"+DT_RECO_Version+"/DT5742_RAW_Run"+str(run)+".root")
                # retrieve the tree
                mytree = myfile.Get('pulse')

                #make output run directory if it doesn't exist
                if not os.path.exists(outputDir):
                    os.makedirs(outputDir)

                #Make XYEff Plots
                if myfile.GetListOfKeys().Contains('pulse')==True:
                    print str(run)
                    dqm.MakeXYEffPlots(mytree, DTChannelAmpThresholdDict, outputDir, "DT5742")
                else:
                    print "input file from Run {0} DOES NOT HAVE pulse tree. Skipping file".format(str(run))
                f = open(outputDir+"/DQMDone_DT.txt", "w")
                f.write("DONE")
                f.close()
            
            
        else :
            print "Data File " + LocalDataLocation+CampaignDirectoryName+"/DT5742/RecoData/RecoWithTracks/"+DT_RECO_Version+"/DT5742_RAW_Run"+str(run)+".root " + "not found."
    
    #copy the index.php into all new subdirectories
    os.system("cd " + WebServerDirectory+ "/DQM/; ./distributeIndexPHP.sh;")

    time.sleep(60)
