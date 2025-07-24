namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using ClosedXML.Excel;

    [Test(Type = TestType.ConnectedStandby)]
    public class MP_S0ix_Gfx_Resumetime : MP_S0ixBase
    {
        private new CSParam powerParam;
        private ChronometerParams cParam;
        private NetParam netParam;
        private string DriverVerifierStatus;
        List<ChronometerResult> profileData = new List<ChronometerResult>();
        private string _logfilePath = "EVENT_RESUME_FROM_CONNECTED_STANDBY.xlsx";
        public MP_S0ix_Gfx_Resumetime()
        {
            cParam = new ChronometerParams();
            cParam.eventNameProfiling = EVENT_NAME_PROFILING.EVENT_RESUME_FROM_CONNECTED_STANDBY;
            powerParam = new CSParam();
            netParam = new NetParam();
            IsResumeTimeTest = true;
            Log.CustomLogPath = ChronometerParams.logFilePath.Split(Path.DirectorySeparatorChar).Last();
            File.Delete(_logfilePath);
        }

        #region Test
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void PreCondition()
        {
            if (base.CurrentConfig.EnumeratedDisplays.Count > 1)
            {
                Log.Abort("System enumerated more than one display, enumerated display are {0}. Hence aborting test execution", GetDisplayListString(base.CurrentConfig.EnumeratedDisplays));
            }
            if (AccessInterface.GetFeature<bool>(Features.DriverVerifier, Action.Get))
                DriverVerifierStatus = "ON";
            else
                DriverVerifierStatus = "OFF";
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void StartStopProfiling()
        {
            Log.Message(true, "Event under test is EVENT_RESUME_FROM_CONNECTED_STANDBY");
            Log.Verbose("Connected Standby duration set to {0} sec", powerParam.Delay);
            Log.Verbose("No of cycle set to {0}", powerParam.Cycle);
            if (Directory.Exists(ChronometerParams.logFilePath))
                Directory.Delete(ChronometerParams.logFilePath, true);
            double TimeTakenForEvent = 0;
            try
            {
                for (int eachCycle = 1; eachCycle <= powerParam.Cycle; eachCycle++)
                {
                    Log.Message(true, "EVENT_RESUME_FROM_CONNECTED_STANDBY---- Cycle {0}", eachCycle);

                    cParam.profilingType = PROFILING_TYPE.START_PROFILING;
                    AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);
                    AccessInterface.SetFeature<bool, CSParam>(Features.ConnectedStandby, Action.SetMethod, powerParam);
                    Log.Message("{0} completed..", powerParam.PowerStates);
                    cParam.profilingType = PROFILING_TYPE.STOP_PROFILING;
                    AccessInterface.SetFeature<bool, ChronometerParams>(Features.Chronometer, Action.SetMethod, cParam);


                    profileData = new List<ChronometerResult>();
                    ChronometerResult data = new ChronometerResult();
                    data.cycle = eachCycle;
                    data.EventName = Convert.ToString(cParam.eventNameProfiling);
                    profileData = AccessInterface.GetFeature<List<ChronometerResult>, ChronometerResult>(Features.Chronometer, Action.GetMethod, Source.AccessAPI, data);
                    if (profileData.First().benchMarkValue == 0)
                    {
                        Log.Abort("Benchmark value for running platform is 0 platform ID not mapped, hence exiting from test execution");
                    }
                    if (profileData.First().chronometerStatus)
                        Log.Message("Resumr time from CS as expected, Benchmark value {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
                    else
                        Log.Alert("Resumr time from CS exceed the expectation, Benchmark Value: {0}ms, Actual: {1}ms", data.benchMarkValue, Math.Round((data.actualValue) / 1000));
                    //CaptureChronometerData();
                    TimeTakenForEvent += Math.Round((profileData.First().actualValue) / 1000);
                }
            }
            catch
            {
                return;
            }
            TimeTakenForEvent /= powerParam.Cycle;
            if(Math.Round(TimeTakenForEvent, 2) > profileData.First().benchMarkValue)
                Log.Fail(true,"Average time taken for " + profileData.First().EventName + " for " + powerParam.Cycle + " cycle(s): " + Math.Round(TimeTakenForEvent, 2).ToString() + " ms");
            else
                Log.Success("Average time taken for " + profileData.First().EventName + " for " + powerParam.Cycle + " cycle(s): " + Math.Round(TimeTakenForEvent, 2).ToString() + " ms");
            //File.Copy(Directory.GetCurrentDirectory() + "\\" + _logfilePath, ChronometerParams.logFilePath + "\\" + _logfilePath, true);
            //File.Delete(Directory.GetCurrentDirectory() + "\\" + _logfilePath);
        }

        public void CaptureChronometerData()
        {
            List<string> LogData = new List<string>();
            LogData.Add(profileData.First().EventName);
            LogData.Add(profileData.First().cycle.ToString());
            LogData.Add(base.MachineInfo.Driver.Version);
            LogData.Add(profileData.First().actualValue.ToString());
            LogData.Add(profileData.First().status);
            LogData.Add(base.MachineInfo.PlatformDetails.Platform.ToString());
            LogData.Add(base.MachineInfo.PhysicalMemory);
            LogData.Add(base.MachineInfo.BIOSVersion);
            LogData.Add(DriverVerifierStatus);
            LogData.Add(base.MachineInfo.Name);
            LogData.Add(base.MachineInfo.OS.Description);
            WriteLogDataToExcel(LogData);
        }

        private void WriteLogDataToExcel(List<string> LogData)
        {
            var ChronometerWorkbook = new XLWorkbook();
            if (!File.Exists(_logfilePath))
            {
                // Create workbook
                ChronometerWorkbook = new XLWorkbook();
                var testWorkSheet = ChronometerWorkbook.AddWorksheet("Sheet1");
                ChronometerWorkbook.SaveAs(_logfilePath);

                // Open first worksheet
                ChronometerWorkbook = new XLWorkbook(_logfilePath);
                var ChronometerEventWorksheetForHeader = ChronometerWorkbook.Worksheet(1);
                ChronometerEventWorksheetForHeader.Name = (LogData.First().ToString().Replace("EVENT_", "")); // Change worksheet name to chronometer event

                // Capture event name
                IXLRange TableRangeForHeader = ChronometerEventWorksheetForHeader.Range(2, 1, 2, 3);
                TableRangeForHeader.Merge();
                TableRangeForHeader.Style.Font.SetFontName("Cambria");
                TableRangeForHeader.Style.Fill.SetBackgroundColor(XLColor.BabyBlueEyes);
                TableRangeForHeader.Style.Alignment.SetHorizontal(XLAlignmentHorizontalValues.Center);
                ChronometerEventWorksheetForHeader.Cell(2, 1).Value = (LogData.First().ToString());

                // Write table header with filter
                TableRangeForHeader = ChronometerEventWorksheetForHeader.Range(3, 1, 3, 10);
                TableRangeForHeader.SetAutoFilter();
                TableRangeForHeader.Style.Font.SetFontName("Cambria");
                TableRangeForHeader.Style.Font.SetBold();
                IXLRanges TableRanges = ChronometerEventWorksheetForHeader.Ranges("A3:K3");
                ChronometerEventWorksheetForHeader.Cell(3, 1).Value = "Cycle No";
                ChronometerEventWorksheetForHeader.Cell(3, 2).Value = "Driver Version";
                ChronometerEventWorksheetForHeader.Cell(3, 3).Value = "Event Duration (microSeconds)";
                ChronometerEventWorksheetForHeader.Cell(3, 4).Value = "Result";
                ChronometerEventWorksheetForHeader.Cell(3, 5).Value = "Platform";
                ChronometerEventWorksheetForHeader.Cell(3, 6).Value = "Memory";
                ChronometerEventWorksheetForHeader.Cell(3, 7).Value = "BIOS";
                ChronometerEventWorksheetForHeader.Cell(3, 8).Value = "Driver Verifier";
                ChronometerEventWorksheetForHeader.Cell(3, 9).Value = "Machine Name";
                ChronometerEventWorksheetForHeader.Cell(3, 10).Value = "Operating System";
                TableRangeForHeader.Style.Border.SetBottomBorder(XLBorderStyleValues.Thin);
                TableRangeForHeader.Style.Border.SetLeftBorder(XLBorderStyleValues.Thin);
                TableRangeForHeader.Style.Border.SetRightBorder(XLBorderStyleValues.Thin);
                TableRangeForHeader.Style.Border.SetTopBorder(XLBorderStyleValues.Thin);
                ChronometerEventWorksheetForHeader.Columns().AdjustToContents();
                ChronometerWorkbook.SaveAs(_logfilePath);
            }

            // Open first worksheet
            ChronometerWorkbook = new XLWorkbook(_logfilePath);
            var ChronometerEventWorksheet = ChronometerWorkbook.Worksheet(1);
            ChronometerEventWorksheet.Name = (LogData.First().ToString().Replace("EVENT_", "")); // Change worksheet name to chronometer event

            // Insert new row
            int RowIndex = 4; // Always insert 4th row and write to it. This is to have the newest on top.
            int ColumnIndex = 1;
            IXLRange TableRange = ChronometerEventWorksheet.Range(RowIndex, 1, RowIndex, 10);
            TableRange.InsertRowsAbove(1);
            TableRange = ChronometerEventWorksheet.Range(RowIndex, 1, RowIndex, 10);
            TableRange.Style.Font.SetBold(false);
            foreach (string Data in LogData.Skip(1).ToList())
            {
                ChronometerEventWorksheet.Cell(RowIndex, ColumnIndex++).Value = Data;
                if (Data.ToUpper() == "PASS")
                {
                    ChronometerEventWorksheet.Cell(RowIndex, ColumnIndex - 1).Style.Fill.SetBackgroundColor(XLColor.LightGreen);
                    ChronometerEventWorksheet.Cell(RowIndex, ColumnIndex - 1).Value = Data;
                }
                else if (Data.ToUpper() == "FAIL")
                {
                    ChronometerEventWorksheet.Cell(RowIndex, ColumnIndex - 1).Style.Fill.SetBackgroundColor(XLColor.Red);
                    ChronometerEventWorksheet.Cell(RowIndex, ColumnIndex - 1).Value = Data;
                }
            }
            ChronometerEventWorksheet.Columns().Style.Alignment.SetHorizontal(XLAlignmentHorizontalValues.Center);
            ChronometerEventWorksheet.Columns().Style.Alignment.SetVertical(XLAlignmentVerticalValues.Center);
            ChronometerEventWorksheet.Columns().AdjustToContents();
            ChronometerWorkbook.SaveAs(_logfilePath);
        }
        private string GetDisplayListString(List<DisplayInfo> argEnumeratedDisplay)
        {
            string listString = string.Empty;
            foreach (DisplayInfo info in argEnumeratedDisplay)
            {
                listString = listString + info.DisplayType.ToString() + " ";
            }
            return listString;
        }

        #endregion
    }
}
