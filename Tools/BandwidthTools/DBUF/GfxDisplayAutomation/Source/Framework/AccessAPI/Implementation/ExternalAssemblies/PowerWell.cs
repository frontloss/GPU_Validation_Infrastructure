namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Xml.Serialization;
    using System.Collections.Generic;

    internal class PowerWell : FunctionalBase, IGet//, IParse
    {
        private const string MIPI_DUAL_LINK_MODE = "MIPI_DUAL_LINK_MODE";
        private const string VDSC_ENABLED = "VDSC_ENABLED";
        private const string PWR_WELL_CTL_DDI2 = "PWR_WELL_CTL_DDI2";
        private const string PWR_WELL_CTL_AUX2 = "PWR_WELL_CTL_AUX2";
        private const string _ENABLED = "_ENABLED";

        private Dictionary<PIPE, System.Action> _EnablePowerWell = new Dictionary<PIPE, System.Action>();
        private Dictionary<POWERWELL, bool> _PowerWellStatus = new Dictionary<POWERWELL, bool>();
        private Dictionary<PORT, bool> _PortsStatus = new Dictionary<PORT, bool>();

        public PowerWell()
        {
            _EnablePowerWell.Add(PIPE.PIPE_EDP, EnablePG1);
            _EnablePowerWell.Add(PIPE.PIPE_A, EnablePG3);
            _EnablePowerWell.Add(PIPE.PIPE_B, EnablePG3);
            _EnablePowerWell.Add(PIPE.PIPE_C, EnablePG4);

            _PowerWellStatus.Add(POWERWELL.POWERWELL_PG1, false);
            _PowerWellStatus.Add(POWERWELL.POWERWELL_PG2, false);
            _PowerWellStatus.Add(POWERWELL.POWERWELL_PG3, false);
            _PowerWellStatus.Add(POWERWELL.POWERWELL_PG4, false);

            _PortsStatus.Add(PORT.PORTA, false);
            _PortsStatus.Add(PORT.PORTB, false);
            _PortsStatus.Add(PORT.PORTC, false);
            _PortsStatus.Add(PORT.PORTD, false);
            _PortsStatus.Add(PORT.PORTE, false);
        }

        void EnablePG1()
        {
            _PowerWellStatus[POWERWELL.POWERWELL_PG1] = true;
        }
        void EnablePG2()
        {
            _PowerWellStatus[POWERWELL.POWERWELL_PG2] = true;
            EnablePG1();
        }
        void EnablePG3()
        {
            _PowerWellStatus[POWERWELL.POWERWELL_PG3] = true;
            EnablePG2();
        }
        void EnablePG4()
        {
            _PowerWellStatus[POWERWELL.POWERWELL_PG4] = true;
            EnablePG3();
        }

        private bool VerifyPowerWell()
        {
            bool status = true;

            Config config = base.CreateInstance<Config>(new Config());
            DisplayConfig displayConfig = config.Get as DisplayConfig;

            AudioEnumeration audioEnum = base.CreateInstance<AudioEnumeration>(new AudioEnumeration());
            AudioDataProvider audioData = audioEnum.GetAll as AudioDataProvider;
            bool IsAudioEnabled = audioData.ActiveAudioEndpointDevice != 0 ? true : false;
            //bool IsAudioEnabled = false;

            displayConfig.CustomDisplayList.ForEach(eachDisplay =>
            {
                DisplayInfo displayInfo =  this.EnumeratedDisplays.Where(dI => dI.DisplayType == eachDisplay).First();

                PipePlane pipePlane = base.CreateInstance<PipePlane>(new PipePlane());
                PipePlaneParams pipePlaneParams = new PipePlaneParams(eachDisplay);
                pipePlaneParams = (PipePlaneParams)pipePlane.GetMethod(pipePlaneParams);

                _EnablePowerWell[pipePlaneParams.Pipe]();
                _PortsStatus[displayInfo.Port] = true;

                if(displayInfo.Port>= PORT.PORTB)
                {
                    EnablePG3();
                }

                if (eachDisplay == DisplayType.MIPI)
                {
                    //TRANS_DDI_FUNC_CTL2 Port Sync Mode 
                    bool isDualLinkEnabled = VerifyRegisters(MIPI_DUAL_LINK_MODE, PIPE.NONE, PLANE.NONE, displayInfo.Port);
                    if (isDualLinkEnabled)
                    {
                        Log.Message("Data is driven in Dual Link mode");
                        _PortsStatus[PORT.PORTA] = true;
                        _PortsStatus[PORT.PORTB] = true;
                    }
                }
            });


            bool IsVdscEnabled = VerifyRegisters(VDSC_ENABLED, PIPE.NONE, PLANE.NONE, PORT.NONE);
            if (IsVdscEnabled)
            {
                Log.Verbose("VDSC is enabled.");
                EnablePG2();
            }
            else
            {
                Log.Verbose("VDSC is not enabled.");
            }
            
            if(IsAudioEnabled)
            {
                EnablePG3();
            }


            //Actual Verification of the powerwell.
            foreach (POWERWELL eachPowerWell in _PowerWellStatus.Keys)
            {
                string eventName = eachPowerWell.ToString() + _ENABLED;

                bool expectedStatus = _PowerWellStatus[eachPowerWell];
                bool currentStatus = VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, PORT.NONE);
                string st = currentStatus ? "Enabled" : "Disabled";

                if (expectedStatus == currentStatus)
                {
                    Log.Success("{0} is {1} as expected.", eachPowerWell, st);
                }
                else
                {
                    status = false;
                    Log.Fail("{0} is {1}, which is not expected.", eachPowerWell, st);
                }
            }


            //Need to implement verification of the DDI IO and AUX IO for the ports.
            foreach (PORT eachPort in _PortsStatus.Keys)
            {
                bool expectedStatus = _PortsStatus[eachPort];
                bool currentStatus = VerifyRegisters(PWR_WELL_CTL_DDI2, PIPE.NONE, PLANE.NONE, eachPort);

                string st = currentStatus ? "Enabled" : "Disabled";

                if (expectedStatus == currentStatus)
                {
                    Log.Success("PowerWell DDI {0} is {1} as expected.", eachPort, st);
                }
                else
                {
                    status = false;
                    Log.Fail("PowerWell DDI {0} is {1}, which is not expected.", eachPort, st);
                }

                //Commenting this part of code. Need to create separate thread while reading this register.
                //currentStatus = VerifyRegisters(PWR_WELL_CTL_AUX2, PIPE.NONE, PLANE.NONE, eachPort);
                //st = currentStatus ? "Enabled" : "Disabled";

                //if (expectedStatus == currentStatus)
                //{
                //    Log.Success("PowerWell AUX {0} is {1} as expected.", eachPort, st);
                //}
                //else
                //{
                //    status = false;
                //    Log.Fail("PowerWell AUX {0} is {1}, which is not expected.", eachPort, st);
                //}
            }

            return status;
        }

        protected bool VerifyRegisters(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventRegisterInfo pipePlane = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            EventInfo returnEventInfo = (EventInfo)pipePlane.GetMethod(eventInfo);

            return returnEventInfo.RegistersMatched;
        }

        public object Get
        {
            get {
                
                //if(base.MachineInfo.PlatformDetails.Platform != Platform.ICL)
                //{
                //    Log.Abort("This feature is applicable only on {0} platform.", Platform.ICL);
                //}

                return VerifyPowerWell();
            }
        }

        //[ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "PowerStates:PoweState" }, Comment = "Performs power event(S5 not supported)")]
        //public void Parse(string[] args)
        //{
        //    PowerStates powerState;
        //    if (args.Length > 1 && args[0].ToLower().Contains("set") && Enum.TryParse(args[1], true, out powerState))
        //    {
        //        PowerParams powerParams = new PowerParams();
        //        powerParams.PowerStates = powerState;
        //        int delay = 30;
        //        if (args.Length.Equals(3))
        //            Int32.TryParse(args[2], out delay);
        //        powerParams.Delay = delay;
        //        if (!this.SetMethod(powerParams))
        //            Log.Alert("{0} not successful!", powerState);
        //    }
        //    else
        //        this.HelpText();
        //}
    }
}