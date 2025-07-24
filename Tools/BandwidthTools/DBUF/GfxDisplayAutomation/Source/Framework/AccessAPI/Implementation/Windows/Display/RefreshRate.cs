namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class RefreshRate:Modes,IParse
    {
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "DisplayType:DisplayType:sp", "RefreshRate:RefreshRate" },Comment="Sets the refresh rate for a display")]
        [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" },Comment="Gets the Refreh rate of a display")]
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
                Log.Message("Scaling: " + (ScalingOptions)currentMode.ScalingOptions[0]);
                #endregion
            }
            if (args[0].ToLower().Contains("set"))
            {
                #region SET CALL
                args = args.Skip(1).ToArray();
                DisplayType display = (DisplayType)Enum.Parse(typeof(DisplayType), args[0], true);
                uint refreshRate = Convert.ToUInt32(args[1]);
                DisplayMode mode = base.GetCurrentMode(display, base.EnumeratedDisplays.Where(dI => dI.DisplayType == display).Select(dI => dI.WindowsMonitorID).FirstOrDefault());
                List<DisplayModeList> supportedModes = (List<DisplayModeList>)base.GetAllMethod(new List<DisplayType>() { display });
                List<uint> supRefRate = supportedModes.First().supportedModes.Where(dI =>dI.display==display).Select(dI => dI.RR).ToList();
                if (supRefRate.Contains(refreshRate))
                {
                    mode.display = display;
                    mode.RR = refreshRate;
                    if (this.SetMethod(mode))
                        Log.Success("Refresh rate {0} successfully applied to {1}", refreshRate, display);
                    else
                        Log.Fail("Failed to apply the Refresh rate {0} to {1}",refreshRate,display);
                }
                else
                {
                    Log.Fail("Refresh Rate {0} not supported by {1}", refreshRate, display);
                }
                #endregion
            }
        }
    }
}
