namespace Intel.VPG.Display.Automation
{
    #region Assembly DivaUtilityCLR.dll, v1.0.5982.2947
    // C:\Perforce\gfx_ValDisplay\DEV\GfxDisplayAutomation\Source\Framework\AccessAPI\Assemblies\x64\DivaUtilityCLR.dll
    #endregion

    using Microsoft.Win32.SafeHandles;
    using System;
    using System.Collections;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;

    public class SB_DP_SST_Base : TestBase
    {
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected Dictionary<DisplayType, string> _changeEdid = null;
        protected List<DisplayType> _semiAutomatedDispList = null;
        static DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = null;
        public DIVA_DISPLAY_DETAILS_ARGS_CLR[] DisplayDetailsArgs;
        protected Dictionary<DisplayType, PORT> DisplayPortMap = null;
        protected Dictionary<PORT, int> PortBufCTLRegMap = null;

        DisplayConfig configBefore, configAfter, ConfigAfterSwitch;
        DisplayInfo curDispInfo;
        DisplayMode ResolutionOSPage, ResolutionCUISDK;

        //Constants to store bitmap and golden value
        public const uint DP_HOTPLUG_BITMAP = 0x00000001;
        public const uint DP_HOTPLUG_GOLDENVALUE = 0x00000001;
        uint uiDPCDOffset = 0x600;

        public SB_DP_SST_Base()
        {
            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _changeEdid = new Dictionary<DisplayType, string>();

            //These are needed to access DDI (i.e port) on which DP is connected. It also stores Buffer control register address for that port
            DisplayPortMap = new Dictionary<DisplayType, PORT>();
            PortBufCTLRegMap = new Dictionary<PORT, int>();
            PortBufCTLRegMap.Add(PORT.PORTA, 64000);
            PortBufCTLRegMap.Add(PORT.PORTB, 64100);
            PortBufCTLRegMap.Add(PORT.PORTC, 64200);
            PortBufCTLRegMap.Add(PORT.PORTD, 64300);
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (ApplicationManager.ApplicationSettings.UseDivaFramework || ApplicationManager.ApplicationSettings.UseULTFramework)
            {
                _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
                _changeEdid.Add(DisplayType.DP, "DP_HP_ZR2240W.EDID");
                _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
                _changeEdid.Add(DisplayType.DP_2, "DP_3011.EDID");

                _defaultEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
                _changeEdid.Add(DisplayType.HDMI, "HDMI_DELL_U2711_XVYCC.EDID");
                _defaultEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");
                _changeEdid.Add(DisplayType.HDMI_2, "HDMI_HP.EDID");
            }

            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
            {
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
            }
        }

        protected string GetTrimmedDisplayName(string completeDisplayName)
        {
            string dispName = Regex.Replace(completeDisplayName, "Digital Television 2", " ");
            dispName = Regex.Replace(dispName, "Digital Television", " ");
            if (dispName.Length == completeDisplayName.Length)
            {
                dispName = Regex.Replace(dispName, "Digital Display 2", " ");
                dispName = Regex.Replace(dispName, "Digital Display", " ");
            }
            return dispName.Trim();
        }

        protected void ApplyConfigOS(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }

