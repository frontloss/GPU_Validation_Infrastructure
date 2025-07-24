namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;

    class SB_PPC_Base : TestBase
    {
        private const string PIPE_HOR_SOURCE_SIZE = "PIPE_HOR_SOURCE_SIZE";
        private const string PIPE_VER_SOURCE_SIZE = "PIPE_VER_SOURCE_SIZE";
        private const string PF_INTERLACE_ENABLE = "PF_INTERLACE_ENABLE";
        private const string IS_AUDIO_96_BCLK = "IS_AUDIO_96_BCLK";

      
        public Dictionary<Platform, List<double>> PlatformCDClock
        {
            get
            {
                Dictionary<Platform, List<double>> platCDClock = new Dictionary<Platform, List<double>>()
                { 
                     {Platform.CNL,new List<double>(){168,336,528}},
                     {Platform.GLK,new List<double>(){79.2,158.4,316.8}}
                };

                return platCDClock;
            }
        }

      
        public Dictionary<Platform, List<string>> GenericPlanes
        {
            get
            {
                Dictionary<Platform, List<string>> planes = new Dictionary<Platform, List<string>>()
                { 
                     {Platform.CNL,new List<string>(){"PLANE_1","PLANE_2", "PLANE_3", "PLANE_4"}},
                     {Platform.GLK,new List<string>(){"PLANE_1","PLANE_2", "PLANE_3", "PLANE_4"}}
                };

                return planes;
            }
        }

      
        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());  
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
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }

        protected List<DisplayModeList> GetAllModes(List<DisplayType> argCustomDisplayList)
        {
            List<DisplayModeList> listDisplayMode = new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argCustomDisplayList);
            List<DisplayMode> commonModes = null;

            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                commonModes = allModeList.Where(dML => dML.display == base.CurrentConfig.PrimaryDisplay).Select(dML => dML.supportedModes).FirstOrDefault();
                allModeList.Skip(1).ToList().ForEach(dML => commonModes = commonModes.Intersect(dML.supportedModes, new DisplayMode()).ToList());
                if (commonModes.Count() > 0)
                    listDisplayMode.Add(new DisplayModeList() { display = base.CurrentConfig.PrimaryDisplay, supportedModes = commonModes });
            }
            else
                listDisplayMode = allModeList;
            return listDisplayMode;
        }

        protected void VerifyPPC()
        {
            bool status = true;
            List<double> possibleCDClocks = new List<double>();
            Log.Message(true, "Verify PPC");

            double currentCDClock = GetCurrentCDClock();

            if (currentCDClock == 0)
                Log.Fail("CD Clock should not be zero. Abort the test");
            else
            {
                foreach (DisplayType display in base.CurrentConfig.CustomDisplayList)
                {
                    List<double> tempCDClock = new List<double>();
                    bool tempStatus = CheckIfDrivenWithLowerCDClock(display, currentCDClock, ref tempCDClock);

                    if (tempStatus == true)
                    {
                        if (possibleCDClocks.Count == 0)
                            possibleCDClocks.AddRange(tempCDClock);
                        else
                        {
                            possibleCDClocks = possibleCDClocks.Intersect(tempCDClock).ToList();
                        }
                    }
                    else
                    {
                        status =false;
                    }
                }

                if (status != true)
                {
                    Log.Success("CD Clock:{0} was programmed as per expected.", currentCDClock);
                }
                else
                {
                    Log.Fail("CD Clock:{0} was programmed incorrectly. Can drive with lower CD Clock.", currentCDClock);
                    possibleCDClocks.ForEach(cdClock => Log.Message("Display can driven at CD Clock: {0}.", cdClock));
                }
            }

        }

        private bool CheckIfDrivenWithLowerCDClock(DisplayType display, double currentCDClock, ref List<double> possibleCDClocks)
        {
            double pipeRatio = 1;
            PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);

            Dictionary<SCALAR, SCALAR_MAP> ScalarMapper = new Dictionary<SCALAR, SCALAR_MAP>();
            foreach (SCALAR currScalar in Enum.GetValues(typeof(SCALAR)))
            {
                if (currScalar == SCALAR.NONE)
                    continue;

                string eventName = currScalar + "_Enable";
                if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE, false))
                {
                    //checking if plane scalar is enabled.
                    SCALAR_MAP tempScalar = SCALAR_MAP.NONE;
                    GetScalarBinding(display, pipePlaneObject, currScalar, false, ref tempScalar);
                    ScalarMapper.Add(currScalar, tempScalar);
                    Log.Verbose("{0} is enabled and mapped to {1} for {2}", currScalar, tempScalar, display);
                }
                else
                    Log.Verbose("{0} is not enabled for {1}", currScalar, display);
            }

            double xScaling = 0, yScaling = 0;
            foreach (KeyValuePair<SCALAR, SCALAR_MAP> currItem in ScalarMapper)
            {
                if (!(currItem.Value == SCALAR_MAP.NONE || currItem.Value == SCALAR_MAP.PIPE))
                {
                    string eventName = currItem.Key + "_Size";
                    uint plane_Size = GetRegisterValue(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
                    uint SrcSizeX = GetRegisterValue(plane_Size, 0, 12);
                    uint SrcSizeY = GetRegisterValue(plane_Size, 16, 27);

                    eventName = currItem.Key + "_Win_Size";
                    uint window_Size = GetRegisterValue(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
                    uint DestSizeX = GetRegisterValue(window_Size, 0, 12);
                    uint DestSizeY = GetRegisterValue(window_Size, 16, 29);

                    xScaling = Math.Min(1, SrcSizeX / DestSizeX);
                    yScaling = Math.Min(1, SrcSizeY / DestSizeY);

                    pipeRatio = Math.Min(pipeRatio, xScaling * yScaling);
                }
            }

            double hDownScaling = 0, vDownScaling = 0;
            foreach (KeyValuePair<SCALAR, SCALAR_MAP> currItem in ScalarMapper)
            {
                if (currItem.Value == SCALAR_MAP.PIPE)
                {
                    Log.Verbose("Pipe Scalar is enabled.");
                    uint SrcSizeX = GetRegisterValue(PIPE_HOR_SOURCE_SIZE, PIPE.NONE, pipePlaneParams.Plane, PORT.NONE);
                    SrcSizeX = GetRegisterValue(SrcSizeX, 16, 28);

                    uint SrcSizeY = GetRegisterValue(PIPE_VER_SOURCE_SIZE, PIPE.NONE, pipePlaneParams.Plane, PORT.NONE);

                    string eventName = currItem.Key + "_Win_Size";
                    uint window_Size = GetRegisterValue(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
                    uint DestSizeX = GetRegisterValue(window_Size, 0, 12);
                    uint DestSizeY = GetRegisterValue(window_Size, 16, 29);

                    hDownScaling = Math.Min(1, SrcSizeX / DestSizeX);
                    vDownScaling = Math.Min(1, SrcSizeY / DestSizeY);
                    double pipeDownScalingAmount = hDownScaling * vDownScaling;

                    pipeRatio = pipeRatio * pipeDownScalingAmount;
                    Log.Message(string.Format("Pipe Ratio is : {0}", pipeRatio));

                    bool PFInterlaced = VerifyRegisters(PF_INTERLACE_ENABLE, pipePlaneParams.Pipe, PLANE.NONE, PORT.NONE, false);
                    if (PFInterlaced == true)
                    {
                        pipeRatio *= 2;
                        Log.Message(string.Format("Pipe Ratio when Progressive Fetch - Interlace Display enabled : {0}", pipeRatio));
                    }
                    else
                    {
                        Log.Verbose("Progressive Fetch - Interlace Display  is not Enabled");
                    }
                }
            }

            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
            DisplayMode displayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

            double currentPixelClock = displayMode.pixelClock;
            Log.Verbose("Display {0} is driven at {1} Pixel Clock", display, currentPixelClock);

            List<double> SupportedCDClocksLess = PlatformCDClock[base.MachineInfo.PlatformDetails.Platform].Where(item => item < currentCDClock).ToList();
            
            SupportedCDClocksLess.ForEach(eachClock => Log.Verbose("Possible CD Clock which is less than currenly programmed is: {0}", eachClock));

            //CD Clock should be 2 * Audio BCLK clock ex: for 96MHz BCLK, 168 CD Clock is not supported.
            double audioBCLK = 48;
            bool IsAudio96MHz = VerifyRegisters(IS_AUDIO_96_BCLK, pipePlaneParams.Pipe, PLANE.PLANE_A, PORT.NONE, false);
            if (IsAudio96MHz == true)
            {
                audioBCLK = 96;
                Log.Message("Removing CD CLock's which doesn't satisfy CD Clock should be 2 * Audio BCLK clock.");
                SupportedCDClocksLess.RemoveAll(item => item < 2 * audioBCLK);
            }

            bool status = false;
            SupportedCDClocksLess.ForEach(eachClock => Log.Verbose("Possible CD Clock is {0}", eachClock));
            foreach (double item in SupportedCDClocksLess)
            {
                Log.Verbose("Checking if display can be driven with CD Clock {0}", item);
                if (currentPixelClock < (2 * item * pipeRatio))
                {
                    Log.Message("Display can be driven with CD Clock {0}", item);
                    possibleCDClocks.Add(item);
                    status |= true;
                }
                else
                {
                    Log.Verbose("Display can't be driven with CD Clock {0}", item);
                    status |= false;
                }
            }

            return status;
        }

        private bool GetScalarBinding(DisplayType display, PipePlaneParams pipePlaneObject, SCALAR currentScalar, bool IsPipeCall, ref SCALAR_MAP currentScalarMap)
        {
            bool status = true;
            string eventName = currentScalar.ToString() + "_Binding";
            uint scalarVal = GetRegisterValue(eventName, pipePlaneObject.Pipe, pipePlaneObject.Plane, PORT.NONE);
            currentScalarMap = (SCALAR_MAP)scalarVal;

            return status;
        }

        private double GetCurrentCDClock()
        {
            double currentCDClock = 0;

            PlatformCDClock[base.MachineInfo.PlatformDetails.Platform].ForEach(item =>
                {
                    string eventName="CDClock_"+item;
                    if (VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, PORT.NONE, false))
                    {
                        currentCDClock = item;
                    }
                });
            
            Log.Message("Display is driven at CD Clock: {0}", currentCDClock);

            return currentCDClock;

        }

        //private bool CheckIfScalarEnabled(DisplayType display, PipePlaneParams pipePlaneObject, GENERIC_PLANE gPlane, ref SCALAR_MAP scalar)
        //{
        //    bool status = true;
        //    uint scalarVal = GetRegisterValue("", pipePlaneObject.Pipe, pipePlaneObject.Plane, PORT.NONE);
        //    SCALAR_MAP currentScalar = (SCALAR_MAP)scalarVal;

        //    status = currentScalar.ToString() == gPlane.ToString();
        //    scalar = currentScalar;

        //    if (status == true)
        //    {
        //        //checking if scalar is eanbled.
        //        string eventName = currentScalar + "_Enable";
        //        if (!VerifyRegisters(eventName, pipePlaneObject.Pipe, pipePlaneObject.Plane, PORT.NONE, false))
        //        {
        //            status = false;
        //        }
        //    }
        //    return status;
        //}
    }
}



