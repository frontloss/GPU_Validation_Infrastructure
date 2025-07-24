namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.ServiceProcess;
    using System.Net;
    using System.Text.RegularExpressions;

    class InitClearDumpsNEvents : InitEnvironment
    {
        private RebootDataProvider _rebootReason = null;
        private string bugCheckCode = null;
        IApplicationSettings _appSettings = null;
        public InitClearDumpsNEvents(IApplicationManager argManager)
            : base(argManager)
        {
            if(File.Exists(CommonExtensions._mpBSODAnalysisPath))
                _rebootReason = CommonExtensions.RebootLogDeSerialize();
            this._appSettings = argManager.ApplicationSettings;
        }
        public override void DoWork()
        {
            ValidateFile();
            CommonExtensions.DumpPaths.ToList().ForEach(kV =>
            {
                if (!(File.Exists(CommonExtensions._mpBSODAnalysisPath)))
                {
                    if (Directory.Exists(kV.Value))
                    {
                        string[] files = Directory.GetFiles(kV.Value, "*.dmp");
                        if (files.Count() > 0)
                            files.ToList().ForEach(f => File.Delete(f));
                    }
                }
                else
                {
                    Log.Verbose("Looking for {0}'s @ {1}", kV.Key, kV.Value);
                    if ((kV.Key == DumpCategory.Minidump))
                    {
                        if (Directory.Exists(kV.Value))
                        {
                            string[] files = Directory.GetFiles(kV.Value, "*.dmp");
                            if (files.Count() > 0)
                                Log.Alert("{0} dump found", kV.Key);
                        }
                    }
                    else if ((kV.Key == DumpCategory.Memorydump))
                        this.ReportDump(kV.Value);
                    else
                        this.CheckForDumpsNAct(kV.Value, this.DeleteDump);
                }
            });

            ServiceController sC = new ServiceController("eventlog");
            if (sC.Status == ServiceControllerStatus.Running)
            {
                Log.Verbose("{0} ({1}) service is running", sC.DisplayName, sC.ServiceName);
                EventLog eventLog = new EventLog("System", Environment.MachineName);
                Log.Verbose("Clearing System EventLog on {0}", Environment.MachineName);
                eventLog.Clear();
            }
            else
                Log.Abort("{0} ({1}) service is not running!", sC.DisplayName, sC.ServiceName);
        }
        private void CheckForDumpsNAct(string argPath, Action<string, string> argAction)
        {
            if (Directory.Exists(argPath))
            {
                string[] files = Directory.GetFiles(argPath, "*.dmp");
                if (files.Count() > 0)
                    files.ToList().ForEach(f => argAction(argPath, f));
                else
                    Log.Verbose("No dump file(s) found!");
            }
            else
                Log.Verbose("No such directory found!");
        }
        private void DeleteDump(string argPath, string argFile)
        {
            Log.Alert("Deleting {0}", argFile);
            File.Delete(Path.Combine(argPath, argFile));
        }
        private void ReportDump(string argPath)
        {
            bool bsod = false;
            if (Directory.Exists(argPath))
            {
                string[] files = Directory.GetFiles(argPath, "*.dmp");
                DateTime bsodOccuranceEventViewer = AssertBsodEvent();
                if (bsodOccuranceEventViewer != default(DateTime))
                {
                    Log.Alert("BSOD Occured at {0} from EventViewer", bsodOccuranceEventViewer);
                    bsod = true;
                    if (files.Length > 0)
                    {
                        DateTime dumpCreationTime = File.GetCreationTime(Path.Combine(argPath, files[0]));
                        if (!(dumpCreationTime.Hour == bsodOccuranceEventViewer.Hour && (Math.Abs(dumpCreationTime.Minute - bsodOccuranceEventViewer.Minute)) < 5))
                            bsod = false;
                        else
                        {
                            Log.Alert("Dump Created at same time as BSOD event in event viewer");
                            Log.Verbose("Verify Dump creation time between Test start time and Current time");
                            if (File.GetCreationTime(CommonExtensions._mpBSODAnalysisPath) < dumpCreationTime && dumpCreationTime < DateTime.Now)
                                bsod = true;
                            else
                                bsod = false;
                        }
                    }
                }
            }
            if (bsod)
            {
                Log.Fail("BSOD occured Bugcheck:: {0}", bugCheckCode);
                CommonExtensions.Exit(0);
            }
        }
        
        private void ValidateFile()
        {
            if (File.Exists(CommonExtensions._mpBSODAnalysisPath))
            {
                DateTime createdTime = File.GetCreationTime(CommonExtensions._mpBSODAnalysisPath);
                TimeSpan diff = DateTime.Now.Subtract(createdTime);
                if (diff.Days > _appSettings.RebootFlgTimespanInDays &&
                    CommonExtensions._rebootAnalysysInfo.identifier.Equals(_rebootReason.identifier))
                    File.Delete(CommonExtensions._mpBSODAnalysisPath);
            }
        }
        private DateTime AssertBsodEvent()
        {
            DateTime initTime = default(DateTime);
            EventLog BSODeventLog = new EventLog("System", Environment.MachineName);
            EventLogEntry logEntry = (from EventLogEntry currentEntry in BSODeventLog.Entries
                                      where currentEntry.EntryType == EventLogEntryType.Error && currentEntry.Source.Equals("BugCheck")
                                      select currentEntry).LastOrDefault();
            if (logEntry != null)
            {
                initTime = logEntry.TimeGenerated;
                bugCheckCode = logEntry.ReplacementStrings.First().Split('(').First().Trim().ToString();
            }
            return initTime;
        }
    }
}