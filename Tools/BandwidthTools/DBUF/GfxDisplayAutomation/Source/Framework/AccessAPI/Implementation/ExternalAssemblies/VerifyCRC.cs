namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;

    internal class VerifyCRC : FunctionalBase, IGetMethod, IParse
    {
        [ParseAttribute(InterfaceName = InterfaceType.IGet, Comment = "Gets the current display Configuration")]
        public void Parse(string[] args)
        {
            if (args[0].ToLower().Contains("get"))
            {
                object ob = new object();
                bool crcStatus = (bool)this.GetMethod(ob);
                Log.Verbose("Current CRC Status - {0} ", crcStatus);
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("Usage for a GET Operation::").Append(Environment.NewLine);
            sb.Append("..\\>Execute VerifyCRC Get EDP").Append(Environment.NewLine);

            Log.Verbose(sb.ToString());

        }

        private bool GetPortCRC(DisplayType display, PORT port, bool isPipeCRC, ref uint tempCRC)
        {
            bool status = true;
            CRCArgs obj = new CRCArgs();
            obj.displayType = display;
            obj.port = port;
            obj.ComputePipeCRC = isPipeCRC;

            CRC crc = base.CreateInstance<CRC>(new CRC());
            obj = (CRCArgs)crc.GetMethod(obj);

            tempCRC = obj.CRCValue;

            if (tempCRC == 0)
                status = false;

            return status;
        }
        private bool GetGoldenCRC(DisplayInfo curDispInfo, DisplayMode curDispMode, bool isPipeCRC, ref uint tempCRC)
        {
            bool status = true;

            CrcGoldenDataArgs obj = new CrcGoldenDataArgs();
            obj.displayInfo = curDispInfo;
            obj.displayMode = curDispMode;
            obj.IsPipeCRC = isPipeCRC;

            CrcGoldenData crcGoldenData = base.CreateInstance<CrcGoldenData>(new CrcGoldenData());
            obj = (CrcGoldenDataArgs)crcGoldenData.GetMethod(obj);

            tempCRC = obj.CRCValue;

            if (tempCRC == 0 || obj.IsCRCPresent == false)
                status = false;

            return status;
        }

        public object GetMethod(object argMessage)
        {
            bool Status = false;
            uint currentCRC = 0;
            uint goldenCRC = 0;

            VerifyCRCArgs verifyCrcArgs = argMessage as VerifyCRCArgs;
            DisplayType display = verifyCrcArgs.display;
            bool isPipeCRC = verifyCrcArgs.ComputePipeCRC;

            if (isPipeCRC)
                Log.Message(true, "Verifying Pipe CRC's.");
            else
                Log.Message(true, "Verifying Port CRC's.");

            DisplayInfo curDispInfo = base.EnumeratedDisplays.Where(di => di.DisplayType == display).FirstOrDefault();
            Modes modes = base.CreateInstance<Modes>(new Modes());
            DisplayMode curDispMode = (DisplayMode)modes.GetMethod(curDispInfo);

            if (curDispMode.InterlacedFlag == 1)
            {
                Log.Alert("Skipping corruption check for Interlaced mode: {0}", curDispMode.GetCurrentModeStr(false));
                return false;
            }

            SetUpDesktopArgs driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.PrepareDesktop);
            driverParams.display = display;
            driverParams.currentConfig = verifyCrcArgs.currentConfig;
            driverParams.displayMode = curDispMode;

            SetUpDesktop setupDesktop = base.CreateInstance<SetUpDesktop>(new SetUpDesktop());
            if (!setupDesktop.SetMethod(driverParams))
                Log.Fail("Failed to Prepare Desktop.");
            else
            {
                if (GetGoldenCRC(curDispInfo, curDispMode, isPipeCRC, ref goldenCRC))
                {
                    GetPortCRC(display, curDispInfo.Port, isPipeCRC, ref currentCRC);

                    if (currentCRC == 0 || goldenCRC == 0)
                        Log.Fail("CRC should not be zero. Expected:{0}, Current CRC:{1}.", goldenCRC, currentCRC);
                    else
                    {
                        if (currentCRC == goldenCRC)
                        {
                            Status = true;
                            Log.Success("CRC Matched for {0}", curDispMode.GetCurrentModeStr(false));
                        }
                        else
                        {
                            Log.Alert("CRC mismatch. Sleep for 10sec and compute crc again.");
                            System.Threading.Thread.Sleep(10000);

                            GetPortCRC(display, curDispInfo.Port, isPipeCRC, ref currentCRC);

                            if (currentCRC == 0 || goldenCRC == 0)
                                Log.Fail("CRC should not be zero. Expected:{0}, Current CRC:{1}.", goldenCRC, currentCRC);
                            else
                            {
                                if (currentCRC == goldenCRC)
                                {
                                    Log.Success("CRC Matched for {0}", curDispMode.GetCurrentModeStr(false));
                                }
                                else
                                {
                                    Log.Fail("CRC Not Matched. Expected:0x{0}, Current CRC:0x{1} for {2}: {3}", goldenCRC.ToString("X"), currentCRC.ToString("X"), curDispMode.display, curDispMode.GetCurrentModeStr(false));
                                }
                            }
                        }
                    }
                }
                else
                    Log.Fail("Golden CRC not available for {0}", curDispMode.GetCurrentModeStr(false));


                driverParams = new SetUpDesktopArgs(SetUpDesktopArgs.SetUpDesktopOperation.RestoreDesktop);
                if (!setupDesktop.SetMethod(driverParams))
                    Log.Fail("Failed to Restore Desktop.");
            }

            return Status;
        }
    }
}
