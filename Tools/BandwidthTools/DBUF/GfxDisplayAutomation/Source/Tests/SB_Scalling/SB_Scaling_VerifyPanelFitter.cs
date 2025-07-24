using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Scaling_VerifyPanelFitter : TestBase
    {
        Dictionary<DisplayType, bool> panelFitter = new Dictionary<DisplayType, bool>();
        [Test(Type = TestType.Method, Order = 0)]
        public virtual void TestStep0()
        {
            //ApplyConfigOS(base.CurrentConfig);
            //List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            //allModeList.ForEach(curDisp =>
            //{
            //    Log.Message(true, "Applying Mode to ; {0}", curDisp.display);
            //    List<DisplayMode> modeList = curDisp.supportedModes;
            //    uint nativeHZres = modeList.Last().HzRes;
            //    uint nativeVTres = modeList.Last().VtRes;

            //    List<uint> nativeRR = new List<uint>();
            //    modeList.ForEach(curMode =>
            //    {
            //        if (curMode.HzRes == nativeHZres && curMode.VtRes == nativeVTres)
            //            nativeRR.Add(curMode.RR);
            //    });

            //    curDisp.supportedModes.ForEach(curMode =>
            //    {
            //        Log.Message(true, "current mode {0}", curMode.GetCurrentModeStr(true));
            //        while (curMode.ScalingOptions.Count != 0)
            //        {
            //            ScalingOptions scaleOp = (ScalingOptions)curMode.ScalingOptions.First();
            //            if (scaleOp != ScalingOptions.Customize_Aspect_Ratio && curMode.InterlacedFlag!=1)
            //            {
            //                if (ApplyMode(curMode, scaleOp))
            //                {
            //                    Log.Success("{0} applied successfully", curMode.GetCurrentModeStr(true));


            //                    bool panelFitter = true;
            //                    if (curMode.InterlacedFlag == 1)
            //                        panelFitter = true;
            //                    else if (scaleOp == ScalingOptions.Maintain_Display_Scaling)
            //                        panelFitter = false;
            //                    else if (curMode.HzRes == nativeHZres && curMode.VtRes == nativeVTres)
            //                        panelFitter = false;
            //                    else if (scaleOp == ScalingOptions.Customize_Aspect_Ratio)
            //                        panelFitter = true;
            //                    else if (!nativeRR.Contains(curMode.RR))
            //                    {
            //                        panelFitter = false;
            //                        Log.Message("New RR: {0} is exepcetd not to enable panel fitter for {1}", curMode.GetCurrentModeStr(false), scaleOp);
            //                    }
            //                    else
            //                        panelFitter = true;

            //                    VerifyPanelFitterRegisters(curDisp.display, scaleOp, panelFitter);

            //                }
            //            }
            //            curMode.ScalingOptions.RemoveAt(0);
            //        }

            //    });
            //});
                  base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    DisplayScaling curScale = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, curDisp);
                    VerifyPanelFitterRegisters(curDisp, curScale.scaling, true);
                });
            Log.Message(true,"\n \n **********************Panel Fitter Status*****************");
            panelFitter.ToList().ForEach(dI =>
                {
                    Log.Message("{0} Panel Fitter : {1}", dI.Key, dI.Value);
                });
           
        }
        public bool ApplyMode(DisplayMode argDispMode, ScalingOptions argScalingOp)
        {

            DisplayMode mode = new DisplayMode() { display = argDispMode.display };

            if (argScalingOp == ScalingOptions.Customize_Aspect_Ratio)
            {
                DisplayScaling dsScaling = new DisplayScaling(argDispMode.display, argScalingOp);
                
                dsScaling.customX = 0;
                dsScaling.customY = 50;

                Log.Message(true, "{0}", dsScaling.ToString());
                AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);

                DisplayScaling curr_Scalling_SDK_Manager = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, argDispMode.display);

                if (dsScaling.Equals(curr_Scalling_SDK_Manager))
                {
                    Log.Success("Current Scalling : {0}  ------  Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling.ToString());
                    return true;
                }
                else
                    Log.Fail("Scalling Differ - Current Scalling from SDK Manager : {0} Expected(Applied) Scalling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling.ToString());
            }
            else
            {
                if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argDispMode))
                {
                    Log.Success("{0} applied successfully", argDispMode.GetCurrentModeStr(true));
                    return true;
                }
                else
                {
                    Log.Fail("Failed to apply {0}", argDispMode.GetCurrentModeStr(false));
                }
            }
            return false;
        }
        public void VerifyPanelFitterRegisters(DisplayType argDispType, ScalingOptions argScaleOption, bool argPanelFitter)
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

           // if (argPanelFitter)
            //{
                if (pipePlane1.Plane == PLANE.PLANE_A || pipePlane1.Plane == PLANE.PLANE_B)
                {
                    Log.Message("The count is {0}", returnEventInfo.listRegisters.Count());
                    if (ReadRegister(returnEventInfo.listRegisters.First()))
                    {
                        Log.Message("panel fitter 1 is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                        panelFitter.Add(argDispType, true);
                    }
                    else if ((base.MachineInfo.PlatformDetails.Platform == Platform.SKL || 
                        base.MachineInfo.PlatformDetails.Platform == Platform.KBL || 
                        base.MachineInfo.PlatformDetails.Platform == Platform.BXT) && ReadRegister(returnEventInfo.listRegisters.Last()))
                    {
                        Log.Message("panel fitter 2 is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                        panelFitter.Add(argDispType, true);
                    }
                    else
                    {
                        Log.Message("No panel fitter is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                        panelFitter.Add(argDispType, false);
                    }

                }
                else
                {
                    if (ReadRegister(returnEventInfo.listRegisters.First()))
                        Log.Message("panel fitter  is enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
                }
            //}
            //else
            //{
            //    returnEventInfo.listRegisters.ForEach(curEvent =>
            //    {
            //        if (!ReadRegister(curEvent))
            //            Log.Message("Panel fitter not enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
            //        else
            //            Log.Message("Panel fitter enabled for {0} {1}", pipePlane1.Pipe, argScaleOption);
            //    });
            //}
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
        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
    }
}
