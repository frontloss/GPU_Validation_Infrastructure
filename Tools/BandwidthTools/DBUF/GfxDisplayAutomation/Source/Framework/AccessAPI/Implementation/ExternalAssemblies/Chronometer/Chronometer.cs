namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Text.RegularExpressions;
    using System.Xml;
    public class Chronometer : FunctionalBase, ISetMethod, IGetMethod
    {
        private static string _currSystemTime = string.Empty;
        private static string _miniDumpFileName = string.Empty;
        private static string _datFileName = string.Empty;
        private static string _fullDumpFileName = string.Empty;
        private List<ProfileInfo> _parseData = new List<ProfileInfo>();
        private List<ChronometerResult> _result = new List<ChronometerResult>();
        private string _logFilePath = ChronometerParams.logFilePath;
        private NetParam netParam;

        private void StartProfiling(EVENT_NAME_PROFILING eventName)
        {
            if (EVENT_NAME_PROFILING.EVENT_RESUME_FROM_CONNECTED_STANDBY == eventName)
                eventName = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_SLEEP;
            Log.Verbose(String.Format("Calling GfxStartProfiling for event {0}..", eventName));
            CommonExtensions.StartProcess("StartStopProfiling.exe", String.Concat("start ", eventName), 3);
        }

        private void StopProfiling(EVENT_NAME_PROFILING eventName)
        {
            if (EVENT_NAME_PROFILING.EVENT_RESUME_FROM_CONNECTED_STANDBY == eventName)
                eventName = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_SLEEP;
            Log.Verbose(String.Format("Calling GfxStopProfiling for event {0}..", eventName));
            CommonExtensions.StartProcess("StartStopProfiling.exe", String.Concat("stop ", eventName), 4);
            string fileNameStart = "GfxPerf_" + eventName.ToString();
            _miniDumpFileName = fileNameStart + ".txt";
            _fullDumpFileName = fileNameStart + "_Full.txt";
            _datFileName = "GfxPerf" + eventName + ".dat";
        }

        public bool SetMethod(object argMessage)
        {
            ChronometerParams CmeterParam = argMessage as ChronometerParams;
            if (CmeterParam.profilingType == PROFILING_TYPE.START_PROFILING)
                StartProfiling(CmeterParam.eventNameProfiling);
            else if (CmeterParam.profilingType == PROFILING_TYPE.STOP_PROFILING)
                StopProfiling(CmeterParam.eventNameProfiling);
            return true;
        }

        public object GetMethod(object argMessage)
        {
            ChronometerResult info = argMessage as ChronometerResult;
            PopulateBenchMarkValue(info);
            return GetResult(info);
        }

        private List<ChronometerResult> GetResult(ChronometerResult info)
        {
            return ParseProfileLogs(info);
        }

        private void PopulateBenchMarkValue(ChronometerResult argInfo)
        {
            if (string.IsNullOrEmpty(base.MachineInfo.PlatformDetails.Platform.ToString()))
            {
                Log.Abort("Unable to find Platform information");
            }
            ProfileInfo data = new ProfileInfo();
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\S0ixdata.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/Chronometer_Benchmark_Value");
            foreach (XmlNode eventNode in eventBenchmarkRoot.ChildNodes)
            {
                if (eventNode.Attributes["name"].Value == argInfo.EventName)
                {
                    data.EventName = Convert.ToString(eventNode.Attributes["name"].Value);
                    foreach (XmlNode node in eventNode.ChildNodes)
                    {
                        if (base.MachineInfo.PlatformDetails.Platform.ToString() == Convert.ToString(node.Attributes["id"].Value))
                        {
                            data.benchMarkValue = Convert.ToDouble(node.Attributes["BenchMark"].Value);
                            break;
                        }
                    }
                }
            }
            _parseData.Add(data);
        }

        private List<ChronometerResult> ParseProfileLogs(ChronometerResult chronometerData)
        {
            double benchMarkValue = _parseData.Find(BI => BI.EventName == chronometerData.EventName).benchMarkValue;
            chronometerData.benchMarkValue = benchMarkValue;
            Directory.CreateDirectory(_logFilePath);
            double timeTakenForEvtToCompMicroSec = 0;
            _currSystemTime = DateTime.Now.Hour + "-" + DateTime.Now.Minute + "-" + DateTime.Now.Second;

            if (File.Exists(_miniDumpFileName))
            {
                Log.Verbose("Parsing the profile log file {0}..", _miniDumpFileName);
                StreamReader reader = new StreamReader(_miniDumpFileName);
                string line = "";
                while ((line = reader.ReadLine()) != null)
                {
                    if (line.Contains("Graphics Driver Time Taken for executing the Event"))
                    {
                        string[] temp = line.Trim().Split(':');
                        timeTakenForEvtToCompMicroSec = Convert.ToInt32(Regex.Match(temp[1], @"\d+").Value);
                    }
                }
                reader.Close();
                Log.Message("Time taken for the event completion - {0} ms", Math.Round(timeTakenForEvtToCompMicroSec / 1000));
                chronometerData.actualValue = timeTakenForEvtToCompMicroSec;
                if (Math.Round(timeTakenForEvtToCompMicroSec / 1000) <= (benchMarkValue))
                {
                    chronometerData.chronometerStatus = true;
                    chronometerData.status = "PASS";
                }
                else
                {
                    chronometerData.chronometerStatus = false;
                    chronometerData.status = "FAIL";
                }
                File.Delete(_miniDumpFileName);
                DoDetailAnalysys(chronometerData);
            }
            else
            {
                Log.Fail("Error in creating the mini dump file!");
                Log.Abort("Aborting test execution.");
            }
            return _result;
        }

        private void CopyFile(string sourcePath, string destinationPath, int cycleNo)
        {
            string newdestinationPath = destinationPath.Remove(destinationPath.IndexOf(".txt")) + "_" + _currSystemTime + "_" + "Cycle_" + cycleNo + ".txt";
            File.Move(sourcePath, newdestinationPath);
            File.Delete(sourcePath);
        }

        private List<ChronometerResult> DoDetailAnalysys(ChronometerResult chronometerData)
        {
            Log.Verbose("Parsing the full log file {0}..", _fullDumpFileName);
            if (File.Exists(_datFileName))
            {
                CommonExtensions.StartProcess("PerfParser.exe", _datFileName);
                if (File.Exists(_fullDumpFileName))
                {
                    File.Delete(_datFileName);

                    List<DDI_Info> ddiDetails = PopulateDDIInfo(chronometerData);
                    foreach (DDI_Info ddiInfo in ddiDetails)
                    {
                        ChronometerResult temp = new ChronometerResult();
                        temp.actualValue = chronometerData.actualValue;
                        temp.benchMarkValue = chronometerData.benchMarkValue;
                        temp.chronometerStatus = chronometerData.chronometerStatus;
                        temp.cycle = chronometerData.cycle;
                        temp.EventName = chronometerData.EventName;
                        temp.status = chronometerData.status;
                        temp.DDI_Name = ddiInfo.DDI_Name;
                        temp.noOfTimesCalled = ddiInfo.DDI_Count;
                        temp.totalDDIExecutionTime = ddiInfo.DDI_Time;
                        _result.Add(temp);
                    }
                    CopyFile(_fullDumpFileName, _logFilePath + "\\" + Path.GetFileName(_fullDumpFileName), chronometerData.cycle);
                }
                else
                    Log.Alert("Error in creating the complete dump file!");
            }
            else
            {
                Log.Abort("Error in creating the dat file!");
            }
            return _result;
        }
        private List<DDI_Info> PopulateDDIInfo(ChronometerResult chronometerData)
        {
            int index = 0;
            string SearchString = string.Empty;
            string FullLog = string.Empty;
            string[] LogStrings = { "Dummy" };
            string[] DDI_Detail = { "Dummy" };
            List<DDI_Info> DDI_Details = new List<DDI_Info>();

            try
            {
                FullLog = File.ReadAllText(_fullDumpFileName);
                SearchString = "Per DDI Profiling Data for the Event";
                index = FullLog.IndexOf(SearchString);
                FullLog = FullLog.Remove(0, index);
                SearchString = "Bucketing log based on Execution times for each DDI";
                index = FullLog.IndexOf(SearchString);
                FullLog = FullLog.Remove(index);

                SearchString = "__________________________________________________________________________________________________________";
                index = FullLog.IndexOf(SearchString) + SearchString.Length;
                FullLog = FullLog.Remove(0, index);

                SearchString = "----------------------------------------------------------------------------------------------------------";
                index = FullLog.IndexOf(SearchString);
                FullLog = FullLog.Remove(index);

                LogStrings = FullLog.Split(new string[] { Environment.NewLine }, StringSplitOptions.None);
                foreach (string DDI_Info in LogStrings)
                {
                    DDI_Info temp = new DDI_Info();
                    if (DDI_Info == string.Empty || DDI_Info == " ")
                        continue;
                    DDI_Detail = DDI_Info.Split('\t');
                    temp.DDI_Name = DDI_Detail[0].Trim();
                    temp.DDI_Count = Convert.ToInt32((DDI_Detail[2].Trim()));
                    temp.DDI_Time = Convert.ToInt32(DDI_Detail[3].Trim());
                    DDI_Details.Add(temp);
                }
            }
            catch (Exception ex)
            {
                Log.Verbose("{0}", ex.StackTrace);
                Log.Abort("Exception caught while acquiring DDI information: {0}", ex.Message);
            }
            return DDI_Details;
        }

    }
}