        protected void VerifyConfigOS(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDisplayConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDisplayConfig.GetCurrentConfigStr()))
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            else
                Log.Fail("Config {0} does not match with current config {1}", argDisplayConfig.GetCurrentConfigStr(), currentConfig.GetCurrentConfigStr());
        }

        protected void InvokePowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking power event {0}", argPowerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            powerParams.PowerStates = argPowerState;
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }

        /*++
        Function Name : VerifyInOS
        Description   : Verifies the status of the display config 
        Arguments     : DislayConfig (before and after hotplug)
        isHotplug (Bool value returning true if display is hotplugged)
        Return Value  : None
        --*/

        public void VerifyInOS(DisplayConfig config1, DisplayConfig config2, DisplayAction DispAction)
        {
            IEnumerable<DisplayType> unpluggedDisplayTypes;
            IEnumerable<DisplayType> pluggedDisplayTypes;
            // Verify whether OS page enumerates only connected displays 
            Log.Message(true, "Verify the selected display got unplugged  through OS");

            List<DisplayType> before = new List<DisplayType>();

            before.Add(config1.PrimaryDisplay);
            before.Add(config1.SecondaryDisplay);
            before.Add(config1.TertiaryDisplay);

            List<DisplayType> after = new List<DisplayType>();

            after.Add(config2.PrimaryDisplay);
            after.Add(config2.SecondaryDisplay);
            after.Add(config2.TertiaryDisplay);

            switch (DispAction)
            {
                case DisplayAction.HOTPLUG:
                    pluggedDisplayTypes = after.Except(before);
                    foreach (DisplayType curDisp in (base.ApplicationManager.ParamInfo.Get<DisplayList>(ArgumentType.Display)).ToList())
                    {
                        foreach (DisplayType pluggedType in pluggedDisplayTypes)
                        {
                            if (curDisp == pluggedType)
                                Log.Success("Plugged Display" + curDisp);
                        }
                    }
                    break;
                case DisplayAction.HOTUNPLUG:
                    unpluggedDisplayTypes = before.Except(after);
                    foreach (DisplayType curDisp in (base.ApplicationManager.ParamInfo.Get<DisplayList>(ArgumentType.Display)).ToList())
                    {
                        foreach (DisplayType unpluggedType in unpluggedDisplayTypes)
                        {
                            if (curDisp == unpluggedType)
                                Log.Success("Unplugged Display" + curDisp);
                        }
                    }
                    break;
                case DisplayAction.MONITORTURNOFF:
                    if (config1.ToString().Equals(config2.ToString()))
                    {
                        Log.Message("All Displays are enumerated successfully before/after monitor turn off");
                    }
                    else
                    {
                        Log.Fail("All Displays failed to enumerate before/after monitor turn off");
                    }
                    break;
                case DisplayAction.DISPLAYCONFIGSWITCH:
                    if (config1.ToString().Equals(config2.ToString()))
                    {
                        Log.Success("Display configuration Switching successfull");
                        Log.Message("Display Configuration Switching successful");
                    }
                    else
                    {
                        Log.Fail("Display configuration Switching Failed!");
                        Log.Fail("Display Configuration Switching Failed!");
                    }
                    break;
                default:
                    Log.Alert("Invalid Display Operation");
                    break;
            }
        }

        /*++
        Function Name : VerifyDPCDRegisterValue
        Description   : Reads DPCD register value and compares against golden/expected values 
        Arguments     : DisplayType (for which DPCD read performed)
        DPCDOffset (DPCD Register Offset)
        Bitmap (Bits which need to be checked)
        GoldenValue (Expected Value of register read)
        Return Value  : None
        --*/

        protected void VerifyDPCDRegisterValue(DisplayType display, uint uiDPCDOffset, uint uiBitmap, uint uiGoldenValue)
        {
            DpcdInfo DPCDInfo = new DpcdInfo();
            DPCDInfo.Offset = uiDPCDOffset;
            DPCDInfo.DispInfo = base.EnumeratedDisplays.Find(dI => dI.DisplayType == display);

            //// Read DPCD register value
            AccessInterface.GetFeature<DpcdInfo, DpcdInfo>(Features.DpcdRegister, Action.GetMethod, Source.AccessAPI, DPCDInfo);
            RegisterInf regInfo = new RegisterInf(uiDPCDOffset.ToString(), System.Convert.ToString(uiBitmap, 2), uiGoldenValue.ToString());

            // Compare DPCD value against golden/expected values and prints success/failure message depending on results
            if (CompareRegisters(DPCDInfo.Value, regInfo))
            {
                Log.Success("DPCD register offset (0x{0:x}) verification successful", uiDPCDOffset);
            }
            else
            {
                Log.Fail("DPCD register offset (0x{0:x}) verification Failed", uiDPCDOffset);
            }
        }

        protected void PowerEvent(int delay, PowerStates _PowerState)
        {
            Log.Verbose("Putting the system into {0} state & resume ", _PowerState);
            PowerParams powerParams = new PowerParams();
            powerParams.Delay = delay;
            base.InvokePowerEvent(powerParams, _PowerState);
            Log.Success("Put the system into {0} state & resumed ", _PowerState);
        }

        public void doHotplug(DisplayType display, Boolean inLowPowerState = false, PowerStates argState = 0, string EDID = null)
        {
            string EDIDStr = _defaultEDIDMap[display];
            configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            if (inLowPowerState)
            {
                int delay = 30;
                PowerParams _powerParams = new PowerParams();
                _powerParams.Delay = delay;

                if (EDID == null)
                {
                    //Register for hotplug event in low power state
                    base.HotPlug(display, _defaultEDIDMap[display], inLowPowerState);
                }
                else
                {
                    //Register for hotplug event in low power state
                    base.HotPlug(display, EDID, inLowPowerState);
                }

                //Put system into low power state, hotplug will happen when system goes into Low power state
                base.InvokePowerEvent(_powerParams, argState);
            }
            else
            {
                if (EDID == null)
                {
                    //Register for hotplug event in low power state
                    base.HotPlug(display, _defaultEDIDMap[display]);
                }
                else
                {
                    //Register for hotplug event in low power state
                    base.HotPlug(display, EDID);
                }
            }
            // Apply/Set SD on secondary Display
            DisplayConfig sec = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = display };
            ApplyConfigOS(sec);

            //Call only after bringing up system
            configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            // Retrieve DisplayID of the external Display1
            curDispInfo = base.EnumeratedDisplays.Where(di => di.DisplayType == display).FirstOrDefault();

            if (DisplayExtensions.GetDisplayType(display) == DisplayType.DP)
            {
                // Call VerifyDPCDRegisterValue function to read DPCD register value and compare against golden/expected values
                VerifyDPCDRegisterValue(display, uiDPCDOffset, DP_HOTPLUG_BITMAP, DP_HOTPLUG_GOLDENVALUE);
            }
            VerifyInOS(configBefore, configAfter, DisplayAction.HOTPLUG);
        }

        /*++ 
        Function Name : doHotUnPlug 
        Description   : Perform hotplug/unplug during/after power events  
        Arguments     : DisplayType, EDID and low power event 
        Return Value  : None 
        --*/
        public void doHotUnPlug(DisplayType display, Boolean inLowPowerState = false, PowerStates argState = 0)
        {
            configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (inLowPowerState)
            {
                int delay = 15;
                PowerParams _powerParams = new PowerParams();
                _powerParams.Delay = delay;

                //Register for hotplug event in low power state
                base.HotUnPlug(display, inLowPowerState);

                //Put system into low power state, hotplug will happen when system goes into Low power state
                base.InvokePowerEvent(_powerParams, argState);
            }
            else
            {
                base.HotUnPlug(display);
            }
            configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            VerifyInOS(configBefore, configAfter, DisplayAction.HOTUNPLUG);
        }

        /*++
        Function Name : doHotUnPlugPlug
        Description   : Perform hotplug/unplug during/after power events 
        Arguments     : DisplayType, EDID and low power event
        Return Value  : None
        --*/
        public void doHotUnPlugPlug(DisplayType display, string EDID, Boolean inLowPowerState = false, PowerStates argState = 0)
        {
            configBefore = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (inLowPowerState)
            {
                int delay = 15;
                PowerParams _powerParams = new PowerParams();
                _powerParams.Delay = delay;

                // Unplug DFT in LowPowerState
                base.HotUnPlug(display, true);

                // Plug DFT in LowPowerState
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == display).FirstOrDefault();
                base.HotPlug(display, true, displayInfo.WindowsMonitorID, EDID, true);

                //Put system into low power state, hotplug will happen when system goes into Low power state
                base.InvokePowerEvent(_powerParams, argState);
            }

            configAfter = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);

            VerifyInOS(configBefore, configAfter, DisplayAction.HOTUNPLUG);
        }

        /*++ 
        Function Name : SwapDisplaysAndApplyConfig 
        Description   : Swaps displays. For dual display -> Primary becomes Secondary and vice-versa. For Tri display -> 
                        Primary becomes Secondary, Secondary becomes Tertiary and Tertiary becomes Primary. 
        Arguments     : DisplayType, EDID and low power event 
        Return Value  : None 
        --*/
        public void SwapDisplaysAndApplyConfig(DisplayConfig argDisplayConfig)
        {
            Log.Message(true, "Swapping the displays");
            DisplayType primary = argDisplayConfig.PrimaryDisplay;
            DisplayType secondary = argDisplayConfig.SecondaryDisplay;
            DisplayType tertiary = argDisplayConfig.TertiaryDisplay;

            // Primary and Secondary displays are swapped here 
            DisplayConfig config = new DisplayConfig()
            {
                PrimaryDisplay = secondary,
                SecondaryDisplay = primary
            };
            // Tri display combination handled here. 
            if ((argDisplayConfig.ConfigType == DisplayConfigType.TDC) || (argDisplayConfig.ConfigType == DisplayConfigType.TED))
            {
                config.PrimaryDisplay = secondary;
                config.SecondaryDisplay = tertiary;
                config.TertiaryDisplay = primary;
            }
            config.ConfigType = argDisplayConfig.ConfigType;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.SDKConfig, Action.SetMethod, config))
            {
                Log.Success("{0} Applied successfully", config.GetCurrentConfigStr());
            }
            else
            {
                Log.Fail("Failed to Apply {0}", config.GetCurrentConfigStr());
            }
        }

        /*++
        Function Name : ApplyConfig_Swap_CheckMaxRes_TwoDisplays
        Description   : Apply config, Swap dual displays and verify maximum resolution enumerated by CUI/OS are identical/not
        Arguments     : Display config
        Return Value  : None
        --*/
        protected void ApplyConfig_Swap_CheckMaxRes_TwoDisplays(DisplayConfig CurrentConfig)
        {
            // Verify LFP (eDP) + DFP (DP/HDMI) in Dual-Clone mode works as expected
            CurrentConfig.ConfigType = DisplayConfigType.DDC;

            // Apply and verify config
            ApplyConfigOS(CurrentConfig);
            VerifyConfigOS(CurrentConfig);

            // Verify LFP (eDP) + DFP (DP/HDMI) in Dual-Extended mode works as expected
            CurrentConfig.ConfigType = DisplayConfigType.ED;

            // Apply and verify config
            ApplyConfigOS(CurrentConfig);
            VerifyConfigOS(CurrentConfig);

            // Verify maximum resolution enumerated by CUI and OS page are identical or not
            VerifyMaxResolution_CUI_OSPage(base.CurrentConfig.EnumeratedDisplays);

            // Swap the dual displays
            SwapDisplaysAndApplyConfig(CurrentConfig);
        }

        /*++
        Function Name : ApplyConfig_Swap_CheckMaxRes_TwoDisplays
        Description   : Apply config, Swap dual displays and verify maximum resolution enumerated by CUI/OS are identical/not
        Arguments     : Display config
        Return Value  : None
        --*/
        protected void ApplyConfig_Swap_CheckMaxRes_ThreeDisplays(DisplayConfig CurrentConfig)
        {
            // Verify LFP (eDP) + DFP (DP/HDMI) in Tri-Clone mode works as expected
            CurrentConfig.ConfigType = DisplayConfigType.TDC;

            // Apply and verify config
            ApplyConfigOS(CurrentConfig);
            ConfigAfterSwitch = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            VerifyInOS(CurrentConfig, ConfigAfterSwitch, DisplayAction.DISPLAYCONFIGSWITCH);

            // Verify LFP (eDP) + DFP (DP/HDMI) in Tri-Extended mode works as expected
            CurrentConfig.ConfigType = DisplayConfigType.TED;

            // Apply and verify config
            ApplyConfigOS(CurrentConfig);
            ConfigAfterSwitch = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            VerifyInOS(CurrentConfig, ConfigAfterSwitch, DisplayAction.DISPLAYCONFIGSWITCH);

            // Verify maximum resolution enumerated by CUI and OS page are identical or not
            VerifyMaxResolution_CUI_OSPage(base.CurrentConfig.EnumeratedDisplays);

            // Swap the tri displays
            SwapDisplaysAndApplyConfig(CurrentConfig);
        }

        /*++
        Function Name : VerifyMaxResolution_CUI_OSPage
        Description   : Retrieves maximum resolutions from OS page and CUI SDK and then verifies max resolution
                        enumerated by CUI/OS are identical/not
        Arguments     : Display config
        Return Value  : None
        --*/
        public void VerifyMaxResolution_CUI_OSPage(List<DisplayInfo> CustomDisplayList)
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggedDisplayList)
            {
                // Verify mode enumeration only for DP display
                if ((DT == DisplayType.DP) || (DT == DisplayType.DP_2) || (DT == DisplayType.DP_3))
                {
                    // Retrieve maximum resolution from OS
                    ResolutionOSPage = base.EnumeratedDisplays.Find(Disp => Disp.DisplayType == DT).DisplayMode;

                    // Retrieve maximum resolution from CUI SDK
                    List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.PluggedDisplayList);//.CurrentConfig.CustomDisplayList);
                    List<DisplayMode> supportedModeList;

                    for (int i = 0; i < base.CurrentConfig.PluggedDisplayList.Count; i++)
                    {
                        if (allModeList[i].display == DT)
                        {
                            supportedModeList = allModeList[i].supportedModes;
                            ResolutionCUISDK = supportedModeList[supportedModeList.Count - 1];
                        }
                    }

                    // Verify whether max resolution enumerated by CUI and OS are identical or not
                    if ((ResolutionOSPage.HzRes == ResolutionCUISDK.HzRes) && (ResolutionOSPage.VtRes == ResolutionCUISDK.VtRes))
                    {
                        Log.Success("Max resolution enumerated by OS page and CUI for {0} are identical", DT);
                    }
                    else
                    {
                        Log.Fail("Maximum resolution enumerated by OS page and CUI for {0} are not identical", DT);
                    }
                }
            }
        }

        /*
   Function Name : getSupportedPorts
   Description   : returns ports supported by given display type on current platform
   Argument      : DisplayType
   return type   : List of Supported Ports
 */
        public Hashtable getSupportedPorts(DisplayType display)
        {
            //  bool status = false;
            Hashtable ht = new Hashtable();
            if (DivaDisplayFeatureUtility == null)
                DivaDisplayFeatureUtility = GetDivaDisplayFeatureUtility();
            DIVA_ENUM_DEVICE_ARGS_CLR enumDeviceArgs = new DIVA_ENUM_DEVICE_ARGS_CLR();

            // Enumerate devices.
            DivaDisplayFeatureUtility.EnumerateDevices(enumDeviceArgs);
            DisplayDetailsArgs = enumDeviceArgs.DisplayDetailsArgs;

            for (int i = 0; i < DisplayDetailsArgs.Length; i++)
            {
                if (DisplayDetailsArgs[i].DisplayUID != 0)
                {
                    ht.Add(DisplayDetailsArgs[i].DisplayUID, DisplayDetailsArgs[i].PortType);

                }
            }

            return ht;
        }

        /*
         * This function provides CLR utility handle. Using CLR utillity we are accessing DisplayUID and corresponding port mapping
         * This mapping gives us DisplayUID and DP panel supporting ports. 
         * Once we have DisplayUID for DP ports, we can use them for hotplug purpose (Refer SB_DP_SST_Hotplug_All_Ports testcase)
         */
        private static DivaDisplayFeatureUtilityCLR GetDivaDisplayFeatureUtility()
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();
            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            return DivaDisplayFeatureUtility;
        }
    }
}