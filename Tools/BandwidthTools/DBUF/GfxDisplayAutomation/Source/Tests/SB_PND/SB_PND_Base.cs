namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    
    using System;
    using System.IO;
    using System.Threading;
    using System.Runtime.InteropServices;
    using System.Globalization;

    class SB_PND_Base : TestBase
    {
        # region CONSTANTS_DECLARATIONS
        const uint CLOCK_CROSS = 128, BPP_CONSTANT = 8;
        const double DOTCLOCK_CONSTANT = 1000000;
        const int SPRITE_YUV422_bpp = 2;
        
        private const string PF_HRATIO = "PF_HRATIO";
        private const string PF_VRATIO = "PF_VRATIO";
        private const string OVERLAY_ENABLE = "OVERLAY_ENABLE";
        private const string PANEL_FITTER_ENABLE = "PANEL_FITTER_ENABLE";
        
        private const string PND_Max_FIFO_ENABLE = "PND_Max_FIFO_ENABLE";
        private const string SPRITE_FIFO_DRAIN_LATENCY = "SPRITE_FIFO_DRAIN_LATENCY";
        private const string PLANE_FIFO_DRAIN_PRECISION = "PLANE_FIFO_DRAIN_PRECISION";
        private const string PLANE_FIFO_DRAIN_LATENCY = "PLANE_FIFO_DRAIN_LATENCY";
        private const string SPRITE_FIFO_DRAIN_PRECISION = "SPRITE_FIFO_DRAIN_PRECISION";

        #endregion

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
            {
                Log.Success("{0} is verified by OS", argDisplayConfig.GetCurrentConfigStr());
            }
            else
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDisplayConfig.GetCurrentConfigStr());
        }

        protected void TestMaxFifo(DisplayConfig mode)
        {
            bool MaxFifo_Status = VerifyRegisters(PND_Max_FIFO_ENABLE, PIPE.NONE, PLANE.NONE, PORT.PORTA, false);
            CheckMaxFIFOStatus(mode, MaxFifo_Status, true);

            if (base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
            {
                bool sbRegisterStatus = false;
                SBRegisterData sbRegisterData = new SBRegisterData();
                sbRegisterData.DSP_SS_PM_REG = 0x36;
                sbRegisterData.PUNIT_PORT_ID = 0x4;
                DriverEscapeData<SBRegisterData, uint> driverData = new DriverEscapeData<SBRegisterData, uint>();
                driverData.input = sbRegisterData;
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.SBRegisterRead, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read SBRegister with offset as {0}, {1}", driverData.input.DSP_SS_PM_REG.ToString("X"), driverData.input.PUNIT_PORT_ID.ToString("X"));
                else
                {
                    Log.Verbose("PUNIT Register: {0}, {1}: Value: {2}", driverData.input.DSP_SS_PM_REG.ToString("X"), driverData.input.PUNIT_PORT_ID.ToString("X"), driverData.output.ToString("X"));
                    sbRegisterStatus = GetRegisterValue(driverData.output, 6, 6) == 1 ? true : false;
                    CheckMaxFIFOStatus(mode, sbRegisterStatus, false);
                }
            }
          
        }

        private void CheckMaxFIFOStatus(DisplayConfig mode, bool MaxFifo_Status, bool isMMIOFIFO)
        {
            string currentFIFO = isMMIOFIFO ? "MMIO" : "PUNIT";
            string status = MaxFifo_Status ? "Enabled" : "Disabled";

            if (MaxFifo_Status == true && mode.ConfigType == DisplayConfigType.SD)
            {
                Log.Success(string.Format("{0} MaxFifo is enabled which is expected, mode: {1}", currentFIFO, mode.GetCurrentConfigStr()));
            }
            else if (MaxFifo_Status != true && mode.ConfigType != DisplayConfigType.SD)
            {
                Log.Success(string.Format("{0} MaxFifo is not enabled which is expected, mode: {1}", currentFIFO, mode.GetCurrentConfigStr()));
            }
            else
            {
                if (mode.ConfigType == DisplayConfigType.SD)
                    Log.Fail(string.Format(" {0}  MaxFifo: {1} which is not expected, mode: {2}",currentFIFO,status, mode.GetCurrentConfigStr()));
                else
                    Log.Fail(string.Format("{0} MaxFifo: {1} which is not expected, mode: {2}", currentFIFO, status, mode.GetCurrentConfigStr()));
            }
        }
        /// <summary>
        /// This calculates the Drian Latency
        /// </summary>
        private void GetDainLatencyValue(Platform currentPlatform, double dotClockMHz, uint uPrecision, uint bpp, out uint uDrain_latency)
        {
            uint platformFactor = 2;
            if (currentPlatform == Platform.VLV)
                platformFactor = 1;

            uDrain_latency = (uint)Math.Truncate(((64 * uPrecision * 4) / (dotClockMHz * bpp * platformFactor)));
        }

        /// <summary>
        /// This method checks for latency values that is programmed in Registers.
        /// </summary>
        protected void TestPndLatency(PipePlaneParams pipePlaneParam, uint Bpp, uint pixelClock)
        {
            uint uDrainLatency;
            uint uDrainLatencySprite;
            uint uPrecision;
            double dDotClockMHz = 0;
            uint plane_Bpp = Bpp / BPP_CONSTANT;//For 16bpp, plane_bpp is 2 and for 32bpp, plane_bpp is 4;
            plane_Bpp = 4; //[212105] Fix for After system open game "Counter Strike 1.6" with VGA, monitor no display and Monitor Led is off

            Platform currentPlatform = base.MachineInfo.PlatformDetails.Platform;

            //As per the bug 5617028, For CHV the precision values are taken as 16 and 32 and for valleyview it is 32 and 64

            uint expectedLowPrecision = 16;
            uint expectedHighPrecision = 32;

            if (currentPlatform == Platform.VLV)
            {
                expectedLowPrecision = 32;
                expectedHighPrecision = 64;
            }

            dDotClockMHz = GetCorrectedDotClock(pipePlaneParam, pixelClock);
            //For Plane Latency Check
            if ((dDotClockMHz * 4) <= 256)
                uPrecision = expectedLowPrecision;
            else
                uPrecision = expectedHighPrecision;

            Log.Message(string.Format("PND Latency: Precision Value = {0}", uPrecision));
            GetDainLatencyValue(currentPlatform, dDotClockMHz, uPrecision, plane_Bpp, out uDrainLatency);

            uint planeLatencyValue = GetRegisterValue(PLANE_FIFO_DRAIN_LATENCY, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE);
            if (uDrainLatency == planeLatencyValue)
            {
                Log.Success(string.Format("Plane Latency Values Matched for {0} : Calculated {1}, RegisterValue {2}", pipePlaneParam.DisplayType, uDrainLatency, planeLatencyValue));
            }
            else
            {
                Log.Fail(string.Format("Plane Latency Values MisMatched for {0} : Calculated {1}, RegisterValue {2}", pipePlaneParam.DisplayType, uDrainLatency, planeLatencyValue));
            }

            bool IsPlanePrecision64 = VerifyRegisters(PLANE_FIFO_DRAIN_PRECISION, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE,false);
            if (uPrecision == expectedHighPrecision && IsPlanePrecision64 == true)
            {
                Log.Success(string.Format("Plane Precision Matched for {0} : Precision {1}, PlanePrecision {2} bit", pipePlaneParam.DisplayType, uPrecision, IsPlanePrecision64 ? expectedHighPrecision : expectedLowPrecision));
            }
            else if (uPrecision == expectedLowPrecision && IsPlanePrecision64 != true)
            {
                Log.Success(string.Format("Plane Precision Matched for {0} : Precision {1}, PlanePrecision {2} bit", pipePlaneParam.DisplayType, uPrecision, IsPlanePrecision64 ? expectedHighPrecision : expectedLowPrecision));
            }
            else
                Log.Fail(string.Format("Plane Precision MisMatched for {0} : Precision {1}, PlanePrecision {2} bit", pipePlaneParam.DisplayType, uPrecision, IsPlanePrecision64 ? expectedHighPrecision : expectedLowPrecision));

            //For Sprite Latency Check
            if (VerifyRegisters(OVERLAY_ENABLE, pipePlaneParam.Pipe, pipePlaneParam.Plane, PORT.NONE, false))
            {
                if ((dDotClockMHz * 2) < 256)
                    uPrecision = expectedLowPrecision;
                else
                    uPrecision = expectedHighPrecision;
                
                Log.Message(string.Format("PND Latency: Precision Value = {0}", uPrecision));
                GetDainLatencyValue(currentPlatform, dDotClockMHz, uPrecision, SPRITE_YUV422_bpp, out uDrainLatencySprite);

                uint spriteLatencyValue = GetRegisterValue(SPRITE_FIFO_DRAIN_LATENCY, pipePlaneParam.Pipe, pipePlaneParam.Plane, PORT.NONE);
                spriteLatencyValue = GetRegisterValue(spriteLatencyValue, 8, 14);
                if (uDrainLatencySprite == spriteLatencyValue)
                {
                    Log.Success(string.Format("Sprite Latency Values Matched for {0} : Calculated {1}, RegisterValue {2}", pipePlaneParam.DisplayType, uDrainLatencySprite, spriteLatencyValue));
                }
                else
                {
                    Log.Fail(string.Format("Sprite Latency Values MisMatched for {0} : Calculated {1}, RegisterValue {2}", pipePlaneParam.DisplayType, uDrainLatencySprite, spriteLatencyValue));
                }

                bool IsSpritePrecision64 = VerifyRegisters(SPRITE_FIFO_DRAIN_PRECISION, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE, false);
                if (uPrecision == expectedHighPrecision && IsSpritePrecision64 == true)
                {
                    Log.Success(string.Format("Plane Precision Matched for {0} : Precision {1}, SpritePrecision: {2}bit", pipePlaneParam.DisplayType, uPrecision, IsSpritePrecision64 ? expectedHighPrecision : expectedLowPrecision));
                }
                else if (uPrecision == expectedLowPrecision && IsSpritePrecision64 == true)
                {
                    Log.Success(string.Format("Plane Precision Matched for {0} : Precision {1}, SpritePrecision: {2}bit", pipePlaneParam.DisplayType, uPrecision, IsSpritePrecision64 ? expectedHighPrecision : expectedLowPrecision));
                }
                else
                    Log.Fail(string.Format("Plane Precision Didn't Match for {0} : Precision {1}, SpritePrecision {2}bit", pipePlaneParam.DisplayType, uPrecision, IsSpritePrecision64 ? expectedHighPrecision : expectedLowPrecision));
            }
        }

        #region CommonMethods


        private uint GetCorrectedDotClock(PipePlaneParams pipePlaneParam,uint dotClockValue)
        {
            uint xScaling = 0, yScaling = 0;
            
            if (VerifyRegisters(PANEL_FITTER_ENABLE, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE, false))
            {
                Log.Verbose("Panel Fitter is Enabled");
                uint temp = 0;
                float PFHorRatio, PFVerRatio;

                temp = GetRegisterValue(PF_HRATIO, PIPE.PIPE_A, PLANE.NONE, PORT.NONE);

                string st = GetRegisterValue(temp, 0, 11).ToString() + "," + GetRegisterValue(temp, 12, 12).ToString();
                PFHorRatio = float.Parse(st, CultureInfo.GetCultureInfo("de-DE").NumberFormat);

                temp = GetRegisterValue(PF_VRATIO, PIPE.PIPE_A, PLANE.NONE, PORT.NONE);
                string st1 = GetRegisterValue(temp, 16, 27).ToString() + "," + GetRegisterValue(temp, 28, 28).ToString();
                PFVerRatio = float.Parse(st1, CultureInfo.GetCultureInfo("de-DE").NumberFormat);

                if (PFHorRatio > 1 || PFVerRatio > 1)
                {
                    Log.Verbose(string.Format("DotClock Value Before downscaled value is : {0}", dotClockValue));

                    xScaling = (PFHorRatio < 1) ? 1000 : xScaling * 1000;
                    yScaling = (PFVerRatio < 1) ? 1000 : yScaling * 1000;
                    Log.Verbose(string.Format("xScaling : {0}  yScaling : {1}", xScaling, yScaling));
                    dotClockValue = GetRoundedDotClock(dotClockValue, xScaling, yScaling, 1);
                }
                else
                {
                    Log.Verbose("No change in DotClock, as it is not downscaling.");
                }
            }
            else
            {
                Log.Message("Panel Fitter is not Enabled");
            }

            Log.Message(string.Format("The Values of DotClock = {0}",
                dotClockValue));

            return dotClockValue;
        }

        private uint GetRegisterValue(uint RegisterValue, int start, int end)
        {
            uint value = RegisterValue << (31 - end);
            value >>= (31 - end + start);
            return value;
        }

        /// <summary>
        /// Returns the Round-Up DotClock
        /// </summary>
        /// <param name="a">multiplicative element</param>
        /// <param name="b">multiplicative element</param>
        /// <param name="c">multiplicative element</param>
        /// <param name="d">Division of this number</param>
        /// <returns></returns>
        private uint GetRoundedDotClock(uint a, uint b, uint c, int d)
        {
            double dc = (a * b * c) / (d * DOTCLOCK_CONSTANT);
            double floorvalue = Math.Floor(dc);

            double temp = (dc - floorvalue) > 0.99 ? floorvalue + 1 : floorvalue;
            return Convert.ToUInt32(temp);
        }

        #endregion
    }
}