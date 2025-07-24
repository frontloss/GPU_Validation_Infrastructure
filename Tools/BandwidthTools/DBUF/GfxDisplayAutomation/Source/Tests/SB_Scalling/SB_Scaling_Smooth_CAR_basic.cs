using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_Smooth_CAR_basic : TestBase
    {
        protected List<DisplayMode> dispModes = new List<DisplayMode>();
        protected Dictionary<ScalingOptions, List<DisplayMode>> scalingList = new Dictionary<ScalingOptions, List<DisplayMode>>();
        protected List<ScalingOptions> _scalingList = new List<ScalingOptions>();
        [Test(Type = TestType.Method, Order = 0)]
        public virtual void TestStep0()
        {
            scalingList.Add(ScalingOptions.Center_Image, new List<DisplayMode>());
            scalingList.Add(ScalingOptions.Customize_Aspect_Ratio, new List<DisplayMode>());
            scalingList.Add(ScalingOptions.Maintain_Aspect_Ratio, new List<DisplayMode>());
            scalingList.Add(ScalingOptions.Maintain_Display_Scaling, new List<DisplayMode>());
            scalingList.Add(ScalingOptions.Scale_Full_Screen, new List<DisplayMode>());

            _scalingList = new List<ScalingOptions>() {ScalingOptions.Maintain_Display_Scaling , ScalingOptions.Customize_Aspect_Ratio,
                                                                            ScalingOptions.Maintain_Display_Scaling, ScalingOptions.Customize_Aspect_Ratio,
                                                                             ScalingOptions.Center_Image, ScalingOptions.Customize_Aspect_Ratio,
                                                                              ScalingOptions.Scale_Full_Screen, ScalingOptions.Customize_Aspect_Ratio,
                                                                               ScalingOptions.Center_Image, ScalingOptions.Customize_Aspect_Ratio,
                                                                              ScalingOptions.Scale_Full_Screen, ScalingOptions.Customize_Aspect_Ratio
            };
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            ApplyConfig(base.CurrentConfig);
            List<uint> xList = new List<uint>() { 0, 100, 0, 50, 100, 50 };
            List<uint> yList = new List<uint>() { 0, 100, 50, 100, 0, 50 };

            _scalingList.ForEach(curScale =>
                {
                    if (curScale == ScalingOptions.Customize_Aspect_Ratio)
                        GetModeForScaling(curScale, base.CurrentConfig.PrimaryDisplay, xList, yList);
                    else
                        GetModeForScaling(curScale, base.CurrentConfig.PrimaryDisplay);
                });
        }

        protected void ApplyAndVerifyCAR(DisplayType pDisplayType, DisplayMode dispMode, List<uint> customX, List<uint> customY)
        {

            Log.Message(true, "CAR {0} {1}", pDisplayType, dispMode);
            DisplayScaling dsScaling = null;




            List<ScalingOptions> all_Scallings_SDK_Manager = AccessInterface.GetFeature<List<ScalingOptions>, DisplayType>(Features.Scaling, Action.GetAllMethod, Source.AccessAPI, pDisplayType);
            if (!all_Scallings_SDK_Manager.Contains(ScalingOptions.Customize_Aspect_Ratio))
            {
                Log.Alert("{0} does not support CAR for {1}", pDisplayType, dispMode.GetCurrentModeStr(false));
            }
            all_Scallings_SDK_Manager.ForEach(apply_Scaling =>
            {
                if (apply_Scaling == ScalingOptions.Customize_Aspect_Ratio)
                {
                    dsScaling = new DisplayScaling(pDisplayType, apply_Scaling);

                    for (int index = 0; index < customX.Count; index++)
                    {
                        dsScaling.customX = customX[index];
                        dsScaling.customY = customY[index];

                        Log.Message(true, "{0}", dsScaling.ToString());
                        AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);

                        DisplayScaling curr_Scalling_SDK_Manager = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, pDisplayType);

                        if (dsScaling.Equals(curr_Scalling_SDK_Manager))
                        {
                            Log.Success("Current Scalling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling.ToString());
                            CheckRegister(pDisplayType, ScalingOptions.Customize_Aspect_Ratio);
                        }
                        else
                            Log.Fail("Scalling Differ - Current Scalling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling.ToString());
                    }
                }
            });
        }

        public void GetModeForScaling(ScalingOptions argScaleOption, DisplayType argDispType)
        {
            List<uint> xList = new List<uint>() { 0 };
            List<uint> yList = new List<uint>() { 0 };
            GetModeForScaling(argScaleOption, argDispType, xList, yList);
        }
        public void GetModeForScaling(ScalingOptions argScaleOption, DisplayType argDispType, List<uint> customX, List<uint> customY)
        {
            Log.Message(true, "Applying {0} {1}", argScaleOption, argDispType);
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            dispModes = allModeList.Where(dML => dML.display == argDispType).Select(dML => dML.supportedModes).FirstOrDefault();

            List<DisplayMode> tempMode = new List<DisplayMode>();
            dispModes.Reverse();

            uint nativeHZRes = dispModes.First().HzRes;
            uint nativeVTRes = dispModes.First().VtRes;

            if (argScaleOption != ScalingOptions.Maintain_Display_Scaling)
            {
                dispModes.ForEach(curMode =>
                    {
                        if (curMode.HzRes != nativeHZRes && curMode.VtRes != nativeVTRes)
                            tempMode.Add(curMode);
                    });
                dispModes = tempMode;
            }


            bool flag = false;
            uint scale = (uint)argScaleOption;
            List<DisplayMode> modeListForScale = scalingList[argScaleOption];

            DisplayMode Mode = new DisplayMode();
            dispModes.ForEach(curMode =>
            {
                if (curMode.ScalingOptions.Contains(scale) && !flag)
                {
                    if (modeListForScale.Count == 0)
                    {
                        flag = true;
                        Mode = curMode;
                    }
                    else
                    {
                        bool alreadyExist = false;
                        modeListForScale.ForEach(appliedMode =>
                        {
                            if (appliedMode.GetCurrentModeStr(true).Equals(curMode.GetCurrentModeStr(true)))
                            {
                                alreadyExist = true;
                            }
                        });
                        if (!alreadyExist)
                        {
                            flag = true;
                            Mode = curMode;
                        }
                    }
                }
            });
            if (flag)
            {
                Mode.ScalingOptions.Clear();
                Mode.ScalingOptions.Add(scale);
                modeListForScale.Add(Mode);
            }
            else
            {
                if (modeListForScale.Count == 0)
                    Log.Fail("Cannot find a mode with {0}", argScaleOption);
                else
                {
                    Mode = modeListForScale.First();
                    Log.Message("Cannot find another {0}, so re applying {1}", argScaleOption, modeListForScale.First().GetCurrentModeStr(true));
                }
            }
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, Mode))
            {
                Log.Success("{0} applied successfully", Mode.GetCurrentModeStr(true));
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == Mode.display).First();
                DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                if (actualMode.GetCurrentModeStr(true).Equals(Mode.GetCurrentModeStr(true)))
                {
                    Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), Mode);
                }
                else
                {
                    Log.Fail("Failed to apply {0}, current mode {1}",Mode.GetCurrentModeStr(false),actualMode.GetCurrentModeStr(false));
                }
            }
            else
                Log.Fail("{0} not applied", Mode.GetCurrentModeStr(true));

            if (argScaleOption == ScalingOptions.Customize_Aspect_Ratio)
            {


                ApplyAndVerifyCAR(argDispType, Mode, customX, customY);
            }

        }
        public void CheckRegister(DisplayType argDispType, ScalingOptions argScaleOption)
        {
            if (argDispType == DisplayType.EDP || argDispType == DisplayType.MIPI)
                Log.Alert("{0} does not support CAR", argDispType);
            else
            {
                VerifyPanelFitterRegisters(argDispType, argScaleOption);
            }
        }
        public void VerifyPanelFitterRegisters(DisplayType argDispType, ScalingOptions argScaleOption)
        {
            PipeDbufInfo curPipeDbuf = new PipeDbufInfo();
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);

            bool match = false;
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = pipePlane1.Plane;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = "PANEL_FITTER";

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            if (argScaleOption != ScalingOptions.Maintain_Display_Scaling)
            {
                if (pipePlane1.Pipe == PIPE.PIPE_A || pipePlane1.Pipe == PIPE.PIPE_B)
                {
                    Log.Message("The count is {0}", returnEventInfo.listRegisters.Count());
                    if (ReadRegister(returnEventInfo.listRegisters.First()))
                        Log.Success("panel fitter 1 is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                    else if ((base.MachineInfo.PlatformDetails.Platform == Platform.SKL || base.MachineInfo.PlatformDetails.Platform == Platform.KBL) && ReadRegister(returnEventInfo.listRegisters.Last()))
                        Log.Success("panel fitter 2 is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                    else
                    {
                        Log.Fail("No panel fitter is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                    }

                }
                else
                {
                    if (ReadRegister(returnEventInfo.listRegisters.First()))
                        Log.Success("panel fitter  is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                }
            }
            else
            {
                returnEventInfo.listRegisters.ForEach(curEvent =>
                    {
                        if (!ReadRegister(curEvent))
                            Log.Success("Panel fitter not enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                        else
                            Log.Fail("Panel fitter enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                    });
            }
        }
        public bool ReadRegister(RegisterInf reginfo)
        {
            Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                Log.Abort("Failed to read Register with offset as {0}", driverData.input);
            else
                if (!MyCompareRegisters(driverData.output, reginfo))
                {
                    Log.Message("Register with offset {0} doesnot match required values", driverData.input.ToString("X"));
                    return false;
                }
            return true;
        }
        public bool MyCompareRegisters(uint argDriverData, RegisterInf argRegInfo)
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
        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
            {
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            }
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
    }

}

