import sys 
sys.path.append('../BackEndProcesses/')
import AllModules as am
import ProcessCMDs as pc
import ParseFunctions as pf
import condorUtils as cu                                                                                                                                                                                                  

def exists_remote(host, path):                                                                                                                                                                                                                                                                                                
	status = subprocess.call(['ssh', host, 'test -f {0}'.format(pipes.quote(path))])                                                                                                                                                                                                                                          
	if status == 0:                                                                                                                                                                                                                                                                                                           
		return True                                                                                                                                                                                                                                                                                                           
	if status == 1:                                                                                                                                                                                                                                                                                                           
		return False                                                                                                                                                                                                                                                                                                          
	raise Exception('SSH failed') 

def GetSessionOutputRealTime(session):
	while True:
		line = session.stdout.readline().rstrip()
		if not line:
			break
		print((type(line)))
		yield line

def TrackFileRemoteExists(RunNumber):
	TrackFilePathRulinux = am.BaseTrackDirRulinux +'CMSTimingConverted/Run%i_CMSTiming_converted.root' % RunNumber                                                                                                                                                                                                                       
	return exists_remote(am.RulinuxSSH, am.TrackFilePathRulinux), am.TrackFilePathRulinux                                                                                                                                                                                                                                              

def TrackFileLocalExists(RunNumber):
	TrackFilePathLocal = am.BaseTrackDirLocal + 'Run%i_CMSTiming_converted.root' % RunNumber                                                                                                                                                                                                                                             
	return am.os.path.exists(TrackFilePathLocal), TrackFilePathLocal                                                                                                                                                                                                                                                             

def FileSizeBool(FilePath, SizeCut):
	if am.os.path.exists(FilePath):
		return am.os.stat(FilePath).st_size < SizeCut
	else: return True

