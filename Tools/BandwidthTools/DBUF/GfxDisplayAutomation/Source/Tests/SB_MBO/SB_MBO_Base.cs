namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Threading;
    using System.IO;
    using System.Diagnostics;
    using System.Drawing;
    using Microsoft.Win32;
    using System.Collections.Generic;

    public class SB_MBO_Base : TestBase
    {
       protected List<DisplayType> _pluggableDisplays  = null;
       protected Dictionary<DisplayType, string> _availableDisplays = null;
       private int failSafeRetryCount = 0;
       private bool isProcessExitReq = true;
       private const string eventName1 = "MBO_ENABLE";
       private const string eventName2 = "PSR_STATUS_REG";
       private const string eventName3 = "MBO_NV12_EN";
       private const string eventName4 = "DC6_STATE_DIS";
       private const string eventName5 = "DC6_STATE_EN";
       private const string eventName6 = "MBO_DISABLE";

       public SB_MBO_Base()
       {
           _availableDisplays = new Dictionary<DisplayType, string>();
           _availableDisplays.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
           _availableDisplays.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");

           _availableDisplays.Add(DisplayType.DP, "DP_3011.EDID");
           _availableDisplays.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");

           _pluggableDisplays = new List<DisplayType>();          
       }
       protected void MBO_RegEdit(int argValue)
       {
           Log.Message(true, "Make changes in Registry for Enabling MBO_Feature...");
           RegistryParams registryParams = new RegistryParams();
           registryParams.value = argValue;
           registryParams.infChanges = InfChanges.ModifyInf;
           registryParams.registryKey = Registry.LocalMachine;
           registryParams.keyName = "MBOFeatureSupport";
           AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
       }
       protected void ApplyConfigOS(DisplayConfig argDispConfig)
       {
           if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
               Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
           else
               Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
       }
       public virtual void VerifyConfigOS(DisplayConfig argDisplayConfig)
       {
           Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
           DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
           if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
           {
               Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
           }
           else
               Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
       }
       protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
       {
           Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
           argSelectedMode.display = argDisplayType;
           if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
               Log.Success("Mode applied Successfully");
           else
               Log.Fail("Fail to apply Mode");
       }
       protected void PlayVideo()
       {
           Log.Message(true, "Play clip");
           if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO"))
           {
               Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO");
           }
           if (isProcessExitReq)
           {
               Process[] explorerProcess = Process.GetProcessesByName("explorer");
               if (explorerProcess.Length > 0)
               {
                   foreach (Process p in explorerProcess)
                       p.Kill();
               }
           }
           CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO");

           string fileName = Path.GetFileName("Wildlife.wmv");

           if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
               SendKeys.SendWait("{F11}");
           Thread.Sleep(3000);
           AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, fileName);
           Thread.Sleep(5000);
       }       
       protected void StopVideo()
       {
           SendKeys.SendWait("%{F4}");
           Thread.Sleep(1000);
           Process[] explorerProcess = Process.GetProcessesByName("explorer");
           if (explorerProcess.Length > 0)
           {
               foreach (Process p in explorerProcess)
                   p.Kill();
           }
           isProcessExitReq = false;
       }
     
       protected void PlugDisplays()
       {
           base.CurrentConfig.DisplayList.ForEach(curDisp =>
           {
               if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
               {
                   base.HotPlug(curDisp, _availableDisplays[curDisp]);
                   _pluggableDisplays.Add(curDisp);
               }
           });
       }
       protected void UnPlugDisplays()
       {
           _pluggableDisplays.ForEach(curDisp =>
           {
               base.HotUnPlug(curDisp);
           });
           base.CleanUpHotplugFramework();
       }
       protected bool RegisterCheck(DisplayType display, DisplayInfo displayInfo,string eventName)
       {
           PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
           
           PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
           if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false))
           {
               Log.Success("Registers Verified for Event {0} on Display {1}", eventName, display);
               CheckWatermark(display);
               return true;
           }
           else
           {
               Log.Alert("Registers Mismatch for event {0} on display {1}", eventName, display);
               return false;
           }
       }
       protected DisplayHierarchy GetDispHierarchy(List<DisplayType> argCustomDisplayList, DisplayType argDisplayType)
       {
           int index = argCustomDisplayList.FindIndex(dT => dT != DisplayType.None && dT == argDisplayType);
           switch (index)
           {
               case 0:
                   return DisplayHierarchy.Display_1;
               case 1:
                   return DisplayHierarchy.Display_2;
               case 2:
                   return DisplayHierarchy.Display_3;
               case 3:
                   return DisplayHierarchy.Display_4;
               case 4:
                   return DisplayHierarchy.Display_5;
               default:
                   return DisplayHierarchy.Unsupported;
           }
       }
       protected bool VerifyMBOEnable()
       {
           Log.Message("Verifying MBO_Enable...");
           DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();
           DisplayHierarchy dh = this.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, DisplayType.EDP);
           if (RegisterCheck(DisplayType.EDP, displayInfo, eventName1))
           {
               failSafeRetryCount = 0;
               if (VerifyDPCDValue())
                   return true;
               else
                   return false;
           }
           else
           {
               failSafeRetryCount++;
               if(failSafeRetryCount<=3)
               {
                   Log.Message("Relaunching Video");
                   this.StopVideo();
                   this.PlayVideo();
                   Thread.Sleep(2000);
                   if (this.VerifyMBOEnable())
                       return true;
                   else
                       return false;
               }
               else
               {
                   Log.Fail("Registers Match Failed for event {0}", eventName1);
                   failSafeRetryCount = 0;
                   return false;
               }
           }
       }
       protected bool VerifyDPCDValue()
       {
           DpcdInfo dpcd = new DpcdInfo();
           dpcd.Offset = Convert.ToUInt32("00170", 16);
           dpcd.DispInfo = base.EnumeratedDisplays.Find(dI => dI.DisplayType == DisplayType.EDP);
           Thread.Sleep(3000);
           AccessInterface.GetFeature<DpcdInfo, DpcdInfo>(Features.DpcdRegister, Action.GetMethod, Source.AccessAPI, dpcd);

           RegisterInf reginfo = new RegisterInf("00170", "00000007", "7");

           if (CompareRegisters(dpcd.Value, reginfo))
           {
               Log.Success("DPCD register verification successful");
               failSafeRetryCount = 0;
               if (VerifyPSR())
                   return true;
               else
                   return false;
           }
           else
           {
               failSafeRetryCount++;
               if (failSafeRetryCount <= 3)
               {
                   Log.Alert("DPCD Register Mismatch");
                   Log.Message("Relaunching Video");
                   this.StopVideo();
                   this.PlayVideo();
                   Thread.Sleep(2000);
                   if (this.VerifyDPCDValue())
                       return true;
                   else
                       return false;
               }
               else
               {
                   Log.Fail("DPCD register verification Failed");
                   failSafeRetryCount = 0;
                   return false;
               }
           }
       }
       protected bool VerifyPSR()
       {
           Log.Message("Verifying PSR_Entered...");
           DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();
           DisplayHierarchy dh = this.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, DisplayType.EDP);
           RegisterCheck(DisplayType.EDP, displayInfo, eventName2);
           if(VerifyDC6_State())
               return true;
           else
               return false;
       }
       protected bool VerifyNV12()
       {
           Log.Message(" -> Verifying NV12...");
           EventInfo eventInfo = new EventInfo();
           eventInfo = new EventInfo();
           eventInfo.pipe = PIPE.NONE;
           eventInfo.plane = PLANE.PLANE_A;
           eventInfo.port = PORT.NONE;
           eventInfo.eventName = eventName3;
           EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
           Log.Message("the event MBO_NV12 has {0} reg events ", returnEventInfo.listRegisters.ToList().Count());
           if(CompareRegisters(returnEventInfo.listRegisters[0].BitmappedValue, returnEventInfo.listRegisters[0]))
           {
               Log.Success("NV12 - Enabled");
               return true;
           }
           else
           {
               Log.Success("NV12 - Disabled");
               return false;
           }
       }
       protected bool VerifyDC6_State()
       {
           Log.Message("Verifying DC6_Sate...");
           DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();
           DisplayHierarchy dh = this.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, DisplayType.EDP);

           if (VerifyNV12())
           {
               Log.Message("NV12_Enabled Hence Checking DC6_State_Disable Register...");
               EventInfo eventInfo = new EventInfo();
               eventInfo = new EventInfo();
               eventInfo.pipe = PIPE.PIPE_EDP;
               eventInfo.plane = PLANE.NONE;
               eventInfo.port = PORT.NONE;
               eventInfo.eventName = eventName4;
               EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
               Log.Message("the event DC6_STATE_Disable has {0} reg events ", returnEventInfo.listRegisters.ToList().Count());
               if (RegisterCheck(DisplayType.EDP, displayInfo, eventName4))
                   return true;
               else
                   return false;
           }
           else
           {
               Log.Message("NV12_Disabled Hence Checking DC6_State_Enable Register...");
               EventInfo eventInfo = new EventInfo();
               eventInfo = new EventInfo();
               eventInfo.pipe = PIPE.PIPE_EDP;
               eventInfo.plane = PLANE.NONE;
               eventInfo.port = PORT.NONE;
               eventInfo.eventName = eventName5;
               EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
               Log.Message("the event DC6_STATE_Enable has {0} reg events ", returnEventInfo.listRegisters.ToList().Count());
               if (RegisterCheck(DisplayType.EDP, displayInfo, eventName5))
                   return true;
               else
                   return false;
           }
       }
       protected bool VerifyMBODisable()
       {
           Log.Message("Verifying MBO_Disable...");
           DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.EDP).FirstOrDefault();
           DisplayHierarchy dh = this.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, DisplayType.EDP);
           if (RegisterCheck(DisplayType.EDP, displayInfo, eventName6))
           {
               failSafeRetryCount = 0;
               return true;
           }
           else
           {
               failSafeRetryCount++;
               if (failSafeRetryCount <= 2)
               {
                   Log.Message("Relaunching Video");
                   this.StopVideo();
                   this.PlayVideo();
                   if (this.VerifyMBODisable())
                       return true;
                   else
                       return false;
               }
               else
               {
                   Log.Fail("Registers Match Failed for event {0}", eventName6);
                   failSafeRetryCount = 0;
                   return false;
               }
           }
       }
       protected void ApplySDEDP()
       {
           DisplayConfig sdEDPConfig = new DisplayConfig
           {
               ConfigType = DisplayConfigType.SD,
               PrimaryDisplay = DisplayType.EDP
           };
           this.ApplyConfigOS(sdEDPConfig);
       }
       protected void SwitchToACMode()
       {
           Log.Message(true, "Enable AC Mode");
           PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

           if (powerState == PowerLineStatus.Offline)
           {
               if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                   Log.Success("System is Running in AC Mode");
               else
                   Log.Fail("Fail to set AC mode");
           }
           else
               Log.Success("System is Running in AC Mode");
       }
       protected void SwitchToDCMode()
       {
           Log.Message(true, "Enable DC Mode");
           PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

           if (powerState == PowerLineStatus.Online)
           {
               if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                   Log.Success("System is Running in DC Mode");
               else
                   Log.Fail("Fail to set DC Mode");
           }
           else
               Log.Success("System is Running in DC Mode");

       }
       protected DisplayMode GetAppliedMode(DisplayType argDisplayType)
       {
           DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
           DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
           return currentMode;
       }
    }
}
