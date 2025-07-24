namespace Intel.VPG.Display.Automation
{
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Linq;
    using System;
    using System.IO;
    using System.Reflection;
    using System.Text.RegularExpressions;
    using System.Security.Principal;
    using System.Runtime.InteropServices;
    class InitCleanupSimulatedDisplays : InitEnvironment
    {
        public InitCleanupSimulatedDisplays(IApplicationManager argManager)
            : base(argManager)
        { }

        public override void DoWork()
        {
            string testName = base.Manager.ParamInfo[ArgumentType.TestName] as string;
            if (testName.ToLower().StartsWith("mp_") || testName.ToLower().StartsWith("sb_"))
            {
                if (base.Manager.ApplicationSettings.UseULTFramework || base.Manager.ApplicationSettings.UseDivaFramework || base.Manager.ApplicationSettings.UseSHEFramework)    //SHE
                { 
                    HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, true);
                    AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFramework);

                    HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, false);
                    AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFeature);
                }
                else
                {
                    if (base.Manager.Dvmu4DeviceStatus)
                    {
                        InitHotplugFramework hotplugFW = new InitHotplugFramework(base.Manager);
                        hotplugFW.DoWork();
                        List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);

                        if (enumeratedDisplays.Select(eachdispInfo => eachdispInfo.DisplayType).ToList().Intersect(new List<DisplayType> { DisplayType.HDMI, DisplayType.HDMI_2 }).ToList().Count != 0)
                        {
                            HotPlugUnplug argPup = new HotPlugUnplug(FunctionName.UNPLUG, DisplayType.HDMI, DVMU_PORT.PORTA);
                            argPup.SkipDisplayEnumeration = true;

                            List<DVMU_PORT> dvmuPortList = new List<DVMU_PORT>() { DVMU_PORT.PORTA, DVMU_PORT.PORTB };
                            foreach (DVMU_PORT eachPort in dvmuPortList)
                            {
                                argPup.Port = eachPort;
                                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, argPup);
                            }
                        }
                    }
                    else
                        Log.Verbose("DVMU4 not present.");
                }
            }
        }
    }
}
