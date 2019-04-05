import socket
import sys
import time
import os
import AllModules as am

def init_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Initialize"
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))                                                                                                                                                                         
    time.sleep(5)

def config_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                                                                                                                                      
    MESSAGE = "OtherRuns0,Configure,T992Config"
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))                                                                                                                                                                          
    time.sleep(5)

def start_ots(Delay=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Start, %d" % (GetRunNumber()+1)
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))
    if Delay: time.sleep(5)
    return 
    
def stop_ots(Delay=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Stop"
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))
    if Delay: time.sleep(5)

def GetRunNumber():
    runFile = open(am.localRunFileName)
    nextRun = int(runFile.read().strip()) 
    return nextRun

def UpdateRunNumber(nextRunNum):
    incrementRunFile = open(am.localRunFileName,"w")
    incrementRunFile.write(str(nextRunNum)+"\n")
    incrementRunFile.close()

def GetRunFile():
    CMD = 'scp otsdaq@ftbf-daq-08.fnal.gov:' + am.runFileName + ' ' + am.localRunFileName
    session = am.subprocess.Popen('%s' % CMD,stdout=am.PIPE, stderr=am.subprocess.PIPE, shell=True)       

def SendRunFile():
    CMD = 'scp ' + am.localRunFileName +' otsdaq@ftbf-daq-08.fnal.gov:' + am.runFileName
    session = am.subprocess.Popen('%s' % CMD,stdout=am.PIPE, stderr=am.subprocess.PIPE, shell=True)       
