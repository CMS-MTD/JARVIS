from ProcessExec import *
import condorUtils as cu
import time
ExecutionOrder = 0 #This is descending Run number order, Refer to the dictionary in all modules
PID = 2 #2 means Timingdaq, Refer to the dictionary in all modules
GetRunListEachTime = False #Could be true also for this case.

#Give the range of run numbers to process
StartRunNumber = 99 #35084#34511   
StopRunNumber = 1903#34679

############ Doesn't matter for tracking ###########
SaveWaveForms = False
telescope_version = "v1"
ConfigVersion = "v2"
scopeNum = "1" #set to "1" this if doing re-reco + merging of both scopes, will do scope 2 automatically as well
testbeam_name = "2026_05_SNSPD"
DigitizerKey = 6 #key=3 for KeySightScope, Refer Allmodules

print("\n##############################")
print("## Starting Data processing ##")
print("##############################\n")
Digitizer = am.DigitizerDict[DigitizerKey]
ProcessName = list(am.ProcessDict[PID].keys())[0] + Digitizer
#ConfigFilePath = am.TwoStageRecoDigitizers[Digitizer]['ConfigFileBasePath'] + testbeam_name + '/'+'Scope%s_%s.config' % (scopeNum,ConfigVersion)
ConfigFilePath = am.TwoStageRecoDigitizers[Digitizer]['ConfigFileBasePath'].replace("LecroyScope_","config/"+testbeam_name+'/')+'LecroyScope_Scope%s_%s.config' % (scopeNum,ConfigVersion)
RecoBaseLocalPath = am.TwoStageRecoDigitizers[Digitizer]['RecoTimingDAQLocalPath'] + 'RecoWithTracks/' + ConfigVersion + '/'+"Scope"+scopeNum+'/'
#RecoBaseLocalPath = RecoBaseLocalPath.replace("LecroyScope", "LecroyScope"+scopeNum)

cu.prepareDirs()
if not am.os.path.exists(RecoBaseLocalPath):
	am.os.makedirs(RecoBaseLocalPath)

for run in range(StartRunNumber, StopRunNumber + 1):
	RawLocalPath = (
		am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQLocalPath']
		+ "Scope" + scopeNum +'/'
		+ am.TwoStageRecoDigitizers[Digitizer]['RawTimingDAQFileNameFormat']
		+ str(run)
		+ '.root'
	)
	RecoLocalPath = (
		RecoBaseLocalPath
		+ am.TwoStageRecoDigitizers[Digitizer]['FinalFileNameFormat']
		+ str(run)
		+ '.root'
	)
	TrackFilePathLocal = (
		am.BaseTrackDirLocal + telescope_version+'/'
		+ am.ResultTrackFileNameBeforeRunNumber
		+ str(run)
		+ am.ResultTrackFileNameAfterRunNumberFast
	).replace("Raw","Reco")
	CMD = (
		'./{exec_name} --config_file={config} --input_file={raw} '
		'--output_file={reco} --save_meas --pixel_input_file={tracks}'
	).format(
		exec_name=am.TwoStageRecoDigitizers[Digitizer]['DatToROOTExec'],
		config=ConfigFilePath,
		raw=RawLocalPath,
		reco=RecoLocalPath,
		tracks=TrackFilePathLocal,
	)
	am.DeleteProcessLog(ProcessName, run)
	am.ProcessLog(ProcessName, run, CMD)
	jdlname = cu.prepareJDL(PID, DigitizerKey, run, CMD)
	cu.prepareExecutable(PID, DigitizerKey, run, CMD)
	print(CMD)
	print(run)
	print(jdlname)
	session = am.subprocess.Popen(
		'cd %s; condor_submit %s; cd -' % (am.CondorDir, jdlname),
		stdout=am.subprocess.PIPE,
		stderr=am.subprocess.STDOUT,
		shell=True,
		universal_newlines=True,
	)
	line = session.stdout.readline()
	am.ProcessLog(ProcessName, run, line)
	time.sleep(0.25)

print("\n##############################")
print("## Completed Data processing ##")
print("##############################\n")
