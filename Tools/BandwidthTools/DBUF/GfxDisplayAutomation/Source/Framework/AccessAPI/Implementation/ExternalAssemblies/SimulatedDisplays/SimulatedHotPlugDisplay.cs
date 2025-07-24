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
    using SHEDLL;      //SHE
      
    internal class SimulatedHotPlugDisplay : FunctionalBase, ISetMethod, IParse
    {
        string message = default(string);
        public bool SetMethod(object argMessage)
        {
            bool status = true;
            List<byte> EdidData = new List<byte>();
            List<byte> DpcdData = new List<byte>();
            HotPlugUnplug HotPlugUnplugObject = argMessage as HotPlugUnplug;

            PlugUnPlugEnumeration plugUnPlugEnum = base.CreateInstance<PlugUnPlugEnumeration>(new PlugUnPlugEnumeration());

            if (HotPlugUnplugObject.FunctionName == FunctionName.PLUG)
            {
                uint displayUID = 0;
                UpdateHtPlgHtUnplgObj(HotPlugUnplugObject);
				if (base.AppManager.ApplicationSettings.UseSHEFramework)    //SHE
                {
                    status = SHE_HotPlug(HotPlugUnplugObject.display, HotPlugUnplugObject.InLowPowerState);
                }
                else
                {
                string edidPath = HotPlugUnplugObject.EdidFilePath;
                EdidData = File.ReadAllBytes(HotPlugUnplugObject.EdidFilePath).ToList();

                if (DisplayExtensions.GetDisplayType(HotPlugUnplugObject.display) == DisplayType.DP || DisplayExtensions.GetDisplayType(HotPlugUnplugObject.display) == DisplayType.EDP)
                {
                    string dpcdFilePath = default(string);
                    if (!string.IsNullOrEmpty(HotPlugUnplugObject.DpcdFilePath))
                    {
                        dpcdFilePath = HotPlugUnplugObject.DpcdFilePath;
                    }
                    else
                    {
                        dpcdFilePath = edidPath.Substring(0, edidPath.Length - Path.GetExtension(edidPath).Length) + "_DPCD.bin";
                    }
                    
                    if (!File.Exists(dpcdFilePath))
                    {
                        Log.Fail("DPCD File {0} doesn't exist", dpcdFilePath);
                        status = false;
                    }
                    else
                    {
                        DpcdData = File.ReadAllBytes(dpcdFilePath).ToList();
                    }
                }

                if (base.AppManager.ApplicationSettings.UseDivaFramework)
                {
                    Log.Message("DIVA: Plugging {0}", HotPlugUnplugObject.display);
                    if (HotPlugUnplugObject.UseWindowsMonitorID)
                    {
                        displayUID = HotPlugUnplugObject.WindowsMonitorID;
                        DIVA_PORT_TYPE_CLR portType = DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR;

                        DivaDeviceSimulation.Plug(ConvertToDivaDisplayType(HotPlugUnplugObject.display), displayUID, portType, EdidData, DpcdData, HotPlugUnplugObject.InLowPowerState);
                    }
                    else
                    {
                        DivaDeviceSimulation.Plug(ConvertToDivaDisplayType(HotPlugUnplugObject.display), EdidData, DpcdData, HotPlugUnplugObject.InLowPowerState);
                    }
                }
                else //ULT Framework using Escape calls.
                {
                    if (HotPlugUnplugObject.UseWindowsMonitorID)
                    {
                        displayUID = HotPlugUnplugObject.WindowsMonitorID;
                    }
                    else
                    {
                        status = GetAvailableDisplayUID(HotPlugUnplugObject.display, ref displayUID);
                    }

                    if (status == true && displayUID != 0)
                    {
                        status = ULT_FW_PlugDisplay(displayUID, true, EdidData, DpcdData, HotPlugUnplugObject.InLowPowerState);
                    }
                    else
                    {
                        Log.Fail("WindowsMonitorID should not be 0.");
                        return false;
                    }
                }
                }
                if (status == true)
                {
                    if (!TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.SimulatedDisplay))
                    {
                        TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.SimulatedDisplay, null);
                    }
                    Log.Message("{0} will be plugged {1}.", HotPlugUnplugObject.display, message);
                    Thread.Sleep(2000);

                    if (HotPlugUnplugObject.InLowPowerState != true)
                    {
                        plugUnPlugEnum.SetMethod(HotPlugUnplugObject);
                    }
                    else
                        base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo.Add(HotPlugUnplugObject);

                    DisplayExtensions.pluggedDisplayList.Add(HotPlugUnplugObject.display);
                }
                else
                {
                    Log.Fail("Failed to plug Simulated Display {0} {1}", HotPlugUnplugObject.display, message);
                    status = false;
                }
            }
            else if (HotPlugUnplugObject.FunctionName == FunctionName.UNPLUG)
            {
                UpdateHtPlgHtUnplgObj(HotPlugUnplugObject);
               

                if (base.AppManager.ApplicationSettings.UseSHEFramework)    //SHE
                {
                    status = SHE_HotUnplug(HotPlugUnplugObject.display, HotPlugUnplugObject.InLowPowerState);
                }
                else
                {
                    uint displayUID = base.EnumeratedDisplays.Where(item => item.DisplayType == HotPlugUnplugObject.display).FirstOrDefault().WindowsMonitorID;
                    if (base.AppManager.ApplicationSettings.UseDivaFramework)
                    {
                        Log.Message("DIVA: Unplugging {0}", HotPlugUnplugObject.display);
                        DivaDeviceSimulation.UnPlug(displayUID, HotPlugUnplugObject.InLowPowerState);
                    }
                    else
                    {
                        status = ULT_FW_PlugDisplay(displayUID, false, EdidData, DpcdData, HotPlugUnplugObject.InLowPowerState);
                    }
                }
             
                if (status == true)
                {
                    Log.Message("{0} will be unplugged {1}.", HotPlugUnplugObject.display, message);
                    Thread.Sleep(2000);

                    if (HotPlugUnplugObject.InLowPowerState != true)
                        plugUnPlugEnum.SetMethod(HotPlugUnplugObject);
                    else
                        base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo.Add(HotPlugUnplugObject);
                    DisplayExtensions.pluggedDisplayList.Remove(HotPlugUnplugObject.display);
                }
                else
                {
                    Log.Fail("Failed to unplug Simulated Display {0}  {1}", HotPlugUnplugObject.display, message);
                    status = false;
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
            else if (HotPlugUnplugObject.FunctionName == FunctionName.SimulationFramework)
            {

                if (base.AppManager.ApplicationSettings.UseDivaFramework || base.AppManager.ApplicationSettings.UseSHEFramework)   //SHE
                {
                    Log.Message("DIVA: Setting GfxValStub Framework to {0}", HotPlugUnplugObject.Status);
                    DivaDeviceSimulation.EnableFramework(HotPlugUnplugObject.Status);

                    if (base.AppManager.ApplicationSettings.UseSHEFramework && !HotPlugUnplugObject.Status)   //SHE
                    {
                        SHE_HotUnplug(DisplayType.DP, false);
                        SHE_HotUnplug(DisplayType.HDMI, false);
                    }
                }
                else
                {
                    EnableULT(HotPlugUnplugObject.Status);
                }
            }
            else if (HotPlugUnplugObject.FunctionName == FunctionName.SimulationFeature)
            {

                if (base.AppManager.ApplicationSettings.UseDivaFramework || base.AppManager.ApplicationSettings.UseSHEFramework)   //SHE
                {
                    Log.Message("DIVA: Setting GfxValStub Feature: {0} to {1}", DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM, HotPlugUnplugObject.Status);
                    DivaDeviceSimulation.EnableFeature(HotPlugUnplugObject.Status, DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM);

                    if (base.AppManager.ApplicationSettings.UseSHEFramework && !HotPlugUnplugObject.Status)   //SHE
                    {
                        SHE_HotUnplug(DisplayType.DP, false);
                        SHE_HotUnplug(DisplayType.HDMI, false);
                    }
                }
                else
                {
                    EnableFeature(HotPlugUnplugObject.Status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_DEV_SIM);
                }
            }
            return status;
        }

        private void UpdateHtPlgHtUnplgObj(HotPlugUnplug HotPlugUnplugObject)
        {
            if (!base.AppManager.ApplicationSettings.UseSHEFramework)    //SHE
            {
                if (string.IsNullOrEmpty(HotPlugUnplugObject.EdidFilePath))
                {
                    string edidFileName = string.Empty;
                    base.AppManager.HotplugUnplugCntx.EDID_Files.TryGetValue(HotPlugUnplugObject.display, out edidFileName);
                    if (string.IsNullOrEmpty(edidFileName))
                        Log.Abort("Edid file not found for plugging display {0}", HotPlugUnplugObject.display.ToString());
                    HotPlugUnplugObject.EdidFilePath = edidFileName;
                }
            }
            
            if (HotPlugUnplugObject.InLowPowerState)
            {
                base.AppManager.HotplugUnplugCntx.PlugUnplugInLowPower = true;
            }
            if (HotPlugUnplugObject.InLowPowerState)
            {
                base.AppManager.HotplugUnplugCntx.PlugUnplugInLowPower = true;
                message = "In LowPower State";
            }
        }

        private DivaDeviceSimulation.DisplayType ConvertToDivaDisplayType(DisplayType display)
        {
            DivaDeviceSimulation.DisplayType divaDispType = DivaDeviceSimulation.DisplayType.None;

            switch (display)
            {
                case DisplayType.CRT:
                    divaDispType = DivaDeviceSimulation.DisplayType.CRT;
                    break;
                case DisplayType.DP:
                case DisplayType.DP_2:
                case DisplayType.DP_3:
                    divaDispType = DivaDeviceSimulation.DisplayType.DP;
                    break;
                case DisplayType.EDP:
                    divaDispType = DivaDeviceSimulation.DisplayType.EDP;
                    break;
                case DisplayType.MIPI:
                    divaDispType = DivaDeviceSimulation.DisplayType.MIPI;
                    break;
                case DisplayType.HDMI:
                case DisplayType.HDMI_2:
                case DisplayType.HDMI_3:
                    divaDispType = DivaDeviceSimulation.DisplayType.HDMI;
                    break;
                case DisplayType.WIDI:
                    divaDispType = DivaDeviceSimulation.DisplayType.WIDI;
                    break;
                case DisplayType.DVI:
                    divaDispType = DivaDeviceSimulation.DisplayType.DVI;
                    break;
                default:
                    break;
            }
            return divaDispType;
        }

        private bool SHE_HotPlug(DisplayType _dipslayType, bool InLowPowerState)     //SHE
        {
            Log.Message("SHE - Performing HotPlug of display {0} ", _dipslayType);
            bool status = false;
            string plugDelay = "0";
            if (InLowPowerState)
            {
                plugDelay = "15";
            }

            SHEDLL.serialPortAccess portaccess = new SHEDLL.serialPortAccess();            
            
            if (_dipslayType == DisplayType.HDMI)
            {
                status = portaccess.SerialWrite("7", plugDelay);
            }
            else if (_dipslayType == DisplayType.DP)
            {
                status = portaccess.SerialWrite("1", plugDelay);
            }
            else if (_dipslayType == DisplayType.DP_2)
            {
                status = portaccess.SerialWrite("3", plugDelay);
            }
            else if (_dipslayType == DisplayType.DP_3)
            {
                status = portaccess.SerialWrite("5", plugDelay);
            }
            else if (_dipslayType == DisplayType.EDP)
            {
                status = portaccess.SerialWrite("9", plugDelay);
            }
            if (status == true)
            {
                Log.Success("SHE - Plugged {0} display", _dipslayType);
            }
            else
            {
                Log.Fail("SHE - Failed to Plug {0} display", _dipslayType);
            }            
            return status;

        }

        private bool SHE_HotUnplug(DisplayType _dipslayType, bool InLowPowerState)   //SHE
        {
            Log.Message("SHE - Performing HotUnPlug of display {0} ", _dipslayType);
            bool status = false;
            string plugDelay = "0";
            if (InLowPowerState)
            {
                plugDelay = "15";
            }
            
            SHEDLL.serialPortAccess portaccess = new SHEDLL.serialPortAccess(); 
            if (_dipslayType == DisplayType.HDMI)
            {
                status = portaccess.SerialWrite("8", plugDelay);
            }
            else if (_dipslayType == DisplayType.DP)
            {
                status = portaccess.SerialWrite("2", plugDelay);
            }
            else if (_dipslayType == DisplayType.DP_2)
            {
                status = portaccess.SerialWrite("4", plugDelay);
            }
            else if (_dipslayType == DisplayType.DP_3)
            {
                status = portaccess.SerialWrite("6", plugDelay);
            }
            else if (_dipslayType == DisplayType.EDP)
            {
                status = portaccess.SerialWrite("10", plugDelay);
            }
            if (status == true)
            {
                Log.Success("SHE - UnPlugged {0} display", _dipslayType);
            }
            else
            {
                Log.Fail("SHE - Failed to Unplug {0} display", _dipslayType);
            }            
            return status;

        }

        private bool ULT_FW_PlugDisplay(uint displayUID, bool plugType, List<byte> EdidData, List<byte> dpcdData, bool IslowPower = false)
        {
            bool status=true;

            ULT_DEVICE_INFO ult_Device_Info = new ULT_DEVICE_INFO();
            ult_Device_Info.bAttach = plugType;
            ult_Device_Info.OpType =(uint) ULT_OP_TYPE.OP_SET;
            ult_Device_Info.ulDisplayUID = displayUID;
            ult_Device_Info.bDisplayEdid = new byte[768];
            ult_Device_Info.bSimConnectionInLowPower = IslowPower;

            if (plugType == true)
            {
                for (int i = 0; i < EdidData.Count; i++)
                {
                    ult_Device_Info.bDisplayEdid[i] = EdidData[i];
                }

                if (dpcdData.Count != 0)
                {
                    status = ProgramAllDPCDData(displayUID, dpcdData);
                }
            }
            
            if (status == true)
            {
                ULT_ESC_GET_SET_DEVICE_CONNECTIVITY_ARGS escParams = new ULT_ESC_GET_SET_DEVICE_CONNECTIVITY_ARGS();
                escParams.stDeviceInfo = new ULT_DEVICE_INFO[20];
                escParams.ulEscapeDataSize = (uint)Marshal.SizeOf(escParams) - 16;
                escParams.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_GET_SET_SIMULATE_DEVICE;
                escParams.ulNumDevices = 1;// (uint)displayList.Count;
                escParams.stDeviceInfo[0] = ult_Device_Info;

                if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_GET_SET_SIMULATE_DEVICE, escParams))
                {
                    status = false;
                }

                if (escParams.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(escParams.dwRetErrorCode);
                    status = false;
                }
           
            }
            return status;
        }
        internal bool ProgramAllDPCDData(uint displayUID, List<byte> dpcdData)
        {
            bool status = true;
            List<byte> ucDPCDs_202_204 = new List<byte> { 0xFF, 0xFF, 0xFF };
            List<byte> ucDPCDs_10_1F = new List<byte> { 0xA4, 0x1F, 0xBC, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

            //Write 14 bytes of DPCD data from _DPCD.bin file.
            status &= ULT_FW_WriteDPCD(displayUID, 0x0, dpcdData.ToList());

            //write ucDPCDs_202_204[] to address 202
            if(status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x202, ucDPCDs_202_204);

            //write 0 to address 101
            if (status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x101, 0);

            //write 0 to address 200
            if (status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x200, 0);

            //write 0 to address 206
            if (status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x206, 0);

            //write ucDPCDs_10_1F[] to address 202
            if (status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x10, ucDPCDs_10_1F);

            //write 0 to address 600
            if (status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x600, 1);

            //write 0 to address 205
            if (status)
            status &= ULT_FW_WriteDPCD(displayUID, 0x205, 1);

            return status;
        }

        internal bool ULT_FW_WriteDPCD(uint displayUID, uint address, byte DPCDByte)
        {
            List<byte> DPCDData = new List<byte>();
            DPCDData.Add(DPCDByte);

            return ULT_FW_WriteDPCD(displayUID, address, DPCDData);
        }

        internal bool ULT_FW_WriteDPCD(uint displayUID, uint address, List<byte> DPCDData)
        {
            bool status = true;
            ULT_ESC_DPCD_INFO escParams = new ULT_ESC_DPCD_INFO();
            escParams.ulEscapeDataSize = (uint)Marshal.SizeOf(escParams) - 16;
            escParams.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_SET_DPCD_INFO;
            escParams.bDPCDData = new byte[512];

            escParams.ulDisplayUID = displayUID;
            escParams.ulDPCDAddress = address;
            escParams.ulSize = (uint)DPCDData.Count;

            for (int i = 0; i < DPCDData.Count; i++)
            {
                escParams.bDPCDData[i] = DPCDData[i];
            }

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_SET_DPCD_INFO, escParams))
            {
                status = false;
                Log.Fail(String.Format("Failed to write DPCD Data with address: {0} for UID:{1}", address, displayUID));
            }

            if (escParams.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(escParams.dwRetErrorCode);
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
                    {// openDVMU();
                    }
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

        private bool GetAvailableDisplayUID(DisplayType display, ref uint displayUID)
        {
            bool status = false;
            List<ULT_DISPLAY_DETAILS_ARGS> supportedDisplaysList = new List<ULT_DISPLAY_DETAILS_ARGS>();

            ULT_ESC_ENUM_DEVICE_ARGS ult_Esc_Args = new ULT_ESC_ENUM_DEVICE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENUM_DEVICE;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.stDisplayDetailsArgs = new ULT_DISPLAY_DETAILS_ARGS[36];

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_ENUM_DEVICE, ult_Esc_Args))
            {
                return false;
            }

            if (ult_Esc_Args.dwRetErrorCode != 0)
            {
                CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                return false;
            }

            supportedDisplaysList.AddRange(ult_Esc_Args.stDisplayDetailsArgs);

            //Getting all displays which were currently attached.
            List<ULT_DISPLAY_DETAILS_ARGS> attachedDisplays = new List<ULT_DISPLAY_DETAILS_ARGS>();
            base.EnumeratedDisplays.ForEach(enumeratedDisplay =>
                {
                    attachedDisplays.AddRange(supportedDisplaysList.Where(item => item.ulDisplayUID == enumeratedDisplay.WindowsMonitorID).ToList());
                });


            //Removing attached displays from list
            supportedDisplaysList.RemoveAll(item => attachedDisplays.Contains(item));

            //Fetching attached displays to the same port. And remove it from the list.
            List<ULT_DISPLAY_DETAILS_ARGS> ToRemove = new List<ULT_DISPLAY_DETAILS_ARGS>();

            attachedDisplays.ForEach(attachedItem =>
            {
                ToRemove.AddRange(supportedDisplaysList.Where(item => GetPhysicalPortConnected(item.ePortType) == GetPhysicalPortConnected(attachedItem.ePortType)));
            });
            supportedDisplaysList.RemoveAll(item => ToRemove.Contains(item));

            if (supportedDisplaysList.Count == 0)
            {
                return false;
            }

            //get the difference of the displays and return a display.
            List<ULT_DISPLAY_DETAILS_ARGS> displaysSamePort = supportedDisplaysList.Where(eachElement => supportedDisplaysList.Where(item => GetPhysicalPortConnected(item.ePortType) == GetPhysicalPortConnected(eachElement.ePortType)).ToList().Count == 1).ToList();
            foreach (ULT_DISPLAY_DETAILS_ARGS dispDetails in displaysSamePort)
            {
                if (GetConnectorType(dispDetails.ePortType) == DisplayExtensions.GetDisplayType(display))
                {
                    status = true;
                    displayUID = dispDetails.ulDisplayUID;
                    break;
                }
            }

            if (displayUID == 0)
            {
                //get any display matching to the displaytype.
                foreach (ULT_DISPLAY_DETAILS_ARGS dispDetails in supportedDisplaysList)
                {
                    if (GetConnectorType(dispDetails.ePortType) == display)
                    {
                        status = true;
                        displayUID = dispDetails.ulDisplayUID;
                        break;
                    }
                }
            }

            return status;
        }

        private PORT GetPhysicalPortConnected(ULT_PORT_TYPE displayPort)
        {
            PORT actualPort= PORT.NONE;

            switch (displayPort)
            {
                case ULT_PORT_TYPE.ULT_INTDPA_PORT:
                case ULT_PORT_TYPE.ULT_DVOA_PORT:
                case ULT_PORT_TYPE.ULT_INTMIPIA_PORT:
                case ULT_PORT_TYPE.ULT_LVDS_PORT:
                    actualPort = PORT.PORTA;
                    break;
                case ULT_PORT_TYPE.ULT_INTDPB_PORT:
                case ULT_PORT_TYPE.ULT_DVOB_PORT:
                case ULT_PORT_TYPE.ULT_INTHDMIB_PORT:
                    actualPort = PORT.PORTB;
                    break;
                case ULT_PORT_TYPE.ULT_INTDPC_PORT:
                case ULT_PORT_TYPE.ULT_DVOC_PORT:
                case ULT_PORT_TYPE.ULT_INTHDMIC_PORT:
                case ULT_PORT_TYPE.ULT_INTMIPIC_PORT:
                    actualPort = PORT.PORTC;
                    break;
                case ULT_PORT_TYPE.ULT_INTDPD_PORT:
                case ULT_PORT_TYPE.ULT_DVOD_PORT:
                case ULT_PORT_TYPE.ULT_INTHDMID_PORT:
                    actualPort = PORT.PORTD;
                    break;
                case ULT_PORT_TYPE.ULT_ANALOG_PORT:
                    actualPort = PORT.PORTE;
                    break;
                case ULT_PORT_TYPE.ULT_TPV_PORT:
                    actualPort = PORT.TVPORT;
                    break;
                default:
                    actualPort = PORT.NONE;
                    break;
            }

            return actualPort;
        }

        internal DisplayType GetConnectorType(ULT_PORT_TYPE displayPort)
        {
            switch (displayPort)
            {
                case ULT_PORT_TYPE.ULT_INTDPB_PORT:
                case ULT_PORT_TYPE.ULT_INTDPC_PORT:
                case ULT_PORT_TYPE.ULT_INTDPD_PORT:
                    return DisplayType.DP;
                case ULT_PORT_TYPE.ULT_INTHDMIB_PORT:
                case ULT_PORT_TYPE.ULT_INTHDMIC_PORT:
                case ULT_PORT_TYPE.ULT_INTHDMID_PORT:
                case ULT_PORT_TYPE.ULT_DVOB_PORT:
                case ULT_PORT_TYPE.ULT_DVOC_PORT:
                case ULT_PORT_TYPE.ULT_DVOD_PORT:
                    return DisplayType.HDMI;
                case ULT_PORT_TYPE.ULT_INTDPA_PORT:
                    return DisplayType.EDP;
                case ULT_PORT_TYPE.ULT_ANALOG_PORT:
                    return DisplayType.CRT;
                case ULT_PORT_TYPE.ULT_INTMIPIA_PORT:
                case ULT_PORT_TYPE.ULT_INTMIPIC_PORT:
                    return DisplayType.MIPI;
                default:
                    return DisplayType.None;
            }
        }

        private bool GetDeviceConnectedStatus(uint displayUID)
        {
            bool status = false;
            ULT_ESC_GET_DEVICE_CONNECTIVITY_ARGS ult_Esc_Args = new ULT_ESC_GET_DEVICE_CONNECTIVITY_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_DEVICE_CONNECTIVITY;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ult_Esc_Args.ulDisplayUID = displayUID;


            if (DoULTEscape(ULT_ESCAPE_CODE.ULT_DEVICE_CONNECTIVITY, ult_Esc_Args))
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                    status = false;
                }
                else
                {
                    status = ult_Esc_Args.bAttached;
                }
            }
            return status;
        }

        private void EnableULT(bool status)
        {
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.bEnableULT = status;

            Log.Message("Setting ULT Framework to {0}", status);

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                }
            }
        }
        private void EnableFeature(bool status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = status;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            Log.Message("Setting ULT Feature: {0} to {1}", featureType, status);

            if (!DoULTEscape(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE, ult_Esc_Args))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                if (ult_Esc_Args.dwRetErrorCode != 0)
                {
                    CommonExtensions.PrintULTErrorCodes(ult_Esc_Args.dwRetErrorCode);
                }
            }
        }

        private bool DoULTEscape(ULT_ESCAPE_CODE escapeCode, object Ult_Esc_Args)
        {
            bool status = true;

            ULT_Framework u = new ULT_Framework();
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(escapeCode, Ult_Esc_Args);
            if (!u.SetMethod(escapeParams))
            {
                Log.Fail(String.Format("Failed to perform: {0}", escapeParams.ULT_Escape_Type));
                status = false;
            }

            return status;
        }

    }
}
