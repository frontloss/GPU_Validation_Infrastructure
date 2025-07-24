namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using System.Text;
    delegate void DvmuStatusHandler(bool b_ok, string status);

    internal class DvmuHotPlugStatus : FunctionalBase, ISetMethod, IParse
    {
        private event DvmuStatusHandler OnDvmuStatus;
        public bool DvmuOpenSucceeded = false;

        public bool SetMethod(object argMessage)
        {
            HotPlugUnplug HotPlugUnplugObject = argMessage as HotPlugUnplug;
            PlugUnPlugEnumeration plugUnPlugEnum = base.CreateInstance<PlugUnPlugEnumeration>(new PlugUnPlugEnumeration());

            if (HotPlugUnplugObject.FunctionName == FunctionName.Install)
                this.InstallDvmuDriver("dvmu4");
            else
            {
                if (!base.AppManager.Dvmu4DeviceStatus)
                {
                    Log.Abort("DVMU4 not present.");
                }
            }

            if (HotPlugUnplugObject.FunctionName == FunctionName.OPEN)
                return openDVMU();
            else if (HotPlugUnplugObject.FunctionName == FunctionName.PLUG)
            {
                UpdateHtPlgHtUnplgObj(HotPlugUnplugObject);
                if (HotPlugUnplugObject.display != DisplayType.None && HotPlugUnplugObject.Port == DVMU_PORT.None)
                {
                    if (HotPlugUnplugObject.display == DisplayType.HDMI)
                        HotPlugUnplugObject.Port = DVMU_PORT.PORTA;
                    else if (HotPlugUnplugObject.display == DisplayType.HDMI_2)
                        HotPlugUnplugObject.Port = DVMU_PORT.PORTB;

                    HotPlugUnplugObject.Delay = HotPlugUnplug.DEFAULT_DELAY;
                    if (HotPlugUnplugObject.InLowPowerState == true)
                        HotPlugUnplugObject.Delay = 15;
                }

                Log.Message("Performing hotplug of display {0} with edid {1} on port {2}", HotPlugUnplugObject.display, Path.GetFileName(HotPlugUnplugObject.EdidFilePath), HotPlugUnplugObject.Port);
                if (ProgramEdid(HotPlugUnplugObject.Port, HotPlugUnplugObject.EdidFilePath) == DVMU4_STATUS.SUCCESS)
                    Log.Success("the status of program edid is Success");
                else
                {
                    Log.Fail("Program edid failed on port {0}", HotPlugUnplugObject.Port);
                }
               
                Log.Message("{0} will be plugged in {1} sec", HotPlugUnplugObject.Port.ToString(), HotPlugUnplugObject.Delay);
                if (PlugDisplay(HotPlugUnplugObject.Port, HotPlugUnplugObject.Delay) == DVMU4_STATUS.SUCCESS)
                {
                    Thread.Sleep(4000);
                    if (HotPlugUnplugObject.Delay == HotPlugUnplug.DEFAULT_DELAY)
                    {
                        if (!HotPlugUnplugObject.SkipDisplayEnumeration)
                            plugUnPlugEnum.SetMethod(HotPlugUnplugObject);
                    }
                    else
                        base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo.Add(HotPlugUnplugObject);
                    DisplayExtensions.pluggedDisplayList.Add(HotPlugUnplugObject.display);
                }
                else
                {
                    Log.Fail("Failed to plug Display to DVMU {1}", HotPlugUnplugObject.Port.ToString());
                    return false;
                }
            }
            else if (HotPlugUnplugObject.FunctionName == FunctionName.UNPLUG)
            {
                UpdateHtPlgHtUnplgObj(HotPlugUnplugObject);
                if (HotPlugUnplugObject.display != DisplayType.None && HotPlugUnplugObject.Port == DVMU_PORT.None)
                {
                    HotPlugUnplugObject.Port = base.EnumeratedDisplays.Where(DT => DT.DisplayType == HotPlugUnplugObject.display).FirstOrDefault().DvmuPort;
                    
                    HotPlugUnplugObject.Delay = HotPlugUnplug.DEFAULT_DELAY;
                    if (HotPlugUnplugObject.InLowPowerState == true)
                        HotPlugUnplugObject.Delay = 15;
                }

                if (HotPlugUnplugObject.Port == DVMU_PORT.None)
                    Log.Abort("Unable to find DVMU port for display {0}", HotPlugUnplugObject.display);

                Log.Message("{0} will be unplugged in {1} sec ", HotPlugUnplugObject.Port.ToString(), HotPlugUnplugObject.Delay);
                if (UnplugDisplay(HotPlugUnplugObject.Port, HotPlugUnplugObject.Delay) == DVMU4_STATUS.SUCCESS)
                {
                    Thread.Sleep(4000);
                    if (HotPlugUnplugObject.Delay == HotPlugUnplug.DEFAULT_DELAY)
                    {
                        if (!HotPlugUnplugObject.SkipDisplayEnumeration)
                            plugUnPlugEnum.SetMethod(HotPlugUnplugObject);
                    }
                    else
                        base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo.Add(HotPlugUnplugObject);
                    DisplayExtensions.pluggedDisplayList.Remove(HotPlugUnplugObject.display);
                }
                else
                {
                    Log.Fail("Failed to unplug {0} ", HotPlugUnplugObject.Port.ToString());
                    return false;
                }
            }
            else if (HotPlugUnplugObject.FunctionName == FunctionName.PlugEnumerate)
            {
                plugUnPlugEnum.SetMethod(HotPlugUnplugObject);
            }
            else if (HotPlugUnplugObject.FunctionName == FunctionName.UnplugEnumerate)
            {
                plugUnPlugEnum.SetMethod(HotPlugUnplugObject);
            }
            else if (HotPlugUnplugObject.FunctionName == FunctionName.CaptureFrame)
            {
               return CaptureFrame(HotPlugUnplugObject.Port, HotPlugUnplugObject.FrameFileName);
            }
            //else if (HotPlugUnplugObject.FunctionName == FunctionName.CheckCorruption)
            //{
            //    return CheckCorruption(HotPlugUnplugObject.Port, HotPlugUnplugObject.FrameFileName);
            //}

            return true;
        }

        private void UpdateHtPlgHtUnplgObj(HotPlugUnplug HotPlugUnplugObject)
        {
            if (string.IsNullOrEmpty(HotPlugUnplugObject.EdidFilePath))
            {
                string edidFileName = string.Empty;
                base.AppManager.HotplugUnplugCntx.EDID_Files.TryGetValue(HotPlugUnplugObject.display, out edidFileName);
                if (string.IsNullOrEmpty(edidFileName))
                    Log.Abort("Edid file not found for plugging display {0}", HotPlugUnplugObject.display.ToString());
                HotPlugUnplugObject.EdidFilePath = edidFileName;
            }
            if (HotPlugUnplugObject.InLowPowerState)
            {
                base.AppManager.HotplugUnplugCntx.PlugUnplugInLowPower = true;
            }
        }

        private bool CaptureFrame(DVMU_PORT port, string fileName)
        {
            bool status = true;
            uint crc=0;
            DVMU_MEASUREMENTS measurements;

            string filenameWithoutExt = Path.GetFileNameWithoutExtension(fileName);

            Interop.GetCRC(port,out crc, true);

            if (Interop.FetchVideoData(port, filenameWithoutExt + ".raw", 1) != DVMU4_STATUS.SUCCESS)
            {
                Log.Fail("Failed to FetchVideoData() from DVMU4 {1}", port.ToString());
                status = false;
            }

            if (Interop.GetPortMeasurements(port, out measurements) == DVMU4_STATUS.SUCCESS)
            {
                int x = (int)measurements.hsync.frequency;
                int y = (int)measurements.vsync.frequency;
                //HotPlugUnplugObject.yResolution = (int)measurements.vsync.frequency;
                Interop.GetBmpFromFrame(filenameWithoutExt + ".raw", filenameWithoutExt + ".bmp", y, x);
            }
            else
            {
                Log.Fail("Failed to fetch PortMeasurements from DVMU4 {1}", port.ToString());
                status = false;
            }

            return status;
        }
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "FunctionName:FunctionName:sp", "DVMU_PORT:DVMUPort:sp", "Edid_File:EdidFile:sp" }, Comment = "Hotplug/unplugs the display to the dvmu port")]
        public void Parse(string[] args)
        {
            // args[0]=set args[1]=function args[2]=display type args[3]=port args[4]=edid file

            HotPlugUnplug obj = new HotPlugUnplug();
            if (args.IsHelpCall())
                this.HelpMenu();
            else if (args.Length > 0 && args[0].ToLower().Equals("set"))
            {
                FunctionName Fn; DisplayType Dt; DVMU_PORT DP;
                if (args.Length > 1 && Enum.TryParse<FunctionName>(args[1], true, out Fn))
                {
                    obj.FunctionName = Fn;
                    if (obj.FunctionName == FunctionName.PLUG || obj.FunctionName == FunctionName.UNPLUG)
                        openDVMU();
                }
                if (args.Length > 2 && Enum.TryParse<DVMU_PORT>(args[2], true, out DP))
                    obj.Port = DP;
                string path = "DP.EDID";
                if (args.Length.Equals(4) && !string.IsNullOrEmpty(args[3]))
                {
                    path = args[3];
                }
                obj.EdidFilePath = path;

                this.SetMethod(obj);
            }
        }

        private bool openDVMU()
        {
            OnDvmuStatus += OnStatusHandler;
            DVMU4_STATUS status = DVMU4_STATUS.FAIL;
            try
            {
                Interop.DvmuGetAllDevices();
                if (File.Exists(Path.Combine(Directory.GetCurrentDirectory(), "DviceInfo.txt")))
                {
                    String[] data = File.ReadAllLines(Path.Combine(Directory.GetCurrentDirectory(), "DviceInfo.txt"));
                    string[] deviceId = data.First().Split(':');
                    // int id = Convert.ToInt32(Regex.Match(data.First(), @"\d+").Value);
                    int id = Convert.ToInt32(deviceId.Last());
                    status = Interop.Open(id);
                }
                else
                {
                    status = Interop.Open(0);
                }
                if (status == DVMU4_STATUS.SUCCESS)
                {
                    DvmuOpenSucceeded = true;
                    Log.Verbose("DVMU Open status is  success");
                }
                else
                {
                    Log.Verbose("DVMU Open status is  fail");
                    this.InstallDvmuDriver("dvmu4");
                }
            }
            catch (Exception ex)
            {
                if (null != ex.InnerException)
                    ex = ex.InnerException;
                this.openDVMU_OldFirmware();
            }
            return DvmuOpenSucceeded;
        }
        private void openDVMU_OldFirmware()
        {
            DVMU4_STATUS status = DVMU4_STATUS.FAIL;
            try
            {
                status = Interop.Open(0);

                if (status == DVMU4_STATUS.SUCCESS)
                {
                    DvmuOpenSucceeded = true;
                    Log.Verbose("DVMU Open status is  success");
                }
                else
                {
                    Log.Verbose("DVMU Open status is  fail");
                    this.InstallDvmuDriver("dvmu4");
                }
            }
            catch (Exception ex)
            {
                if (null != ex.InnerException)
                    ex = ex.InnerException;
                if (ex.Message.ToUpper().Contains("DVMU4.OPEN"))
                    this.InstallDvmuDriver("dvmu4");
            }
        }        
        private void InstallDvmuDriver(string argSimulatorType)
        {
            ProcessStartInfo psi = new ProcessStartInfo("DvmuInstaller\\installer.exe  ");   // Program name
            // Assemble all the arguments
            psi.Arguments = string.Concat("-install -", argSimulatorType);
            psi.WorkingDirectory = ".\\DvmuInstaller\\";
            psi.RedirectStandardOutput = true;  // Redirect msgs
            psi.WindowStyle = ProcessWindowStyle.Normal;
            psi.CreateNoWindow = false;
            psi.UseShellExecute = false;

            Log.Verbose("Launching {0} Installer: {1}", argSimulatorType, psi.Arguments);

            Process installerProcess = Process.Start(psi);
            // Read all msgs in console from process
            string msgs = installerProcess.StandardOutput.ReadToEnd();
            installerProcess.WaitForExit();
            Log.Verbose("{0} Installer exited normally:", argSimulatorType);
            Thread.Sleep(10000);
        }
        private void HelpMenu()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>execute dvmuhotplugstatus help").Append(Environment.NewLine);
            sb.Append("..\\>excute dvmuhotplugstatus set plug <Display Type> <Port> <Edid File>").Append(Environment.NewLine);
            sb.Append("..\\>excute dvmuhotplugstatus set unplug <Display Type> <Port>").Append(Environment.NewLine);
            sb.Append("Display Type[HDMI, HDMI_2]").Append(Environment.NewLine);
            sb.Append("Port [PortA, PortB]").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        private DVMU4_STATUS ProgramEdid(DVMU_PORT port, String filename)
        {
            Byte[] edid = new Byte[256];
            Byte[] data = File.ReadAllBytes(filename);
            int length = data.Length;
            if (!UpdateChecksum(ref data))
            {
                // OnDvmuStatus(false, "EDID data size must be > 127 bytes!");
                Log.Verbose("EDID data size must be > 127 bytes!");
                return DVMU4_STATUS.FAIL;
            }
            Log.Verbose("\n the checksum was success");
            try
            {
                if (Interop.ProgramEdid(port, data, Convert.ToUInt16(data.Length), true) != DVMU4_STATUS.SUCCESS)
                {
                    Log.Verbose("The program edid status  for Plug is{0} ", DVMU4_STATUS.FAIL);
                    return DVMU4_STATUS.FAIL;
                }
                else
                {
                    Log.Verbose("The program edid status  for plug is {0}", DVMU4_STATUS.SUCCESS);
                }
            }
            catch (Exception ex)
            {
                throw new TestException(ex.InnerException ?? ex, "ProgramEDID failed. DVMU Hotplug or system reboot might be required! - Port#{0} - EDDIFilename:: {1}", port, filename);
            }
            return DVMU4_STATUS.SUCCESS;
        }
        private bool UpdateChecksum(ref byte[] edid)
        {
            if (edid.Length < 128)
                return false;
            byte total = 0; byte checksum = 0;
            for (int i = 0; i < 127; i++)
                total += edid[i];
            checksum = (byte)(0xff - (int)total + 1);
            edid[127] = checksum;
            return true;
        }
        private DVMU4_STATUS UnplugDisplay(DVMU_PORT port, short delay = 4)
        {
            if (Convert.ToBoolean(Interop.EnableHPD(port, delay, true, false) != DVMU4_STATUS.SUCCESS))
            {
                Log.Verbose("The EnabledHPD for unplug status is " + DVMU4_STATUS.FAIL);
                return DVMU4_STATUS.FAIL;
            }
            Log.Verbose("The EnabledHPD for unplug status is " + DVMU4_STATUS.SUCCESS);
            return DVMU4_STATUS.SUCCESS;
        }
        private DVMU4_STATUS PlugDisplay(DVMU_PORT port, short delay = 4)
        {
            //step 2 enable HPD
            if (Interop.EnableHPD(port, delay, true, true) != DVMU4_STATUS.SUCCESS)
            {
                Log.Verbose("The enableHPD for plug status is " + DVMU4_STATUS.FAIL);
                return DVMU4_STATUS.FAIL;
            }
            else
            {
                Log.Verbose("The enableHPD for plug status is " + DVMU4_STATUS.SUCCESS);
            }
            Thread.Sleep(3000);
            Log.Verbose("The hot plug status is " + DVMU4_STATUS.SUCCESS);
            return DVMU4_STATUS.SUCCESS;
        }
        private void OnStatusHandler(bool status, string message)
        {
            if (DvmuOpenSucceeded)
            {
                if (!status)
                {
                    String errorStr = GetLastErrorStr();
                    if (errorStr.Contains("I2C"))
                    {
                        throw (new Exception("I2C error caught. Stop current test with errors"));
                    }
                }
            }
        }
        private string GetLastErrorStr()
        {
            IntPtr ptr = Interop.GetLastErrorStr_IntPtr();
            if (IntPtr.Zero.Equals(ptr))
                return "Error. Failed to get error string";
            return Marshal.PtrToStringAnsi(ptr);
        }
    }
}
