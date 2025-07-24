namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text.RegularExpressions;

    #region EDP_Params
    public class eDP_Link_Lane_Config
    {
        public List<Config_Name> configNameList;
    }

    public class Config_Name
    {
        public string eventName;

        public string Lane_Count;

        public string Link_Rate;

        public string EDID_Name;

        public string DPCD_Name;

        public bool Run;

        public Platform Platform;
    }

    public enum UI_Link_Rate
    {
        None,
        UI_Rate_1 = 1,
        UI_Rate_4 = 2,
        UI_Rate_7 = 4,
    }

    public enum LaneCount
    {
        Lanes_1 = 0,
        Lanes_2 = 1,
        Lanes_4 = 3,
    }
    #endregion

    class SB_EDP_LR_LC_All : SB_EDP_Base
    {
        private const string HACTIVE = "HACTIVE";
        private const string VACTIVE = "VACTIVE";
        private const string PIPE_HOR_SOURCE_SIZE = "PIPE_HOR_SOURCE_SIZE";
        private const string PIPE_VER_SOURCE_SIZE = "PIPE_VER_SOURCE_SIZE";
        private const string EDP_Vswing_Emp_Sel = "EDP_Vswing_Emp_Sel";
        private const string EDP_TP_CTL = "EDP_TP_CTL";
        private const string EDP_Port_Reversal_4Lane_Caps = "EDP_Port_Reversal_4Lane_Caps";
        private const string TRANS_DDI_PORT_WIDTH = "TRANS_DDI_PORT_WIDTH";
        private const string TRANS_DDI_MODE_SEL_DP_SST = "TRANS_DDI_MODE_SEL_DP_SST";
        private const string DITHERING_BPC_ = "DITHERING_BPC_";
        private const string DITHERING_ENABLE = "DITHERING_ENABLE";
        private const string FBC_REGISTER = "FBC_REGISTER";
        private const string TRANS_CONF_ENABLE = "TRANS_CONF_ENABLE";
        private const string PF_PD_ENABLE = "PF_PD_ENABLE";
        private const string PIPE_CS_RGB = "PIPE_CS_RGB";
        private const string BPC = "BPC_";
        private const string _Binding = "_Binding";
        private const string EDP_Context_Config_File = "EDP_Context.config";
        private int context = 0;
        public int Current_BPC = 8;
        public int Source_BPC = 8;
        protected List<Config_Name> configNameList = new List<Config_Name>();

        protected UI_Link_Rate Link_Rate; //If this value is None, all the scenarios in the config file will be executed otherwise the overridden link rate will be run.
        public SB_EDP_LR_LC_All()
        {
            configNameList = GetConfigNameList();
            Link_Rate = UI_Link_Rate.None;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (!base.CurrentConfig.CustomDisplayList.Contains(DisplayType.EDP))
                Log.Abort("Please pass EDP as a display in the command line.");
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            
            //plug the EDP Display and restart the system.
            Log.Message("Plugging EDP with EDID:{0}, DPCD: {1}", configNameList[context].EDID_Name, configNameList[context].DPCD_Name);
            base.HotPlug(DisplayType.EDP, true, 0x40F04, configNameList[context].EDID_Name, false, configNameList[context].DPCD_Name);

            SaveContext(context, configNameList.Count);

            InvokePowerEvent(PowerStates.S5);

            //base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });
            //base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            ApplyConfig(this.CurrentConfig);
            VerifyConfig(this.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            //Overriding function for other tests.
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            context = RestoreContext();
            Config_Name currentParameters = configNameList[context];

            this.CurrentConfig.CustomDisplayList.ForEach(display =>
                {
                    if (display == DisplayType.EDP)
                    {
                        bool IsFbcEnabled = false;
                        bool PanelFitterEnabled = false;
                        bool ditheringExpected = false;
                        uint PipeSrcSizeX = 0, PipeSrcSizeY = 0, HorActive = 0, VertActive = 0, currentPortWidth = 0;
                        LaneCount expectedPortWidth = (LaneCount)Enum.Parse(typeof(LaneCount), currentParameters.Lane_Count);
                        DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == display);
                        DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                        DisplayMode targetMode = base.GetTargetResolution(display);

                        PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
                        PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
                        string eventName = default(string);

                        if(base.CurrentConfig.ConfigType.GetUnifiedConfig()== DisplayUnifiedConfig.Single || base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                        {
                            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);

                            DisplayMode nativeResolution = displayInfo.DisplayMode;
                            bool status = allModeList.Where(eachModeList => eachModeList.display == display).First().supportedModes.Where(eachMode => eachMode.Equals(eachMode, nativeResolution)).ToList().Count>0;

                            if (status)
                                Log.Success("{0} is enumerated as expected.", nativeResolution);
                            else
                                Log.Fail("{0} was not enumerated.", nativeResolution);
                        }

                        #region Scaler_Enabled

                        Dictionary<SCALAR, SCALAR_MAP> ScalarMapper = new Dictionary<SCALAR, SCALAR_MAP>();
                        foreach (SCALAR currScaler in Enum.GetValues(typeof(SCALAR)))
                        {
                            if (currScaler == SCALAR.NONE)
                                continue;

                            eventName = currScaler + "_Enable";
                            if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false))
                            {
                                //checking if plane scalar is enabled.
                                SCALAR_MAP tempScalar = SCALAR_MAP.NONE;
                                GetSKLScalarBinding(display, pipePlaneObject, currScaler, false, ref tempScalar);
                                ScalarMapper.Add(currScaler, tempScalar);
                                Log.Verbose("{0} is enabled and mapped to {1} for {2}", currScaler, tempScalar, display);
                            }
                            else
                                Log.Verbose("{0} is not enabled for {1}", currScaler, display);
                        }

                        if (ScalarMapper.Values.Contains(SCALAR_MAP.PIPE))
                            PanelFitterEnabled = true;
                        
                        #endregion

                        #region PortVerification

                        eventName = display + "_ENABLED";
                        if (VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, displayInfo.Port, true))
                            Log.Success("{0} is enabled on expected port {1}", display, displayInfo.Port);
                        else
                            Log.Fail("{0} is not enabled on expected port {1}", display, displayInfo.Port);

                        //if (VerifyRegisters(EDP_Vswing_Emp_Sel, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                        //    Log.Fail("Mismatch in the expected DP_Vswing_Emp_Sel register values.");
                        //else
                        //    Log.Success("DP_Vswing_Emp_Sel register values Matched.");

                        if (VerifyRegisters(EDP_TP_CTL, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected EDP_TP_CTL register values.");
                        else
                            Log.Success("EDP_TP_CTL register values matched.");

                        if (VerifyRegisters(EDP_Port_Reversal_4Lane_Caps, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected EDP_Port_Reversal_4Lane_Caps register values.");
                        else
                            Log.Success("EDP_Port_Reversal_4Lane_Caps register values matched.");

                        currentPortWidth = GetRegisterValue(TRANS_DDI_PORT_WIDTH, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port);
                        if (currentPortWidth != (uint)expectedPortWidth)
                            Log.Fail("Mismatch in the PortWidth. Expected:{0}, Observed:{1}", expectedPortWidth, currentPortWidth);
                        else
                            Log.Success("PortWidth:{0} is as expected.", expectedPortWidth);

                        if (VerifyRegisters(TRANS_DDI_MODE_SEL_DP_SST, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected TRANS_DDI_MODE_SEL_DP_SST register values.");
                        else
                            Log.Success("TRANS_DDI_MODE_SEL_DP_SST register values matched.");

                        Current_BPC = GetCurrentBPC(displayInfo);
                        eventName = BPC + Current_BPC.ToString();  //ex: BPC_12 or BPC_10
                        if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, true))
                            Log.Success("DeepColor Register values matched for {0}.", displayInfo.DisplayType);
                        #endregion

                        #region Pipe_Verification
                        if (Current_BPC < Source_BPC && Current_BPC != 12)
                        {
                            ditheringExpected = true;
                            eventName = DITHERING_BPC_ + Current_BPC;
                            if (!VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false))
                                Log.Fail("Mismatch in Dithering BPC.");
                            else
                                Log.Success("Dithering BPC:{0} value is as expected.", Current_BPC);
                        }

                        if (VerifyRegisters(DITHERING_ENABLE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != ditheringExpected)
                            Log.Fail("Mismatch in Dithering status. Expected:{0}, Observed:{1}.", ditheringExpected, !ditheringExpected);
                        else
                            Log.Success("Dithering status is {0} as expected.", ditheringExpected);

                        IsFbcEnabled = VerifyRegisters(FBC_REGISTER, PIPE.PIPE_A, PLANE.NONE, PORT.NONE, false);//need to modify the factory

                        if (VerifyRegisters(TRANS_CONF_ENABLE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected TRANS_CONF_ENABLE register values.");
                        else
                            Log.Success("TRANS_CONF_ENABLE register values matched.");

                        if (VerifyRegisters(PF_PD_ENABLE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected PF_PD_ENABLE register values.");
                        else
                            Log.Success("PF_PD_ENABLE register values matched.");

                        if (VerifyRegisters(PIPE_CS_RGB, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected PIPE_CS_RGB register values.");
                        else
                            Log.Success("PIPE_CS_RGB register values matched.");

                        //Pipe Source size and HActive/VActive verification.
                        PipeSrcSizeX = GetBitmappedRegisterValue(PIPE_HOR_SOURCE_SIZE, PIPE.NONE, pipePlaneParams.Plane, displayInfo.Port);
                        PipeSrcSizeY = GetBitmappedRegisterValue(PIPE_VER_SOURCE_SIZE, PIPE.NONE, pipePlaneParams.Plane, displayInfo.Port);

                        HorActive = GetBitmappedRegisterValue(HACTIVE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port);
                        VertActive = GetBitmappedRegisterValue(VACTIVE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port);

                        if (PipeSrcSizeX < 8 || PipeSrcSizeY < 8)
                            Log.Fail("Issue: Pipe Source size programmed less than 8. SrcSizeX:{0}, SrcSizeY:{1}", PipeSrcSizeX, PipeSrcSizeY);
                        else
                            Log.Success("Pipe Source size programmed greater than 8. SrcSizeX:{0}, SrcSizeY:{1}", PipeSrcSizeX, PipeSrcSizeY);

                        if (HorActive < 64)
                            Log.Fail("Issue: Horizontal Active size programmed less than 64. HorActive:{0}", HorActive);
                        else
                            Log.Success("Horizontal Active size programmed greater than 64. HorActive:{0}", HorActive);

                        if (currentMode.HzRes != PipeSrcSizeX)
                            Log.Fail("Mismatch in HzRes: {0} and PipeSrcSizeX: {1}", currentMode.HzRes, PipeSrcSizeX);
                        else
                            Log.Success("HzRes: {0} matched with PipeSrcSizeX", currentMode.HzRes);

                        if (currentMode.VtRes != PipeSrcSizeY)
                            Log.Fail("Mismatch in VtRes : {0} and PipeSrcSizeY: {1}", currentMode.VtRes, PipeSrcSizeY);
                        else
                            Log.Success("VtRes and PipeSrcSize matched with value: {0}", currentMode.VtRes);

                        if (targetMode.HzRes != HorActive)
                            Log.Fail("Mismatch in Target HzRes: {0} and HorActive: {1}", targetMode.HzRes, HorActive);
                        else
                            Log.Success("Target HzRes and HorActive matched with value: {0}", targetMode.HzRes);

                        if (targetMode.VtRes != VertActive)
                            Log.Fail("Mismatch in Target VtRes : {0} and VertActive: {1}", targetMode.VtRes, VertActive);
                        else
                            Log.Success("Target VtRes and VertActive matched with value: {0}", targetMode.VtRes);

                        if (PanelFitterEnabled != true)
                        {
                            if (PipeSrcSizeX != HorActive)
                                Log.Fail("Mismatch in PipeSourceSizeX and HorizontalActive. SrcSizeX: {0}, HorActive: {1}", PipeSrcSizeX, HorActive);
                            else
                                Log.Success("PipeSourceSizeX and HorizontalActive matched with value: {0}", PipeSrcSizeX);

                            if (PipeSrcSizeY != VertActive)
                                Log.Fail("Mismatch in pipeSourceSizeY and VertActive. SrcSizeY: {0}, VertActive: {1}", PipeSrcSizeY, VertActive);
                            else
                                Log.Success("PipeSourceSizeY and VertActive matched with value: {0}", PipeSrcSizeY);
                        }

                        if (IsFbcEnabled || PanelFitterEnabled)
                        {
                            if (PipeSrcSizeX > 4096)
                                Log.Fail("Horizontal Pipe Src Size should not be greater than 4096.");
                            else
                                Log.Success("Horizontal Pipe Src Size is less than 4096.");
                        }

                        #endregion

                        //if (display == DisplayType.HDMI)
                        //{
                        //    if (HorActiveX < 256)
                        //    {
                        //        Log.Fail("Issue: Horizontal Active size for HDMI programmed less than 256. HorActiveX:{0}", HorActiveX);
                        //    }
                        //}

                    }
                });

            if (++context < configNameList.Count)
            {
                SkipToMethod(2);
            }
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            base.HotUnPlug(DisplayType.EDP);
            
            InvokePowerEvent(PowerStates.S5);
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Success("Test completed.");
        }

        private int GetCurrentBPC(DisplayInfo displayInfo)
        {
            int currentBPC = displayInfo.ColorInfo.MaxDeepColorValue;

            currentBPC = Math.Min(currentBPC, Source_BPC);

            if (displayInfo.DisplayType == DisplayType.HDMI && currentBPC == 10)
            {
                Log.Message("Max BPC value for HDMI must not be 10, doing the min with 8BPC.");
                currentBPC = Math.Min(8, Source_BPC);
            }

            if (displayInfo.DisplayType == DisplayType.HDMI && currentBPC > 8)
            {
                DisplayMode targetResolution = base.GetTargetResolution(displayInfo.DisplayType);

                if (targetResolution.HzRes >= 1920 && targetResolution.VtRes > 1080)
                {
                    currentBPC = Math.Min(8, Source_BPC);
                }
            }

            return currentBPC;
        }

        private bool GetSKLScalarBinding(DisplayType display, PipePlaneParams pipePlaneObject, SCALAR currentScalar, bool IsPipeCall, ref SCALAR_MAP currentScalarMap)
        {
            bool status = true;
            string eventName = currentScalar.ToString() + _Binding;
            uint scalarVal = GetRegisterValue(eventName, pipePlaneObject.Pipe, pipePlaneObject.Plane, PORT.NONE);
            currentScalarMap = (SCALAR_MAP)scalarVal;

            return status;
        }

        private void SaveContext(int c, int max)
        {
            if (File.Exists(EDP_Context_Config_File))
            {
                File.Delete(EDP_Context_Config_File);
            }

            File.WriteAllText(EDP_Context_Config_File, c.ToString());
        }

        private int RestoreContext()
        {
            int context = 0;

            if (File.Exists(EDP_Context_Config_File))
            {
                String text = File.ReadAllText(EDP_Context_Config_File);
                if (String.IsNullOrEmpty(text) != true)
                {
                    context = int.Parse(text.Trim());
                }
                File.Delete(EDP_Context_Config_File);
            }

            return context;
        }
        protected void FilterConfigurationsByLinkRate()
        {
            List<Config_Name> tempConfigNameList = new List<Config_Name>();
            if(Link_Rate != UI_Link_Rate.None)
            {
                foreach(var item in configNameList)
                {
                    if (Link_Rate.ToString() == item.Link_Rate)
                        tempConfigNameList.Add(item);
                }
                configNameList = tempConfigNameList;
            }
        }
    }
}
