namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    using System.Xml.Linq;
    using System.IO;
    public class SB_EDP_Base : TestBase
    {
       protected uint GetBitmappedRegisterValue(string registerEvent, PIPE pipe, PLANE plane, PORT port)
       {
           uint res = 0;
           EventInfo eventInfo = new EventInfo();
           eventInfo = new EventInfo();
           eventInfo.pipe = pipe;
           eventInfo.plane = plane;
           eventInfo.port = port;
           eventInfo.eventName = registerEvent;

           Log.Verbose("Event being checked = {0}", eventInfo.eventName);
           EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

           RegisterInf reginfo = returnEventInfo.listRegisters[0];
           uint bit = Convert.ToUInt32(reginfo.Bitmap, 16);
           res = bit & Convert.ToUInt32(reginfo.RegisterValue, 16);
           Log.Verbose("Value Before Bitmap: {0}, Value after bitmap: {1}", reginfo.RegisterValue, res.ToString("X"));

           return reginfo.BitmappedValue;
       }

        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        public void VerifyConfig(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0}", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified.", argDisplayConfig.GetCurrentConfigStr());
            }
            else
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
        }

        protected virtual void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            powerParams.Delay = 30;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }

        protected List<Config_Name> GetConfigNameList()
        {
            List<Config_Name> configNameList = new List<Config_Name>();

            XDocument events = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), @"\Mapper\EDP_Params.map"));

            foreach (var eachItem in events.Descendants("Config_Name"))
            {
                Config_Name cfgName = new Config_Name();
                cfgName.eventName = eachItem.Attribute("name").Value;
                cfgName.Lane_Count = eachItem.Elements("Lane_Count").FirstOrDefault().Value;
                cfgName.Link_Rate = eachItem.Elements("Link_Rate").FirstOrDefault().Value;
                cfgName.EDID_Name = eachItem.Elements("EDID_Name").FirstOrDefault().Value;
                cfgName.DPCD_Name = eachItem.Elements("DPCD_Name").FirstOrDefault().Value;
                cfgName.Run = Convert.ToBoolean(eachItem.Elements("Run").FirstOrDefault().Value);
                cfgName.Platform = (Platform)Enum.Parse(typeof(Platform), eachItem.Elements("Platform").FirstOrDefault().Value, true);

                configNameList.Add(cfgName);
            }

            return configNameList;

        }
    }
}
