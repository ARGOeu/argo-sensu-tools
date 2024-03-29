import unittest

from argo_sensu_tools.run import process_line

LINE1 = "[1704795120] PROCESS_SERVICE_CHECK_RESULT;ce2.cis.gov.pl;" \
        "org.nordugrid.ARC-CE-sw-python-ops;0;Found Python version 2.7.5.\n"

LINE2 = ("[1704795120] PROCESS_SERVICE_CHECK_RESULT;t2-ce-04.to.infn.it;"
         "ch.cern.HTCondorCE-JobState;0;"
         "OK - Job successfully completed (status:COMPLETED, id:5837754)\\n"
         "=== ETF job log:\\nTimeout limits configured were:\\n=== Credentials"
         ":\\nx509:\\n/DC=EU/DC=EGI/C=HR/O=Robots/O=SRCE/CN=Robot:argo-egi@"
         "cro-ngi.hr/CN=1520149896\\r\\n/ops/Role=NULL/Capability=NULL\\r\\n\\n"
         "=== Job description:\\nJDL([(\\'universe\\', \\'vanilla\\'), "
         "(\\'executable\\', \\'hostname\\'), (\\'transfer_executable\\', "
         "\\'true\\'), (\\'output\\', \\'/var/lib/gridprobes/ops/scondor/"
         "t2-ce-04.to.infn.it/out/gridjob.out\\'), (\\'error\\', \\'/var/lib/"
         "gridprobes/ops/scondor/t2-ce-04.to.infn.it/out/gridjob.err\\'), "
         "(\\'log\\', \\'/var/lib/gridprobes/ops/scondor/t2-ce-04.to.infn.it/"
         "out/gridjob.log\\'), (\\'log_xml\\', \\'true\\'), "
         "(\\'should_transfer_files\\', \\'YES\\'), "
         "(\\'when_to_transfer_output\\', \\'ON_EXIT\\'), "
         "(\\'use_x509userproxy\\', \\'true\\')])\\n=== Job submission command:"
         "\\ncondor_submit --spool --name t2-ce-04.to.infn.it --pool "
         "t2-ce-04.to.infn.it:9619 /var/lib/gridprobes/ops/scondor/"
         "t2-ce-04.to.infn.it/gridjob.jdl\\nSubmitting job(s).\\r\\n1 job(s) "
         "submitted to cluster 5837754.\\r\\n\\n=== Job log:\\nArguments = "
         "\"\"\\r\\nBytesRecvd = 15784.0\\r\\nBytesSent = 11.0\\r\\nClusterId ="
         " 5837754\\r\\nCmd = \"hostname\"\\r\\nCommittedSlotTime = 0\\r\\n"
         "CommittedSuspensionTime = 0\\r\\nCommittedTime = 0\\r\\n"
         "CompletionDate = 1704957442\\r\\nCondorPlatform = \"$CondorPlatform: "
         "x86_64_CentOS7 $\"\\r\\nCondorVersion = \"$CondorVersion: 9.0.20 "
         "Nov 15 2023 BuildID: 690225 PackageID: 9.0.20-1 $\"\\r\\nCoreSize = 0"
         "\\r\\nCumulativeRemoteSysCpu = 0.0\\r\\nCumulativeRemoteUserCpu = 0.0"
         "\\r\\nCumulativeSlotTime = 0\\r\\nCumulativeSuspensionTime = 0\\r\\n"
         "CurrentHosts = 0\\r\\nDiskUsage = 40\\r\\nDiskUsage_RAW = 40\\r\\n"
         "EncryptExecuteDirectory = false\\r\\nEnteredCurrentStatus = "
         "1704957407\\r\\nEnvironment = \"\"\\r\\nErr = "
         "\"_condor_stderr\"\\r\\nExecutableSize = 17\\r\\nExecutableSize_RAW "
         "= 16\\r\\nExitBySignal = false\\r\\nExitCode = 0\\r\\nExitStatus = 0"
         "\\r\\nGlobalJobId = \"t2-ce-04.to.infn.it#5837754.0#1704957405"
         "\"\\r\\nHoldReason = undefined\\r\\nHoldReasonCode = undefined"
         "\\r\\nImageSize = 17\\r\\nImageSize_RAW = 16\\r\\nIn = \"/dev/null\""
         "\\r\\nIwd = \"/var/lib/condor-ce/spool/7754/0/cluster5837754.proc0."
         "subproc0\"\\r\\nJobCurrentStartDate = 1704957440\\r\\n"
         "JobCurrentStartExecutingDate = 1704957442\\r\\nJobFinishedHookDone = "
         "1704957467\\r\\nJobLeaseDuration = 2400\\r\\nJobNotification = 0"
         "\\r\\nJobPrio = 0\\r\\nJobRunCount = 1\\r\\nJobStartDate = 1704957440"
         "\\r\\nJobStatus = 4\\r\\nJobUniverse = 5\\r\\nLastHoldReason = "
         "\"Spooling input data files\"\\r\\nLastHoldReasonCode = 16\\r\\n"
         "LastJobStatus = 1\\r\\nLastSuspensionTime = 0\\r\\nLeaveJobInQueue = "
         "JobStatus == 4 \u0026\u0026 (CompletionDate =?= undefined "
         "\\\\u2758\\\\u2758 CompletionDate == 0 \\\\u2758\\\\u2758 ((time() - "
         "CompletionDate) \u003c 864000))\\r\\nManaged = \"ScheddDone\"\\r\\n"
         "ManagedManager = \"\"\\r\\nMaxHosts = 1\\r\\nMemoryUsage = "
         "((ResidentSetSize + 1023) / 1024)\\r\\nMinHosts = 1\\r\\nMyType = "
         "\"Job\"\\r\\nNumCkpts = 0\\r\\nNumCkpts_RAW = 0\\r\\n"
         "NumJobCompletions = 0\\r\\nNumJobMatches = 1\\r\\nNumJobStarts = 1"
         "\\r\\nNumRestarts = 0\\r\\nNumShadowStarts = 1\\r\\nNumSystemHolds "
         "= 0\\r\\nOnExitHold = false\\r\\nOnExitRemove = true\\r\\nOut = "
         "\"_condor_stdout\"\\r\\nOwner = \"ops016\"\\r\\nPeriodicHold = false"
         "\\r\\nPeriodicRelease = false\\r\\nPeriodicRemove = false\\r\\nProcId"
         " = 0\\r\\nQDate = 1704957404\\r\\nRank = 0.0\\r\\nReleaseReason = "
         "\"Data files spooled\"\\r\\nRemoteSysCpu = 0.0\\r\\nRemoteUserCpu = "
         "0.0\\r\\nRemoteWallClockTime = 2.0\\r\\nRequestCpus = 1\\r\\n"
         "RequestDisk = DiskUsage\\r\\nRequestMemory = ifthenelse("
         "MemoryUsage =!= undefined,MemoryUsage,(ImageSize + 1023) / 1024)"
         "\\r\\nRequirements = (TARGET.Arch == \"X86_64\") \u0026\u0026 "
         "(TARGET.OpSys == \"LINUX\") \u0026\u0026 (TARGET.Disk \u003e= "
         "RequestDisk) \u0026\u0026 (TARGET.Memory \u003e= RequestMemory) "
         "\u0026\u0026 (TARGET.HasFileTransfer)\\r\\nResidentSetSize = 0\\r\\n"
         "ResidentSetSize_RAW = 0\\r\\nRootDir = \"/\"\\r\\nRoutedToJobId = "
         "\"6335938.0\"\\r\\nScratchDirFileCount = 10\\r\\nServerTime = "
         "1704960988\\r\\nShouldTransferFiles = \"YES\"\\r\\n"
         "SpooledOutputFiles = \"\"\\r\\nStageInFinish = 1704957406\\r\\n"
         "StageInStart = 1704957406\\r\\nStreamErr = false\\r\\n"
         "StreamOut = false\\r\\nSUBMIT_Cmd = \"/var/lib/gridprobes/ops/"
         "scondor/t2-ce-04.to.infn.it/hostname\"\\r\\nSUBMIT_Iwd = \""
         "/var/lib/gridprobes/ops/scondor/t2-ce-04.to.infn.it\"\\r\\n"
         "SUBMIT_TransferOutputRemaps = \"_condor_stdout=/var/lib/gridprobes/"
         "ops/scondor/t2-ce-04.to.infn.it/out/gridjob.out;_condor_stderr="
         "/var/lib/gridprobes/ops/scondor/t2-ce-04.to.infn.it/out/gridjob.err"
         "\"\\r\\nSUBMIT_UserLog = \"/var/lib/gridprobes/ops/scondor/"
         "t2-ce-04.to.infn.it/out/gridjob.log\"\\r\\nSUBMIT_x509userproxy = "
         "\"/etc/sensu/certs/userproxy.pem\"\\r\\nTargetType = \"Machine"
         "\"\\r\\nTotalSubmitProcs = 1\\r\\nTotalSuspensions = 0\\r\\n"
         "TransferIn = false\\r\\nTransferInputSizeMB = 0\\r\\n"
         "TransferOutputRemaps = undefined\\r\\nUser = \"ops016@infnto\"\\r\\n"
         "UserLog = \"gridjob.log\"\\r\\nUserLogUseXML = true\\r\\n"
         "WantCheckpoint = false\\r\\nWantRemoteIO = true\\r\\n"
         "WantRemoteSyscalls = false\\r\\nWhenToTransferOutput = \"ON_EXIT\""
         "\\r\\nx509userproxy = \"userproxy.pem\"\\r\\nx509UserProxyEmail = "
         "\"argo-egi@cro-ngi.hr\"\\r\\nx509UserProxyExpiration = 1704988962"
         "\\r\\nx509UserProxyFirstFQAN = \"/ops/Role=NULL/Capability=NULL"
         "\"\\r\\nx509UserProxyFQAN = \"/DC=EU/DC=EGI/C=HR/O=Robots/O=SRCE/CN="
         "Robot:argo-egi@cro-ngi.hr,/ops/Role=NULL/Capability=NULL\"\\r\\n"
         "x509userproxysubject = \"/DC=EU/DC=EGI/C=HR/O=Robots/O=SRCE/CN="
         "Robot:argo-egi@cro-ngi.hr\"\\r\\nx509UserProxyVOName = \"ops\""
         "\\r\\n\\r\\n\\n=== Last job status:\\nArguments = \"\"\\r\\n"
         "BytesRecvd = 15784.0\\r\\nBytesSent = 11.0\\r\\nClusterId = 5837754"
         "\\r\\nCmd = \"hostname\"\\r\\nCommittedSlotTime = 0\\r\\n"
         "CommittedSuspensionTime = 0\\r\\nCommittedTime = 0\\r\\n"
         "CompletionDate = 1704957442\\r\\nCondorPlatform = \"$CondorPlatform: "
         "x86_64_CentOS7 $\"\\r\\nCondorVersion = \"$CondorVersion: 9.0.20 "
         "Nov 15 2023 BuildID: 690225 PackageID: 9.0.20-1 $\"\\r\\nCoreSize = 0"
         "\\r\\nCumulativeRemoteSysCpu = 0.0\\r\\nCumulativeRemoteUserCpu = 0.0"
         "\\r\\nCumulativeSlotTime = 0\\r\\nCumulativeSuspensionTime = 0\\r\\n"
         "CurrentHosts = 0\\r\\nDiskUsage = 40\\r\\nDiskUsage_RAW = 40\\r\\n"
         "EncryptExecuteDirectory = false\\r\\nEnteredCurrentStatus = "
         "1704957407\\r\\nEnvironment = \"\"\\r\\nErr = \"_condor_stderr"
         "\"\\r\\nExecutableSize = 17\\r\\nExecutableSize_RAW = 16\\r\\n"
         "ExitBySignal = false\\r\\nExitCode = 0\\r\\nExitStatus = 0\\r\\n"
         "GlobalJobId = \"t2-ce-04.to.infn.it#5837754.0#1704957405\"\\r\\n"
         "HoldReason = undefined\\r\\nHoldReasonCode = undefined\\r\\n"
         "ImageSize = 17\\r\\nImageSize_RAW = 16\\r\\nIn = \"/dev/null\"\\r\\n"
         "Iwd = \"/var/lib/condor-ce/spool/7754/0/cluster5837754.proc0.subproc0"
         "\"\\r\\nJobCurrentStartDate = 1704957440\\r\\n"
         "JobCurrentStartExecutingDate = 1704957442\\r\\nJobFinishedHookDone = "
         "1704957467\\r\\nJobLeaseDuration = 2400\\r\\nJobNotification = 0"
         "\\r\\nJobPrio = 0\\r\\nJobRunCount = 1\\r\\nJobStartDate = "
         "1704957440\\r\\nJobStatus = 4\\r\\nJobUniverse = 5\\r\\n"
         "LastHoldReason = \"Spooling input data files\"\\r\\n"
         "LastHoldReasonCode = 16\\r\\nLastJobStatus = 1\\r\\n"
         "LastSuspensionTime = 0\\r\\nLeaveJobInQueue = JobStatus == 4 "
         "\u0026\u0026 (CompletionDate =?= undefined \\\\u2758\\\\u2758 "
         "CompletionDate == 0 \\\\u2758\\\\u2758 ((time() - CompletionDate) "
         "\u003c 864000))\\r\\nManaged = \"ScheddDone\"\\r\\nManagedManager = "
         "\"\"\\r\\nMaxHosts = 1\\r\\nMemoryUsage = ((ResidentSetSize + 1023) /"
         " 1024)\\r\\nMinHosts = 1\\r\\nMyType = \"Job\"\\r\\nNumCkpts = 0"
         "\\r\\nNumCkpts_RAW = 0\\r\\nNumJobCompletions = 0\\r\\n"
         "NumJobMatches = 1\\r\\nNumJobStarts = 1\\r\\nNumRestarts = 0\\r\\n"
         "NumShadowStarts = 1\\r\\nNumSystemHolds = 0\\r\\nOnExitHold = false"
         "\\r\\nOnExitRemove = true\\r\\nOut = \"_condor_stdout\"\\r\\nOwner = "
         "\"ops016\"\\r\\nPeriodicHold = false\\r\\nPeriodicRelease = false"
         "\\r\\nPeriodicRemove = false\\r\\nProcId = 0\\r\\nQDate = 1704957404"
         "\\r\\nRank = 0.0\\r\\nReleaseReason = \"Data files spooled\"\\r\\n"
         "RemoteSysCpu = 0.0\\r\\nRemoteUserCpu = 0.0\\r\\n"
         "RemoteWallClockTime = 2.0\\r\\nRequestCpus = 1\\r\\nRequestDisk = "
         "DiskUsage\\r\\nRequestMemory = ifthenelse(MemoryUsage =!= undefined,"
         "MemoryUsage,(ImageSize + 1023) / 1024)\\r\\nRequirements = ("
         "TARGET.Arch == \"X86_64\") \u0026\u0026 (TARGET.OpSys == \"LINUX\") "
         "\u0026\u0026 (TARGET.Disk \u003e= RequestDisk) \u0026\u0026 ("
         "TARGET.Memory \u003e= RequestMemory) \u0026\u0026 ("
         "TARGET.HasFileTransfer)\\r\\nResidentSetSize = 0\\r\\n"
         "ResidentSetSize_RAW = 0\\r\\nRootDir = \"/\"\\r\\nRoutedToJobId = "
         "\"6335938.0\"\\r\\nScratchDirFileCount = 10\\r\\nServerTime = "
         "1704960987\\r\\nShouldTransferFiles = \"YES\"\\r\\n"
         "SpooledOutputFiles = \"\"\\r\\nStageInFinish = 1704957406\\r\\n"
         "StageInStart = 1704957406\\r\\nStreamErr = false\\r\\nStreamOut = "
         "false\\r\\nSUBMIT_Cmd = \"/var/lib/gridprobes/ops/scondor/"
         "t2-ce-04.to.infn.it/hostname\"\\r\\nSUBMIT_Iwd = \"/var/lib/"
         "gridprobes/ops/scondor/t2-ce-04.to.infn.it\"\\r\\n"
         "SUBMIT_TransferOutputRemaps = \"_condor_stdout=/var/lib/gridprobes/"
         "ops/scondor/t2-ce-04.to.infn.it/out/gridjob.out;_condor_stderr=/"
         "var/lib/gridprobes/ops/scondor/t2-ce-04.to.infn.it/out/gridjob.err"
         "\"\\r\\nSUBMIT_UserLog = \"/var/lib/gridprobes/ops/scondor/"
         "t2-ce-04.to.infn.it/out/gridjob.log\"\\r\\nSUBMIT_x509userproxy = "
         "\"/etc/sensu/certs/userproxy.pem\"\\r\\nTargetType = \""
         "Machine\"\\r\\nTotalSubmitProcs = 1\\r\\nTotalSuspensions = 0\\r\\n"
         "TransferIn = false\\r\\nTransferInputSizeMB = 0\\r\\n"
         "TransferOutputRemaps = undefined\\r\\nUser = \"ops016@infnto\"\\r\\n"
         "UserLog = \"gridjob.log\"\\r\\nUserLogUseXML = true\\r\\n"
         "WantCheckpoint = false\\r\\nWantRemoteIO = true\\r\\n"
         "WantRemoteSyscalls = false\\r\\nWhenToTransferOutput = "
         "\"ON_EXIT\"\\r\\nx509userproxy = \"userproxy.pem\"\\r\\n"
         "x509UserProxyEmail = \"argo-egi@cro-ngi.hr\"\\r\\n"
         "x509UserProxyExpiration = 1704988962\\r\\nx509UserProxyFirstFQAN = "
         "\"/ops/Role=NULL/Capability=NULL\"\\r\\nx509UserProxyFQAN = "
         "\"/DC=EU/DC=EGI/C=HR/O=Robots/O=SRCE/CN=Robot:argo-egi@cro-ngi.hr,"
         "/ops/Role=NULL/Capability=NULL\"\\r\\nx509userproxysubject = "
         "\"/DC=EU/DC=EGI/C=HR/O=Robots/O=SRCE/CN=Robot:argo-egi@cro-ngi.hr\""
         "\\r\\nx509UserProxyVOName = \"ops\"\\r\\n\\r\\n\\nCOMPLETED")


class ProcessLineTests(unittest.TestCase):
    def test_process_line(self):
        self.assertEqual(
            process_line(LINE1),
            "[1704795120] PROCESS_SERVICE_CHECK_RESULT;ce2.cis.gov.pl;"
            "org.nordugrid.ARC-CE-sw-python-ops;0;Found Python version 2.7.5."
        )
        self.assertEqual(
            process_line(LINE2),
            "[1704795120] PROCESS_SERVICE_CHECK_RESULT;t2-ce-04.to.infn.it;"
            "ch.cern.HTCondorCE-JobState;0;"
            "OK - Job successfully completed (status:COMPLETED, id:5837754)"
            "(...)COMPLETED"
        )
