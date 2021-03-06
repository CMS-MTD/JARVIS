#!/usr/bin/python

import os
import datetime
import time
import subprocess
import glob
import TransferUtils

print "\n##############################"
print "## Starting RAW Data Archival ##"
print "################################\n"

#You need to change this the kerberos principal being used
user = "sxie"

#Change to the location disk location
LocalDataLocation = "/data2/"

#change to name of the testbeam campaign directory
CampaignDirectoryName = "2019_04_April_CMSTiming"

DoXRDTransfer = False


continueLoop = True
while continueLoop : 

    print "\n########################################"
    print "## Starting a new data transfer cycle   ##"
    print "Time: ", str(datetime.datetime.now())
    print "##########################################\n"


    #Copy Strip Tracking Data from ftbf-daq-08 and to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring Strip Telescope Raw Data from ftbf-daq-08"
    print   "######################################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/OtsData/* " + LocalDataLocation+CampaignDirectoryName+"/OtsData/"
    print command
    os.system(command)
    print "\n\n"
    print "\n###################################################"
    print   "Transferring Strip Telescope Raw Data to CMSLPC EOS"
    print   "###################################################\n"

    if DoXRDTransfer:
        TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                           "/store/group/cmstestbeam/" + CampaignDirectoryName + "/OtsData/",
                                           LocalDataLocation+CampaignDirectoryName+"/OtsData/")
                                        
                                        
    #Copy NimPlus Data from ftbf-daq-08 and to CMSLPC EOS
    #need to use xrdcp
    print "\n\n"
    print "\n######################################################"
    print   "Transferring NimPlus Data from ftbf-daq-08"
    print   "######################################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/NimPlus/* " + LocalDataLocation+CampaignDirectoryName+"/NimPlus/"
    print command
    os.system(command)
    print "\n\n"
    print "\n###################################################"
    print   "Transferring NimPlus Data to CMSLPC EOS"
    print   "###################################################\n"
    if DoXRDTransfer:
        TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                           "/store/group/cmstestbeam/" + CampaignDirectoryName + "/NimPlus/",
                                           LocalDataLocation+CampaignDirectoryName+"/NimPlus/")

    #Copy VME RAW Data from ftbf-daq-08 and to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring VME RAW Data from ftbf-daq-08"
    print   "######################################################\n"
    command = "rsync -uv --progress otsdaq@ftbf-daq-08.fnal.gov:/data/TestBeam/"+CampaignDirectoryName+"/CMSTiming/* " + LocalDataLocation+CampaignDirectoryName+"/VME/RawData/"
    print command
    os.system(command)
    print "\n\n"
    print "\n###################################################"
    print   "Transferring VME RAW Data to CMSLPC EOS"
    print   "###################################################\n"
    if DoXRDTransfer:
        TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                           "/store/group/cmstestbeam/" + CampaignDirectoryName + "/VME/RawData/",
                                           LocalDataLocation+CampaignDirectoryName+"/VME/RawData/")


 
    #Copy DT5742 RAW Data to CMSLPC EOS
    print "\n\n"
    print "\n###################################################"
    print   "Transferring DT5742 RAW Data to CMSLPC EOS"
    print   "###################################################\n"
    if DoXRDTransfer:
        TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                           "/store/group/cmstestbeam/" + CampaignDirectoryName + "/DT5742/RawData/",
                                           LocalDataLocation+CampaignDirectoryName+"/DT5742/RawData/")

 
    #Copy Keysight Scope RAW Data to CMSLPC EOS
    print "\n\n"
    print "\n######################################################"
    print   "Transferring Keysight Scope from timingdaq02"
    print   "######################################################\n"
    command = "rsync -uv --progress daq@timingdaq02.dhcp.fnal.gov:/home/daq/"+CampaignDirectoryName+"/KeySightScope/RawData//* " + LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RawData/"
    print command
    os.system(command)
    #Copy DT5742 RAW Data to CMSLPC EOS
    print "\n\n"
    print "\n###################################################"
    print   "Transferring Keysight Scope Raw Data to CMSLPC EOS"
    print   "###################################################\n"
    if DoXRDTransfer:
        TransferUtils.XrdCopyLocalToRemote("cmseos.fnal.gov", 
                                           "/store/group/cmstestbeam/" + CampaignDirectoryName + "/KeySightScope/RawData/",
                                           LocalDataLocation+CampaignDirectoryName+"/KeySightScope/RawData/")


    
    #Copy Raspberry Pi Conditions Data from timingdaq02
    print "\n\n"
    print "\n######################################################"
    print   "Transferring Raspberry Pi from timingdaq02"
    print   "######################################################\n"
    command = "rsync -uv --progress daq@timingdaq02.dhcp.fnal.gov:/home/daq/"+CampaignDirectoryName+"/RP/* " + LocalDataLocation+CampaignDirectoryName+"/RP/"
    print command
    os.system(command)

    time.sleep(10)

    
