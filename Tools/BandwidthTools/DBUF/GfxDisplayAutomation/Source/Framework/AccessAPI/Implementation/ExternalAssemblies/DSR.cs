namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;

    public delegate void DSRDelegate();

    internal class DSR : FunctionalBase, IGetMethod
    {
        protected const string DSR_UTILITY_APP = "Naakuthanthi.exe";
        protected const string CURSOR_CHANGE_TMP_FILE = "CursorShapeChange.tmp";

        protected string _dsrLog = "";
        protected bool _startCapture = false;
        protected Platform _platform = Platform.BXT; // default;
        protected DSRDelegate _dsrDelObj = default(DSRDelegate);
        protected IAsyncResult _iAsyncResult = default(IAsyncResult);

        protected int _dsrEntryExitCount = 0;
        protected string _currentDsrMode = "NONE";

        protected uint _dsiPllEnableReg = 0x0;
        protected uint _dePllEnableReg = 0x0;
        protected uint _pwrWellCtr2Reg = 0x0;   // 30th bit
        protected uint _dcStateEnReg = 0x0;     // only bit 3 - shd be 1
        protected uint _dePwr1Reg = 0x0;        //31st & 28th bit

        protected const string dsiPllEnableReg_Event = "DSI_PLL_ENABLE_Register";
        protected const string dePllEnableReg_Event = "DE_PLL_ENABLE_Register";
        protected const string pwrWellCtr2Regt_Event = "PWR_WELL_CTL2_Register";
        protected const string dcStateEnReg_Event = "DC_STATE_EN_Register";
        protected const string dePwr1Reg_Event = "DE_PWR_1_Register";

        protected const string MIPI_DUAL_LINK_MODE_EVENT = "MIPI_DUAL_LINK_MODE";
        protected const string MIPI_DEVICE_READY_EVENT = "MIPI_DEVICE_READY_REG";
        protected const string MIPI_DSI_FUNC_PRG_EVENT = "MIPI_DSI_FUNC_PRG_REG";

        public object GetMethod(object argMessage)
        {
            DsrStat dsrStat = new DsrStat();
            DsrInput dsrInput = argMessage as DsrInput;

            if (dsrInput.captureIntervalInSec < 10)
                dsrInput.captureIntervalInSec = 11;

            if (!File.Exists(DSR_UTILITY_APP))
            {
                Log.Verbose("DSR Utility App (Naakuthanthi.exe) is not found.");
                dsrStat.dsrWorkingState = DsrWorkingState.DsrUtilityAppMissing;
                return dsrStat;
            }

            if (dsrInput.currentConfig.PrimaryDisplay != DisplayType.MIPI || dsrInput.currentConfig.ConfigType != DisplayConfigType.SD)
            {
                Log.Verbose("Current Config is not SD MIPI. PSR works only in SD MIPI Config.");
                dsrStat.dsrWorkingState = DsrWorkingState.DsrWrongConfig;
                return dsrStat;
            }

            ACPIFunctions acpi = new ACPIFunctions();
            PowerLineStatus plineStatus = (PowerLineStatus)acpi.Get;
            if (plineStatus != PowerLineStatus.Offline)
            {
                if (DisplayExtensions.VerifyCSSystem(base.MachineInfo))
                {
                    Log.Verbose("Checking DSR in AC Mode with CS Enabled system.");
                }
                else
                    Log.Verbose("Checking DSR in AC Mode with Non-CS system.");
            }
            else
                Log.Verbose("Checking DSR in Battery Mode.");

            InitializeDsrLogging();

            if (CheckDsrSupportabilityInDriver(dsrInput))
            {
                Log.Verbose("Connected MIPI is DSR supported MIPI..");                              
            }
            else
            {
                Log.Verbose("Connected MIPI is NOT DSR supported.");
                dsrStat.dsrWorkingState = DsrWorkingState.DsrSupportabilityFailed;
                return dsrStat;
            }

            checkDsrBasic(dsrInput);
            dsrStat.dsrCapturedData.currentEntryExitCount = _dsrEntryExitCount;
            dsrStat.dsrCapturedData.requiredEntryExitCount = (dsrInput.captureIntervalInSec - 5);
            dsrStat.dsrCapturedData.currentDsrMode = _currentDsrMode;

            if (dsrInput.dsrEventType == PsrEventType.CursorMove)
                dsrStat.dsrCapturedData.requiredEntryExitCount = (int)(dsrInput.captureIntervalInSec / 2);

            if (dsrInput.dsrEventType == PsrEventType.CursorChange)
            {
                if (File.Exists(CURSOR_CHANGE_TMP_FILE))
                {
                    dsrStat.dsrCapturedData.requiredEntryExitCount = File.ReadAllLines(CURSOR_CHANGE_TMP_FILE).Length;
                    dsrStat.dsrCapturedData.requiredEntryExitCount = (int)(dsrStat.dsrCapturedData.requiredEntryExitCount * 0.9);
                }
            }

            if (_dsrEntryExitCount >= dsrStat.dsrCapturedData.requiredEntryExitCount)
                dsrStat.dsrWorkingState = DsrWorkingState.DsrEnabledAndWorkingProperly;
            else if ((_dsrEntryExitCount < dsrStat.dsrCapturedData.requiredEntryExitCount) &&
                (dsrStat.dsrCapturedData.currentEntryExitCount != 0))
                dsrStat.dsrWorkingState = DsrWorkingState.DsrEnabledButLessEntryExitCount;
            else if (_dsrEntryExitCount == 0)
                dsrStat.dsrWorkingState = DsrWorkingState.DsrEnabledButNotWorking;

            return dsrStat;
        }

        private void checkDsrBasic(DsrInput dsrObj)
        {
            string args = "c:clock e:showtime x:300 y:300";
            if (dsrObj.dsrEventType == PsrEventType.CursorMove)
            {
                args = "c:cursor e:move o:random";
                Log.Verbose("Launching Cursor Move...");
            }
            else if (dsrObj.dsrEventType == PsrEventType.CursorChange)
            {
                args = "c:cursor e:shapechange p:50";
                Log.Verbose("Launching Cursor Change...");
            }
            else
            {
                args = "c:clock e:showtime x:300 y:300";
                Log.Verbose("Launching Digital Clock...");
            }

            Log.Verbose("PSR Check is in progress..");

            Process procNaakuthanthi = new Process();
            procNaakuthanthi.StartInfo.UseShellExecute = false;
            procNaakuthanthi.StartInfo.CreateNoWindow = false;
            procNaakuthanthi.StartInfo.FileName = DSR_UTILITY_APP;
            procNaakuthanthi.StartInfo.Arguments = args;

            if (dsrObj.dsrEventType != PsrEventType.Nothing)
                procNaakuthanthi.Start();

            StartDsrLogging();

            if (dsrObj.dsrEventType == PsrEventType.CursorChange)
                procNaakuthanthi.WaitForExit();
            else
                Thread.Sleep(dsrObj.captureIntervalInSec * 1000);

            StopDsrLogging();

            if (dsrObj.dsrEventType != PsrEventType.Nothing)
            {
                if (!procNaakuthanthi.HasExited)
                    procNaakuthanthi.Kill();
            }

            Log.Verbose("DSR Entry/ Exit Count: {0}", _dsrEntryExitCount);
        }

        protected bool VerifyRegister(string regEvent, PIPE pipe, PLANE plane, PORT port)
        {
            bool bRet = false;
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors:{1},{2},{3}", regEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = regEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);
            
            if (returnEventInfo.listRegisters.Count > 0)
            {
                uint regValue = 0x0;
                if(ReadMMIORegister(Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16), ref regValue))
                {
                    if ((regValue & Convert.ToUInt32(returnEventInfo.listRegisters[0].Bitmap, 16)) == Convert.ToUInt32(returnEventInfo.listRegisters[0].Value, 16))
                    {
                        bRet = true;
                    }
                }
            }

            return bRet;
        }

        protected bool CheckDsrSupportabilityInDriver(DsrInput dsrObj)
        {
            bool bRetVal = true;
            Log.Message("Check DSR Supportability in the driver");

            Process procNaak = new Process();
            procNaak.StartInfo.UseShellExecute = false;
            procNaak.StartInfo.CreateNoWindow = false;
            procNaak.StartInfo.FileName = DSR_UTILITY_APP;
            procNaak.StartInfo.Arguments = "c:draw e:pixelpath w:300 h:300";
            procNaak.Start();

            Thread.Sleep(2 * 1000);

            bool isDeviceReady = VerifyRegister(MIPI_DEVICE_READY_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA);
            if(isDeviceReady)
            {
                Log.Success("Test: MIPI is connected.");
            }
            else
            {
                bRetVal = false;
                Log.Fail("Test: MIPI is not connected.");
            }

            bool isCmdDsr = VerifyRegister(MIPI_DSI_FUNC_PRG_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA);
            if (isCmdDsr)
            {
                Log.Success("MIPI: Command mode and DSR supported");
            }
            else
            {
                bRetVal = false;
                Log.Fail("MIPI: Not command mode or Not DSR supported");
            }

            bool isDualLinkEnabled = VerifyRegister(MIPI_DUAL_LINK_MODE_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA);
            if (isDualLinkEnabled)
            {
                Log.Success("MIPI: Data is driven in Dual Link mode.");
            }
            else
            {
                Log.Success("MIPI: Dual Link is not enabled.");
            }

            if (!procNaak.HasExited)
                procNaak.Kill();

            return bRetVal;
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

        protected void InitializeDsrLogging()
        {
            Log.Message("DSRCapture: Intializing DSR logging..");

            _dsrLog = "DSRLog.txt";

            _dsiPllEnableReg = GetRegisterOffset(dsiPllEnableReg_Event, PIPE.NONE, PLANE.NONE, PORT.NONE);
            _dePllEnableReg = GetRegisterOffset(dePllEnableReg_Event, PIPE.NONE, PLANE.NONE, PORT.NONE);
            _pwrWellCtr2Reg = GetRegisterOffset(pwrWellCtr2Regt_Event, PIPE.NONE, PLANE.NONE, PORT.NONE);
            _dcStateEnReg = GetRegisterOffset(dcStateEnReg_Event, PIPE.NONE, PLANE.NONE, PORT.NONE);
            _dePwr1Reg = GetRegisterOffset(dePwr1Reg_Event, PIPE.NONE, PLANE.NONE, PORT.NONE);            
        }

        protected void StartDsrLogging()
        {
            Log.Verbose("Starting DSR Logging...");
            _startCapture = true;

            _dsrDelObj = DSRCaptureBXT;
            if (_dsrDelObj != default(DSRDelegate))
                _iAsyncResult = _dsrDelObj.BeginInvoke(default(AsyncCallback), default(Object));
        }

        protected void StopDsrLogging()
        {
            Log.Verbose("Stopping DSR Logging...");
            _startCapture = false;

            if (_iAsyncResult != default(IAsyncResult))
                _iAsyncResult.AsyncWaitHandle.WaitOne();
            _dsrDelObj = default(DSRDelegate);
        }

        private bool ReadMMIORegister(uint offset, ref uint value)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = offset;
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            DriverEscape driverEscapeObj = new DriverEscape();
            bool bRet = driverEscapeObj.SetMethod(driverParams);
            value = driverData.output;
            return bRet;
        }

        private void DSRCaptureBXT()
        {
            if (File.Exists(_dsrLog))
            {
                File.Delete(_dsrLog);
            }

            using (StreamWriter sw = File.AppendText(_dsrLog))
            {
                while (!_startCapture) ;

                _dsrEntryExitCount = 0;

                bool bPrevState = false;
                bool bCurState = false;

                uint mipi_pwrWell_Ctl2_val = 0x0;
                uint mipi_de_pwr_1_val = 0x0;
                uint mipi_DSI_PLL_En_val = 0x0;
                uint mipi_DE_PLL_En_val = 0x0;
                uint mipi_Allow_dc9_state = 0x0;

                uint uflag = 0x0;

                while (_startCapture)
                {
                    ReadMMIORegister(_pwrWellCtr2Reg, ref mipi_pwrWell_Ctl2_val);
                    ReadMMIORegister(_dePwr1Reg, ref mipi_de_pwr_1_val);
                    ReadMMIORegister(_dsiPllEnableReg, ref mipi_DSI_PLL_En_val);
                    ReadMMIORegister(_dcStateEnReg, ref mipi_Allow_dc9_state);

                    bPrevState = bCurState;

                    if (((mipi_pwrWell_Ctl2_val & 0x40000000) == 0x00000000) && ((mipi_de_pwr_1_val & 0x90000000) == 0x00000000)) // DC9 case (Panel PWM - Pipe A)
                    {
                        ReadMMIORegister(_dePllEnableReg, ref mipi_DE_PLL_En_val);
                        uflag = 1;
                        if (((mipi_DSI_PLL_En_val & 0x40000000) == 0x00000000) && ((mipi_DE_PLL_En_val & 0x40000000) == 0x00000000) && ((mipi_Allow_dc9_state & 0x00000008) == 0x00000008))
                        {
                            bCurState = true;
                        }
                        else
                        {
                            bCurState = false;
                        }
                    }
                    else if (((mipi_pwrWell_Ctl2_val & 0x40000000) == 0x00000000) && ((mipi_de_pwr_1_val & 0x90000000) == 0x10000000)) // LPSP mode on Pipe A
                    {
                        uflag = 2;
                        if (((mipi_DSI_PLL_En_val & 0x40000000) == 0x00000000) && ((mipi_Allow_dc9_state & 0x00000008) == 0x00000000))
                        {
                            bCurState = true;
                        }
                        else
                        {
                            bCurState = false;
                        }
                    }
                    else if (((mipi_pwrWell_Ctl2_val & 0x40000000) == 0x40000000) && ((mipi_de_pwr_1_val & 0x90000000) == 0x80000000)) // Non LPSP mode on Pipe B/C
                    {
                        uflag = 3;
                        if (((mipi_DSI_PLL_En_val & 0x40000000) == 0x00000000) && ((mipi_Allow_dc9_state & 0x00000008) == 0x00000000))
                        {
                            bCurState = true;
                        }
                        else
                        {
                            bCurState = false;
                        }
                    }
                    else
                    {
                        // DSR Disabled
                        bCurState = false;
                    }

                    if (bCurState != bPrevState)
                    {
                        if (bCurState)
                        {
                            _dsrEntryExitCount++;
                            sw.WriteLine("MIPI_DSR_Entered (Count: " + _dsrEntryExitCount + ")");
                        }
                        else
                        {
                            sw.WriteLine("MIPI_DSR_Exited (Count: " + _dsrEntryExitCount + ")");
                        }

                        if (uflag == 1)
                        {
                            _currentDsrMode = "DC9 MODE";
                            sw.WriteLine("DC9 mode");
                        }
                        else if (uflag == 2)
                        {
                            _currentDsrMode = "LPSP (PIPE A) MODE";
                            sw.WriteLine("LPSP mode - Pipe A");
                        }
                        else if (uflag == 3)
                        {
                            _currentDsrMode = "NON-LPSP MODE";
                            sw.WriteLine("Non-LPSP Mode");
                        }
                        else
                        {
                            _currentDsrMode = "INVALID";
                            sw.WriteLine("ATTENTION: Invalid condition");
                        }

                        sw.WriteLine("---------------------------------------------------------->");
                    }

                    Thread.Sleep(60); // Revisit if required
                }
                sw.Close();
            }
        }

        

        
    }
}
