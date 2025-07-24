using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;


namespace Intel.VPG.Display.Automation
{

       class SB_HDR_Base : TestBase
    {

        protected string _HDRMetadataEvent = "HDR_METADATA";
        protected string _HDR_Verification30 = "HDR_4K2K@30COLOR";
        protected string _HDR_Verification60 = "HDR_4K2K@60COLOR";
        protected string _HDR_BPC10 = "HDR_PIPE_BPC_10";
        protected string _HDR_BPC12 = "HDR_PIPE_BPC_12";
        protected string _HDR_CSCCoeff = "HDR_CSCCOEFF";
        protected string _HDR_CSCPOSTOFF = "HDR_CSCPOSTOFF";
        
        protected List<uint> metadataHW = null;
        protected List<uint> RegsHW = null;
        protected List<uint> metadataFile = null;
        protected List<uint> CSCCoeff = null;
        protected List<uint> CSCPostOff = null;

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {

            Log.Message(true, "Checking Preconditions and Plugging in HDR supported panel");
            if (!base.CurrentConfig.DisplayList.Contains(DisplayType.DP))
                Log.Abort("DP not passed in command line...Aborting the test");

        }
        
        protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
            {
                Log.Success("Mode applied Successfully");
            }
            else
                Log.Fail("Fail to apply Mode");
        }

