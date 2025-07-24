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
    class InitHotplugFramework : InitEnvironment
    {
        public InitHotplugFramework(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            if (base.Manager.ApplicationSettings.UseULTFramework || base.Manager.ApplicationSettings.UseDivaFramework || base.Manager.ApplicationSettings.UseSHEFramework)    //SHE
            {
                Log.Verbose("Initializing DFT Display simulation");
                HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, true);
                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFramework);

                HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, true);
                AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFeature);
            }
            else
            {
                if (base.Manager.Dvmu4DeviceStatus)
                {
                    Log.Verbose("Opening DVMU for Hotplug/Unplug");
                    HotPlugUnplug pUP = new HotPlugUnplug();
                    pUP.FunctionName = FunctionName.OPEN;
                    AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, pUP);
                }
            }
        }
    }
}
