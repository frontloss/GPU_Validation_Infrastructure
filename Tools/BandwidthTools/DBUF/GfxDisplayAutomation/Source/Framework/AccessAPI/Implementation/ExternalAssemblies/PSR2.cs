namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;

    class PSR2 : FunctionalBase, IGetMethod
    {
        protected string _psr2CaptureLog = "";
        protected bool _startCapture = false;
        protected Platform _platform = Platform.SKL; // default;
        protected PsrPollDelegate _psr2DelegateObj = default(PsrPollDelegate);
        protected IAsyncResult _iAsyncResult = default(IAsyncResult);

        protected uint _psr2CtrlReg = 0x0;
        protected uint _psr2StatReg = 0x0;
        protected uint _psr2PerfReg = 0x0;

        protected uint _psr2StatReg_Psr2StatusBitmap = 0x0;
        protected uint _psr2StatReg_LinkStatusBitmap = 0x0;

        protected int _psr2DeepSleepCount = 0;
        protected int _psr2PerfCount = 0;

        protected const string psr2CtrlReg_Event = "PSR2_CTRL_EDP_REG";
        protected const string psr2StatReg_Psr2StatusEvent = "PSR2_STAT_REG_PSR2STATUS";
        protected const string psr2StatReg_LinkStatusEvent = "PSR2_STAT_REG_LINKSTATUS";
        protected const string psr2PerfReg_Event = "PSR1_PERF_CNT_REG";

        protected const string PSR_UTILITY_APP = "Naakuthanthi.exe";
        protected const string CURSOR_CHANGE_TMP_FILE = "CursorShapeChange.tmp";

        [DllImport("User32.dll")]
        static extern int SetForegroundWindow(IntPtr point);

        public object GetMethod(object argMessage)
        {
            PsrStatus psrStatus = new PsrStatus();
            PsrTestInput psrGetObject = argMessage as PsrTestInput;

            if (psrGetObject.captureIntervalInSec < 10)
                psrGetObject.captureIntervalInSec = 12;

            if (!File.Exists(PSR_UTILITY_APP))
            {
                Log.Verbose("PSR Utility App (Naakuthanthi.exe) is not found.");
                psrStatus.psrWorkingState = PsrWorkingState.PsrUtilityAppMissing;
                return psrStatus;
            }

            if (psrGetObject.currentConfig.PrimaryDisplay != DisplayType.EDP || psrGetObject.currentConfig.ConfigType != DisplayConfigType.SD)
            {
                Log.Verbose("Current Config is not SD eDP. PSR2 works only in SD eDP Config.");
                psrStatus.psrWorkingState = PsrWorkingState.PsrWrongConfig;
                return psrStatus;
            }

            ACPIFunctions acpi = new ACPIFunctions();
            PowerLineStatus plineStatus = (PowerLineStatus)acpi.Get;
            if (plineStatus != PowerLineStatus.Offline)
            {
                if (DisplayExtensions.VerifyCSSystem(base.MachineInfo))
                {
                    Log.Verbose("Checking PSR in AC Mode with CS Enabled system.");
                }
                else
                    Log.Verbose("Checking PSR in AC Mode with Non-CS system (PSR is expected to fail here).");
            }
            else
                Log.Verbose("Checking PSR in Battery Mode.");

            InitializePsr2Capture();

            if (CheckPsr2CapabilityInPanel())
            {
                Log.Verbose("Connected eDP is PSR2 supported eDP..");

                if (_platform != Platform.VLV && _platform != Platform.CHV)
                {
                    if (CheckPsr2CapabilityInDriver())
                    {
                        Log.Verbose("PSR Feature is ENABLED in Driver..");
                    }
                    else
                    {
                        Log.Verbose("PSR Feature is DISABLED in Driver..");
                        psrStatus.psrWorkingState = PsrWorkingState.PsrNotEnabledAtSource;
                        return psrStatus;
                    }
                }
            }
            else
            {
                Log.Verbose("Connected eDP is NOT PSR2 supported eDP.");
                psrStatus.psrWorkingState = PsrWorkingState.PsrNotEnabledAtSink;
                return psrStatus;
            }

            if (psrGetObject.psrEventType == PsrEventType.KeyPress)
                checkPsr2BasicWithKeyPress(psrGetObject);
            else
                checkPsr2BasicWithNaakuthanthi(psrGetObject);

            psrStatus.psrCapturedData.currentEntryExitCount = _psr2DeepSleepCount;
            psrStatus.psrCapturedData.requiredEntryExitCount = (psrGetObject.captureIntervalInSec - 5);
            psrStatus.psrCapturedData.currentResidencyTime = _psr2PerfCount;
            psrStatus.psrCapturedData.currentResidencyTime = (int)((psrGetObject.captureIntervalInSec / 2) * 500);

            if (psrGetObject.psrEventType == PsrEventType.CursorMove)
                psrStatus.psrCapturedData.requiredEntryExitCount = (int)(psrGetObject.captureIntervalInSec / 2);

            if (_psr2DeepSleepCount >= psrStatus.psrCapturedData.requiredEntryExitCount)
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledAndWorkingProperly;
            else if ((_psr2DeepSleepCount < psrStatus.psrCapturedData.requiredEntryExitCount) &&
                (psrStatus.psrCapturedData.currentEntryExitCount != 0))
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledButLessEntryExitCount;
            else if (_psr2DeepSleepCount == 0)
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledButNotWorking;

            return psrStatus;
        }

        private void checkPsr2BasicWithKeyPress(PsrTestInput psrLegacyObj)
        {
            Log.Verbose("PSR2 Check: Launching Notepad for KeyPress...");
            Process pNotepad = new Process();
            pNotepad.StartInfo.CreateNoWindow = false;
            pNotepad.StartInfo.FileName = "notepad.exe";
            pNotepad.StartInfo.WindowStyle = ProcessWindowStyle.Maximized;
            pNotepad.EnableRaisingEvents = true;
            pNotepad.Start();

            StartPsr2Capture();
            Thread.Sleep(1000);

            IntPtr hPtr = pNotepad.MainWindowHandle;
            SetForegroundWindow(hPtr);
            if (pNotepad.Responding)
            {
                string strNotepadTyping = "\n0123456789\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz";
                for (int i = 0; i < psrLegacyObj.captureIntervalInSec; i++)
                {
                    Thread.Sleep(1000);
                    int j = (i >= strNotepadTyping.Length) ? (i - strNotepadTyping.Length) : i;
                    SendKeys.SendWait(strNotepadTyping[j] + " ");
                }
            }

            Thread.Sleep(1000);
            StopPsr2Capture();

            if (!pNotepad.HasExited)
                pNotepad.Kill();

            Log.Verbose("PSR2 Deep Sleep Count: {0}", _psr2DeepSleepCount);
        }

        private void checkPsr2BasicWithNaakuthanthi(PsrTestInput psrLegacyObj)
        {
            string args = "c:clock e:showtime x:300 y:300";
            if (psrLegacyObj.psrEventType == PsrEventType.CursorMove)
            {
                args = "c:cursor e:move o:random";
                Log.Verbose("PSR2 Check: Launching Cursor Move...");
            }
            else if (psrLegacyObj.psrEventType == PsrEventType.CursorChange)
            {
                args = "c:cursor e:shapechange p:50";
                Log.Verbose("PSR2 Check: Launching Cursor Change...");
            }
            else
            {
                args = "c:clock e:showtime x:300 y:300";
                Log.Verbose("PSR2 Check: Launching Digital Clock...");
            }

            Process procNaakuthanthi = new Process();
            procNaakuthanthi.StartInfo.UseShellExecute = false;
            procNaakuthanthi.StartInfo.CreateNoWindow = false;
            procNaakuthanthi.StartInfo.FileName = PSR_UTILITY_APP;
            procNaakuthanthi.StartInfo.Arguments = args;

            if (psrLegacyObj.psrEventType != PsrEventType.Nothing)
                procNaakuthanthi.Start();

            StartPsr2Capture();

            if (psrLegacyObj.psrEventType == PsrEventType.CursorChange)
                procNaakuthanthi.WaitForExit();
            else
                Thread.Sleep(psrLegacyObj.captureIntervalInSec * 1000);

            StopPsr2Capture();

            if (psrLegacyObj.psrEventType != PsrEventType.Nothing)
            {
                if (!procNaakuthanthi.HasExited)
                    procNaakuthanthi.Kill();
            }

            Log.Verbose("PSR2 Deep Sleep Count: {0}", _psr2DeepSleepCount);
        }

        protected bool CheckPsr2CapabilityInPanel()
        {
            DpcdInfo dpcd = new DpcdInfo();
            dpcd.Offset = 0x00700; //DPCD_EDP_REV_ADDR
            dpcd.DispInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkDpcd = sdkExtn.GetSDKHandle(SDKServices.DpcdRegister);
            sdkDpcd.Get(dpcd);
            if (dpcd.Value >= 0x03)
            {
                Log.Verbose("Connected eDP panel revision is v1.{0}", (dpcd.Value == 3 ? "4" : "4a"));
            }
            else
            {
                Log.Verbose("Connected eDP panel revision is v1.{0}, PSR requirement is eDP v1.4 or later", (dpcd.Value + 1));
                return false;
            }

            dpcd.Offset = 0x00070; //DPCD_CAPS_SUPPORTED_AND_VERSION
            dpcd.Value = 0;
            sdkDpcd.Get(dpcd);

            if (dpcd.Value == 0x02) // 2 ==> PSR2 without YCord
            {
                Log.Verbose("Connected eDP panel supports PSR capability version_2 without YCord (00070H ==> 02h)");
            }
            else if (dpcd.Value == 0x03) // 3 ==> PSR2 with YCord
            {
                Log.Verbose("Connected eDP panel supports PSR capability version_2 with YCord (00070H ==> 03h)");
            }
            else
            {
                Log.Verbose("Connected eDP panel does not support PSR capability version_2 with/without YCord (00070H ==> {0:00}h", dpcd.Value);
                return false;
            }

            // Rest of the requirements to be put here

            return true; ;
        }

        protected bool CheckPsr2CapabilityInDriver()
        {
            // Only for >= SKL
            Log.Message("Check PSR2 capability in the driver");

            EventInfo returnEventInfo = new EventInfo();
            if(!GetRegistersInfo(psr2CtrlReg_Event, ref returnEventInfo))
            {
                Log.Fail("PSR2 Ctrl Reg fetching failed..");
                return false;
            }
            else
            {
                _psr2CtrlReg = Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16);
                if (returnEventInfo.RegistersMatched)
                {
                    Log.Success("PSR2 Feature is enabled in the driver..");
                }
                else
                {
                    Log.Fail("PSR2 Feature is not enabled in the driver..");
                    return false;
                }
            }

            return true;
        }

        protected bool GetRegistersInfo(string registerEvent, ref EventInfo returnEventInfo)
        {
            bool bRetVal = false;
            PipePlaneParams pipePlane = new PipePlaneParams(DisplayType.EDP);
            PipePlane pPlane = base.CreateInstance<PipePlane>(new PipePlane());
            pipePlane = (PipePlaneParams)pPlane.GetMethod(pipePlane);
            DisplayInfo displayInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();

            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors ==> Pipe:{1}, Plane:{2}, Port:{3}", registerEvent, pipePlane.Pipe.ToString(), pipePlane.Plane.ToString(), displayInfo.Port.ToString());
            eventInfo.pipe = pipePlane.Pipe;
            eventInfo.plane = pipePlane.Plane;
            eventInfo.port = displayInfo.Port;
            eventInfo.eventName = registerEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);

            if (returnEventInfo.listRegisters.Count > 0)
                bRetVal = true;

            return bRetVal;
        }

        protected void InitializePsr2Capture()
        {
            Log.Message("Psr2Capture: Intializing PSR2 capture..");

            _psr2CaptureLog = "Psr2Log.txt";
            _platform = base.MachineInfo.PlatformDetails.Platform;
           
            EventInfo retEventInfo = new EventInfo();
            if (!GetRegistersInfo(psr2StatReg_Psr2StatusEvent, ref retEventInfo))
            {
                Log.Fail("PSR2 Stat Reg (for PSR2 status) fetching failed..");
            }
            else
            {
                _psr2StatReg = Convert.ToUInt32(retEventInfo.listRegisters[0].Offset, 16);
                _psr2StatReg_Psr2StatusBitmap = Convert.ToUInt32(retEventInfo.listRegisters[0].Bitmap, 16);
            }

            if (!GetRegistersInfo(psr2StatReg_LinkStatusEvent, ref retEventInfo))
            {
                Log.Fail("PSR2 Stat Reg (for Link status) fetching failed..");
            }
            else
            {
                _psr2StatReg_LinkStatusBitmap = Convert.ToUInt32(retEventInfo.listRegisters[0].Bitmap, 16);
            }

            if (!GetRegistersInfo(psr2PerfReg_Event, ref retEventInfo))
            {
                Log.Fail("PSR2 Perf Reg fetching failed..");
            }
            else
            {
                _psr2PerfReg = Convert.ToUInt32(retEventInfo.listRegisters[0].Offset, 16);
            }
        }

        protected void StartPsr2Capture()
        {
            Log.Verbose("Starting PSR2 Capture...");
            _startCapture = true;

            if (_platform >= Platform.SKL)  // Platform supported ==> SKL, KBL, BXT, CNL, GLK, ICL, etc
            {
                _psr2DelegateObj = Psr2CaptureSKLplus_DMC;
            }
            else
            {
                _psr2DelegateObj = default(PsrPollDelegate);
                Log.Fail(true, "Wrong platform. PSR2 not supported on the specified platform.");
            }

            if (_psr2DelegateObj != default(PsrPollDelegate))
                _iAsyncResult = _psr2DelegateObj.BeginInvoke(default(AsyncCallback), default(Object));
        }

        protected void StopPsr2Capture()
        {
            Log.Verbose("Stopping PSR2 Capture...");
            _startCapture = false;

            if (_iAsyncResult != default(IAsyncResult))
                _iAsyncResult.AsyncWaitHandle.WaitOne();
            _psr2DelegateObj = default(PsrPollDelegate);
        }

        protected bool ReadMMIORegister(uint offset, ref uint value)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = offset;
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            DriverEscape driverEscapeObj = new DriverEscape();
            bool bRet = driverEscapeObj.SetMethod(driverParams);
            value = driverData.output;
            return bRet;
        }

        const uint IGFX_I2C_AUX_READ = 9;
        const uint DPCD_BUFFER_SIZE = 0x0008;

        private void Psr2CaptureSKLplus()
        {
            if (File.Exists(_psr2CaptureLog))
            {
                File.Delete(_psr2CaptureLog);
            }

            using (StreamWriter sw = File.AppendText(_psr2CaptureLog))
            {
                while (!_startCapture) ;

                _psr2DeepSleepCount = 0;
                _psr2PerfCount = 0;

                uint uPsr2Stat_LastState = 0xE0000000;
                uint uLink_LastStatus = 0x0C000000;
                uint uPsr2_LastDeepSleepCount = 0;

                uint uPsr2Stat_RegValue = 0;
                uint uPsr2Perf_RegValue = 0;

                uint uPsr2Perf_LastPerfCount = 0; // 0x00FFFFFF;

                ReadMMIORegister(_psr2StatReg, ref uPsr2Stat_RegValue); // PSR STAT Reg
                uPsr2_LastDeepSleepCount = ((uPsr2Stat_RegValue & 0x000F0000) >> 16);

                ReadMMIORegister(_psr2PerfReg, ref uPsr2Perf_RegValue); // PSR Perf Count Reg
                uPsr2Perf_LastPerfCount = uPsr2Perf_RegValue;

                while (_startCapture)
                {
                    ReadMMIORegister(_psr2StatReg, ref uPsr2Stat_RegValue); // PSR STAT Reg

                    uint uPsr2Stat_CurState = uPsr2Stat_RegValue & 0xE0000000; // 31:29b
                    uint uLink_CurStatus = uPsr2Stat_RegValue & 0x0C000000; // 27:26b
                    uint uPsr2Stat_CurDeepSleepCount = ((uPsr2Stat_RegValue & 0x000F0000) >> 16); // 19:16b

                    ReadMMIORegister(_psr2PerfReg, ref uPsr2Perf_RegValue); // PSR Perf Count Reg
                    uint uPsr2Perf_CurPerfCount = uPsr2Perf_RegValue; // 23:0b

                    if (uPsr2Stat_CurState != uPsr2Stat_LastState)
                    {
                        switch (uPsr2Stat_CurState)
                        {
                            case 0x00000000: sw.WriteLine("PSR2_state = IDLE (Reset state)");
                                break;
                            case 0x10000000: sw.WriteLine("PSR2_state = CAPTURE (Send capture frame)");
                                break;
                            case 0x20000000: sw.WriteLine("PSR2_state = CPTURE_FS (Fast sleep after capture frame is sent)");
                                break;
                            case 0x30000000: sw.WriteLine("PSR2_state = SLEEP (Selective Update)");
                                break;
                            case 0x40000000: sw.WriteLine("PSR2_state = BUFON_FW (Turn Buffer on and Send Fast wake)");
                                break;
                            case 0x50000000: sw.WriteLine("PSR2_state = ML_UP (Turn Main link up and send SR)");
                                break;
                            case 0x60000000: sw.WriteLine("PSR2_state = SU_STANDBY (Selective update or Standby state)");
                                break;
                            case 0x70000000: sw.WriteLine("PSR2_state = FAST_SLEEP (Send Fast sleep)");
                                break;
                            case 0x80000000: sw.WriteLine("PSR2_state = DEEP_SLEEP (Enter Deep sleep)");
                                break;
                            case 0x90000000: sw.WriteLine("PSR2_state = BUF_ON (Turn ON IO Buffer)");
                                break;
                            case 0xA0000000: sw.WriteLine("PSR2_state = TG_ON (Turn ON Timing Generator)");
                                break;
                            default: sw.WriteLine("PSR2_state = Reserved (Wrong State)");
                                break;
                        }

                        uPsr2Stat_LastState = uPsr2Stat_CurState;
                    }

                    if (uLink_CurStatus != uLink_LastStatus)
                    {
                        switch (uLink_CurStatus)
                        {
                            case 0x00000000: sw.WriteLine("Link_status = Link is Full Off");
                                break;
                            case 0x04000000: sw.WriteLine("Link_status = Link is Full On");
                                break;
                            case 0x08000000: sw.WriteLine("Link_status = Link is In Standby");
                                break;
                            default: sw.WriteLine("Link_status = Reserved (Wrong State)");
                                break;
                        }

                        uLink_LastStatus = uLink_CurStatus;
                    }

                    if (uPsr2Stat_CurDeepSleepCount != uPsr2_LastDeepSleepCount)
                    {
                        if (uPsr2Stat_CurDeepSleepCount < uPsr2_LastDeepSleepCount)
                        {
                            _psr2DeepSleepCount += (int)((uPsr2Stat_CurDeepSleepCount + 16) - uPsr2_LastDeepSleepCount);
                        }
                        else
                        {
                            _psr2DeepSleepCount += (int)(uPsr2Stat_CurDeepSleepCount - uPsr2_LastDeepSleepCount);
                        }
                        sw.WriteLine("\nPSR2_Deep_Sleep_Count = " + _psr2DeepSleepCount);

                        uPsr2_LastDeepSleepCount = uPsr2Stat_CurDeepSleepCount;

                        if (uPsr2Perf_CurPerfCount != uPsr2Perf_LastPerfCount)
                        {
                            if (uPsr2Perf_CurPerfCount < uPsr2Perf_LastPerfCount)
                            {
                                _psr2PerfCount += (int)((uPsr2Perf_CurPerfCount + 16777216) - uPsr2Perf_LastPerfCount);
                            }
                            else
                            {
                                _psr2PerfCount += (int)(uPsr2Perf_CurPerfCount - uPsr2Perf_LastPerfCount);
                            }
                            sw.WriteLine("PSR2_Perf_Count = " + _psr2PerfCount + "\n");

                            uPsr2Perf_LastPerfCount = uPsr2Perf_CurPerfCount;
                        }
                    }                     

                    Thread.Sleep(100); // Check
                }
                sw.Close();
            }
        }

        private void Psr2CaptureSKLplus_DMC() // For DMC
        {
            if (File.Exists(_psr2CaptureLog))
            {
                File.Delete(_psr2CaptureLog);
            }

            using (StreamWriter sw = File.AppendText(_psr2CaptureLog))
            {
                while (!_startCapture) ;

                _psr2DeepSleepCount = 0;

                uint uPsr2Stat_LastState = 0xE0000000;
                uint uLink_LastStatus = 0x0C000000;

                uint uPsr2Stat_RegValue = 0;

                while (_startCapture)
                {
                    ReadMMIORegister(_psr2StatReg, ref uPsr2Stat_RegValue); // PSR STAT Reg

                    uint uPsr2State = uPsr2Stat_RegValue & _psr2StatReg_Psr2StatusBitmap; // 31:28b
                    uint uLinkStatus = uPsr2Stat_RegValue & _psr2StatReg_LinkStatusBitmap; // 27:26b

                    if (uPsr2State != uPsr2Stat_LastState)
                    {
                        switch (uPsr2State)
                        {
                            case 0x00000000: sw.WriteLine("PSR2_state = IDLE (Reset state)");
                                break;
                            case 0x10000000: sw.WriteLine("PSR2_state = CAPTURE (Send capture frame)");
                                break;
                            case 0x20000000: sw.WriteLine("PSR2_state = CPTURE_FS (Fast sleep after capture frame is sent)");
                                break;
                            case 0x30000000: sw.WriteLine("PSR2_state = SLEEP (Selective Update)");
                                break;
                            case 0x40000000: sw.WriteLine("PSR2_state = BUFON_FW (Turn Buffer on and Send Fast wake)");
                                break;
                            case 0x50000000: sw.WriteLine("PSR2_state = ML_UP (Turn Main link up and send SR)");
                                break;
                            case 0x60000000: sw.WriteLine("PSR2_state = SU_STANDBY (Selective update or Standby state)");
                                break;
                            case 0x70000000: sw.WriteLine("PSR2_state = FAST_SLEEP (Send Fast sleep)");
                                break;
                            case 0x80000000: sw.WriteLine("PSR2_state = DEEP_SLEEP (Enter Deep sleep)");
                                _psr2DeepSleepCount++;
                                sw.WriteLine("\nPSR2_Deep_Entry_Count = " + _psr2DeepSleepCount);
                                break;
                            case 0x90000000: sw.WriteLine("PSR2_state = BUF_ON (Turn ON IO Buffer)");
                                break;
                            case 0xA0000000: sw.WriteLine("PSR2_state = TG_ON (Turn ON Timing Generator)");
                                break;
                            default: sw.WriteLine("PSR2_state = Reserved (Wrong State)");
                                break;
                        }

                        uPsr2Stat_LastState = uPsr2State;
                    }

                    if (uLinkStatus != uLink_LastStatus)
                    {
                        switch (uLinkStatus)
                        {
                            case 0x00000000: sw.WriteLine("Link_status = Link is Full Off");
                                break;
                            case 0x04000000: sw.WriteLine("Link_status = Link is Full On");
                                break;
                            case 0x08000000: sw.WriteLine("Link_status = Link is In Standby");
                                break;
                            default: sw.WriteLine("Link_status = Reserved (Wrong State)");
                                break;
                        }

                        uLink_LastStatus = uLinkStatus;
                    }                    

                    Thread.Sleep(100); // Check
                }
                sw.Close();
            }
        }

    }
}
