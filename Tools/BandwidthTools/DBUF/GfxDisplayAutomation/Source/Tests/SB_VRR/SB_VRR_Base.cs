using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_VRR_Base:TestBase
    {
        string eventName = "VRR_Enable";
        string eventMax = "VRR_Max";
        string eventMin = "VRR_Min";
        string eventFlipDone = "VRR_flipdone";        

        public void calc_Vmin_Vmax(DisplayType curDisp, out uint Vmin, out uint Vmax)
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();                                
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            PipePlaneParams pipePlane1 = new PipePlaneParams(curDisp);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            uint htotal = base.GetRegisterValue("HTOTAL", pipePlane1.Pipe, PLANE.NONE, PORT.NONE);
            
            if (displayInfo.VRRInfo.RR_max != 0 && displayInfo.VRRInfo.RR_min != 0)
            {
                Log.Message("actual current mode: HzRes= {0}, VtRes= {1}, RR= {2}, pixel_clock= {3},", actualMode.HzRes, actualMode.VtRes, actualMode.RR, actualMode.pixelClock);
                //we round of the value by flooring it, and the value that gets programmed in register is zero based.
                Vmin = Convert.ToUInt32(Math.Floor((actualMode.pixelClock * 1000 * 1000) / (htotal * actualMode.RR)) - 1);
                Vmax =  Convert.ToUInt32(Math.Floor((actualMode.pixelClock * 1000 * 1000) / (htotal * displayInfo.VRRInfo.RR_min)) - 1);
            }
            else { Vmin = 0; Vmax = 0; }
        }

        public void VerifyVRR(DisplayType disp)
        {
            PipeDbufInfo curPipeDbuf = new PipeDbufInfo();
            PipePlaneParams pipePlane1 = new PipePlaneParams(disp);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            uint Vmin, Vmax;

            Log.Message("----------Test sleeping for 5 sec. Put the game application to fullscreen immediately.-------");
            System.Threading.Thread.Sleep(5000);
            calc_Vmin_Vmax(disp, out Vmin, out Vmax);

            Log.Message("pipe {0} , plane {1}", pipePlane1.Pipe, pipePlane1.Plane);
            base.VerifyRegisters(eventName, pipePlane1.Pipe, PLANE.NONE, PORT.NONE, true);
            base.VerifyRegisters(eventFlipDone, PIPE.NONE, pipePlane1.Plane, PORT.NONE, true);

            uint regVal_vmax = base.GetRegisterValue(eventMax, pipePlane1.Pipe, PLANE.NONE, PORT.NONE);
            uint regVal_vmin = base.GetRegisterValue(eventMin, pipePlane1.Pipe, PLANE.NONE, PORT.NONE);            

            if (Vmax == regVal_vmax)
                Log.Success("Vmax is programmed correctly. Vmax= {0}", Vmax);
            else
                Log.Fail("Vmax is programmed wrong. Expected val= {0}, RegVal= {1}", Vmax, regVal_vmax);

            
            if (Vmin == regVal_vmin)
                Log.Success("Vmin is programmed correctly. Vmin= {0}", Vmin);
            else
                Log.Fail("Vmin is programmed wrong. Expected val= {0}, RegVal= {1}", Vmin, regVal_vmin);            
        }

        //checks VRR status register and returns the VRR enable live status.        
        public uint IsVRREnabled(DisplayType disp)
        {
            uint ret = 0;
            PipePlaneParams pipePlane1 = new PipePlaneParams(disp);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("----------Test sleeping for 5 sec. Put the game application to fullscreen immediately.-------");
            System.Threading.Thread.Sleep(5000);
            ret= base.GetRegisterValue("VRR_Status", pipePlane1.Pipe, PLANE.NONE, PORT.NONE);
            return ret;
        }
        
        //checks VRR capability of all connected displays and adds to displayList
        public void GetVRRCapableDisplays(DisplayList displayList)
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if(curDisp == DisplayType.EDP || curDisp == DisplayType.DP)
                {
                    //get MSA_timing_par_ignored from DPCD (offset 00007h: bit 6)
                    DpcdInfo dpcd = new DpcdInfo();
                    dpcd.Offset = Convert.ToUInt32("00007", 16);
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                    dpcd.DispInfo = displayInfo;
                    AccessInterface.GetFeature<DpcdInfo, DpcdInfo>(Features.DpcdRegister, Action.GetMethod, Source.AccessAPI, dpcd);
                    uint msa_timing_par_ignored= (dpcd.Value & 0x40) >> 6;

                    //get continuous_freq_sup, VRR_min and VRR_max from EDID
                    if(msa_timing_par_ignored==1 && displayInfo.VRRInfo.ContFreqSup && displayInfo.VRRInfo.RR_min!=0 && displayInfo.VRRInfo.RR_max!=0)
                    {
                        displayList.Add(curDisp);
                    }                   
                }
            });
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
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            else
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
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
            Log.Message(true, "Verify the selected mode got applied for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
    }
}
