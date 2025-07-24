namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using System.IO;

    internal static class Extensions
    {
        private static Dictionary<string, DISPLAYCONFIG_SCALING> _scalingEnum = null;
        private static Dictionary<string, Action<string>> _paramMethod = null;
        private static Dictionary<string, Action<object[]>> _paramArgs = null;
        private static DisplayMode _parseMode;

        internal static Process StartProcess(string argFileName)
        {
            return StartProcess(argFileName, string.Empty);
        }
        internal static Process StartProcess(string argFileName, string arguments)
        {
            return StartProcess(argFileName, arguments, 90);
        }
        internal static Process StartProcess(string argFileName, string arguments, int argDelay)
        {
            return StartProcess(argFileName, arguments, argDelay, string.Empty);
        }
        internal static Process StartProcess(string argFileName, string arguments, int argDelay, string argWorkingDir)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.RedirectStandardOutput = true;
            processStartInfo.RedirectStandardInput = true;
            processStartInfo.UseShellExecute = false;
            processStartInfo.CreateNoWindow = false;
            processStartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processStartInfo.WorkingDirectory = argWorkingDir;
            processStartInfo.FileName = argFileName;
            if (!string.IsNullOrEmpty(arguments))
                processStartInfo.Arguments = arguments;
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();
            if (!argDelay.Equals(0))
                process.WaitForExit(argDelay * 1000);
            return process;
        }
        internal static DisplayInfo GetDisplayInfo(this List<DisplayInfo> argEnumeratedDisplays, string argDisplayType)
        {
            return argEnumeratedDisplays.Where(dI => dI.DisplayType.ToLower().Equals(argDisplayType.ToLower())).FirstOrDefault();
        }
        internal static DisplayMode GetCurrentDisplayMode(this List<DisplayInfo> argEnumeratedDisplays, uint argWinMonID)
        {
            return argEnumeratedDisplays.Where(dI => dI.WindowsMonitorID.Equals(argWinMonID)).Select(dI => dI.CurrentMode).FirstOrDefault();
        }
        internal static DisplayMode GetOptimalDisplayMode(this List<DisplayInfo> argEnumeratedDisplays, uint argWinMonID)
        {
            DisplayInfo displayInfo = argEnumeratedDisplays.Where(dI => dI.WindowsMonitorID.Equals(argWinMonID)).FirstOrDefault();
            if (null != displayInfo && null != displayInfo.SupportedModes)
                return displayInfo.SupportedModes.Last();
            return default(DisplayMode);
        }
        internal static DisplayMode PrepareSetMode(this DisplayMode argOptimalMode, uint argHzRes, uint argVtRes, uint argAngle)
        {
            DisplayMode setMode = argOptimalMode.Clone();
            setMode.Angle = argAngle;
            setMode.HzRes = argHzRes;
            setMode.VtRes = argVtRes;
            return setMode;
        }
        internal static DisplayMode GetExistingMode(this List<DisplayMode> argContext, DEVMODE argDevMode)
        {
            return argContext.Where(dM =>
                dM.HzRes.Equals(argDevMode.dmPelsWidth) &&
                dM.VtRes.Equals(argDevMode.dmPelsHeight) &&
                dM.RR.Equals(argDevMode.dmDisplayFrequency) &&
                dM.Bpp.Equals(argDevMode.dmBitsPerPel) &&
                dM.InterlacedFlag.Equals(argDevMode.dmDisplayFlags)
                ).FirstOrDefault();
        }
        internal static Action<object[]> ParseArgs(this string[] args)
        {
            if (GetParamArgs.ContainsKey(args.First()))
                return GetParamArgs[args.First()];
            return null;
        }

        private static void VerifyScaling(this List<DisplayMode> argContext, DisplayMode argNewMode)
        {
            List<uint> scalingOptions = argContext.Where(dM =>
                dM.Bpp.Equals(argNewMode.Bpp) &&
                dM.HzRes.Equals(argNewMode.HzRes) &&
                dM.InterlacedFlag.Equals(argNewMode.InterlacedFlag) &&
                dM.RR.Equals(argNewMode.RR) &&
                dM.VtRes.Equals(argNewMode.VtRes))
                .Select(dM => dM.ScalingOptions.First()).ToList();

            if (!scalingOptions.Count.Equals(0) && !scalingOptions.Contains(argNewMode.ScalingOptions.First()))
            {
                argNewMode.ScalingOptions.Clear();
                argNewMode.ScalingOptions.Add(scalingOptions.First());
            }
        }
        private static void SetAngleInMode(string argAngle)
        {
            _parseMode.Angle = Convert.ToUInt32(argAngle);
        }
        private static void SetResInMode(string argRes)
        {
            _parseMode.HzRes = Convert.ToUInt32(argRes.Split('x').First());
            _parseMode.VtRes = Convert.ToUInt32(argRes.Split('x').Last());
        }
        private static void SetRRInMode(string argRR)
        {
            _parseMode.InterlacedFlag = Convert.ToUInt32(argRR.ToLower().Contains("i").GetHashCode());
            _parseMode.RR = Convert.ToUInt32(argRR.Substring(0, argRR.IndexOf(Convert.ToBoolean(_parseMode.InterlacedFlag) ? "i" : "p")));
        }
        private static void SetScalingInMode(string argScaling)
        {
            if (GetScalingEnum.ContainsKey(argScaling.ToLower()))
                _parseMode.ScalingOptions = new List<uint>() { (uint)GetScalingEnum[argScaling.ToLower()] };
        }
        private static Dictionary<string, DISPLAYCONFIG_SCALING> GetScalingEnum
        {
            get
            {
                if (null == _scalingEnum)
                {
                    _scalingEnum = new Dictionary<string, DISPLAYCONFIG_SCALING>();
                    _scalingEnum.Add("maintain", DISPLAYCONFIG_SCALING.DISPLAYCONFIG_SCALING_IDENTITY);
                    _scalingEnum.Add("stretch", DISPLAYCONFIG_SCALING.DISPLAYCONFIG_SCALING_STRETCHED);
                    _scalingEnum.Add("center", DISPLAYCONFIG_SCALING.DISPLAYCONFIG_SCALING_CENTERED);
                    _scalingEnum.Add("aspectratio", DISPLAYCONFIG_SCALING.DISPLAYCONFIG_SCALING_ASPECTRATIO_CENTEREDMAX);
                }
                return _scalingEnum;
            }
        }
        private static Dictionary<string, Action<string>> GetParamMethod
        {
            get
            {
                if (null == _paramMethod)
                {
                    _paramMethod = new Dictionary<string, Action<string>>();
                    _paramMethod.Add("-res", SetResInMode);
                    _paramMethod.Add("-angle", SetAngleInMode);
                    _paramMethod.Add("-scaling", SetScalingInMode);
                    _paramMethod.Add("-rr", SetRRInMode);
                }
                return _paramMethod;
            }
        }
        private static Dictionary<string, Action<object[]>> GetParamArgs
        {
            get
            {
                if (null == _paramArgs)
                {
                    _paramArgs = new Dictionary<string, Action<object[]>>();
                    _paramArgs.Add("-listmonitors", ListAllDisplays);
                    _paramArgs.Add("-set", SetMode);
                    _paramArgs.Add("-supportedmodes", ListSupportedModes);
                }
                return _paramArgs;
            }
        }
        private static void ListAllDisplays(object[] argContext)
        {
            string outputFile = string.Concat(Directory.GetCurrentDirectory(), "\\ListAllDisplays.rep");
            if (File.Exists(outputFile))
                File.Delete(outputFile);
            List<DisplayInfo> enumeratedDisplays = argContext.First() as List<DisplayInfo>;
            enumeratedDisplays.ForEach(dI => 
                {
                    File.AppendAllText(outputFile, string.Format("{0} ({1}) {2}{3}", dI.DisplayType, (dI.IsActive ? "Active" : "InActive"), dI.CurrentMode.ToString(), Environment.NewLine));
                    Console.WriteLine("{0} ({1}) {2}", dI.DisplayType, (dI.IsActive ? "Active" : "InActive"), dI.CurrentMode.ToString());
                });
        }
        private static void ListSupportedModes(object[] argContext)
        {
            List<DisplayInfo> enumeratedDisplays = argContext.First() as List<DisplayInfo>;
            string display = (argContext.Last() as string[]).First();
            DisplayInfo displayInfo = enumeratedDisplays.GetDisplayInfo(display);
            if (null != displayInfo)
            {
                Console.WriteLine("Listing all supported modes for {0}", display);
                if (null != displayInfo.SupportedModes && !displayInfo.SupportedModes.Count.Equals(0))
                {
                    Console.WriteLine("****************************************************");
                    displayInfo.SupportedModes.ForEach(dM => Console.WriteLine("{0}", dM.ToString()));
                }
                else
                    Console.WriteLine("No supported modes found!");
            }
            else
                Console.WriteLine("{0} not enumerated!", display);
        }
        private static void SetMode(object[] argContext)
        {
            string display = string.Empty;
            DisplayMode parseMode = new DisplayMode();
            DisplayMode setMode = new DisplayMode();

            List<DisplayInfo> enumeratedDisplays = argContext.First() as List<DisplayInfo>;
            string[] args = argContext.Last() as string[];
            parseMode = args.ParseSetMode(out display);
            DisplayInfo currentDisplay = enumeratedDisplays.GetDisplayInfo(display);
            if (null != currentDisplay)
            {
                setMode = currentDisplay.CurrentMode.PrepareSetMode(parseMode, currentDisplay);
                if (WindowsFunctions.SetDisplayMode(setMode, currentDisplay, enumeratedDisplays))
                    Console.WriteLine("Mode set succeeded");
                else
                {
                    Console.WriteLine("{0}", Environment.NewLine);
                    Console.WriteLine("DisplayName:: {0}", display);
                    Console.WriteLine("Parse DisplayMode:: {0}", parseMode.ToString());
                    Console.WriteLine("Set DisplayMode:: {0}", setMode.ToString());
                }
            }
            else
                Console.WriteLine("{0} not enumerated!", display);
        }
        private static DisplayMode ParseSetMode(this string[] args, out string argDisplay)
        {
            argDisplay = string.Empty;
            _parseMode.Angle = 1;
            _parseMode.InterlacedFlag = 9;

            List<string> paramList = new List<string>() { "-res", "-angle", "-scaling", "-rr" };
            string paramStr = string.Concat(string.Join(" ", args), " -END");
            Match getParam = null;

            getParam = Regex.Match(paramStr, @"-display(.+?)(-).+");
            if (getParam.Success && getParam.Groups.Count.Equals(3))
                argDisplay = getParam.Groups[1].Value.Trim();

            paramList.ForEach(param =>
            {
                if (GetParamMethod.ContainsKey(param))
                {
                    getParam = Regex.Match(paramStr, string.Concat(param, @"(.+?)(-).+"));
                    if (getParam.Success && getParam.Groups.Count.Equals(3))
                        GetParamMethod[param](getParam.Groups[1].Value.Trim());
                }
            });
            return _parseMode;
        }
        private static DisplayMode PrepareSetMode(this DisplayMode argOptimalMode, DisplayMode argNewMode, DisplayInfo argDisplayInfo)
        {
            DisplayMode setMode = argOptimalMode.Clone();
            if (!argNewMode.Angle.Equals(1))
                setMode.Angle = argNewMode.Angle;
            if (!argNewMode.Bpp.Equals(0))
                setMode.Bpp = argNewMode.Bpp;
            if (!argNewMode.HzRes.Equals(0))
                setMode.HzRes = argNewMode.HzRes;
            if (!argNewMode.InterlacedFlag.Equals(9))
                setMode.InterlacedFlag = argNewMode.InterlacedFlag;
            if (!argNewMode.RR.Equals(0))
                setMode.RR = argNewMode.RR;
            if (!argNewMode.VtRes.Equals(0))
                setMode.VtRes = argNewMode.VtRes;
            if (null != argNewMode.ScalingOptions && !argNewMode.ScalingOptions.Count.Equals(0))
                setMode.ScalingOptions = argNewMode.ScalingOptions;
            if (null != argDisplayInfo.SupportedModes)
                argDisplayInfo.SupportedModes.VerifyScaling(setMode);
            return setMode;
        }
    }
}