        protected void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the  mode  for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
                CheckWatermark(argDisplayType);
              
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }

        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }

        public virtual void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
                
            }
            else
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
        }
        protected void InstallDirectX()
        {
            if (Directory.Exists(@"C:\Program Files (x86)\Microsoft DirectX SDK (June 2010)") || (Directory.Exists(@"C:\Program Files\Microsoft DirectX SDK (June 2010)")))
            {
                Log.Message("DirectX is installed");
            }
            else
            {
                Log.Message("Installing DirectX SDK. Do not touch any UI buttons.");
                Process p = Process.Start(base.ApplicationManager.ApplicationSettings.DirectX, "/U");
                p.WaitForExit();
                Log.Message("Installion of  DirectX SDK was successfull");
            }
        }

        protected void LaunchMDAPlayer()
        {
            Log.Verbose("Launching MDA player in fullscreen mode.");
            string imagePath = String.Concat(base.ApplicationManager.ApplicationSettings.DisplayToolsPath, "\\HDR\\MDA\\fixed_nits_grayscale_3840x2160_64_940_1350f.h265"); 
            string argument = string.Format("--hevc --reorder --disp --dxvahd --fps ntsc -i {0} --excl --hdepth",imagePath);
            string executable = String.Concat(base.ApplicationManager.ApplicationSettings.DisplayToolsPath, "\\HDR\\MDA\\mv_decoder_adv.exe"); 
            Log.Message("Command is: " + argument);
            Process.Start(executable, argument);
        }

        protected void LaunchTenPlayerFullScreen(DisplayType dispType , string ImageFile , string MetadataFile , uint bpc)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == dispType).First();
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.TenPlayerHDR);
            driverParams.display = dispType;
            driverParams.currentConfig = base.CurrentConfig;
            driverParams.displayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            driverParams.BPC = bpc;
            driverParams.ImageFilePath = base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\HDR\\Images\\" + ImageFile + ".bmp";
            driverParams.MetadataFilePath = base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\HDR\\Metadata\\" + MetadataFile + ".txt";

            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Abort("Failed to launch Tenplayer.");

        }

        protected void CloseTenPlayerFullScreen()
        {
            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop);

            driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop);
            if (!AccessInterface.SetFeature<bool, SetUpDesktopArgs>(Features.SetUpDesktop, Action.SetMethod, driverParams))
                Log.Fail("Failed to close Tenplayer");
        }

        protected bool ParseHDRLog() 
        {
            bool returnStatus = false;
            using (var file = File.OpenText("C:\\Intel\\tenplayerlog.txt"))  // location
            {
                string line = "";
                while ((line = file.ReadLine()) != null)
                {
                    if (line.ToLower().CompareTo("hdr log") == 0)
                    {
                        string hdrStatus = "";
                        hdrStatus = file.ReadLine();

                        if(hdrStatus.ToLower().CompareTo("hdr passed") == 0)
                        {
                            Log.Message("HDR : Get and Set escape calls passed");
                            returnStatus = true;
                        }
                        else if (hdrStatus.ToLower().CompareTo("hdr failed") == 0)
                        {
                            Log.Message("HDR : Get and Set escape calls failed !!! ");
                            string failureCode = "";
                            failureCode = file.ReadLine();
                            Log.Message("GetCaps failure {0}", failureCode);
                        }
                        
                        break;
                    }
                    else
                        continue;
                }
            }

            return returnStatus;
        }


        protected void  ValidateColorRegistersProgramming(string pRegisterEvent , DisplayType argDispType)
        {
            Log.Message(true, "Verifying CSC,Gamma programming for {0}", argDispType);
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            if (VerifyRegisters(pRegisterEvent, PIPE.NONE, pipePlane1.Plane, PORT.NONE))
            {
                Log.Success("HDR color registers verified successfully for  {0}", argDispType);
            }
            else
            {
                Log.Fail("HDR color registers mismatch for {0}", argDispType);
            }


        }

        protected void ValidateBPCProgramming(string pRegisterEvent , DisplayType argDispType)
        {
            Log.Message(true, "Verifying BPC programming for {0}", argDispType);
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            if (VerifyRegisters(pRegisterEvent, pipePlane1.Pipe, PLANE.NONE, PORT.NONE))
            {
                Log.Success("BPC registers verified successfully for  {0}", argDispType);
            }
            else
            {
                Log.Fail("BPC registers mismatch for {0}", argDispType);
            }
        }


        protected bool VerifyRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort, bool compare = true)
        {
            Log.Message("Verifying Register for event : {0}", pRegisterEvent);
            bool regValueMatched = true;

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    if (compare)
                    {
                        if (!CompareRegisters(driverData.output, reginfo))
                        {
                            Log.Message("Register with offset {0} doesnot match required values", reginfo.Offset);
                            regValueMatched = false;
                        }
                    }
            }

            return regValueMatched;
        }

        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            Log.Verbose("Bitmap in uint = {0}, Value from register read = {1}", bit, argDriverData);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            Log.Verbose("value from reg read in ubit = {0}", hex);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            if (String.Equals(valu, argRegInfo.Value))
            {
                Log.Message("Register Values Matched");
                return true;
            }
            return false;
        }
        
        protected void ValidateMetadata(string inputFile)
        {
                   
            bool result = true;
                    // Read the VSC packet registers from H/W                    
                    FetchMetadataFromHWRegisters(DisplayType.DP);

                    // Parsing the metadatafile 
                    ParseInputMetadataFile(inputFile);

                    if (metadataFile.Count != metadataHW.Count)
                    {
                        Log.Fail("Mismatch in the metadata list size File :{0} ,HW :{1}", metadataFile.Count, metadataHW.Count);
                        result = false;
                    }
                    else
                    {
                        Log.Message("Metadata Count : {0}", metadataFile.Count);
                        for (int i = 0; i < metadataFile.Count; i++) // Loop with for.
                        {
                            if (metadataFile[i].CompareTo(metadataHW[i]) != 0)
                            {
                                Log.Fail("Input and Register metadata not matching at index {0} I/p Value - {1}  HW Reg Value - {2} ", i, metadataFile[i], metadataHW[i]);
                                result = false;
                            }
                        }

                    }

                    if (result == true)
                        Log.Success("HDR metadata matched !!");
            
        
        }

         protected void FetchMetadataFromHWRegisters( DisplayType argDispType)
        {
            metadataHW = new List<uint>();
            Log.Message(true, "Verifying HDR Metadata for {0}", argDispType);
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            if (ReadMetadataRegisters(_HDRMetadataEvent, pipePlane1.Pipe, PLANE.NONE, PORT.NONE))
            {
                Log.Success("HDR metadata register read successfully for  {0}", argDispType);
            }
            else
            {
                Log.Fail("HDR register reads failed for {0}", argDispType);
            }

            metadataHW.Add(RegsHW[0]); // Header 0x1D4C
            metadataHW.Add(GetValue(RegsHW[1], 16, 17)); // EOTF
            metadataHW.Add(GetValue(RegsHW[2], 0, 15)); // Disp X1
            metadataHW.Add(GetValue(RegsHW[2], 16, 31)); // Disp Y1
            metadataHW.Add(GetValue(RegsHW[3], 0, 15)); // Disp x2
            metadataHW.Add(GetValue(RegsHW[3], 16, 31)); // Disp y2
            metadataHW.Add(GetValue(RegsHW[4], 0, 15)); // Disp X3
            metadataHW.Add(GetValue(RegsHW[4], 16, 31)); // Disp y3
            metadataHW.Add(GetValue(RegsHW[5], 0, 15)); // white X
            metadataHW.Add(GetValue(RegsHW[5], 16, 31));  // white Y
            metadataHW.Add(GetValue(RegsHW[6], 0, 15)); // maxlum
            metadataHW.Add(GetValue(RegsHW[6], 16, 31)); // minlum
            metadataHW.Add(GetValue(RegsHW[7], 0, 15)); // maxCLL
            metadataHW.Add(GetValue(RegsHW[7], 16, 31)); // maxFALL
                      
        }


         protected bool ReadMetadataRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort, bool compare = true)
         {
             Log.Message("Verifying Register for event : {0}", pRegisterEvent);
             bool retVal = true;
             RegsHW = new List<uint>();

             EventInfo eventInfo = new EventInfo();
             eventInfo = new EventInfo();
             eventInfo.pipe = pPipe;
             eventInfo.plane = pPlane;
             eventInfo.port = pPort;
             eventInfo.eventName = pRegisterEvent;
             EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            
             uint MetadataBaseAddress = Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16);
             
             
             for (uint i = 0; i < 8; i++ )
             {
                
                 DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                 driverData.input = MetadataBaseAddress + ( i * 4);
                 DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                 if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                 {
                     Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                     retVal = false;
                     break;
                 }
                 else
                 {

                     RegsHW.Add(driverData.output);
                 }

                
             }

                 return retVal;
         }
         
        protected void ParseInputMetadataFile(string inputFile)
         {

             string DataFileName = base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\HDR\\Metadata\\" + inputFile + ".txt";
             metadataFile = new List<uint>();
             using (var file = File.OpenText(DataFileName))  // location
            {
                string line = "";
                metadataFile.Add((uint)0x4C1D8700); // Header
                while ((line = file.ReadLine()) != null)
                {
                    string[] parts = line.Split(':');
                    string key = parts[0];

                    key = key.ToLower();

                    string value = parts[1];

                    

                    if (key.CompareTo("eotf") == 0)
                        metadataFile.Add((uint)Convert.ToInt32(value));
                    else if (key.CompareTo("redx") == 0)
                       metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("redy") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("greenx") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("greeny") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("bluex") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("bluey") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("whitex") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("whitey") == 0)
                        metadataFile.Add((uint)Math.Round(Convert.ToDouble(value) * 50000.0));
                    else if (key.CompareTo("maxluminance") == 0)
                        metadataFile.Add((uint)Convert.ToInt32(value));
                    else if (key.CompareTo("minluminance") == 0)
                        metadataFile.Add((uint)Convert.ToInt32(value));
                    else if (key.CompareTo("maxcll") == 0)
                        metadataFile.Add((uint)Convert.ToInt32(value));
                    else if (key.CompareTo("maxfall") == 0)
                        metadataFile.Add((uint)Convert.ToInt32(value));
                     
                   
                }

            }

        }

        protected void ValidateCSCCoeff_PostOffsetRegisters( DisplayType argDispType)
        {

            List<uint> RegHW = new List<uint>();
            CSCCoeff = new List<uint>();
            CSCPostOff = new List<uint>();
           

            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            // CSC Coeff

            Log.Message("Verifying Register for event : {0}", _HDR_CSCCoeff);
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = pipePlane1.Plane;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = _HDR_CSCCoeff;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            uint BaseAddress = Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16);
         
            for (uint i = 0; i < 6; i++)
            {
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = BaseAddress + (i*4);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    RegHW.Add(driverData.output);
               
            }

            CSCCoeff.Add(GetValue(RegHW[0], 16, 31));
            CSCCoeff.Add(GetValue(RegHW[0], 0, 15));
            CSCCoeff.Add(GetValue(RegHW[1], 16, 31));
            CSCCoeff.Add(GetValue(RegHW[2], 16, 31));
            CSCCoeff.Add(GetValue(RegHW[2], 0, 15));
            CSCCoeff.Add(GetValue(RegHW[3], 16, 31));
            CSCCoeff.Add(GetValue(RegHW[4], 16, 31));
            CSCCoeff.Add(GetValue(RegHW[4], 0, 15));
            CSCCoeff.Add(GetValue(RegHW[5], 16, 31));

            
            for (int i = 0; i < 9; i++)
            {
                Log.Message("CSC Coeff Value {0} --> {1}" , (i+1), CSCCoeff[i] );
            }

            // CSC PostOffset

            Log.Message("Verifying Register for event : {0}", _HDR_CSCPOSTOFF);
            eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = pipePlane1.Plane;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = _HDR_CSCPOSTOFF;
            returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);


            BaseAddress = Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16);
          
            for (uint i = 0; i < 3; i++)
            {
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = BaseAddress + (i*4);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                {
                    Log.Message(" CSC PostOffset {0} : {1}", i, driverData.output);
                    CSCPostOff.Add(driverData.output);
                }
            }


        }

        protected void ValidateHDrReset(string pRegisterEvent, DisplayType argDispType)
        {
            bool result = true;
            Log.Message(true, "Verifying HDR to SDR reset for {0}", argDispType);
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipePlane1.Pipe;
            eventInfo.plane = PLANE.NONE;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            Log.Message("Count of reg : {0}", returnEventInfo.listRegisters.Count);
            uint MetadataBaseAddress = Convert.ToUInt32(returnEventInfo.listRegisters[0].Offset, 16);
            Log.Message("base address : {0}", returnEventInfo.listRegisters[0].Offset);
            
            for (uint i = 1; i < 8; i++)
            {
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = MetadataBaseAddress + (i * 4);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                {
                   if (i == 1)
                    {
                        if (GetValue(driverData.output, 16, 17) != 0)
                        {
                            Log.Fail("HDR metadata not cleared at {0} - Current value {1}", i, driverData.output);
                            result = false;
                        }
                    }
                    else
                    {
                        if (driverData.output != 0)
                        {
                            Log.Fail("HDR metadata not cleared at {0} - Current value {1}", i, driverData.output);
                            result = false;
                        }
                        
                    }
                }

               
            }

            if (result == true)
                Log.Success("The HDR metadata is reset successfully");
        }


        protected void ValidateDPCD(DisplayType display, bool isYUV420)
        {
            bool status;
            // +++++++ Colorimetry +++++++++++
            Log.Message("Verifying DPCD AVI infoframe values");

            RegisterInf regColorimetry = new RegisterInf("005C5", "000000C0", "C0");
            status = VerifyDPCDValue("005C5", regColorimetry, display);

            if (!status)
                Log.Fail("Colorimetry values mismatch !!");

            //++++++++++ExtCOlorimetry+++++++++++

            RegisterInf regExtColorimetry = new RegisterInf("005C6", "00000070", "60");
            RegisterInf regRGBQuantRange = new RegisterInf("00170", "0000000C", "0");
            status = VerifyDPCDValue("005C6", regExtColorimetry, display);
            if (!status)
                Log.Fail("ExtColorimetry values mismatch !!");

            status = VerifyDPCDValue("005C6", regRGBQuantRange, display);
            if (!status)
                Log.Fail("RGBQUantRange values mismatch !!");

            //++++++++++EncMode+++++++++++

            RegisterInf regEncMode;
            if (isYUV420)
                regEncMode = new RegisterInf("005C4", "000000E0", "60");
            else
                regEncMode = new RegisterInf("005C4", "000000E0", "0");
            status = VerifyDPCDValue("005C4", regEncMode, display);

            if (!status)
                Log.Fail("EncMode values mismatch !!");

        }

        protected bool VerifyDPCDValue(String offset, RegisterInf regCompare, DisplayType display)
        {
            uint regValue;
            bool status = false;
            DpcdInfo dpcd = new DpcdInfo();

            Log.Message("Reading value from offset" + offset);

            dpcd.Offset = Convert.ToUInt32(offset, 16);
            dpcd.DispInfo = base.EnumeratedDisplays.Find(dI => dI.DisplayType == display);
            regValue = AccessInterface.GetFeature<uint, DpcdInfo>(Features.DpcdRegister, Action.GetMethod, Source.AccessAPI, dpcd);

            

            if (CompareRegisters(regValue, regCompare))
                status = true;
            else
                Log.Fail("DPCD register verification Failed --> Actual :" + regValue + "Expected :" + regCompare.Value);

            return status;
        }


        protected void CRCComputation(DisplayType display)
        {
           
            Log.Message(true, "Verifying CRC for {0}", display);
                        
            CRCArgs obj = new CRCArgs();       
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
            obj.displayType = display;
            obj.port = displayInfo.Port ;
            obj.ComputePipeCRC = true;
            
            AccessInterface.GetFeature<CRCArgs,CRCArgs>(Features.CRC, Action.GetMethod, Source.AccessAPI, obj);
            
            uint PipeCRC = obj.CRCValue;

            CrcGoldenDataArgs obj1 = new CrcGoldenDataArgs();
            obj1.displayInfo = displayInfo;
            obj1.displayMode = AccessInterface.GetFeature<DisplayMode,DisplayInfo>(Features.Modes,Action.GetMethod,Source.AccessAPI,displayInfo);
            obj1.IsPipeCRC = true;
            obj1.IsHDRContent = true;
            obj1.IsHDREnable = true;

            AccessInterface.GetFeature<CrcGoldenDataArgs, CrcGoldenDataArgs>(Features.CrcGoldenData, Action.GetMethod, Source.AccessAPI, obj1);

            uint GoldenCRC = obj1.CRCValue;

            if (PipeCRC == 0 || GoldenCRC == 0)
                Log.Fail("CRC should not be zero. Expected:{0}, Current CRC:{1}.", GoldenCRC, PipeCRC);
            else
            {
                if (PipeCRC == GoldenCRC)
                {

                    Log.Success("CRC Matched for {0}", obj1.displayMode.GetCurrentModeStr(false));
                }
                else
                {
                    Log.Fail("CRC Not Matched. Expected:0x{0}, Current CRC:0x{1} for {2}: {3}", GoldenCRC.ToString("X"), PipeCRC.ToString("X"), display, obj1.displayMode.GetCurrentModeStr(false));
                }
             }
               
        }

        public static uint GetValue(uint value, int start, int end)
        {
            uint retvalue = value << (31 - end);
            retvalue >>= (31 - end + start);
            return retvalue;
        }
    }
}
