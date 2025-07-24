namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;

    class Resolution : Modes, IParse,ISetAllMethod
    {
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "DisplayType:DisplayType:sp", "hzRes:HorizontalRes:sp", "VtRes:VerticalRes"},Comment="Sets the resolution for a display")]
        [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" },Comment="Gets the resolution of a display")]
        [ParseAttribute(InterfaceName = InterfaceType.ISetAllMethod, InterfaceData = new string[] { "HZres:Horizontal Res:sp", "VtRes:Vertical Res" }, Comment = "sets the resolution for all displays")]
        public new void Parse(string[] args)
        {
            if (args[0].ToLower().Contains("get"))
            {
                #region GET CALL
                DisplayType displayType = base.EnumeratedDisplays.Select(dI => dI.DisplayType).First();
                if (args.Length.Equals(2) && !string.IsNullOrEmpty(args[1]))
                    Enum.TryParse(args[1], true, out displayType);
                DisplayMode currentMode = base.GetCurrentMode(displayType, base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).Select(dI => dI.WindowsMonitorID).FirstOrDefault());
                Log.Message("Current Resolution on Display {0}", currentMode.display);
                Log.Message("HRes - {0}, VRes - {1}, bpp - {2}, RR - {3}{4} Angle: {5}",
                    currentMode.HzRes, currentMode.VtRes, currentMode.Bpp, currentMode.RR, (Convert.ToBoolean(currentMode.InterlacedFlag) ? "i" : "p"), currentMode.Angle);
                Log.Message("Scaling: {0}, DotClock {1}", (ScalingOptions)currentMode.ScalingOptions[0], currentMode.pixelClock);

                #endregion
            }
            if (args[0].ToLower().Contains("setall"))
            {
                List<DisplayType> dispList = base.EnumeratedDisplays.Select(dI =>dI.DisplayType).ToList();
                args = args.Skip(1).ToArray();
                uint hzRes = Convert.ToUInt32(args[0]);
                uint vtzRes = Convert.ToUInt32(args[1]);
                foreach (DisplayType curDispType in dispList)
                {
                    SetMethodCall(curDispType, hzRes, vtzRes);   
                }
            }
          else if (args[0].ToLower().Contains("set"))
            {
                #region SET CALL
                args = args.Skip(1).ToArray();                
                DisplayType display = (DisplayType)Enum.Parse(typeof(DisplayType), args[0], true);
                uint hzRes = Convert.ToUInt32(args[1]);
                uint vtzRes = Convert.ToUInt32(args[2]);
                SetMethodCall(display, hzRes, vtzRes);               
                #endregion
            }
        }
        public  object SetAllMethod(object argMessage)
        {
            List<String> args = argMessage as List<string>;
            List<DisplayType> dispList = base.EnumeratedDisplays.Select(dI => dI.DisplayType).ToList();
            uint hzRes = Convert.ToUInt32(args[0]);
            uint vtzRes = Convert.ToUInt32(args[1]);
            foreach (DisplayType curDispType in dispList)
            {
                SetMethodCall(curDispType, hzRes, vtzRes);
            }
            return true;
        }
        private void SetMethodCall(DisplayType argDisplay, uint hzRes, uint vtzRes)
        {
            DisplayMode mode = base.GetCurrentMode(argDisplay, base.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplay).Select(dI => dI.WindowsMonitorID).FirstOrDefault());

            List<DisplayModeList> supportedModes = (List<DisplayModeList>)base.GetAllMethod(new List<DisplayType>() { argDisplay });
            List<string> supHzRes = supportedModes.First().supportedModes.Where(dI => dI.display == argDisplay).Select(dI => dI.HzRes + "x" + dI.VtRes).ToList();
            string curRes = hzRes + "x" + vtzRes;

            if (supHzRes.Contains(curRes))
            {
                mode.display = argDisplay;
                mode.HzRes = hzRes;
                mode.VtRes = vtzRes;
                if (this.SetMethod(mode))
                    Log.Success("{0} resolution applied to {1}", curRes, argDisplay);
                else
                    Log.Fail("Failed to apply the resolution {0} to {1}", curRes, argDisplay);
            }
            else
            {
                Log.Fail("{0} Resolution is not supported by {1}", curRes, argDisplay);
            }

        }
    }
}