def ProcessExec(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True, condor = False, ApplyFilter = False, FNALTelescope = True, ScopeNum = 1):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
		if PID == 0:
			ProcessName = list(am.ProcessDict[PID].keys())[0]
			print(ProcessName)
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TrackingCMDs(RunNumber, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
			print(ResultFileLocationList)
		elif PID == 1 or PID == 11:
			print("scope", ScopeNum)
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.ConversionCMDs(RunNumber, Digitizer, MyKey, False, condor,ScopeNum)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 2 or PID == 12:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False, condor, ScopeNum)
			
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 3:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			DoTracking = False	
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
			print(CMDList)
		elif PID == 5:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.WatchCondorCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[2][list(am.ProcessDict[2].keys())[0]]['SizeCut']		
			print((ResultFileLocationList, RunList))
		elif PID == 6 or PID == 10:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoTracking = True
			if PID==6:CMDList, ResultFileLocationList, RunList, FieldIDList = pc.xrdcpRawCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			else:CMDList, ResultFileLocationList, RunList, FieldIDList = pc.xrdcpRawCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False, 2)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']		
			#print ResultFileLocationList, RunList
		elif PID == 7:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoScope = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.RecoTOFHIRCMDs(RunNumber, Version, DoScope, Digitizer, MyKey)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 8:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoScope = False
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.RecoTOFHIRCMDs(RunNumber, Version, DoScope, Digitizer, MyKey)
			print(CMDList)
			print(ResultFileLocationList)
			print(RunList)
			print(FieldIDList)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 13:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			print(ProcessName)
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.MergeCMDs(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False, condor)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']


		RunListInt = list(map(int,RunList))
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		if CMDList != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
				# if run > 27363: continue 
				if PID!=0: ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
				index = RunList.index(run)
				CMD = CMDList[index]  
				if RunNumber != -1 and len(FieldIDList[index])>0: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation = ResultFileLocationList[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD)
				
				print('\n###############################')
				print(('Starting process %s for run %d\n' % (ProcessName, run)))
								
				if PID == 0:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					if FNALTelescope:
						session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, universal_newlines=True)
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						print(("Looking for file at ",ResultFileLocation))
						if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
						if BadProcessExec:                                                                                                                                                                                                                               
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
							print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
						cu.xrdcpTracks(run,Version)
					else:
						### copy binary file from aidarc to daq compute
						cmd = ["scp", am.RulinuxSSH + ":{}/run{:06d}.raw".format(am.BaseTrackDirRulinux, run), "{}/run{:06d}.raw".format(am.BaseTrackDirLocal,run)]
						print(cmd)
						session = am.subprocess.Popen(cmd,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, universal_newlines=True)
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						## copy from daq computer to cmslpc
						cu.xrdcpTracksRaw(run,Version) #Version doesn't matter, not used in function

						#### then run corryvreckan on cmslpc
						principal = cu.get_kerberos_principal()
						if principal: username = principal.split('@')[0]
						else: 
							print("KERBEROS NOT FOUND!!")
							return False
						print(username)

						cmd = ["cd %s && ./%s %s %s" % (am.CorryvreckanPath, am.CorryvreckanScript, run, Version)]
						print(cmd)
						session = am.subprocess.Popen(["ssh", "%s@cmslpc-el9.fnal.gov" % username, " ".join(cmd)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, universal_newlines = True)
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							print(line)
							if not line and session.poll() != None:
								break

						#### then check if file exists in output path
						OutputRoot = am.eosBaseDir+"Tracks/RecoData/%s/" % (Version) +  am.ResultTrackFileNameBeforeRunNumber + str(run) + am.ResultTrackFileNameAfterRunNumberFast
		
						if not cu.CheckExistsEOSfromDaq(OutputRoot, 2000): BadProcessExec = True                                                                                                                                                                                                                                                     
						if BadProcessExec:                                                                                                                                                                                                                               
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
							print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
						

				elif PID == 1 or PID == 11:
					if not condor:
						if pf.QueryGreenSignal(True):
							pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
							am.time.sleep(15) #may not be necessary to wait too long anymore
						print(CMD)
						conversion_path = am.os.path.dirname(CMD.split(' ')[1])
						session = am.subprocess.Popen('cd %s; %s' % (conversion_path,CMD),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
						ResultFileLocation = ResultFileLocation.replace(am.BaseTestbeamDir,am.eosBaseDir.replace('root://cmseos.fnal.gov//','/eos/uscms/'))
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation):
							BadProcessExec = True
							print(("Looking for file at ",ResultFileLocation))
                                                                                                           
						if BadProcessExec:                                                                                                                                                                                                                               
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
							print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
						print(('Finished process %s for run %d' % (ProcessName, run)))		
						print('###############################\n')

					else:
						if pf.QueryGreenSignal(True) and not ApplyFilter: pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[8], False, MyKey)
						cu.prepareDirs()

						filterList = [0]
						if ApplyFilter: filterList = am.FrequencyList 
						for freq in filterList:
							jdlname = cu.prepareJDL(PID,DigitizerKey,run,CMD,freq)
							cu.prepareExecutable(PID,DigitizerKey,run,CMD,freq)
							## cd and submit to condor
							print(CMD)
							print(jdlname)
							session = am.subprocess.Popen('cd %s; condor_submit %s; cd -' % (am.CondorDir,jdlname),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines = True)                                                                                                                                                                                   			

							## wait for submission
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break

				elif PID == 2 or PID == 3 or PID == 12:
					######## For TimingDAQ02 
					# print CMD
					if not condor: 
						if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
						# session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True)                                                                          
						### Hack for long acq            
						# CMD2 = CMD.replace("makeHitTree","addBranches2.py")    
						# print(am.TimingDAQDir)
						# CMD = CMD.replace(am.BaseTestbeamDir,am.eosBaseDir.replace('root://cmseos.fnal.gov//','/eos/uscms/'))

						CMD = './script.sh %s %s %s' %(str(run), str(Version), str(ScopeNum))
						print((am.TimingDAQDir))
						print(CMD)
						session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)                                                                                                                                                                                   			
						######## For Caltech CMS Timing computer uncomment this and comment out the above line 
						#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)  
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
								
						if DigitizerKey == 5:
							print('Sleeping for 60 sec')
							am.time.sleep(60)
							print('Done sleeping')
						
						ResultFileLocation = ResultFileLocation.replace(am.BaseTestbeamDir,am.eosBaseDir.replace('root://cmseos.fnal.gov//','/eos/uscms/'))
						ResultFileLocation = ResultFileLocation.replace('.root', '_info.root')
						print(("Check output file size > {}: {}".format(SizeCut, ResultFileLocation)))
						if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
						if BadProcessExec:   
							print((FileSizeBool(ResultFileLocation,SizeCut), am.os.path.exists(ResultFileLocation))) 
							print(ResultFileLocation)                                                                                                                                                                                                                           
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
							print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
							if PID == 2 and DigitizerKey == 3:
								import GetEntries as ge
								EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes = ge.RunEntries(ResultFileLocation)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
									am.time.sleep(0.5)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
									am.time.sleep(0.5)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)

						print(('Finished process %s for run %d' % (ProcessName, run)))		
						print('###############################\n')

					elif condor:
						if pf.QueryGreenSignal(True) and not ApplyFilter: pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[8], False, MyKey)
						## generate condor jdl and executable
						cu.prepareDirs()
						filterList = [0]
						if ApplyFilter: filterList = am.FrequencyList 
						for freq in filterList: 
							jdlname = cu.prepareJDL(PID,DigitizerKey,run,CMD,freq)
							cu.prepareExecutable(PID,DigitizerKey,run,CMD,freq)
							## cd and submit to condor
							print (CMD)
							print (run)
							print(jdlname)
							session = am.subprocess.Popen('cd %s; condor_submit %s; cd -' % (am.CondorDir,jdlname),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)                                                                                                                                                                                   			

							# print 'condor_submit %s; cd -' % (jdlname)
							# print am.CondorDir
							## wait for submission
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						

				elif PID == 5:
					## checking on condor processes
					## need to check if a job is completed but file not there -> failed.
					this_proc_key = 2
					if "Conversion" in CMD: 
						this_proc_key=1

					ProcessName = list(am.ProcessDict[this_proc_key].keys())[0] + Digitizer
					
					if "TOFHIR" in CMD:
							ProcessName = "BTLRecoNoScopeTOFHIR"
							this_proc_key = 8
					if cu.CheckExistsLogs(this_proc_key,DigitizerKey,run,CMD):
						print("log exists")
						if cu.CheckExistsEOS(ResultFileLocation,SizeCut):
							print("file exists")
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
						# else:
						# 	if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)

							am.time.sleep(1)
							if this_proc_key==2:
								import GetEntries as ge
								EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes,hits_ch1,hits_ch2,hits_ch3,hits_ch4,hits_ch5,hits_ch6,hits_ch7,hits_ch8, Events_ge8planes, Events_ge8planes_ge1pix = ge.RunEntries(ResultFileLocation)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh1", int(hits_ch1), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh2", int(hits_ch2), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh3", int(hits_ch3), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh4", int(hits_ch4), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh5", int(hits_ch5), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh6", int(hits_ch6), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh7", int(hits_ch7), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "HitsCh8", int(hits_ch8), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "Events_ge8planes", int(Events_ge8planes), False, MyKey)
									am.time.sleep(0.3)
								if pf.QueryGreenSignal(True): 
									pf.UpdateAttributeStatus2(str(FieldID), "Events_ge8planes_ge1pix", int(Events_ge8planes_ge1pix), False, MyKey)
									am.time.sleep(0.3)

						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)

						## add to list of processes to check on
						## loop over list of runs to check on, grep condor logs to tell when complete, then proceed with checks.
					am.time.sleep(1)
				elif PID == 6 or PID == 10:
					## copy raw scope files
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					#am.time.sleep(60) ## allow scope to save at least first channel 
					if (Digitizer == "TOFHIR"):
						#call special TOFHIR xrdcp function for TOFHIR
						cpstatus = cu.xrdcpTOFHIR(run)
					else :
						#cpstatus = cu.xrdcpRaw2(run,Digitizer)
						cpstatus = cu.xrdcpRawTwoScope(run,Digitizer, ScopeNum)

					am.time.sleep(0.5)
					if cpstatus and pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey) 
					elif not cpstatus and pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)
					am.time.sleep(2.5)
				elif (PID == 7 or PID == 8):
					if pf.QueryGreenSignal(True) and not ApplyFilter: pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[8], False, MyKey)

					## generate condor jdl and executable
					cu.prepareDirs()
					filterList = [0]
					if ApplyFilter: filterList = am.FrequencyList 
					for freq in filterList: 
						jdlname = cu.prepareJDLTOFHIR(PID,DigitizerKey,run,CMD,freq)
						cu.prepareExecutableTOFHIR(PID,DigitizerKey,run,CMD,freq)
						## cd and submit to condor
						#print CMD
						print(run)
						session = am.subprocess.Popen('cd %s; condor_submit %s; cd -' % (am.CondorDir,jdlname),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)                                                                                                                                                                                   			
						print('ciao')
						#			# print 'condor_submit %s; cd -' % (jdlname)
						# print am.CondorDir
						## wait for submission
						line = session.stdout.readline()
						print(line)
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break


				elif PID == 13: 
					######## For Merging 
					# print CMD
					if not condor: 
						if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)

						CMD = './merge_script.sh %s %s ' %(str(run), str(Version))
						print((am.TimingDAQDir))
						print(CMD)
						session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)                                                                                                                                                                                   			
						######## For Caltech CMS Timing computer uncomment this and comment out the above line 
						#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)  
						while True:
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
								
						
						ResultFileLocation = ResultFileLocation.replace(am.BaseTestbeamDir,am.eosBaseDir.replace('root://cmseos.fnal.gov//','/eos/uscms/'))
						ResultFileLocation = ResultFileLocation.replace('.root', '_info.root')
						print(("Check output file size > {}: {}".format(SizeCut, ResultFileLocation)))
						if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
						if BadProcessExec:   
							print((FileSizeBool(ResultFileLocation,SizeCut), am.os.path.exists(ResultFileLocation))) 
							print(ResultFileLocation)                                                                                                                                                                                                                           
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
							print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
						else:
							if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)

						print(('Finished process %s for run %d' % (ProcessName, run)))		
						print('###############################\n')

					elif condor:
						if pf.QueryGreenSignal(True) and not ApplyFilter: pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[8], False, MyKey)
						## generate condor jdl and executable
						cu.prepareDirs()
						filterList = [0]
						if ApplyFilter: filterList = am.FrequencyList 
						for freq in filterList: 
							jdlname = cu.prepareJDL(PID,DigitizerKey,run,CMD,freq)
							cu.prepareExecutable(PID,DigitizerKey,run,CMD,freq)
							## cd and submit to condor
							print (CMD)
							print (run)
							print(jdlname)
							session = am.subprocess.Popen('cd %s; condor_submit %s; cd -' % (am.CondorDir,jdlname),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)                                                                                                                                                                                   			

							# print 'condor_submit %s; cd -' % (jdlname)
							# print am.CondorDir
							## wait for submission
							line = session.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session.poll() != None:
								break
						

			if RunNumber != -1:
				break
			
			am.time.sleep(4)	
		
		else:
			print('\n######################')
			print('No runs to process!!!!')
			print('######################\n')
			am.time.sleep(4)

