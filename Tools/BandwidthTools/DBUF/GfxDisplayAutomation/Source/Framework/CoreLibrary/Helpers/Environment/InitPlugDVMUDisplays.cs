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
    class InitPlugDVMUDisplays : InitEnvironment
    {
        public InitPlugDVMUDisplays(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
            if (!(base.Manager.ApplicationSettings.UseULTFramework || base.Manager.ApplicationSettings.UseDivaFramework || base.Manager.ApplicationSettings.UseSHEFramework))  //SHE
            {
                if (base.Manager.Dvmu4DeviceStatus)
                {
                    HotPlugUnplug pUP = new HotPlugUnplug();
                    pUP.FunctionName = FunctionName.OPEN;
                    AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, pUP);

                    pUP.FunctionName = FunctionName.PLUG;
                    DisplayList dispList = base.Manager.ParamInfo.Get<DisplayList>(ArgumentType.Display);
                    List<DisplayInfo> enumeratedDisplay = (List<DisplayInfo>)Manager.ParamInfo[ArgumentType.Enumeration];
                    List<DisplayType> displayToBeEnumerated = dispList.ToList();
                    foreach (DisplayInfo curDispInfo in enumeratedDisplay)
                    {
                        if (displayToBeEnumerated.Contains(curDispInfo.DisplayType))
                        {
                            displayToBeEnumerated.Remove(curDispInfo.DisplayType);
                        }
                    }
                    List<DisplayType> dpList = new List<DisplayType>();
                    List<DisplayType> hdmiList = new List<DisplayType>();
                    foreach (DisplayType curDispType in displayToBeEnumerated)
                    {
                        switch (curDispType)
                        {
                            case DisplayType.HDMI: hdmiList.Add(curDispType); break;
                            case DisplayType.HDMI_2: hdmiList.Add(curDispType); break;
                            case DisplayType.DP: dpList.Add(curDispType); break;
                            case DisplayType.DP_2: dpList.Add(curDispType); break;
                            default: break;
                        }
                    }

                    if (dpList.Count > 0)
                        PerformHotplug(dpList, pUP);
                    if (hdmiList.Count > 0)
                        PerformHotplug(hdmiList, pUP);
                }
                else
                    Log.Verbose("DVMU4 not present.");
            }
        }
        private void PerformHotplug(List<DisplayType> argDispList, HotPlugUnplug argPup)
        {
            foreach (DisplayType curDisp in argDispList)
            {
                List<DVMU_PORT> dvmuPortList = new List<DVMU_PORT>() { DVMU_PORT.PORTA, DVMU_PORT.PORTB };
                List<DisplayInfo> enumeratedDisplays = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
                AccessInterface.SetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.SetMethod, enumeratedDisplays);
                List<DVMU_PORT> enumeratedPortList = enumeratedDisplays.Select(dI => dI.DvmuPort).ToList();
                List<DVMU_PORT> freeDvmuPort = dvmuPortList.Except(enumeratedPortList).ToList();
                if (freeDvmuPort.Count() > 0)
                {
                    argPup.Port = freeDvmuPort.First();
                    argPup.EdidFilePath = "HDMI_DELL.EDID";
                    AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.DvmuHotPlugStatus, Action.SetMethod, argPup);
                }
            }
        }
    }
}
