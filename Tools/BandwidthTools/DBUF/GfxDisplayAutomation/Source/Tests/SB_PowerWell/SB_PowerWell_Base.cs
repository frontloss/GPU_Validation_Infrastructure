namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    //public enum POWERWELL
    //{
    //    POWERWELL_PG1,
    //    POWERWELL_PG2,
    //    POWERWELL_PG3,
    //    POWERWELL_PG4,
    //}   
    class SB_PowerWell_Base : TestBase
    {
        protected void VerifyPowerWell()
        {
            bool PowerWellStatus = AccessInterface.GetFeature<bool>(Features.PowerWell, Action.Get);

            if (PowerWellStatus)
            {
                Log.Success("All PowerWells are programmed as expected.");
            }
            else
            {
                Log.Fail("PowerWells are programmed which was not expected.");
            }
        }

        //protected const string MIPI_DUAL_LINK_MODE = "MIPI_DUAL_LINK_MODE";
        //protected const string VDSC_ENABLED = "VDSC_ENABLED";
        //protected const string PWR_WELL_CTL_DDI2 = "PWR_WELL_CTL_DDI2";
        //protected const string PWR_WELL_CTL_AUX2 = "PWR_WELL_CTL_AUX2";

        //protected Dictionary<PIPE, System.Action> _EnablePowerWell = new Dictionary<PIPE, System.Action>();
        //protected Dictionary<POWERWELL, bool> _PowerWellStatus = new Dictionary<POWERWELL, bool>();
        //protected Dictionary<PORT, bool> _PortsStatus = new Dictionary<PORT, bool>();

        //public SB_PowerWell_Base()
        //{
        //    _EnablePowerWell.Add(PIPE.PIPE_EDP, EnablePG1);
        //    _EnablePowerWell.Add(PIPE.PIPE_A, EnablePG3);
        //    _EnablePowerWell.Add(PIPE.PIPE_B, EnablePG3);
        //    _EnablePowerWell.Add(PIPE.PIPE_C, EnablePG4);

        //    _PowerWellStatus.Add(POWERWELL.POWERWELL_PG1, false);
        //    _PowerWellStatus.Add(POWERWELL.POWERWELL_PG2, false);
        //    _PowerWellStatus.Add(POWERWELL.POWERWELL_PG3, false);
        //    _PowerWellStatus.Add(POWERWELL.POWERWELL_PG4, false);

        //    _PortsStatus.Add(PORT.PORTA, false);
        //    _PortsStatus.Add(PORT.PORTB, false);
        //    _PortsStatus.Add(PORT.PORTC, false);
        //    _PortsStatus.Add(PORT.PORTD, false);
        //    _PortsStatus.Add(PORT.PORTE, false);
        //}

        //[Test(Type = TestType.Method, Order = 0)]
        //public void TestStep0()
        //{
        //    if (base.MachineInfo.PlatformDetails.Platform != Platform.ICL)
        //        Log.Abort("This test is applicable only on {0} only.", Platform.ICL);

        //    if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
        //        Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        //}

        //void EnablePG1()
        //{
        //    _PowerWellStatus[POWERWELL.POWERWELL_PG1] = true;
        //}
        //void EnablePG2()
        //{
        //    _PowerWellStatus[POWERWELL.POWERWELL_PG2] = true;
        //    EnablePG1();
        //}
        //void EnablePG3()
        //{
        //    _PowerWellStatus[POWERWELL.POWERWELL_PG3] = true;
        //    EnablePG2();
        //}
        //void EnablePG4()
        //{
        //    _PowerWellStatus[POWERWELL.POWERWELL_PG4] = true;
        //    EnablePG3();
        //}

        //protected void VerifyPowerWell(DisplayConfig displayConfig)
        //{
        //    bool IsAudioEnabled = AccessInterface.GetFeature<AudioDataProvider>(Features.AudioEnumeration, Action.GetAll, Source.AccessAPI).ActiveAudioEndpointDevice != 0 ? true : false;

        //    //Initialization
        //    foreach (POWERWELL eachPowerWell in _PowerWellStatus.Keys)
        //    {
        //        _PowerWellStatus[eachPowerWell] = false;
        //    }

        //    foreach (PORT eachPort in _PortsStatus.Keys)
        //    {
        //        _PortsStatus[eachPort] = false;
        //    }

        //    displayConfig.DisplayList.ForEach(eachDisplay =>
        //    {
        //        DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == eachDisplay).First();
        //        PipePlaneParams pipePlane = new PipePlaneParams(eachDisplay);

        //        pipePlane = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane);
        //        _EnablePowerWell[pipePlane.Pipe]();
        //        _PortsStatus[displayInfo.Port] = true;

        //        if(displayInfo.Port>= PORT.PORTB)
        //        {
        //            EnablePG3();
        //        }

        //        if (eachDisplay == DisplayType.MIPI)
        //        {
        //            //TRANS_DDI_FUNC_CTL2 Port Sync Mode 
        //            bool isDualLinkEnabled = VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, displayInfo.Port, false);
        //            if (isDualLinkEnabled)
        //            {
        //                Log.Message("Data is driven in Dual Link mode");
        //                _PortsStatus[PORT.PORTA] = true;
        //                _PortsStatus[PORT.PORTB] = true;
        //            }
        //        }
        //    });


        //    bool IsVdscEnabled = VerifyRegisters(VDSC_ENABLED, PIPE.NONE, PLANE.NONE, PORT.NONE, false);
        //    if (IsVdscEnabled)
        //    {
        //        Log.Verbose("VDSC is enabled.");
        //        EnablePG2();
        //    }
        //    else
        //    {
        //        Log.Verbose("VDSC is not enabled.");
        //    }
            
        //    if(IsAudioEnabled)
        //    {
        //        EnablePG3();
        //    }


        //    //Actual Verification of the powerwell.
        //    foreach (POWERWELL eachPowerWell in _PowerWellStatus.Keys)
        //    {
        //        string eventName = eachPowerWell.ToString() + "_ENABLED";

        //        bool expectedStatus = _PowerWellStatus[eachPowerWell];
        //        bool currentStatus = VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, PORT.NONE, false);
        //        string st = currentStatus ? "Enabled" : "Disabled";

        //        if (expectedStatus == currentStatus)
        //        {
        //            Log.Success("{0} is {1} as expected.", eachPowerWell, st);
        //        }
        //        else
        //        {
        //            Log.Fail("{0} is not {1} as expected.", eachPowerWell, st);
        //        }
        //    }


        //    //Need to implement verification of the DDI IO and AUX IO for the ports.
        //    foreach (PORT eachPort in _PortsStatus.Keys)
        //    {
        //        string eventName = PWR_WELL_CTL_DDI2;
        //        bool expectedStatus = _PortsStatus[eachPort];
        //        bool currentStatus = VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, PORT.NONE, false);

        //        string st = currentStatus ? "Enabled" : "Disabled";

        //        if (expectedStatus == currentStatus)
        //        {
        //            Log.Success("PowerWell DDI {0} is {1} as expected.", eachPort, st);
        //        }
        //        else
        //        {
        //            Log.Fail("PowerWell DDI {0} is not {1} as expected.", eachPort, st);
        //        }


        //        eventName = PWR_WELL_CTL_AUX2;
        //        currentStatus = VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, PORT.NONE, false);
        //        st = currentStatus ? "Enabled" : "Disabled";

        //        if (expectedStatus == currentStatus)
        //        {
        //            Log.Success("PowerWell AUX {0} is {1} as expected.", eachPort, st);
        //        }
        //        else
        //        {
        //            Log.Fail("PowerWell AUX {0} is not {1} as expected.", eachPort, st);
        //        }
        //    }
        //}

        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }

        protected bool VerifyConfig(DisplayConfig argDisplayConfig, bool printError = true)
        {
            bool status = true;
            Log.Message(true, "Verifying config {0}.", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified.", argDisplayConfig.GetCurrentConfigStr());
            }
            else
            {
                status = false;
                if (printError)
                    Log.Fail("Config {0} does not match with current config {1}.", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
                else
                    Log.Alert("Config {0} does not match with current config {1}.", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
            }

            return status;
        }

        protected void PowerEvent(PowerStates powerState)
        {
            Log.Verbose("Putting the system into {0} state & resume ", powerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = 30;
            base.InvokePowerEvent(powerParams, powerState);
            Log.Success("Put the system into {0} state & resumed ", powerState);
        }
   }
}
