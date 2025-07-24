namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Text;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    internal class Rotation : Modes, IParse
    {
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "DisplayType:DisplayType:sp", "Angle:Angle" }, Comment = "Sets the Rotation angle for a display")]
        [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" }, Comment = "Gets the Rotation angle for a display")]
        public new void Parse(string[] args)
        {
            if (args.IsHelpCall())
                this.HelpText();
            else if (args[0].ToLower().Contains("get"))
            {
                #region GET CALL
                DisplayType displayType = base.EnumeratedDisplays.Select(dI => dI.DisplayType).First();
                if (args.Length.Equals(2) && !string.IsNullOrEmpty(args[1]))
                    Enum.TryParse(args[1], true, out displayType);
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).First();
                DisplayMode currentMode = (DisplayMode)this.GetMethod(displayInfo);
                Log.Message("Current Resolution on Display {0}", currentMode.display);
                Log.Message("HRes - {0}, VRes - {1}, bpp - {2}, RR - {3}{4} Angle: {5}",
                    currentMode.HzRes, currentMode.VtRes, currentMode.Bpp, currentMode.RR, (Convert.ToBoolean(currentMode.InterlacedFlag) ? "i" : "p"), currentMode.Angle);
                Log.Message("Scaling: " + (ScalingOptions)currentMode.ScalingOptions[0]);
                #endregion
            }
            else if (args[0].ToLower().Contains("set"))
            {
                #region SET CALL
                args = args.Skip(1).ToArray();
                try
                {
                    DisplayMode mode = new DisplayMode();
                    mode.ScalingOptions = new List<uint>();
                    mode.display = (DisplayType)Enum.Parse(typeof(DisplayType), args[0], true);
                    mode.Angle = Convert.ToUInt32(args[(args.Length - 1)]);

                    if (args.Length != 2)
                    {
                        string[] res = null;
                        res = args[1].Split(new[] { 'x' }, StringSplitOptions.RemoveEmptyEntries);
                        mode.HzRes = Convert.ToUInt32(res[0]);
                        mode.VtRes = Convert.ToUInt32(res[1]);
                        mode.Bpp = Convert.ToUInt32(res[2]);
                        if (res[3].ToLower().Contains("i"))
                            mode.InterlacedFlag = Convert.ToUInt32(DisplayFlag.Interlaced);
                        else
                            mode.InterlacedFlag = Convert.ToUInt32(DisplayFlag.Progressive);
                        mode.RR = Convert.ToUInt32(Regex.Match(res[3], @"\d+").Value);

                        if (res.Length == 5)
                        {
                            mode.ScalingOptions = new List<uint>();
                            switch (res[4].ToUpper())
                            {
                                case "MDS":
                                    mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Display_Scaling));
                                    break;
                                case "FULL":
                                    mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Scale_Full_Screen));
                                    break;
                                case "CENTER":
                                    mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Center_Image));
                                    break;
                                case "MAR":
                                    mode.ScalingOptions.Add(Convert.ToUInt32(ScalingOptions.Maintain_Aspect_Ratio));
                                    break;
                                default:
                                    Log.Alert("Invalid Scaling Option");
                                    break;
                            }
                        }
                    }
                    else
                    {
                        //########### set as default resolutions #######
                        DisplayType displayType = base.EnumeratedDisplays.Select(dI => dI.DisplayType).First();
                        if (args.Length.Equals(2) && !string.IsNullOrEmpty(args[1]))
                            Enum.TryParse(args[0], true, out displayType);
                        DisplayInfo displayInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == displayType).First();
                        DisplayMode currentResolution = (DisplayMode)this.GetMethod(displayInfo);
                        mode.HzRes = currentResolution.HzRes;
                        mode.VtRes = currentResolution.VtRes;
                        mode.Bpp = currentResolution.Bpp;
                        mode.RR = currentResolution.RR;
                        mode.InterlacedFlag = currentResolution.InterlacedFlag;
                        mode.ScalingOptions.Add(currentResolution.ScalingOptions.First());
                    }

                    this.SetMethod(mode);

                }
                catch
                {
                    this.HelpText();
                }
                #endregion
            }
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("Usage for a GET Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute Rotation GetCurrentMode [Display]").Append(Environment.NewLine);
            sb.Append("[Display = CRT/EDP/DP/HDMI.....] Display should be Active").Append(Environment.NewLine).Append(Environment.NewLine);

            sb.Append("Usage for a SET Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute Rotation SetOrientation [Display] [Resolutions(Optional)] [Angle{0/90/180/270}]").Append(Environment.NewLine);
            sb.Append("[Display = CRT/EDP/DP/HDMI.....] Display should be Active").Append(Environment.NewLine);
            sb.Append("[Resolutions = HRes x VRes x Bpp x RR[i/p]]").Append(Environment.NewLine).Append(Environment.NewLine);

            sb.Append("Example 1: Execute Rotation SetOrientation EDP 180").Append(Environment.NewLine);
            sb.Append("Note: EDP should Active. rotate EDP to 180 degree.").Append(Environment.NewLine).Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
    }
}