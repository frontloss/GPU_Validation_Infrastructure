namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Threading;
    using System.IO;
    using System.Windows.Forms;

    enum PWR_Status { PWR_ON, PWR_OFF, No_PWR_Change };
    enum CurrentDisp { Internal, External };


    public class MP_Audio_Base : TestBase
    {
        internal List<DisplayModeList> allModeList = new List<DisplayModeList>();
        protected AudioInputSource _audioInputSource;
        protected const string LPSP_REGISTER_EVENT = "LPSP_ENABLE";
        protected AudioDataProvider _audioEndpointData = null;
        private SetAudioParam _inParam = null;
        internal int eSet = 0, eReset = 0, IAset = 0, PDset = 0, CPset = 0, IAreset = 0, PDreset = 0, CPreset = 0, PWR_On =0, PWR_Off=0;

        public MP_Audio_Base()
        {
            _audioInputSource = AudioInputSource.Single;
            _inParam = new SetAudioParam();
        }

        internal bool EnableDisableAudioWTVideo(SetAudioParam setAudioParam)
        {
            DisplayConfig configParam = null;
            if (base.CurrentConfig.CustomDisplayList.Count == 2)
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.DDC,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay
                };
            else if (base.CurrentConfig.CustomDisplayList.Count == 3)
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.TDC,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay,
                    TertiaryDisplay = base.CurrentConfig.TertiaryDisplay
                };
            else
            {
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.SD,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay
                };
            }
            if (!AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, configParam))
                Log.Abort("Unable to set display config {0} ", configParam.GetCurrentConfigStr());
            Log.Message(true, "Setting audio topology to {0} source and audio without video to {1}d", setAudioParam.audioTopology, setAudioParam.audioWTVideo);
            if (AccessInterface.SetFeature<bool, SetAudioParam>(Features.AudioEnumeration, Action.SetMethod, setAudioParam))
            {
                Log.Success("Audio topology changed successfully to {0} source and Audio without video to {1}d", setAudioParam.audioTopology, setAudioParam.audioWTVideo);
                if (setAudioParam.audioWTVideo == AudioWTVideo.Disable)
                    DisplayExtensions.AudioWTVideoEnable = true;
                else
                    DisplayExtensions.AudioWTVideoEnable = false;
                return true;
            }
            else
                Log.Abort("Failed to change audio topology and audio without video");
            return false;
        }

        internal void SetAudioSource()
        {
            DisplayConfig configParam = null;
            if (base.CurrentConfig.CustomDisplayList.Count == 2)
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.DDC,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay
                };
            else if (base.CurrentConfig.CustomDisplayList.Count == 3)
                configParam = new DisplayConfig
                {
                    ConfigType = DisplayConfigType.TDC,
                    PrimaryDisplay = base.CurrentConfig.PrimaryDisplay,
                    SecondaryDisplay = base.CurrentConfig.SecondaryDisplay,
                    TertiaryDisplay = base.CurrentConfig.TertiaryDisplay
                };
            else
                Log.Abort("Test required atleast one external display to run");
            if (!AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, configParam))
                Log.Abort("Unable to set display config {0} ", configParam.GetCurrentConfigStr());
            _inParam.setAudioInfo = Automation.SetAudioSource.SetAudioTopology;
            GetSupportedAudioSource(_audioInputSource);
            _inParam.audioTopology = _audioInputSource;
            Log.Message("Change audio source to {0} through CUI SDK", _audioInputSource.ToString());
            if (AccessInterface.SetFeature<bool, SetAudioParam>(Features.AudioEnumeration, Action.SetMethod, _inParam))
            {
                Log.Success("Audio topology changed successfully");
            }
            else
                Log.Abort("Failed to change audio topology");
        }

        private void GetSupportedAudioSource(AudioInputSource argInputSource)
        {
            switch (base.MachineInfo.PlatformDetails.Platform)
            {
                case Platform.BDW:
                case Platform.CHV:
                case Platform.HSW:
                    _audioInputSource = argInputSource;
                    break;
                default:
                    _audioInputSource = AudioInputSource.Multiple;
                    break;

            }
        }

        internal void VerifyAudioDriverStatus()
        {
            if (base.MachineInfo.Driver.AudioDriverStatus.ToString().ToLower().Contains("ok"))
                Log.Verbose("Intel(R) Audio Driver is Status Verified");
            else
            {
                DriverInfo driverInfo = AccessInterface.GetFeature<DriverInfo, DriverAdapterType>(Features.DriverFunction, Action.GetMethod, Source.AccessAPI, DriverAdapterType.Audio);
                if (driverInfo.AudioDriverStatus.ToString().ToLower().Contains("ok"))
                    Log.Verbose("Intel(R) Audio Driver is Status Verified");
                else
                    Log.Abort("Intel Audio Driver is not installed Under Sound,Video and game controllers");
            }
        }

        protected void EnableFeature(bool status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = status;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)System.Runtime.InteropServices.Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE, ult_Esc_Args);
            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }

        internal void CheckAudioEndPoint(AudioDataProvider argAudioEndpointData)
        {
            bool SUCCESS = true;
            int NoOfExtDisplays = 0;
            int NoOfAudCapableDispalys = 0;

            _audioEndpointData = argAudioEndpointData;
            DisplayConfig currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);

            //Check Endpoint count and Display count  
            Log.Message("Check Audio Endpoint details ");

            NoOfExtDisplays = currentDisplayConfig.CustomDisplayList.Count;
            for (int i = 0; i < NoOfExtDisplays; i++)
            {
                if (argAudioEndpointData.ListAudioDisplayInfo[i].isAudioCapablePannel == true)
                {
                    NoOfAudCapableDispalys++;
                }
            }

            //Check Audio endpoint count in playback device vs actual audio capable displays 
            if ((base.MachineInfo.PlatformDetails.Platform == Platform.BDW))
            {
                if (_audioInputSource == AudioInputSource.Single)

                    if ((currentDisplayConfig.ConfigType == DisplayConfigType.SD) && (currentDisplayConfig.PrimaryDisplay == base.GetInternalDisplay()))
                    {
                        if (argAudioEndpointData.ListAudioEndpointDevice.Count == 0)
                        {
                            Log.Success("Enumurated audio endpoint and attached audio capable display is matching");
                        }
                        else
                            Log.Fail("Enumurated audio endpoint and attached audio capable display is not matching");

                    }
                    else
                    {


                        if (argAudioEndpointData.ListAudioEndpointDevice.Count == 1)
                        {
                            Log.Success("Enumurated audio endpoint and attached audio capable display is matching");
                        }
                        else
                            Log.Fail("Enumurated audio endpoint and attached audio capable display is not matching");
                    }
                else
                {
                    if (argAudioEndpointData.ListAudioEndpointDevice.Count == NoOfAudCapableDispalys)
                        Log.Success("Enumurated audio endpoint and attached audio capable display is matching");

                    else
                        Log.Fail("Enumurated audio endpoint and attached audio capable display is not matching");
                }
            }
            else
            {
                if (argAudioEndpointData.ListAudioEndpointDevice.Count != NoOfAudCapableDispalys)
                    Log.Fail("Enumurated audio endpoint and attached audio capable display is not matching");
                else
                    Log.Success("Enumurated audio endpoint and attached audio capable display is matching");
            }

            if (_audioInputSource == AudioInputSource.Single && currentDisplayConfig.ConfigType == DisplayConfigType.SD && currentDisplayConfig.PrimaryDisplay == base.GetInternalDisplay())
            {
                Log.Message("Current display config is {0}, not checking audio enumeration", currentDisplayConfig.GetCurrentConfigStr());
                return;
            }

            VerifyAudioDriverStatus();

            Log.Message("Verify AUD MMIO");
            //verify aduio endpoints
            if (_audioInputSource == AudioInputSource.Single && (DisplayExtensions.AudioWTVideoEnable == false && DisplayExtensions.EnableMonitorTurnOff == true) &&
                    argAudioEndpointData.ListAudioEndpointDevice.Count != 1 && currentDisplayConfig.ConfigType != DisplayConfigType.TED)
            {
                Log.Fail("Single source audio endpoint enumeration is not as expected");
                Log.Message("Current audio endpoint device are {0} ", argAudioEndpointData.GetCurrentAudioEndpointDevice());
            }
            else if (_audioInputSource == AudioInputSource.Multiple && argAudioEndpointData.ActiveAudioEndpointDevice == argAudioEndpointData.MaxSupportedAudioEndpoint &&
                      currentDisplayConfig.ConfigType == DisplayConfigType.TED && (DisplayExtensions.AudioWTVideoEnable == false && DisplayExtensions.EnableMonitorTurnOff == true) &&
                        argAudioEndpointData.ListAudioEndpointDevice.Count != argAudioEndpointData.MaxSupportedAudioEndpoint)
            {
                Log.Fail("Multi source audio config end point enumeration are not as expected");
                Log.Message("Current audio endpoint device are {0} ", argAudioEndpointData.GetCurrentAudioEndpointDevice());
            }

            else
                Log.Success("Audio endpoint enumeration are as expected");
            Log.Message("AUD_PIN_ELD_CP_VLD Register Value is {0}", argAudioEndpointData.ListAudioDisplayInfo[0].AUD_PIN_ELD_Reg_Value);
            Log.Verbose("Checking Audio register ELD, CP, PD bit are programed correctly or not");

            foreach (AudioDisplayInfo auxDispInfo in argAudioEndpointData.ListAudioDisplayInfo)
            {
                if (!auxDispInfo.isValidRegisterEntry)
                {
                    Log.Fail("Registers are not programed correctly for {0} -> {1}, expected is {2} and actual value is {3}",
                        auxDispInfo.dispType, auxDispInfo.planeInfo, auxDispInfo.expectedRegValue, auxDispInfo.PlaneRegValue);
                    SUCCESS = SUCCESS & false;
                }
            }
            

            // LPSP Verificaiton 
             if(base.MachineInfo.PlatformDetails.Platform != Platform.CHV)
            {

            bool lpspStatus = VerifyRegisters(LPSP_REGISTER_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA, false);
            if (currentDisplayConfig.PrimaryDisplay == base.GetInternalDisplay() && currentDisplayConfig.ConfigType == DisplayConfigType.SD)
                if (lpspStatus == true)
                    Log.Success("LPSP verification success.");
                else
                    Log.Fail("LPSP verification Fail.");

            else
            {
                if (lpspStatus == false)
                    Log.Success("LPSP verification success.");
                else
                    Log.Fail("LPSP verification Failed;");
            }
             }

                //Verify audio bit 
             if (currentDisplayConfig.PrimaryDisplay == base.GetInternalDisplay() && currentDisplayConfig.ConfigType != DisplayConfigType.SD)
             {
                    SUCCESS = VerifyRegisters("AUDIO_PW", PIPE.NONE, PLANE.NONE, PORT.PORTA, false);
                    if (SUCCESS)
                        Log.Success("ox65f10, Registers are programed correctly for all active display");
                    else
                        Log.Fail("Registers are not programed correctly for all active display");
                }
            }


        protected void StartLog()
        {
            //Clean the exicist log files
            Log.Message("Clean old logs ");
            File.Delete(@"Disp_Log.etl");
            Log.Message("Del sucessfully Disp_Log.etl");
            File.Delete(@"ParsLog.txt");
            Log.Message("Del sucessfully ParsLog.txt");
            File.Delete(@"Log.txt");
            Log.Message("Del sucessfully Log.txt");


            //Strat Collecting the ETL file
            Log.Message("Starting Log Message in Disp_Log.etl");
            ProcessStartInfo etl = new ProcessStartInfo();
            string filename = "SB_trace_collector.bat";
            Log.Message("file name{0}",filename);
            string arguments = "Disp_Log.etl";
            etl = new ProcessStartInfo(filename, arguments);
            etl.RedirectStandardOutput = true;
            etl.CreateNoWindow = true;
            etl.UseShellExecute = false;
            Process.Start(etl);
            Log.Message("log started ...........");

            Thread.Sleep(1000);
        }

        internal CurrentDisp Displaytopology()
        {
            CurrentDisp status = CurrentDisp.Internal;
            DisplayConfig currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);

            if (currentDisplayConfig.ConfigType == DisplayConfigType.SD && currentDisplayConfig.PrimaryDisplay == base.GetInternalDisplay())
            {
                status= CurrentDisp.Internal;
            }
            else
                status=CurrentDisp.External;

            return status;
        }
        protected void StopLog()
        {
            //Stop ETL trace Log
            Log.Message("Stopping the Log message of Disp_Log.etl");
            Process Proc = null;
            Proc = new Process();
            Proc.StartInfo.FileName = "Stop_log.bat";
            Proc.StartInfo.CreateNoWindow = true;
            Proc.Start();
            Proc.WaitForExit();
            Thread.Sleep(1000);
            Log.Message("Disp_Log.etl Log Saved Sucessfully");
            Thread.Sleep(1000);
            Log.Message("Please wait while converting the Disp_Log.ETL file into Log.txt file");
            GenerateLog();
            Thread.Sleep(1000);
            Log.Message("Text file created sucessfully");
            ParseLog();
            Thread.Sleep(1000);
        }
         void GenerateLog()
        {
            //Convert the ETL file into txt file
            ProcessStartInfo Log = new ProcessStartInfo();
            string LogFileName = "Traceview.exe";
            string LogArg = "-process Disp_Log.etl -pdb igdkmd64.pdb -o Log.txt";
            Log = new ProcessStartInfo(LogFileName, LogArg);
            Log.RedirectStandardOutput = true;
            Log.CreateNoWindow = true;
            Log.UseShellExecute = false;
            Process processLog = Process.Start(Log);
            Thread.Sleep(1000);
            Enter();
            processLog.WaitForExit();
            Thread.Sleep(1000);

        }
        void ParseLog()
        {
            //Parse the test file into only audio Log
            int counter = 0;
            string line;
            IEnumerable<string> allLine;
            string Filepath = @"Log.txt";
            Log.Message(" Parsing audio data from log.txt");

          //  if (File.Exists(Filepath))
            {
                allLine = File.ReadLines(Filepath);
                StreamReader file = new StreamReader("Log.txt");
                TextWriter outfile = new StreamWriter("ParsLog.txt");
                Log.Message("Please wait while comparing the log");
                Thread.Sleep(3000);
                while ((line = file.ReadLine()) != null)
                {
                    if ((line.Contains("NotifyPowerWellChange called:: bEnable")) ||
                        (line.Contains("Power well OFF")) ||
                        (line.Contains("Power well ON")) ||
                        (line.Contains("Restore Byte0")) ||
                        (line.Contains("restore verb")) ||
                        (line.Contains("HSWHDMICONTROLLER_SetAudioInactive")) ||
                        (line.Contains("HSWHDMICONTROLLER_SetAudioPresence")) ||
                        (line.Contains("HSWHDMICONTROLLER_EnableEld")) ||
                        (line.Contains("HSWHDMICONTROLLER_SetCPReady")) ||
                        (line.Contains("CODEC:GEN9HDMICONTROLLER_NotifyPowerWellChange: PG2")))
                    {
                        int i = line.IndexOf("SoftBios");
                        string txt = line.Substring(line.IndexOf("SoftBios"));
                        outfile.WriteLine(txt + "\r\n");
                    }
                    counter++;
                }
                outfile.Close();
                file.Close();
                Log.Message(" Parsing only audio log from full log file task completed Successfully");
                Thread.Sleep(1000);
            }
        }

        internal Boolean IsPDBpresent()
        {
            string Filepath = @"igdkmd64.pdb";
            string SorceFile = @"C:\Driver\Gfxinstaller\Release\pdb\igdkmd64.pdb";
            if ((base.MachineInfo.PlatformDetails.Platform != Platform.HSW) || (base.MachineInfo.PlatformDetails.Platform != Platform.BDW) || (base.MachineInfo.PlatformDetails.Platform != Platform.BXT) || (base.MachineInfo.PlatformDetails.Platform != Platform.CHV))
            {
                if (File.Exists(Filepath))
                    return true;
                else
                {
                    string fileName = "igdkmd64.pdb";
                    string sourcePath = @"C:\Driver\Gfxinstaller\Release\pdb";
                    if (File.Exists(SorceFile))
                    {
                        string targetPath = Directory.GetCurrentDirectory();
                        string destFile = Path.Combine(targetPath, fileName);
                        string sourceFile = Path.Combine(sourcePath, fileName);

                        System.IO.File.Copy(sourceFile, destFile, true);

                        if (File.Exists(Filepath))
                            return true;
                    }
                }
            }
                return false;

           
        }
        internal PWR_Status VerifyPWRSequence()
        {
            PWR_On = 0;
            PWR_Off = 0;
            //Log.Message(true, "Verifying audio POWERWELL sequence");
            Log.Success("PowerWELL Sequence Verification Started");
            string line;
            PWR_Status Status = PWR_Status.No_PWR_Change;
            IEnumerable<string> allLine;

            //Log file is the one converted from ETL trace Log
            string Filepath = @"ParsLog.txt";
            if (File.Exists(Filepath))
            {
                allLine = File.ReadLines(Filepath);
                StreamReader file = new StreamReader("ParsLog.txt");
                Thread.Sleep(3000);
                while ((line = file.ReadLine()) != null)
                {
                    //Check for PWR OFF log 
                    if ((line.Contains("SoftBios]NotifyPowerWellChange called:: bEnable 0")))
                    {
                        if (Status == PWR_Status.PWR_OFF)
                            Log.Fail("Redundant PWR OFF Occurred");

                        Status = PWR_Status.PWR_OFF;
                        PWR_Off++;
                        Log.Message(" PWR OFF Occurred");
                    }

                    //Check for PWR ON log 
                    if ((line.Contains("SoftBios]NotifyPowerWellChange called:: bEnable 1")))
                    {
                        if (Status == PWR_Status.PWR_ON)
                            Log.Fail("Redundant PWR ON Occurred");
                        
                        Status = PWR_Status.PWR_ON;
                        PWR_On++;
                        Log.Message(" PWR ON Occurred");
                    }

                    if ((line.Contains("PG2 ON notification failed")))
                    {
                        Log.Fail("PowerWELL2 ON notification failed ");
                    }
                    if ((line.Contains("PG2 OFF notification failed")))
                    {
                        Log.Fail("PowerWELL2 OFF notification failed ");
                    }

                }
                file.Close();
                Thread.Sleep(1000);
            }
            Log.Success("PowerWELL Sequence Verification completed");

            return Status;
        }

        internal void GetAUDBitCount()
        {
            Log.Message("Verifying audio bit sequence");
            eSet = 0; eReset = 0; IAset = 0; PDset = 0; CPset = 0; IAreset = 0; PDreset = 0; CPreset = 0;
            string line;
            IEnumerable<string> allLine;

            //Count the audio bits
            string Filepath = @"ParsLog.txt";
            //if (File.Exists(Filepath))
            {
                allLine = File.ReadLines(Filepath);
                StreamReader file = new StreamReader("ParsLog.txt");
                Thread.Sleep(3000);

                while ((line = file.ReadLine()) != null)
                {
                    if (line.Contains("HSWHDMICONTROLLER_EnableEld") && line.Contains("Value: 1"))
                        eSet++;
                    if (line.Contains("HSWHDMICONTROLLER_EnableEld") && line.Contains("Value: 0"))
                        eReset++;
                    if (line.Contains("HSWHDMICONTROLLER_SetAudioPresence") && line.Contains("Value: 1"))
                        PDset++;
                    if (line.Contains("HSWHDMICONTROLLER_SetAudioPresence") && line.Contains("Value: 0"))
                        PDreset++;
                    if (line.Contains("HSWHDMICONTROLLER_SetAudioInactive") && line.Contains("Value: 1"))
                        IAset++;
                    if (line.Contains("HSWHDMICONTROLLER_SetAudioInactive") && line.Contains("Value: 0"))
                        IAreset++;
                    if (line.Contains("HSWHDMICONTROLLER_SetCPReady") && line.Contains("Value: 1"))
                        CPset++;
                    if (line.Contains("HSWHDMICONTROLLER_SetCPReady") && line.Contains("Value: 0"))
                        CPreset++;
                }
                file.Close();
            }
        }

        internal void VerifyAUDseq_Plug()
        {
            GetAUDBitCount();
            Log.Message("Verifying audio bit sequence");
            Log.Message("Plug Bit sequence verification started");

            //Check ELD bit while hot plug
            if (eSet != 1)
                Log.Fail("Eld Bit not set or updated multiple times");
            if (eReset != 0)
                Log.Fail("Eldv reset should not happen during Hot plug");

            //check PD bit
            if (PDset != 1)
                Log.Fail("PD bit multiple times get set or not set PD bit");
            if (PDreset != 0)
                Log.Message("PD bit reset should not happen while Hot Plug the display");

            //IA 
            if (IAreset != 1)
                Log.Fail("IA Bit reset happen multiple times or not set");
            if (IAset != 0)
                Log.Fail("IA bit set should not happen during Hotplug");

            //CP-Ready
            if (CPset != 1)
                Log.Fail("CP-Ready updated multiple times or not updated");
            if (CPreset != 0)
                Log.Message("CP-Ready bit reset should not happen while Hot Plug the display");

            Log.Success("Hot Plug AUD Bit sequence verifiicaton completed");
        }

        internal void VerifyAUDseq_UnPlug()
        {
            GetAUDBitCount();
            Log.Message("Verifying audio bit sequence");

            //check eld bit
            if (eReset != 1)
                Log.Fail("Eld Bit is not reset or reseted multiple times");
            if (eSet != 0)
                Log.Fail("ELD set should not happen during Hot plug");

            //check PD bit
            if (PDreset != 1)
                Log.Fail("PD bit updated multiple times or PD reset did not happen");
            if (PDset != 0)
                Log.Fail("PD bit set should not happen while unpluging the display");


            //IA 
            if (IAset != 1)
                Log.Fail("IA Bit reset updated multiple times or not updated ");
            if (IAreset != 0)
                Log.Fail("IA reset should not happen during unplug");


            //CP-Ready
            if (CPreset != 1)
                Log.Fail("CP-Ready updated multiple times or not updated");
            if (CPset != 0)
                Log.Fail("CP-Ready reset did not happened ");

            Log.Success("Unplug AUD Bit sequence verification completed");
        }

        internal void VerifyAUDseq_PWREvent(int Disp)
        {
            GetAUDBitCount();
            Log.Message("Verifying audio bit sequence");

            //check eld bit
            if ((eSet != Disp))
                Log.Fail("Eld Bit is not set correctly");
            if (eReset != Disp)
                Log.Fail("Eldv reset not happened correctly");

            //check PD bit
            if (PDset != Disp)
                Log.Fail("PD bit not updated properly");
            if (PDreset != Disp)
                Log.Fail("PD bit reset should not happen");


            //IA 
            if (IAreset != Disp)
                Log.Fail("IA Bit not resetted correctly");
            if (IAset != Disp)
                Log.Fail("IA set should not happen in S3");

            //CP-Ready
            if (CPset != Disp)
                Log.Fail("CP-Ready not updated correctly");
            if (CPreset != Disp)
                Log.Fail("CP-Ready reset should not happen in S3 ");

            Log.Success("Power Event AUD Bit sequence verifcaton completed");
        }

        internal void VerifyAUDseq_DispSwitchEvent(int reset, int set)
        {
            GetAUDBitCount();
            Log.Message("Verifying audio bit sequence");

            //check eld bit
            if ((eSet != set))
                Log.Fail("Eld Bit is not updated or updated multiple times");
            if (eReset != reset)
                Log.Fail("Eldv reset should not happen during Hot plug");

            //check PD bit
            if (PDset != set)
                Log.Fail("PD bit not updated properly");
            if (PDreset != reset)
                Log.Fail("PD bit reset should not happen");


            //IA 
            if (IAset != set)
                Log.Fail("IA Bit is not updated");
            if (IAreset != reset)
                Log.Fail("IA Bit is not updated");

            //CP-Ready
            if (CPset != set)
                Log.Fail("CP-Ready updated multiple times or not updated");
            if (CPreset != reset)
                Log.Fail("CP-Ready reset updated ");

            Log.Success("Power Event AUD Bit sequence verifcaton completed");

        }

        public static void Enter()
        {
            SendKeys.SendWait("~");
            // Thread.Sleep(8000);
        }

        internal void AUDseq_Modeset()
        {
            PWR_Status PWRchange;
            Log.Message("Verifying audio bit sequence");

           // PWRchange = VerifyPWRSequence();
            //if (PWRchange == PWR_Status.No_PWR_Change)
            //    Log.Message("PWR Sequence is correct");
            //else
            //    Log.Fail("PWR Sequence is not correct");

            GetAUDBitCount();

            //check ELD bit
            if ((eSet != 1))
                Log.Fail("Eld Bit is not updated or updated multiple times");
            if (eReset != 1)
                Log.Fail("Eldv reset updated multiple times or not reseted");

            //check PD bit
            if (PDset != 1)
                Log.Fail("PD Bit set did not happen or set happened multiple times");
            if (PDreset != 0)
                Log.Fail("PD bit reset should not happen in modeset");

            //IA 
            if (IAreset != 1)
                Log.Fail("IA Bit updated multiple times or not updated");
            if (IAset != 0)
                Log.Fail("IA set should not happen during modeset");

            //CP-Ready
            if ((CPset != 1))
                Log.Fail("CP-Ready Bit updated multiple times or not updated");
            if (CPreset != 0)
                Log.Fail("CP-Ready reset should not happen in modeset");

            Log.Success("Modeset AUD Bit sequence verification completed");
        }

        internal int Get_current_Config()
        {
            int Ext_Disp = 0;
            if ((CurrentConfig.PrimaryDisplay.ToString() == "HDMI") || (CurrentConfig.PrimaryDisplay.ToString() == "DP"))
            {
                Ext_Disp++;
            }
            if ((CurrentConfig.SecondaryDisplay.ToString() == "HDMI") || (CurrentConfig.SecondaryDisplay.ToString() == "DP"))
            {
                Ext_Disp++;
            }
            if ((CurrentConfig.TertiaryDisplay.ToString() == "HDMI") || (CurrentConfig.TertiaryDisplay.ToString() == "DP"))
            {
                Ext_Disp++;
            }
            return Ext_Disp;
        }


        internal bool GetLPSPEnableStatus()
        {
            DisplayConfig currentDisplayConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            if (currentDisplayConfig.ConfigType == DisplayConfigType.SD && currentDisplayConfig.PrimaryDisplay == base.GetInternalDisplay())
            {
                DisplayInfo currentDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).First();
                DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, currentDispInfo);
                if (GetModeStr(currentDispInfo.DisplayMode).Equals(GetModeStr(currentMode)))
                {
                    Log.Message(true, "Verify LPSP Registers for Native mode for paltform {0}", base.MachineInfo.PlatformDetails.Platform.ToString());
                    if (LPSPPlatform())
                        return true;
                }
                else
                {
                    Log.Message(true, "Verify LPSP Registers for Non Native mode for paltform {0}", base.MachineInfo.PlatformDetails.Platform.ToString());
                    if (LPSPPlatform())
                        return true;
                }
            }
            Log.Message(true, "Verify LPSP Registers for non SD EDP config  for paltform {0}", base.MachineInfo.PlatformDetails.Platform.ToString());
            return false;
        }

        private bool LPSPPlatform()
        {
            Platform plat;
            Enum.TryParse<Platform>(base.MachineInfo.PlatformDetails.Platform.ToString(), true, out plat);
            switch (plat)
            {
                case Platform.HSW:
                case Platform.IVBM:
                case Platform.VLV:
                case Platform.CHV:
                    return false;
                default:
                    return true;
            }
        }

        internal string GetModeStrX(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes, "x", argMode.RR, argMode.InterlacedFlag.Equals(0) ? "p Hz" : "i Hz", "x", argMode.Bpp);
        }

        private string GetModeStr(DisplayMode argMode)
        {
            return string.Concat(argMode.HzRes, "x", argMode.VtRes);
        }

        internal AudioMMDeviceData GetDefaultEndPoint()
        {
            AudioMMDeviceData defaultEndpoint = new AudioMMDeviceData();
            if (_audioEndpointData.ListAudioEndpointDevice.Count == 0)
            {
                defaultEndpoint.FriendlyName = "NULL";
                defaultEndpoint.ID = "NULL";
                defaultEndpoint.State = EDeviceState.DEVICE_STATE_NOTPRESENT;
                return defaultEndpoint;
            }
            return AccessInterface.GetFeature<AudioMMDeviceData>(Features.AudioEnumeration, Action.Get, Source.AccessAPI);
        }
        protected void LPSPRegisterVerify(bool pEnable)
        {
            if (VerifyRegisters(LPSP_REGISTER_EVENT, PIPE.NONE, PLANE.NONE, PORT.PORTA, false))
            {
                if (pEnable)
                    Log.Success("LPSP is Enable");
                else
                    Log.Fail("LPSP is Enable");
            }
            else
            {
                if (!pEnable)
                    Log.Success("LPSP is Disable");
                else
                    Log.Fail("LPSP is Disable");
            }
        }

        internal List<DisplayConfig> GetSwitchSequence()
        {
            List<DisplayConfig> switchPatternList = new List<DisplayConfig>();
            int dispFetchKey = base.CurrentConfig.CustomDisplayList.Count;
            int dispByPlatform = base.MachineInfo.PlatformDetails.Platform.GetDisplaysCount();
            if (dispFetchKey > dispByPlatform)
                dispFetchKey = dispByPlatform;
            SwitchPatternList[dispFetchKey](switchPatternList);
            return switchPatternList;
        }

        private Dictionary<int, Action<List<DisplayConfig>>> SwitchPatternList
        {
            get
            {
                Dictionary<int, Action<List<DisplayConfig>>> _switchPatternList = null;
                if (null == _switchPatternList)
                {
                    _switchPatternList = new Dictionary<int, Action<List<DisplayConfig>>>();
                    _switchPatternList.Add(2, this.GetSwitchPatternForDualDisplayMode);
                    _switchPatternList.Add(3, this.GetSwitchPatternForTriDisplayMode);
                }
                return _switchPatternList;
            }
        }

        private void GetSwitchPatternForDualDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for DualDisplay Mode");
            DisplayConfig displayWrapper = null;

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);
        }
        private void GetSwitchPatternForTriDisplayMode(List<DisplayConfig> argList)
        {
            Log.Verbose("Preparing Switch Pattern for TriDisplay Mode");
            DisplayConfig displayWrapper = null;

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
            argList.Add(displayWrapper);

            displayWrapper = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
            argList.Add(displayWrapper);
        }


        internal List<DisplayMode> TestModeslist(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            List<DisplayMode> interlacedModeList = displayModeList.FindAll(DT => DT.InterlacedFlag.Equals(1));
            if (interlacedModeList.Count != 0)
                testModes.Add(interlacedModeList.First());
            testModes.Add(displayModeList.Last());
            return testModes;
        }

        internal bool ApplyAndVerify(DisplayMode argDispMode)
        {
            Log.Message("Setting Mode : {0} for {1}", argDispMode.ToString(), argDispMode.display);

            if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
            {
                Log.Fail("Fail to apply Mode");
                return false;
            }
            else
            {
                Log.Success("Mode applied successfully");
                Log.Message("Fetching Audio endpoint data");
                //StopLog();

                CheckAudioEndPoint(AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI));
                Log.Verbose("Default audio endpoint device {0}", GetDefaultEndPoint().FriendlyName);
                //AUDseq_Modeset();
                return true;
            }
        }
    }
}
