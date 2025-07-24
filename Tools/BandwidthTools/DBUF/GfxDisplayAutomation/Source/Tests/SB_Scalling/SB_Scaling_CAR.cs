namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System;

    public class SB_Scaling_CAR : SB_Scaling_DisplayConfig
    {
        private const String PANEL_FITTER_ENABLE = "PANEL_FITTER_ENABLE";
        private const String SOURCE_PIPE_IMAGE = "SOURCE_PIPE_IMAGE";
        private const String TARGET_PANEL_FITTER_IMAGE = "TARGET_PANEL_FITTER_IMAGE";

        public SB_Scaling_CAR()
        {
            _considerMinRes = true;
        }

        protected override void ApplyAndVerifyScalling(DisplayType pDisplayType, bool pApplyMode)
        {
            List<DisplayMode> dispModes = GetModesForTest(pDisplayType);
            DisplayScaling dsScaling = null;

            uint[] customX = { 100, 100, 0, 50 };
            uint[] customY = { 100, 0, 100, 50 };


            dispModes.ForEach(dm =>
            {
                if (pApplyMode)                
                    AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, dm);

                List<ScalingOptions> all_Scallings_SDK_Manager = AccessInterface.GetFeature<List<ScalingOptions>, DisplayType>(Features.Scaling, Action.GetAllMethod, Source.AccessAPI, pDisplayType);
                if (all_Scallings_SDK_Manager.Count == 0)
                {
                    Log.Alert("{0} does not support CAR for {1}",pDisplayType,dm.GetCurrentModeStr(false));
                }
                all_Scallings_SDK_Manager.ForEach(apply_Scaling =>
                {
                    if (apply_Scaling == ScalingOptions.Customize_Aspect_Ratio)
                    {
                        dsScaling = new DisplayScaling(pDisplayType, apply_Scaling);

                        for (int index = 0; index < customX.Length; index++)
                        {
                            dsScaling.customX = customX[index];
                            dsScaling.customY = customY[index];

                            Log.Message(true, "{0}", dsScaling.ToString());
                            AccessInterface.SetFeature<bool, DisplayScaling>(Features.Scaling, Action.SetMethod, dsScaling);

                            DisplayScaling curr_Scalling_SDK_Manager = AccessInterface.GetFeature<DisplayScaling, DisplayType>(Features.Scaling, Action.GetMethod, Source.AccessAPI, pDisplayType);

                            if (dsScaling.Equals(curr_Scalling_SDK_Manager))
                            {
                                Log.Success("Current Scaling : {0}  ------  Expected(Applied) Scaling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling.ToString());
                                CheckWatermark(pDisplayType);
                            }
                            else
                                Log.Fail("Scaling Differ - Current Scaling from SDK Manager : {0} Expected(Applied) Scaling : {1}", curr_Scalling_SDK_Manager.ToString(), dsScaling.ToString());

                            CheckDeviation(pDisplayType, curr_Scalling_SDK_Manager);
                        }
                    }
                });

            });
        }

        private void CheckDeviation(DisplayType pDisplayType, DisplayScaling pDisplayScaling)
        {
            // Geting PIPE , Plane information for pannels
            PipePlaneParams pipePlane = new PipePlaneParams(pDisplayType);
            pipePlane = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", pDisplayType, pipePlane.Pipe, pipePlane.Plane);

            Log.Message(true, "Verifying Panel Fitter");
            if (VerifyRegisters(PANEL_FITTER_ENABLE, PIPE.NONE, pipePlane.Plane, PORT.NONE))
                Log.Success("Panel Fitter Enable");
            else
                Log.Fail("Panel Fitter Disable");

            int source = ReadRegister(SOURCE_PIPE_IMAGE, PIPE.NONE, pipePlane.Plane, PORT.NONE);
            int target = ReadRegister(TARGET_PANEL_FITTER_IMAGE, PIPE.NONE, pipePlane.Plane, PORT.NONE);

            //Getting X resolution and Y resolution from PIPE Source Register Values 
            int appliedX = source >> 16;
            int appliedY = source << 16;
            appliedY >>= 16;
            appliedX++; //Register is written specified value - 1 : So to get original value adding one 
            appliedY++; //Register is written specified value - 1 : So to get original value adding one 

            //Getting X resolution and Y resolution from PIPE Target Register Values 
            int targetX = target >> 16;
            int targetY = target << 16;
            targetY >>= 16;


            double XFraction, YFraction;
            double MAXIMUM_SCALE_LIMIT = .12;  //12%
            int deviation = 3;

            //[[100- CustomX]% * 12%] * XRes = Expected XRes
            XFraction = ((100.0 - (double)pDisplayScaling.customX) / 100.0) * MAXIMUM_SCALE_LIMIT;
            YFraction = ((100.0 - (double)pDisplayScaling.customY) / 100.0) * MAXIMUM_SCALE_LIMIT;

            int sourceX = Convert.ToInt32(appliedX - Math.Round(XFraction * (double)appliedX, 0));
            int sourceY = Convert.ToInt32(appliedY - Math.Round(YFraction * (double)appliedY, 0));

			/*
            if (base.MachineInfo.Platform.Contains("HSW"))
                AdjustHWLimitation(ref appliedX, ref appliedY, ref sourceX, ref sourceY);
			*/
				
            //If the variation is within the deviation limits(+/- 3) then true;Otherwise, false.
            int deltaX = Math.Abs(targetX - sourceX);
            int deltaY = Math.Abs(targetY - sourceY);

            if (deltaX <= deviation && deltaY <= deviation)
                Log.Success("Resolution matched");
            else
                Log.Fail("Resolution Mismatch");

            Log.Success("Applied resolution in CUI : {0} X {1}", appliedX, appliedY);
            Log.Success("Actual resolution programmed in Target Registers: {0} X {1}", targetX, targetY);
            Log.Success("Expected resolution as per Equation : {0} X {1}", sourceX, sourceY);
        }


        protected int ReadRegister(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            Log.Message("Reading Register for event : {0}", pRegisterEvent);

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);

                return (int)driverData.output;
            }

            return 0;
        }

        protected bool VerifyRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            Log.Message("Verifying Register for event : {0}", pRegisterEvent);
            bool regValueMatched = true;

            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    if (!CompareRegisters(driverData.output, reginfo))
                    {
                        Log.Message("Register with offset {0} doesnot match required values", reginfo.Offset);
                        regValueMatched = false;
                    }
            }

            return regValueMatched;
        }

        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            Log.Verbose("Bitmap in uint = {0}, Value from register read = {1}", bit, argDriverData);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            Log.Verbose("value from reg read in ubit = {0}", hex);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            if (String.Equals(valu, argRegInfo.Value))
            {
                Log.Message("Register Values Matched");
                return true;
            }
            return false;
        }

        /// <summary>
        /// This method will adjust the panel fitter values if the Applied/Source ratio goes beyond 1.125.
        /// It is HSW HW Limitation.
        /// </summary>        
        private void AdjustHWLimitation(ref int pAppliedX, ref int pAppliedY, ref int pSourceX, ref int pSourceY)
        {
            double xRatio = ((double)pAppliedX / (double)pSourceX);
            double yRatio = ((double)pAppliedY / (double)pSourceY);

            if (xRatio > 1.125)
            {
                pSourceX = (int)Math.Ceiling(pAppliedX / 1.125);
                pSourceX = (pSourceX % 2 != 0) ? pSourceX + 1 : pSourceX;
            }

            if (yRatio > 1.125)
            {
                pSourceY = (int)Math.Ceiling(pAppliedY / 1.125);
                pSourceY = (pSourceY % 2 != 0) ? pSourceY + 1 : pSourceY;
            }
        }

    }

}

