namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    class SB_Config_Verification : SB_Config_Base
    {
        private const string HACTIVE = "HACTIVE";
        private const string VACTIVE = "VACTIVE";
        private const string PIPE_HOR_SOURCE_SIZE = "PIPE_HOR_SOURCE_SIZE";
        private const string PIPE_VER_SOURCE_SIZE = "PIPE_VER_SOURCE_SIZE";
        private const string EDP_Vswing_Emp_Sel = "EDP_Vswing_Emp_Sel";
        private const string DP_TP_CTL = "DP_TP_CTL";
        private const string EDP_Port_Reversal_4Lane_Caps = "EDP_Port_Reversal_4Lane_Caps";
        private const string TRANS_DDI_PORT_WIDTH = "TRANS_DDI_PORT_WIDTH";
        private const string TRANS_DDI_MODE_SEL_DP_SST = "TRANS_DDI_MODE_SEL_DP_SST";
        private const string DITHERING_BPC_ = "DITHERING_BPC_";
        private const string DITHERING_ENABLE = "DITHERING_ENABLE";
        private const string FBC_REGISTER = "FBC_REGISTER";
        private const string TRANS_CONF_ENABLE_BIT = "TRANS_CONF_ENABLE_BIT";
        private const string PF_PD_ENABLE = "PF_PD_ENABLE";
        private const string PIPE_CS_RGB = "PIPE_CS_RGB";
        private const string HDMI_MODESET = "HDMI_MODESET";
        private const string BPC = "BPC_";
        private const string _Binding = "_Binding";
        public int Current_BPC = 8;
        public int Source_BPC = 8;


        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
           
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            ApplyConfigOS(this.CurrentConfig);
            VerifyConfigOS(this.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            VerifyRegisters(base.CurrentConfig);
        }

        protected void VerifyRegisters(DisplayConfig currentconfig)
        {
            currentconfig.CustomDisplayList.ForEach(display =>
            {                
                bool IsFbcEnabled = false;
                bool PanelFitterEnabled = false;
                bool ditheringExpected = false;
                uint PipeSrcSizeX = 0, PipeSrcSizeY = 0, HorActive = 0, VertActive = 0;
                DisplayInfo displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == display);
                DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
                DisplayMode targetMode = base.GetTargetResolution(display);

                PipePlaneParams pipePlaneObject = new PipePlaneParams(display);
                PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
                string eventName = default(string);

                if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Single || base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
                {
                    List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.CustomDisplayList);

                    DisplayMode nativeResolution = displayInfo.DisplayMode;
                    bool status = allModeList.Where(eachModeList => eachModeList.display == display).First().supportedModes.Where(eachMode => eachMode.Equals(eachMode, nativeResolution)).ToList().Count > 0;

                    if (status)
                        Log.Success("{0} is enumerated as expected.", nativeResolution);
                    else
                        Log.Fail("{0} was not enumerated.", nativeResolution);
                }

                IsFbcEnabled = VerifyRegisters(FBC_REGISTER, PIPE.PIPE_A, PLANE.NONE, PORT.NONE, false);//need to modify the factor

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
                
                #region Pipe_Verification

                if (VerifyRegisters(PIPE_CS_RGB, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                    Log.Fail("Mismatch in the expected PIPE_CS_RGB register values.");
                else
                    Log.Success("PIPE_CS_RGB register values matched.");

                //Pipe Source size and HActive/VActive verification.
                PipeSrcSizeX = base.GetRegisterValue(PIPE_HOR_SOURCE_SIZE, PIPE.NONE, pipePlaneParams.Plane, displayInfo.Port);
                PipeSrcSizeY = base.GetRegisterValue(PIPE_VER_SOURCE_SIZE, PIPE.NONE, pipePlaneParams.Plane, displayInfo.Port);

                HorActive = base.GetRegisterValue(HACTIVE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port);
                VertActive = base.GetRegisterValue(VACTIVE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port);

                if (PipeSrcSizeX < 8 || PipeSrcSizeY < 8)
                    Log.Fail("Issue: Pipe Source size programmed less than 8. SrcSizeX:{0}, SrcSizeY:{1}", PipeSrcSizeX, PipeSrcSizeY);
                else
                    Log.Success("Pipe Source size programmed greater than 8. SrcSizeX:{0}, SrcSizeY:{1}", PipeSrcSizeX, PipeSrcSizeY);

                if (HorActive < 64)
                    Log.Fail("Issue: Horizontal Active size programmed less than 64. HorActive:{0}", HorActive);
                else
                    Log.Success("Horizontal Active size programmed greater than 64. HorActive:{0}", HorActive);

                if (base.MachineInfo.OS.IsGreaterThan(OSType.WINTHRESHOLD) && !currentMode.ScalingOptions.Contains((uint)ScalingOptions.Maintain_Display_Scaling))
                {
                    if (targetMode.HzRes != PipeSrcSizeX)
                        Log.Fail("Mismatch in Target HzRes: {0} and PipeSrcSizeX: {1}", targetMode.HzRes, PipeSrcSizeX);
                    else
                        Log.Success("Target HzRes and PipeSrcSizeX matched with value: {0}", targetMode.HzRes);

                    if (targetMode.VtRes != PipeSrcSizeY)
                        Log.Fail("Mismatch in Target VtRes : {0} and PipeSrcSizeY: {1}", targetMode.VtRes, PipeSrcSizeY);
                    else
                        Log.Success("Target VtRes and PipeSrcSizeY matched with value: {0}", targetMode.VtRes);
                }
                else
                {
                    if (currentMode.HzRes != PipeSrcSizeX)
                        Log.Fail("Mismatch in HzRes: {0} and PipeSrcSizeX: {1}", currentMode.HzRes, PipeSrcSizeX);
                    else
                        Log.Success("HzRes: {0} matched with PipeSrcSizeX", currentMode.HzRes);

                    if (currentMode.VtRes != PipeSrcSizeY)
                        Log.Fail("Mismatch in VtRes : {0} and PipeSrcSizeY: {1}", currentMode.VtRes, PipeSrcSizeY);
                    else
                        Log.Success("VtRes and PipeSrcSize matched with value: {0}", currentMode.VtRes);
                }

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


                if (VerifyRegisters(TRANS_CONF_ENABLE_BIT, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                    Log.Fail("Mismatch in the expected TRANS_CONF_ENABLE_BIT register values.");
                else
                    Log.Success("TRANS_CONF_ENABLE register values matched.");

                if (VerifyRegisters(PF_PD_ENABLE, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                    Log.Fail("Mismatch in the expected PF_PD_ENABLE register values.");
                else
                    Log.Success("PF_PD_ENABLE register values matched.");

                #endregion

                #region PortVerification

                eventName = DisplayExtensions.GetDisplayType(display) + "_ENABLED";
                if (VerifyRegisters(eventName, PIPE.NONE, PLANE.NONE, displayInfo.Port, true))
                    Log.Success("{0} is enabled on expected port {1}", display, displayInfo.Port);
                else
                    Log.Fail("{0} is not enabled on expected port {1}", display, displayInfo.Port);


                Current_BPC = GetCurrentBPC(displayInfo);
                eventName = BPC + Current_BPC.ToString();  //ex: BPC_12 or BPC_10
                if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, true))
                    Log.Success("DeepColor Register values matched for {0}.", displayInfo.DisplayType);

                #endregion

                if (display == DisplayType.EDP || DisplayExtensions.GetDisplayType(display) == DisplayType.DP)
                {
                    #region PortVerification

                    if (VerifyRegisters(DP_TP_CTL, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                        Log.Fail("Mismatch in the expected DP_TP_CTL register values.");
                    else
                        Log.Success("DP_TP_CTL register values matched.");

                    //currentPortWidth = GetRegisterValue(TRANS_DDI_PORT_WIDTH, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port);
                    //if (currentPortWidth != (uint)expectedPortWidth)
                    //    Log.Fail("Mismatch in the PortWidth. Expected:{0}, Observed:{1}", expectedPortWidth, currentPortWidth);
                    //else
                    //    Log.Success("PortWidth:{0} is as expected.", expectedPortWidth);

                    if (VerifyRegisters(TRANS_DDI_MODE_SEL_DP_SST, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                        Log.Fail("Mismatch in the expected TRANS_DDI_MODE_SEL_DP_SST register values.");
                    else
                        Log.Success("TRANS_DDI_MODE_SEL_DP_SST register values matched.");

                   
                    #endregion

                    if (display == DisplayType.EDP)
                    {
                        #region Port_Verification
                        if (VerifyRegisters(EDP_Port_Reversal_4Lane_Caps, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false) != true)
                            Log.Fail("Mismatch in the expected EDP_Port_Reversal_4Lane_Caps register values.");
                        else
                            Log.Success("EDP_Port_Reversal_4Lane_Caps register values matched.");
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

                        #endregion
                    }

                }
                else if (DisplayExtensions.GetDisplayType(display) == DisplayType.HDMI)
                {
                    if (HorActive < 256)
                    {
                        Log.Fail("Issue: Horizontal Active size for HDMI programmed less than 256. HorActiveX:{0}", HorActive);
                    }

                    if (!VerifyRegisters(HDMI_MODESET, pipePlaneParams.Pipe, pipePlaneParams.Plane, displayInfo.Port, false))
                        Log.Fail("HDMI Registers were not programmed as expected.");
                    else
                        Log.Success("HDMI Registers were programmed as expected.");
                }
            });
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
    }
}
