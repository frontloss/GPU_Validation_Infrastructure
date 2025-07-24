namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;

    public delegate void PsrPollDelegate();

    internal class PSR1 : FunctionalBase, IGetMethod
    {
        protected string _psr1CaptureLog = "";
        protected bool _startCapture = false;
        protected Platform _platform = Platform.VLV; // default;
        protected PsrPollDelegate _psr1DelegateObj = default(PsrPollDelegate);
        protected IAsyncResult _iAsyncResult = default(IAsyncResult);

        protected uint _psr1CtrlReg = 0x0;
        protected uint _psr1StatReg = 0x0;
        protected uint _psr1PerfReg = 0x0;
        protected uint _edpPortCtrlReg = 0x0;

        protected int _psr1ActiveCount = 0;
        protected int _psr1PerfCount = 0;
        protected bool _edpPortDisabled = false;

        protected const string psr1CtrlReg_Event = "PSR1_CTRL_EDP_REG";
        protected const string psr1StatReg_Event = "PSR1_STATUS_REG";
        protected const string psr1PerfReg_Event = "PSR1_PERF_CNT_REG";
        protected const string portCtrlEdpReg_Event = "PORT_CTRL_EDP_REG";

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
                Log.Verbose("Current Config is not SD eDP. PSR works only in SD eDP Config.");
                psrStatus.psrWorkingState = PsrWorkingState.PsrWrongConfig;
                return psrStatus;
            }

            ACPIFunctions acpi = new ACPIFunctions();
            PowerLineStatus plineStatus = (PowerLineStatus)acpi.Get;
            if(plineStatus != PowerLineStatus.Offline)
            {
                if (DisplayExtensions.VerifyCSSystem(base.MachineInfo))
                {
                    Log.Verbose("Checking PSR1 in AC Mode with CS Enabled system.");
                }
                else
                    Log.Verbose("Checking PSR1 in AC Mode with Non-CS system (PSR1 is expected to fail here).");
            }
            else
                Log.Verbose("Checking PSR1 in Battery Mode.");

            InitializePsr1Capture();

            if (CheckPsr1CapabilityInPanel())
            {
                Log.Verbose("Connected eDP is PSR1 supported eDP..");

                if (_platform != Platform.VLV && _platform != Platform.CHV)
                {
                    if (CheckPsr1CapabilityInDriver())
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
                Log.Verbose("Connected eDP is NOT PSR1 supported eDP.");
                psrStatus.psrWorkingState = PsrWorkingState.PsrNotEnabledAtSink;
                return psrStatus;
            }

            if (psrGetObject.psrEventType == PsrEventType.KeyPress)
                checkPsr1BasicWithKeyPress(psrGetObject);
            else
                checkPsr1BasicWithNaakuthanthi(psrGetObject);

            psrStatus.psrCapturedData.currentEntryExitCount = _psr1ActiveCount;
            psrStatus.psrCapturedData.requiredEntryExitCount = (psrGetObject.captureIntervalInSec - 5);
            psrStatus.psrCapturedData.currentResidencyTime = _psr1PerfCount;
            psrStatus.psrCapturedData.requiredResidencyTime = (int)(psrGetObject.captureIntervalInSec * 500 * 0.6);

            if (psrGetObject.psrEventType == PsrEventType.CursorMove)
            {
                psrStatus.psrCapturedData.requiredEntryExitCount = (int)(psrGetObject.captureIntervalInSec * 0.6);
            }
            else if (psrGetObject.psrEventType == PsrEventType.CursorChange)
            {
                if (File.Exists(CURSOR_CHANGE_TMP_FILE))
                    psrStatus.psrCapturedData.requiredEntryExitCount = (int)(File.ReadAllLines(CURSOR_CHANGE_TMP_FILE).Length * 0.8);
                else
                    psrStatus.psrCapturedData.requiredEntryExitCount = (int)(psrGetObject.captureIntervalInSec * 0.8);
            }
            else if (psrGetObject.psrEventType == PsrEventType.Nothing)
            {
                // When event type is 'nothing', requiredEntryExitCount cannot be decided here.
                // The caller has to take care of success or failure criteria
                psrStatus.psrCapturedData.requiredEntryExitCount = 0;
            }

            if (_psr1ActiveCount >= psrStatus.psrCapturedData.requiredEntryExitCount)
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledAndWorkingProperly;
            else if ((_psr1ActiveCount < psrStatus.psrCapturedData.requiredEntryExitCount) &&
                (psrStatus.psrCapturedData.currentEntryExitCount != 0))
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledButLessEntryExitCount;
            else if (_psr1ActiveCount == 0)
                psrStatus.psrWorkingState = PsrWorkingState.PsrEnabledButNotWorking;

            return psrStatus;
        }

        private void checkPsr1BasicWithKeyPress(PsrTestInput psrLegacyObj)
        {
            Log.Verbose("PSR1 Check: Launching Notepad for KeyPress...");
            Process pNotepad = new Process();
            pNotepad.StartInfo.CreateNoWindow = false;
            pNotepad.StartInfo.FileName = "notepad.exe";
            pNotepad.StartInfo.WindowStyle = ProcessWindowStyle.Maximized;
            pNotepad.EnableRaisingEvents = true;
            pNotepad.Start();

            StartPsr1Capture();
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
            StopPsr1Capture();

            if (!pNotepad.HasExited)
                pNotepad.Kill();

            Log.Verbose("PSR1 Active Count: {0}", _psr1ActiveCount);
        }

        private void checkPsr1BasicWithNaakuthanthi(PsrTestInput psrLegacyObj)
        {
            string args = "c:clock e:showtime x:300 y:300";
            if (psrLegacyObj.psrEventType == PsrEventType.CursorMove)
            {
                args = "c:cursor e:move o:random";
                Log.Verbose("PSR1 Check: Launching Cursor Move...");
            }
            else if (psrLegacyObj.psrEventType == PsrEventType.CursorChange)
            {
                args = "c:cursor e:shapechange p:50";
                Log.Verbose("PSR1 Check: Launching Cursor Change...");
            }
            else
            {
                args = "c:clock e:showtime x:300 y:300";
                Log.Verbose("PSR1 Check: Launching Digital Clock...");
            }

            Process procNaakuthanthi = new Process();
            procNaakuthanthi.StartInfo.UseShellExecute = false;
            procNaakuthanthi.StartInfo.CreateNoWindow = false;
            procNaakuthanthi.StartInfo.FileName = PSR_UTILITY_APP;
            procNaakuthanthi.StartInfo.Arguments = args;

            if (psrLegacyObj.psrEventType != PsrEventType.Nothing)
                procNaakuthanthi.Start();

            StartPsr1Capture();

            if(psrLegacyObj.psrEventType == PsrEventType.CursorChange)
                procNaakuthanthi.WaitForExit();
            else
                Thread.Sleep(psrLegacyObj.captureIntervalInSec * 1000);

            StopPsr1Capture();

            if (psrLegacyObj.psrEventType != PsrEventType.Nothing)
            {
                if (!procNaakuthanthi.HasExited)
                    procNaakuthanthi.Kill();
            }

            Log.Verbose("PSR1 Active Count: {0}", _psr1ActiveCount);
        }

        protected bool CheckPsr1CapabilityInPanel()
        {
            DpcdInfo dpcd = new DpcdInfo();
            dpcd.Offset = 0x00700; //DPCD_EDP_REV_ADDR
            dpcd.Value = 0;
            dpcd.DispInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkDpcd = sdkExtn.GetSDKHandle(SDKServices.DpcdRegister);

            sdkDpcd.Get(dpcd);
            if (dpcd.Value >= 0x02)
            {
                Log.Verbose("Connected eDP panel revision is v1.{0}", (dpcd.Value + 1));
            }
            else
            {
                Log.Verbose("Connected eDP panel revision is v1.{0}, PSR requirement is eDP v1.3 or later", (dpcd.Value + 1));
                return false;
            }

            dpcd.Offset = 0x00070; //DPCD_CAPS_SUPPORTED_AND_VERSION
            dpcd.Value = 0;
            sdkDpcd.Get(dpcd);
            if (dpcd.Value == 0x01) // Check whether it shd be >= / PSR2 panel also supports PSR
            {
                Log.Verbose("Connected eDP panel supports PSR capability version_1 (00070H ==> 01h)");
            }
            else
            {
                Log.Verbose("Connected eDP panel does not support PSR capability version_1 (00070H ==> {0:00}h", dpcd.Value);
                return false;
            }

            dpcd.Offset = 0x00003; //DPCD_FLT_FLAG_ADDR
            dpcd.Value = 0;
            sdkDpcd.Get(dpcd);
            if ((dpcd.Value & 0x40) == 0x40)
            {
                Log.Verbose("Connected eDP panel supports Fast Link Training (FLT)");
            }
            else
            {
                Log.Verbose("Connected eDP panel does not suport Fast Link Training (FLT)");
                return false;
            }

            return true; ;
        }

        protected bool CheckPsr1CapabilityInDriver()
        {
            // Only for HSW, BDW, SKL, KBL & BXT
            Log.Message("Check PSR1 capability in the driver");

            uint psr1Ctrl_RegVal = 0x0;
            ReadMMIORegister(_psr1CtrlReg, ref psr1Ctrl_RegVal); // PSR CTRL Reg
            if ((psr1Ctrl_RegVal & 0x80000000) == 0x80000000)
            {
                Log.Success("PSR1 Feature is enabled in the driver..");
            }
            else
            {
                Log.Fail("PSR1 Feature is not enabled in the driver..");
                return false;
            }
            return true;
        }

        protected uint GetRegisterOffset(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors:{1},{2},{3}", registerEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);

            uint offset = 0x0;
            if (returnEventInfo.listRegisters.Count > 0)
            {
                offset = Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16);
            }

            return offset;
        }

        protected void InitializePsr1Capture()
        {
            Log.Message("Psr1Capture: Intializing PSR1 capture..");

            _psr1CaptureLog = "Psr1Log.txt";
            _platform = base.MachineInfo.PlatformDetails.Platform;

            PipePlaneParams pipePlane = new PipePlaneParams(DisplayType.EDP);
            PipePlane pPlane = base.CreateInstance<PipePlane>(new PipePlane());
            pipePlane = (PipePlaneParams)pPlane.GetMethod(pipePlane);
            DisplayInfo displayInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();

            _psr1CtrlReg = GetRegisterOffset(psr1CtrlReg_Event, pipePlane.Pipe, pipePlane.Plane, displayInfo.Port);
            _psr1StatReg = GetRegisterOffset(psr1StatReg_Event, pipePlane.Pipe, pipePlane.Plane, displayInfo.Port);
            if (_platform == Platform.VLV || _platform == Platform.CHV)
            {
                _psr1PerfReg = 0x0; // Not valid for VLV & CHV
                _edpPortCtrlReg = GetRegisterOffset(portCtrlEdpReg_Event, pipePlane.Pipe, pipePlane.Plane, displayInfo.Port);
            }
            else
            {
                _psr1PerfReg = GetRegisterOffset(psr1PerfReg_Event, pipePlane.Pipe, pipePlane.Plane, displayInfo.Port);
                _edpPortCtrlReg = 0x0; // Not required for HSW, BDW, SKL, KBL & BXT. Need to handle this in FW
            }
        }

        protected void StartPsr1Capture()
        {
            Log.Verbose("Starting PSR1 Capture...");
            _startCapture = true;

            switch (_platform)
            {
                case Platform.VLV:
                case Platform.CHV:
                    _psr1DelegateObj = Psr1CaptureVLV_CHV;
                    break;
                case Platform.HSW:
                case Platform.BDW:
                    _psr1DelegateObj = Psr1CaptureHSWplus;
                    break;
                case Platform.SKL:
                case Platform.KBL:
                case Platform.BXT:
                    _psr1DelegateObj = Psr1CaptureSKLplus_DMC;
                    break;
                default: // Assuming it will be same for future platform (CNL, etc)
                    _psr1DelegateObj = Psr1CaptureSKLplus_DMC;
                    break;
            }

            if (_psr1DelegateObj != default(PsrPollDelegate))
                _iAsyncResult = _psr1DelegateObj.BeginInvoke(default(AsyncCallback), default(Object));
        }

        protected void StopPsr1Capture()
        {
            Log.Verbose("Stopping PSR1 Capture...");
            _startCapture = false;

            if (_iAsyncResult != default(IAsyncResult))
                _iAsyncResult.AsyncWaitHandle.WaitOne();
            _psr1DelegateObj = default(PsrPollDelegate);
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

        private void Psr1CaptureVLV_CHV()
        {
            if (File.Exists(_psr1CaptureLog))
            {
                File.Delete(_psr1CaptureLog);
            }
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkDpcd = sdkExtn.GetSDKHandle(SDKServices.DpcdRegister);

            using (StreamWriter sw = File.AppendText(_psr1CaptureLog))
            {
                while (!_startCapture) ;

                _psr1ActiveCount = 0;
                _edpPortDisabled = false;

                uint uPsr1CtlA_RegValue = 0;
                uint uPsr1_StatA_RegValue = 0;
                uint uEdpPort_RegValue = 0;

                bool bPrev_Psr1Active = false;
                bool bCur_Psr1Active = false;

                DpcdInfo dpcd = new DpcdInfo();
                dpcd.Offset = 0x02008; //DPCD_SINK_PSR_STATUS 
                dpcd.DispInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();

                while (_startCapture)
                {
                    ReadMMIORegister(_psr1StatReg, ref uPsr1_StatA_RegValue); // PSR STAT Reg
                    ReadMMIORegister(_psr1CtrlReg, ref uPsr1CtlA_RegValue); // PSR CTRL Reg

                    uint uPsr1StatReg_CurStateValue = uPsr1_StatA_RegValue & 0x00000007; // 2:0b

                    if (uPsr1StatReg_CurStateValue == 0x00000002) // Skip intermediate states in PSR STAT Reg
                    {
                        Thread.Sleep(5);
                        continue;
                    }

                    uint uPsr1CtrlReg_EnabledValue = uPsr1CtlA_RegValue & 0x00000001;       // 0b
                    uint uPsr1CtrlReg_ModeValue = uPsr1CtlA_RegValue & 0x0000001C;          // 4:2b
                    uint uPsr1CtrlReg_ActiveEntryValue = uPsr1CtlA_RegValue & 0x00000100;   // 8b // currently not using                        

                    bPrev_Psr1Active = bCur_Psr1Active;

                    if (((uPsr1StatReg_CurStateValue == 0x00000003) || (uPsr1StatReg_CurStateValue == 0x00000004)) && (uPsr1CtrlReg_EnabledValue == 0x00000001)) //PSR Enabled (PSR Stat Reg)
                    {
                        bCur_Psr1Active = true;
                    }
                    else if (((uPsr1StatReg_CurStateValue == 0x00000000) || (uPsr1StatReg_CurStateValue == 0x00000001) || (uPsr1StatReg_CurStateValue == 0x00000005)) && (uPsr1CtrlReg_EnabledValue == 0x00000000))
                    {
                        bCur_Psr1Active = false;
                    }

                    if (bCur_Psr1Active != bPrev_Psr1Active)
                    {
                        sdkDpcd.Get(dpcd);

                        ReadMMIORegister(_edpPortCtrlReg, ref uEdpPort_RegValue); // PSR STAT Reg
                        uint uEDPPortEnabledValue = uEdpPort_RegValue & 0x80000000;   // 31b

                        if (bCur_Psr1Active)
                        {
                            _psr1ActiveCount++;
                            sw.WriteLine("Psr1_Entered || " + _psr1ActiveCount);

                            if (uPsr1StatReg_CurStateValue == 0x00000003)
                            {
                                sw.WriteLine("PSR1_STATE || PSR_ACTIVE_NO_RFB_UPDATE");
                            }
                            else if (uPsr1StatReg_CurStateValue == 0x00000004)
                            {
                                sw.WriteLine("PSR1_STATE || PSR_ACTIVE_SINGLE_FRAME_UPDATE");
                            }
                            else
                            {
                                sw.WriteLine("PSR1_STATE || PSR_UNKNOWN_STATE");
                            }

                            // Ctrl Reg Check

                            uint uDPCDSinkStatus = (uint)(dpcd.Value & 0x00000007); //2:0b

                            if (uDPCDSinkStatus == 0x2 || uDPCDSinkStatus == 0x1 || uDPCDSinkStatus == 0x3 || uDPCDSinkStatus == 0x4) // Included PSR Active Intermediate States Also
                            {
                                sw.WriteLine("DPCD_STATE || DPCD_PSR_ACTIVE");
                            }
                            else if (uDPCDSinkStatus == 0x0)
                            {
                                sw.WriteLine("DPCD_STATE || DPCD_PSR_INACTIVE (W)");
                            }
                        }
                        else
                        {
                            sw.WriteLine("Psr1_Exited || " + _psr1ActiveCount);

                            if (uPsr1StatReg_CurStateValue == 0x00000000)
                            {
                                sw.WriteLine("PSR1_STATE || PSR_DISABLED");
                            }
                            else if (uPsr1StatReg_CurStateValue == 0x00000001)
                            {
                                sw.WriteLine("PSR1_STATE || PSR_INACTIVE");
                            }
                            else if (uPsr1StatReg_CurStateValue == 0x00000005)
                            {
                                sw.WriteLine("PSR1_STATE || PSR_EXIT");
                            }
                            else
                            {
                                sw.WriteLine("PSR1_STATE || PSR_UNKNOWN_STATE");
                            }

                            // Ctrl Reg Check

                            uint uDPCDSinkStatus = (uint)(dpcd.Value & 0x00000007); //2:0b

                            if (uDPCDSinkStatus == 0x2 || uDPCDSinkStatus == 0x1 || uDPCDSinkStatus == 0x3 || uDPCDSinkStatus == 0x4) // Included PSR Active Intermediate States Also
                            {
                                sw.WriteLine("DPCD_STATE || DPCD_PSR_ACTIVE (W)");
                            }
                            else if (uDPCDSinkStatus == 0x0)
                            {
                                sw.WriteLine("DPCD_STATE || DPCD_PSR_INACTIVE");
                            }
                        }

                        if (uEDPPortEnabledValue == 0x00000000) //Port disabling is optional during PSR
                        {
                            _edpPortDisabled = true;
                            sw.WriteLine("EDP_PORT || PORT_DISABLED");
                        }
                        else
                        {
                            sw.WriteLine("EDP_PORT || PORT_ENABLED");
                        }

                        sw.WriteLine("------------------------------------------->");
                    }

                    Thread.Sleep(60); // Driver time is 60ms
                }
                sw.Close();
            }
        }

        private void Psr1CaptureHSWplus()
        {
            if (File.Exists(_psr1CaptureLog))
            {
                File.Delete(_psr1CaptureLog);
            }

            using (StreamWriter sw = File.AppendText(_psr1CaptureLog))
            {
                while (!_startCapture) ;

                _psr1ActiveCount = 0;
                _psr1PerfCount = 0;
                _edpPortDisabled = false;

                uint uPsr1Stat_LastState = 0xE0000000;
                uint uLink_LastStatus = 0x0C000000;
                uint uPsr1Stat_LastEntryCount = 0;

                uint uPsr1Stat_RegValue = 0;
                uint uPsr1Perf_RegValue = 0;

                uint uPsr1Perf_LastPerfCount = 0; // 0x00FFFFFF;

                ReadMMIORegister(_psr1StatReg, ref uPsr1Stat_RegValue); // PSR STAT Reg
                uPsr1Stat_LastEntryCount = ((uPsr1Stat_RegValue & 0x000F0000) >> 16);

                ReadMMIORegister(_psr1PerfReg, ref uPsr1Perf_RegValue); // PSR Perf Count Reg
                uPsr1Perf_LastPerfCount = uPsr1Perf_RegValue;

                while (_startCapture)
                {
                    ReadMMIORegister(_psr1StatReg, ref uPsr1Stat_RegValue); // PSR STAT Reg

                    uint uPsr1Stat_CurState = uPsr1Stat_RegValue & 0xE0000000; // 31:29b
                    uint uLink_CurStatus = uPsr1Stat_RegValue & 0x0C000000; // 27:26b
                    uint uPsr1Stat_CurEntryCount = ((uPsr1Stat_RegValue & 0x000F0000) >> 16); // 19:16b

                    ReadMMIORegister(_psr1PerfReg, ref uPsr1Perf_RegValue); // PSR Perf Count Reg

                    uint uPsr1Perf_CurPerfCount = uPsr1Perf_RegValue; // 23:0b

                    if (uPsr1Stat_CurState != uPsr1Stat_LastState)
                    {
                        switch (uPsr1Stat_CurState)
                        {
                            case 0x00000000: sw.WriteLine("Psr1_state = IDLE (Reset state)");
                                break;
                            case 0x20000000: sw.WriteLine("Psr1_state = SRDONACK (Wait for TG/Stream to send on frame of data after SRD conditions are met)");
                                break;
                            case 0x40000000: sw.WriteLine("Psr1_state = SRDENT (SRD entry)");
                                break;
                            case 0x60000000: sw.WriteLine("Psr1_state = BUFOFF (Wait for buffer turn off - transcoder EDP only)");
                                break;
                            case 0x80000000: sw.WriteLine("Psr1_state = BUFON (Wait for buffer turn on - transcoder EDP only)");
                                break;
                            case 0xA0000000: sw.WriteLine("Psr1_state = AUXACK (Wait for AUX to acknowledge on SRD exit - transcoder EDP only)");
                                break;
                            case 0xC0000000: sw.WriteLine("Psr1_state = SRDOFFACK (Wait for TG/Stream to acknowledge the SRD VDM exit)");
                                break;
                            default: sw.WriteLine("Psr1_state = Reserved (Wrong State)");
                                break;
                        }

                        uPsr1Stat_LastState = uPsr1Stat_CurState;
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

                    if (uPsr1Stat_CurEntryCount != uPsr1Stat_LastEntryCount)
                    {
                        if (uPsr1Stat_CurEntryCount < uPsr1Stat_LastEntryCount)
                        {
                            _psr1ActiveCount += (int)((uPsr1Stat_CurEntryCount + 16) - uPsr1Stat_LastEntryCount);
                        }
                        else
                        {
                            _psr1ActiveCount += (int)(uPsr1Stat_CurEntryCount - uPsr1Stat_LastEntryCount);
                        }
                        sw.WriteLine("\nPsr1_Entry_Count = " + _psr1ActiveCount);

                        uPsr1Stat_LastEntryCount = uPsr1Stat_CurEntryCount;

                        if (uPsr1Perf_CurPerfCount != uPsr1Perf_LastPerfCount)
                        {
                            if (uPsr1Perf_CurPerfCount < uPsr1Perf_LastPerfCount)
                            {
                                _psr1PerfCount += (int)((uPsr1Perf_CurPerfCount + 16777216) - uPsr1Perf_LastPerfCount);
                            }
                            else
                            {
                                _psr1PerfCount += (int)(uPsr1Perf_CurPerfCount - uPsr1Perf_LastPerfCount);
                            }
                            sw.WriteLine("Psr1_Perf_Count = " + _psr1PerfCount + "\n");

                            uPsr1Perf_LastPerfCount = uPsr1Perf_CurPerfCount;
                        }
                    }

                    //// This code will be enabled once DPCD read bug/ behavior in less then 100ms is finalized in the driver/ CUI SDK side
                    //DpcdInfo dpcd = new DpcdInfo();
                    //dpcd.Offset = 0x02008; //DPCD_PSR_STATUS
                    //dpcd.CuiMonitorId = base.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).Select(dI => dI.CUIMonitorID).FirstOrDefault();
                    //byte[] buffer = new byte[16];
                    //uint uDpcdRetVal = readDPCD(dpcd, ref buffer);
                    //uint uDpcdSinkStatus = uDpcdRetVal & 0x07; // 2:0b
                    //if (uDpcdSinkStatus >= 0x01 && uDpcdSinkStatus <= 0x04) // Included PSR active intermediate states also
                    //{
                    //    sw.WriteLine("DPCD_state = PSR ACTIVE");
                    //}
                    //else if (uDpcdSinkStatus == 0x00)
                    //{
                    //    sw.WriteLine("DPCD_state = PSR INACTIVE");
                    //}

                    Thread.Sleep(100); // Check
                }
                sw.Close();
            }
        }

        private void Psr1CaptureSKLplus_DMC() // For DMC
        {
            if (File.Exists(_psr1CaptureLog))
            {
                File.Delete(_psr1CaptureLog);
            }

            using (StreamWriter sw = File.AppendText(_psr1CaptureLog))
            {
                while (!_startCapture) ;

                _psr1ActiveCount = 0;

                uint uPsr1Stat_LastState = 0xE0000000;
                uint uLink_LastStatus = 0x0C000000;

                uint uPsr1Stat_RegValue = 0;

                while (_startCapture)
                {
                    ReadMMIORegister(_psr1StatReg, ref uPsr1Stat_RegValue); // PSR STAT Reg

                    uint uPsr1Stat_CurState = uPsr1Stat_RegValue & 0xE0000000; // 31:29b
                    uint uLink_CurStatus = uPsr1Stat_RegValue & 0x0C000000; // 27:26b

                    if (uPsr1Stat_CurState != uPsr1Stat_LastState)
                    {
                        switch (uPsr1Stat_CurState)
                        {
                            case 0x00000000: sw.WriteLine("Psr1_state = IDLE (Reset state)");
                                break;
                            case 0x20000000: sw.WriteLine("Psr1_state = SRDONACK (Wait for TG/Stream to send on frame of data after SRD conditions are met)");
                                break;
                            case 0x40000000: sw.WriteLine("Psr1_state = SRDENT (SRD entry)");
                                _psr1ActiveCount++;
                                break;
                            case 0x60000000: sw.WriteLine("Psr1_state = BUFOFF (Wait for buffer turn off - transcoder EDP only)");
                                break;
                            case 0x80000000: sw.WriteLine("Psr1_state = BUFON (Wait for buffer turn on - transcoder EDP only)");
                                break;
                            case 0xA0000000: sw.WriteLine("Psr1_state = AUXACK (Wait for AUX to acknowledge on SRD exit - transcoder EDP only)");
                                break;
                            case 0xC0000000: sw.WriteLine("Psr1_state = SRDOFFACK (Wait for TG/Stream to acknowledge the SRD VDM exit)");
                                break;
                            default: sw.WriteLine("Psr1_state = Reserved (Wrong State)");
                                break;
                        }

                        uPsr1Stat_LastState = uPsr1Stat_CurState;
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

                    Thread.Sleep(100); // Check
                }
                sw.Close();
            }
        }
    }
}