def ProcessExecBTLForTOFHIRTracks(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
		
		if PID == 0:
			ProcessName = list(am.ProcessDict[PID].keys())[0]
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TrackingCMDs(RunNumber, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 1:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.ConversionCMDs(RunNumber, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 2:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoTracking = True
			CMDList1, CMDList2, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTLForTOFHIRTracks(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 3:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			DoTracking = False	
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
			#print RunList
		RunListInt = list(map(int,RunList))
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		if CMDList1 != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD1 = CMDList1[index]  
				CMD2 = CMDList2[index] 
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation = ResultFileLocationList[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD1)
				am.ProcessLog(ProcessName, run, CMD2)
				
				print('\n###############################')
				print(('Starting process %s for run %d\n' % (ProcessName, run)))
								
				if DigitizerKey == 5:
						print('Sleeping for 1 sec')
						am.time.sleep(1)
						print('Done sleeping')
								
				if PID == 0:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, universal_newlines=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 1:
					am.time.sleep(60)
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					# session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
					print(CMD)
					session = am.subprocess.Popen(CMD,stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					if Digitizer == am.DigitizerDict[5]:
						EnvirSetup1 = am.TOFHIRRecoDir
						EnvirSetup2 = am.TOFHIRRecoDir2
						session1 = am.subprocess.Popen('cd %s; %s;cd -' % (EnvirSetup1, str(CMD1)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
						while True:
							line = session1.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session1.poll() != None:
								break
						session2 = am.subprocess.Popen('cd %s; %s;cd -' % (EnvirSetup2, str(CMD2)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
						while True:
							line = session2.stdout.readline()
							am.ProcessLog(ProcessName, run, line)
							if not line and session2.poll() != None:
								break				
				if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
					if PID == 2 and DigitizerKey == 3:
						import GetEntries as ge
						EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes = ge.RunEntries(ResultFileLocation)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)

				print(('Finished process %s for run %d' % (ProcessName, run)))		
				print('###############################\n')
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print('\n######################')
			print('No runs to process!!!!')
			print('######################\n')
			am.time.sleep(4)

def ProcessExecBTL(OrderOfExecution, PID, SaveWaveformBool = None, Version = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version = Version
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
		if PID == 0:
			ProcessName = list(am.ProcessDict[PID].keys())[0]
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TrackingCMDs(RunNumber, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 1:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.ConversionCMDs(RunNumber, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 2:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoTracking = True
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 3:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			DoTracking = False	
			CMDList, ResultFileLocationList, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
			#print RunList
		RunListInt = list(map(int,RunList))
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		print(RunListInt)

		if CMDList != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD = CMDList[index]  
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation = ResultFileLocationList[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD)
				
				print('\n###############################')
				print(('Starting process %s for run %d\n' % (ProcessName, run)))
								
				if DigitizerKey == 5:
						print('Sleeping for 60 sec')
						am.time.sleep(60)
						print('Done sleeping')
				
				if PID == 0:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen(["ssh", am.RulinuxSSH, str(CMD)],stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, universal_newlines=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 1:
					am.time.sleep(60)
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					session = am.subprocess.Popen('source %s; %s' % (am.EnvSetupPath,str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				elif PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					if Digitizer == am.DigitizerDict[5]:
						if PID == 3:
							EnvirSetup = am.TOFHIRRecoDir
						elif PID == 2:
							EnvirSetup = am.TOFHIRRecoDir2
						session = am.subprocess.Popen('cd %s; %s;cd -' % (EnvirSetup, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
					else:
						session = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)                                                                                                                                                                                   			
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session.poll() != None:
							break
				
				if FileSizeBool(ResultFileLocation,SizeCut) or not am.os.path.exists(ResultFileLocation): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
					if PID == 2 and DigitizerKey == 3:
						import GetEntries as ge
						EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes,hits_ch1,hits_ch2,hits_ch3,hits_ch4 = ge.RunEntries(ResultFileLocation)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackScope", int(EntriesWithTrack), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackAndHitScope", int(EntriesWithTrackAndHit), False, MyKey)
							am.time.sleep(0.5)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithHitScope", int(EntriesWithHit), False, MyKey)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "EntriesWithTrackWithoutNplanesScope", int(EntriesWithTrackWithoutNplanes), False, MyKey)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh1", int(hits_ch1), False, MyKey)
							am.time.sleep(0.3)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh2", int(hits_ch2), False, MyKey)
							am.time.sleep(0.3)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh3", int(hits_ch3), False, MyKey)
							am.time.sleep(0.3)
						if pf.QueryGreenSignal(True): 
							pf.UpdateAttributeStatus2(str(FieldID), "HitsCh4", int(hits_ch4), False, MyKey)
							am.time.sleep(0.3)

				print(('Finished process %s for run %d' % (ProcessName, run)))		
				print('###############################\n')
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print('\n######################')
			print('No runs to process!!!!')
			print('######################\n')
			am.time.sleep(4)



def ProcessExecApril(OrderOfExecution, PID, SaveWaveformBool = None, Version1 = None, Version2 = None, RunNumber = -1, DigitizerKey = -1 , MyKey = None, GetRunListEachTime = True):
	
	if not DigitizerKey == -1: Digitizer = am.DigitizerDict[DigitizerKey]
	SaveWaveformBool = SaveWaveformBool
	Version2 = Version2
	Version1 = Version1
	RunNumber = RunNumber
	MyKey = MyKey 

	while True:
	
		if PID == 2:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer	
			DoTracking = True
			CMDList1, CMDList2, ResultFileLocationList1, ResultFileLocationList2, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version1, Version2, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']
		elif PID == 3:
			ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
			DoTracking = False	
			CMDList1, CMSList2, ResultFileLocationList1, ResultFileLocationList2, RunList, FieldIDList = pc.TimingDAQCMDsBTL(RunNumber, SaveWaveformBool, Version1, Version2, DoTracking, Digitizer, MyKey, False)
			SizeCut = am.ProcessDict[PID][list(am.ProcessDict[PID].keys())[0]]['SizeCut']

		RunListInt = list(map(int,RunList))
		if OrderOfExecution == 1: 
			RunListInt.sort() #Ascending Sorting
		else:
			RunListInt.sort(reverse = True)

		if CMDList1 != []:	

			if GetRunListEachTime:
				RunListInt = RunListInt[:1] #Just do the first run of the list

			for run in RunListInt: 
			
				index = RunList.index(run)      
				CMD1 = CMDList1[index]  
				CMD2 = CMDList2[index] 
				if RunNumber != -1: 
					FieldID = FieldIDList[index][0]
				else:
					FieldID = FieldIDList[index]
				ResultFileLocation1 = ResultFileLocationList1[index]
				ResultFileLocation2 = ResultFileLocationList2[index]
				BadProcessExec = False

				##### Command will be in the log file
				am.DeleteProcessLog(ProcessName, run) ###########Delete previous log file if exists
				am.ProcessLog(ProcessName, run, CMD1)
				
				print('\n###############################')
				print(('Starting process %s for run %d\n' % (ProcessName, run)))
								
				if PID == 2 or PID == 3:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[1], False, MyKey)
					######## For TimingDAQ02 
					session1 = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD1)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session1.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session1.poll() != None:
							break
					session2 = am.subprocess.Popen('cd %s; source %s; %s;cd -' % (am.TimingDAQDir, am.EnvSetupPath, str(CMD2)),stdout=am.subprocess.PIPE,stderr=am.subprocess.STDOUT, shell=True, universal_newlines=True)
					######## For Caltech CMS Timing computer uncomment this and comment out the above line 
					#session = am.subprocess.Popen('cd %s; %s;cd -' % (am.TimingDAQDir, str(CMD)),stdout=am.subprocess.PIPE, shell=True)                                                                                                                                                                                   			
					while True:
						line = session2.stdout.readline()
						am.ProcessLog(ProcessName, run, line)
						if not line and session2.poll() != None:
							break
				
				if FileSizeBool(ResultFileLocation1,SizeCut) or FileSizeBool(ResultFileLocation2,SizeCut) or not am.os.path.exists(ResultFileLocation1) or not am.os.path.exists(ResultFileLocation2): BadProcessExec = True                                                                                                                                                                                                                                                     
				if BadProcessExec:                                                                                                                                                                                                                               
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[2], False, MyKey)  
					print(('Bad %s execution for run %d. Either the CMD format is wrong or somwthing else was wrong while execution. Please check the ProcessLog to know more.\n' % (ProcessName, run)))
				else:
					if pf.QueryGreenSignal(True): pf.UpdateAttributeStatus(str(FieldID), ProcessName, am.StatusDict[0], False, MyKey)
				
				print(('Finished process %s for run %d' % (ProcessName, run)))		
				print('###############################\n')
			
			if RunNumber != -1:
				break
			am.time.sleep(1)	
		
		else:
			print('\n######################')
			print('No runs to process!!!!')
			print('######################\n')
			am.time.sleep(4)


