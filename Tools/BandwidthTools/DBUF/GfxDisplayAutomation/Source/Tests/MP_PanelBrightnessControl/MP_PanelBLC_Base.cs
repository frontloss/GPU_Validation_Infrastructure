namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;
    using Microsoft.Win32;

    public enum PanelOnOffEvent
    {
        IGD_PANEL_POWER_OFF,
        IGD_PANEL_POWER_ON,
        IGD_BACKLIGHT_ON,
        IGD_BACKLIGHT_OFF
    }

    class MP_PanelBLC_Base : TestBase
    {
        private PanelDeviceDriverParam PanelDriverParam;
        private PanelDriverInstallUnInstallParam InstallUnInstallParam;
        private PanelDriverAccessParam PanelAccessParam;
        protected RegistryParams registryParams;
        protected List<PanelBLCData> PanelBrightnessControlData;

        private string LogFilePath = @"C:\PanelBLCLogger.txt";
        private string DriverLogFile;
        internal Int64 PanelPowerOnTimmings = 0;
        internal Int64 BackLightOnTimmings = 0;
        private Int64 PanelPowerOnMaxTime = 400;

        internal bool FastModeSet = false;
        internal bool PanelBacklightOff = false;

        internal Dictionary<PanelBLCEventName, System.Action> BacklightOnTimmingsCall;

        public MP_PanelBLC_Base()
        {
            PanelBrightnessControlData = new List<PanelBLCData>();
            PanelDriverParam = new PanelDeviceDriverParam();
            registryParams = new RegistryParams();

            InstallUnInstallParam = new PanelDriverInstallUnInstallParam();
            PanelAccessParam = new PanelDriverAccessParam();
            PanelAccessParam.DriverStringPattern = "PanelBLC";

            BacklightOnTimmingsCall = new Dictionary<PanelBLCEventName, System.Action>();
            BacklightOnTimmingsCall.Add(PanelBLCEventName.IGD_BACKLIGHT_ON, ValidateBackLightOnTimmings);
            DriverLogFile = CommonExtensions._cmdLineArgs.First() + "_PanelDriverLog.dat";
        }

        internal void SetEnvironment()
        {
            File.Delete(LogFilePath);
            File.Delete(DriverLogFile);
            if (SupportedPlatform() == false)
            {
                Log.Abort("Panel Brightness Control Feature dosen't support with currect platform {0}", base.MachineInfo.PlatformDetails.Platform);
            }
            UpdatePanelDriverProperty();
            Log.Message(true, "Test Pre Condition to enable panel BLC");
            DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.GetInternalDisplay() };
            Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Message("Config (SD {0}) applied successfully", displayConfig.PrimaryDisplay);
            else
            {
                Log.Abort("Config (SD {0}) not applied!", displayConfig.PrimaryDisplay);
            }

            if (!CommonExtensions.HasRetryThruRebootFile())
            {
                if (VerifyDriverUpdateStatus() && PanelDriverStatus())
                {
                    Log.Verbose("Panel Backlight Control Stub Driver already installed and Running");
                    EnableDisablePanelBLCInterface(4);
                    EnablePanelDriverPath();
                }
                else
                {
                    EnableDisablePanelBLCInterface(4);
                    if (InstallPanelDriver())
                    {
                        Log.Success("Successfully Installed Panel Brightness Control Stub Driver");
                        File.Delete(LogFilePath);
                        CommonExtensions.WriteRetryThruRebootInfo();
                        this.InvokePowerEvent(new PowerParams() { Delay = 5, PowerStates = PowerStates.S5 }, PowerStates.S5);
                    }
                    else
                        Log.Abort("Unable to installed Panel Brightness Control Stub Driver");
                }
            }
            else
            {
                EnableDisablePanelBLCInterface(4);
                EnablePanelDriverPath();
            }
        }

        internal void EnablePanelDriverPath()
        {
            if (DisablePanelDriver())
                Log.Message("Successfully Disabled Panel Brightness Control Stub Driver");
            else
                Log.Abort("Failed to Disabled Panel Brightness Control Stub Driver");

            if (EnablePanelDriver())
                Log.Message("Successfully Enabled Panel Brightness Control Stub Driver");
            else
                Log.Abort("Failed to Enabled Panel Brightness Control Stub Driver");

            File.Delete(LogFilePath);
        }

        internal bool InstallPanelDriver()
        {
            UninstallPanelDriver();
            PanelDriverParam.ServiceType = NonPnPDriverService.Install;
            Log.Verbose("Installing Panel Brightness Control Stub Driver");
            AccessInterface.SetFeature<bool, PanelDeviceDriverParam>(Features.NonPnPDriverRoutine, Action.SetMethod, PanelDriverParam);
            if (PanelDriverStatus())
                return true;
            else
                return false;

        }
        internal bool VerifyDriverUpdateStatus()
        {
            Log.Verbose("Verify Panel Brightness Control Driver Upgrade Status");
            PanelDriverParam.ServiceType = NonPnPDriverService.VerifyDriverUpdate;
            return AccessInterface.SetFeature<bool, PanelDeviceDriverParam>(Features.NonPnPDriverRoutine, Action.SetMethod, PanelDriverParam);
        }
        internal bool PanelDriverStatus()
        {
            PanelDriverParam.ServiceType = NonPnPDriverService.Status;
            Log.Verbose("Get Panel Brightness Control Driver Status"); 
            return AccessInterface.SetFeature<bool, PanelDeviceDriverParam>(Features.NonPnPDriverRoutine, Action.SetMethod, PanelDriverParam);
        }
        internal bool EnablePanelDriver()
        {
            Log.Verbose("Enabling Panel Brightness Control Stub Driver");
            PanelDriverParam.ServiceType = NonPnPDriverService.Enable;
            return AccessInterface.SetFeature<bool, PanelDeviceDriverParam>(Features.NonPnPDriverRoutine, Action.SetMethod, PanelDriverParam);
        }
        internal bool DisablePanelDriver()
        {
            Log.Verbose("Disabling Panel Brightness Control Stub Driver");
            PanelDriverParam.ServiceType = NonPnPDriverService.Disable;
            return AccessInterface.SetFeature<bool, PanelDeviceDriverParam>(Features.NonPnPDriverRoutine, Action.SetMethod, PanelDriverParam);
        }
        internal bool UninstallPanelDriver()
        {
            Log.Verbose("Un-install Panel Brightness Control Stub Driver");
            PanelDriverParam.ServiceType = NonPnPDriverService.UnInstall;
            return AccessInterface.SetFeature<bool, PanelDeviceDriverParam>(Features.NonPnPDriverRoutine, Action.SetMethod, PanelDriverParam);
        }
        internal void EnableDisablePanelBLCInterface(int argKeyValue)
        {
            Log.Message("Make changes in Registry to {0} Panel Driver Interface", (argKeyValue == 4) ? "Enable" : "Disable");
            registryParams.value = argKeyValue;
            registryParams.infChanges = InfChanges.ModifyInf;
            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "PanelDriver";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        internal List<PanelBLCData> ParsePanelBrightnessControl()
        {
            Log.Verbose("Get Panel Brightness Control log file data");

            PanelBrightnessControlData = AccessInterface.GetFeature<List<PanelBLCData>, string>(Features.PanelBLCInfo, Action.GetMethod, Source.AccessAPI, InstallUnInstallParam.DriverpackagePath);
            return RemoveDuplidateCallSequence();
        }
        private void UpdatePanelDriverProperty()
        {
            InstallUnInstallParam.DriverpackagePath = Directory.GetCurrentDirectory() + @"\PanelBLC";
            if(base.MachineInfo.PlatformDetails.Platform == Platform.SKL)
                InstallUnInstallParam.RegKeyName = "PanelBLC_OLED.reg";
            else if(base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
                InstallUnInstallParam.RegKeyName = "PanelBLC_Xiaomi.reg";

            InstallUnInstallParam.DriverBinaryName = "PanelBLC.sys";
            InstallUnInstallParam.INFFileName = "PanelBLC.inf";

            PanelDriverParam.InstallParam = InstallUnInstallParam;
            PanelDriverParam.AccessParam = PanelAccessParam;
        }
        private bool SupportedPlatform()
        {
            if (base.MachineInfo.PlatformDetails.Platform == Platform.SKL ||
               (base.MachineInfo.PlatformDetails.Platform == Platform.CHV))
                return true;
            else
                return false;
        }

        private List<PanelBLCData> RemoveDuplidateCallSequence()
        {
            List<PanelBLCData> temp = new List<PanelBLCData>();
            for (int indx = 0; indx < PanelBrightnessControlData.Count; )
            {
                if (ValidateDuplicateEntry(indx) == false)
                {
                    temp.Add(PanelBrightnessControlData[indx++]);
                }
                else
                {
                    int currentTempIndx = temp.Count - 1;
                    if (currentTempIndx >= 1)
                    {
                        if (temp[currentTempIndx - 1].PanelNotifyEvent != null)
                        {
                            if (temp[currentTempIndx - 1].PanelNotifyEvent.EventName != PanelBrightnessControlData[indx].PanelNotifyEvent.EventName)
                            {
                                temp.Add(PanelBrightnessControlData[indx]);
                                temp.Add(PanelBrightnessControlData[indx + 1]);
                            }
                        }
                        else
                        {
                            temp.Add(PanelBrightnessControlData[indx]);
                            temp.Add(PanelBrightnessControlData[indx + 1]);
                        }
                    }
                    else
                    {
                        temp.Add(PanelBrightnessControlData[indx]);
                        temp.Add(PanelBrightnessControlData[indx + 1]);
                    }
                    indx += 2;
                }
            }
            RemoveMultipleOnOffCall(ref temp);
            VerifyBacklightOffState(temp);
            VerifyFastModeSet(temp);
            return temp;
        }

        private void RemoveMultipleOnOffCall(ref List<PanelBLCData> panelData)
        {
            //this algorithm will look for below consicutive call sequence.
            //event name IGD_PANEL_POWER_OFF event type IGD_EVENT_TYPE_PRE_EVENT
            //event name IGD_PANEL_POWER_OFF event type IGD_EVENT_TYPE_POST_EVENT
            //event name IGD_PANEL_POWER_ON event type IGD_EVENT_TYPE_PRE_EVENT
            //event name IGD_PANEL_POWER_ON event type IGD_EVENT_TYPE_POST_EVENT
            //sequenceIndex List will store start index of two consicutive OnOff call sequence.

            List<NotifyEvent> PanelOffOnSequence = new List<NotifyEvent>();
            PanelOffOnSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            PanelOffOnSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            PanelOffOnSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            PanelOffOnSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            List<int> sequenceIndex = new List<int>();

            for (int idx = 0; idx < panelData.Count; idx++)
            {
                
                if (panelData[idx].PanelNotifyEvent != null)
                {
                    if (panelData[idx].PanelNotifyEvent.EventName == PanelBLCEventName.IGD_PANEL_POWER_OFF)
                    {
                        int seqIndx;
                        for (seqIndx = 0; seqIndx < PanelOffOnSequence.Count; seqIndx++)
                        {
                            if (panelData[idx + seqIndx] != null)
                            {
                                if (panelData[idx + seqIndx].PanelNotifyEvent != null)
                                {
                                    if (PanelOffOnSequence[seqIndx].EventName != panelData[idx + seqIndx].PanelNotifyEvent.EventName &&
                                        PanelOffOnSequence[seqIndx].EventType != panelData[idx + seqIndx].PanelNotifyEvent.EventType)
                                        break;
                                }
                                else
                                {
                                    //if sequence is not notify event, break it.
                                    break;
                                }
                            }
                        }
                        if (seqIndx == PanelOffOnSequence.Count)
                        {
                            sequenceIndex.Add(idx);
                            idx = idx + (seqIndx - 1);
                        }
                    }
                }

            }

            //Remove Duplicate entity from list.
            for (int idx = 0; idx < PanelOffOnSequence.Count - 1; idx+=2)
            {
                int nextIndx = idx + 1;
                if (sequenceIndex.Count > nextIndx)
                {
                    if ((sequenceIndex[nextIndx] - sequenceIndex[idx]) == PanelOffOnSequence.Count)
                    {
                        panelData.RemoveRange(sequenceIndex[nextIndx], PanelOffOnSequence.Count);
                        for (int ChangeIndex = nextIndx + 1; ChangeIndex < sequenceIndex.Count; ChangeIndex++)
                        {
                            sequenceIndex[ChangeIndex] -= PanelOffOnSequence.Count;
                        }
                    }
                }
            }
        }

        private void VerifyBacklightOffState(List<PanelBLCData> panelData)
        {
            foreach (PanelBLCData panelEvent in panelData)
            {
                if (panelEvent.PanelNotifyEvent != null)
                {
                    if (panelEvent.PanelNotifyEvent.EventName == PanelBLCEventName.IGD_BACKLIGHT_OFF)
                    {
                        PanelBacklightOff = true;
                        break;
                    }
                }
            }
        }

        private void VerifyFastModeSet(List<PanelBLCData> panelData)
        {
            for (int idx = 0; idx < panelData.Count; idx++)
            {
                int nxtIndex = idx + 1;
                if (panelData.Count > nxtIndex)
                {
                    if (panelData[idx].PanelNotifyEvent != null &&
                        panelData[nxtIndex].PanelNotifyEvent != null)
                    {
                        if ((panelData[idx].PanelNotifyEvent.EventName == PanelBLCEventName.IGD_SYSTEM_D0) &&
                            (panelData[nxtIndex].PanelNotifyEvent.EventName == PanelBLCEventName.IGD_BACKLIGHT_ON))
                        {
                            FastModeSet = true;
                            break;
                        }
                    }
                }
            }
        }

        private bool ValidateDuplicateEntry(int idx)
        {
            PanelOnOffEvent OnOffEvent;
            if (PanelBrightnessControlData[idx].PanelNotifyEvent != null)
            {
                if (Enum.TryParse<PanelOnOffEvent>(PanelBrightnessControlData[idx].PanelNotifyEvent.EventName.ToString(), out OnOffEvent))
                {
                    if (idx <= PanelBrightnessControlData.Count - 2)
                    {
                        if (PanelBrightnessControlData[idx + 1].PanelNotifyEvent != null)
                        {
                            if ((PanelBrightnessControlData[idx].PanelNotifyEvent.EventName == PanelBrightnessControlData[idx + 1].PanelNotifyEvent.EventName) &&
                                (PanelBrightnessControlData[idx].PanelNotifyEvent.EventType == PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT) &&
                                (PanelBrightnessControlData[idx + 1].PanelNotifyEvent.EventType == PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT))
                                return true;
                        }
                    }
                }
            }
            return false;
        }

        internal void ValidateBackLightOnTimmings()
        {
            if (PanelPowerOnTimmings != null && BackLightOnTimmings != null)
            {
                Int64 delta = (BackLightOnTimmings - PanelPowerOnTimmings) / 1000;
                if (delta > 0 && delta < PanelPowerOnMaxTime)
                {
                    Log.Success("Time Gap Between Panle Power On and Backlight On is {0} ms", delta);
                }
                else
                {
                    Log.Fail("Time Gap Between Between Panle Power On and Backlight On is not as expected, Expected {0} ms Actual {1} ms", PanelPowerOnMaxTime, delta);
                }
            }
        }

        

        //internal void ValidatePowerEventWakeSequence(ref List<PanelBLCData> panelData)
        //{
        //    List<PanelBLCData> temp = new List<PanelBLCData>();
        //    int D0EventIndex = -1;

        //    //get valid wake sequence start index
        //    for (int idx = 0; idx < panelData.Count; idx++)
        //    {
        //        PanelBLCData data = panelData[idx];
        //        if (data.PanelNotifyEvent != null)
        //        {
        //            if (panelData[(idx + 1)].PanelNotifyEvent != null && panelData.Count > (idx + 1))
        //            {
        //                PanelBLCData nextEvent = panelData[(idx + 1)];
        //                if (data.PanelNotifyEvent.EventName == PanelBLCEventName.IGD_SYSTEM_D0 &&
        //                    nextEvent.PanelNotifyEvent.EventName != PanelBLCEventName.IGD_SYSTEM_D3_D4)
        //                {
        //                    D0EventIndex = idx;
        //                    break;
        //                }
        //            }
        //        }
        //    }

        //    if (D0EventIndex != -1)
        //    {
        //        int currentIndex = D0EventIndex;
        //        int noElement = 0;
        //        List<PanelBLCData> wakeSequenceData = new List<PanelBLCData>();

        //        for (int Idx = currentIndex; Idx < panelData.Count; Idx++)
        //        {
        //            bool elementFound = false;
        //            noElement++;
        //            if (panelData[Idx].PanelNotifyEvent != null)
        //            {
        //                foreach (PanelBLCData seqData in wakeSequenceData)
        //                {
        //                    if (seqData.PanelNotifyEvent != null)
        //                    {
        //                        if (seqData.PanelNotifyEvent.EventName == panelData[Idx].PanelNotifyEvent.EventName &&
        //                            seqData.PanelNotifyEvent.EventType == panelData[Idx].PanelNotifyEvent.EventType)
        //                            elementFound = true;
        //                    }
        //                }
        //                if (false == elementFound)
        //                    wakeSequenceData.Add(panelData[Idx]);
        //            }
        //            else if (panelData[Idx].PanelAuxAccess != null)
        //            {
        //                foreach (PanelBLCData seqData in wakeSequenceData)
        //                {
        //                    if (seqData.PanelAuxAccess != null)
        //                    {
        //                        if (seqData.PanelAuxAccess.AuxStatus == panelData[Idx].PanelAuxAccess.AuxStatus)
        //                            elementFound = true;
        //                    }
        //                }
        //                if (false == elementFound)
        //                    wakeSequenceData.Add(panelData[Idx]);
        //            }
        //        }


        //        if (wakeSequenceData.Count != 0)
        //        {
        //            panelData.RemoveRange(D0EventIndex, noElement);
        //            panelData.AddRange(wakeSequenceData);
        //        }
        //    }
        //}
    }
}