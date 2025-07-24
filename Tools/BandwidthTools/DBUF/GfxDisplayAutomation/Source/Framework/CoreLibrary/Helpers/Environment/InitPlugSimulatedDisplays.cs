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
    class InitPlugSimulatedDisplays : InitEnvironment
    {
        public InitPlugSimulatedDisplays(IApplicationManager argManager)
            : base(argManager)
        { }
        public override void DoWork()
        {
               List<DisplayType> displayToBeEnumerated=new List<DisplayType>();
                
                if(IsDisplayEnumerationNeeded(ref displayToBeEnumerated))
                    PerformHotplug(displayToBeEnumerated);
   
        }

        private void PerformHotplug(List<DisplayType> argDispList)
        {
            foreach (DisplayType curDisp in argDispList) 
            {
                if (DisplayExtensions.GetDisplayType(curDisp) == DisplayType.WIGIG_DP)
                {
                    Log.Message("WiGig Receiver Arrival inside framework");
                    WiGigParams wigigInputParam = new WiGigParams();
                    wigigInputParam.wigigSyncInput = WIGIG_SYNC.Receiver_Arrival;
                    wigigInputParam.wigigDisplay = curDisp;
                    AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.SetMethod, wigigInputParam);
                }
                else if (base.Manager.ApplicationSettings.UseULTFramework || base.Manager.ApplicationSettings.UseDivaFramework || base.Manager.ApplicationSettings.UseSHEFramework)   //SHE
                {
                    HotPlugUnplug argPup = new HotPlugUnplug(FunctionName.PLUG, curDisp, DisplayExtensions.GetEdidFile(curDisp));
                    AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argPup);
                }
            }
        }
        private bool IsDisplayEnumerationNeeded(ref List<DisplayType> displayToBeEnumerated)
        {
            bool status = true;

            DisplayList dispList = base.Manager.ParamInfo.Get<DisplayList>(ArgumentType.Display);
            List<DisplayInfo> enumeratedDisplay = (List<DisplayInfo>)Manager.ParamInfo[ArgumentType.Enumeration];
            displayToBeEnumerated = dispList.ToList();
            //displayToBeEnumerated.Remove(DisplayType.None);
            foreach (DisplayInfo curDispInfo in enumeratedDisplay)
            {
                if (displayToBeEnumerated.Contains(curDispInfo.DisplayType))
                {
                    displayToBeEnumerated.Remove(curDispInfo.DisplayType);
                }
            }

            if (displayToBeEnumerated.Contains(DisplayType.WIDI))
                displayToBeEnumerated.Remove(DisplayType.WIDI);

            if (displayToBeEnumerated.Count == 0)
                status = false;
            
            return status;
        }

        private void EnableDFT()
        {
            HotPlugUnplug argSimulationFramework = new HotPlugUnplug(FunctionName.SimulationFramework, true);
            AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFramework);

            HotPlugUnplug argSimulationFeature = new HotPlugUnplug(FunctionName.SimulationFeature, true);
            AccessInterface.SetFeature<bool, HotPlugUnplug>(Features.SimulatedHotPlugDisplay, Action.SetMethod, argSimulationFeature);
        }
    }
}
