using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_PLL_Base_Chv : SB_PLL_Base
    {
        Platform platform = Platform.CHV;

        Dictionary<DisplayType, List<int>> bitmap = null;
        protected void VerifyPLLRegister(DisplayConfig argDispConfig)
        {
            if (base.MachineInfo.PlatformDetails.Platform != platform)
            {
                base.VerifyPLLRegister(argDispConfig);
            }
            else
            {
                bitmap = new Dictionary<DisplayType, List<int>>() { { DisplayType.HDMI, new List<int>(){24,25} }, 
                { DisplayType.DP, new List<int>(){16,17} }, 
                { DisplayType.EDP, new List<int>(){16,17} } };
                PerformChvPLL(argDispConfig);
            }
        }
       
        protected void VerifyConfig(DisplayConfig argDispConfig)
        {
            base.VerifyConfig(argDispConfig);
        }
        protected void PowerEvent(PowerStates argPowerState)
        {
            base.PowerEvent(argPowerState);
        }

        protected void PerformChvPLL(DisplayConfig argDispConfig)
        {
            argDispConfig.CustomDisplayList.ForEach(curDisp =>
                {
                    if (curDisp != DisplayType.MIPI)
                    {
                        Log.Message("--------------------------------------------------------------------- \n \n ");
                        string eventName = curDisp + "_ENABLED";
                        PORT port = base.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.Port).FirstOrDefault();
                        Log.Message("the port is {0}",port);

                        base.VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, port, true);

                        eventName = curDisp + "_PLL";
                        uint pllValue = ReadRegister(eventName, port,curDisp);
                        Log.Message("Value read from register {0} {1}", curDisp, pllValue);

                        DPLL dpll;
                        Enum.TryParse<DPLL>(pllValue.ToString(), true, out dpll);
                        Log.Message("{0} : {1}", curDisp, dpll);

                        DisplayInfo curDispInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                        curDispInfo.dpll = dpll;

                        if (base.VerifyRegisters(dpll.ToString(), PIPE.NONE, PLANE.NONE, PORT.NONE, true))
                            Log.Success("{0} match expected DPLL {1}", curDisp, dpll);
                        else
                            Log.Fail("{0} does not match expected pll {1}", curDisp, dpll);

                        if (curDisp == DisplayType.EDP)
                        {
                            base.VerifyRegisters(dpll.ToString() + "_SSC", PIPE.NONE, PLANE.NONE, PORT.NONE, true);
                        }
                    }
                });
        }
        private uint ReadRegister(string argEventName, PORT argPort,DisplayType argDisp)
        {
            bool match = false;
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = PLANE.NONE;
            eventInfo.port = argPort;
            eventInfo.eventName = argEventName;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);


                Log.Message("{0} : {1} and bitmap {2}",reginfo.Offset, driverData.output,reginfo.Bitmap);

                uint value = CompareRegisters(driverData.output, reginfo,argDisp);
                Log.Message("after bitmap {0}",value);
                return value;

            }
            Log.Verbose("returning default value 0 for {0}: {1}", argEventName, argPort);
            return 0;
        }
        protected uint CompareRegisters(uint argDriverData, RegisterInf argRegInfo, DisplayType argDisp)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            string binary = argDriverData.ToString("X");
            Log.Verbose("value from reg read in hex = {0}", binary);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            
            uint bitmappedValue= Convert.ToUInt32(valu, 16);

            if (bitmap.Keys.Contains(argDisp))
            {
                List<int> bitValue = bitmap[argDisp];
                uint finalValue = GetRegisterValue(bitmappedValue, bitValue.First(), bitValue.Last());
                return finalValue;
            }
            else
            {
                Log.Fail("{0} not found in dictionary bitmap", argDisp);
                return 0;
            }
            
        }

        private uint GetRegisterValue(uint RegisterValue, int start, int end)
        {
            uint value = RegisterValue << (31 - end);
            value >>= (31 - end + start);
            return value;
        }       
    }
}
