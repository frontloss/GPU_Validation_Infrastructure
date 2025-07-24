using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    # region STRUCT_DECLARATIONS

    public struct LatencyValues
    {
        public uint LatencyDisplay;
        public uint LatencyLP1;
        public uint LatencyLP2;
        public uint LatencyLP3;
        public uint LatencyLP4;
    }

    public struct DotClockValues
    {
        public double DotClock;
        public uint HTotal;
        public uint VTotal;
    }

    public struct WatermarkParams
    {
        public double DotClockinMhz;
        public uint HTotal;
        public uint ColorDepth;
        public uint SurfaceWidth;
        public bool IsSinglePipe;
    }

    public struct WatermarkValues
    {
        public uint PrimaryWatermark;
        public uint SpriteWatermark;
        public uint CursorWatermark;
    }
    public struct PlanesStatus
    {
        public bool DisplayPlane;
        public bool CursorPlane;
        public bool SpritePlane;
    }
    public struct SurfaceWidth
    {
        public uint DisplaySurfaceWidth;
        public uint CursorSurfaceWidth;
        public uint SpriteSurfaceWidth;
    }

    public struct DisplayData
    {
        public WatermarkParams watermarkParams;
        public PlanesStatus planesStatus;
        public PipePlaneParams pipePlaneParams;
        public SurfaceWidth surfaceWidth;
        public List<SKLPlaneParameters> SklPlaneParams;
    }

    public struct SKLPlaneParameters
    {
        public GENERIC_PLANE plane;
        public bool IsEnabled;
        public uint ColorDepthInBytes;
        public TileFormat tileFormat;
        public PlanePixelFormat planePixelFormat;
        public double AdjustedPlanePixelRate;
        public uint planeBufferAllocation;
        public uint horizontalSurfaceSize;
        //public uint verticalSurfaceSize;
        public RotationAngle angle;
    }

    public struct DisplayParameters
    {
        public bool IsFBCEnabled;
        public DisplayConfig displayConfig;
        public LatencyValues latencyValues;
        public Dictionary<WatermarkLevel, uint> SklMemoryLatencyValues;
        public Dictionary<DisplayType, DisplayData> DisplayDataList;
    }

    #endregion

    class Watermark : FunctionalBase, IGetMethod
    {
        # region CONSTANTS_DECLARATIONS
        const uint CLOCK_CROSS = 128, BPP_CONSTANT = 8, WATERMARK_CONSTANT = 1000;
        const uint CONSTANT_CURSOR_BPPVALUE = 32, WATERMARK_DATA = 1;
        const uint INCREMENT_VALUE = 64, DEFAULT_SPRITE_WATERMARK = 56, DEFAULT_CURSOR_WATERMARK = 24, SURFACEWIDTH_ADDON = 2;
        const uint LATENCY_CONSTANT_100 = 100, LATENCY_CONSTANT_500 = 500, LATENCY_ADDON_VALUE = 600, MINIMUM_WATERMARK = 128;
        const double DOTCLOCK_CONSTANT = 1000000;

        private const string WM_LINETIME = "WM_LINETIME";

        private const string HTOTAL = "HTOTAL";
        private const string VTOTAL = "VTOTAL";

        private const string PIPE_HOR_SOURCE_SIZE = "PIPE_HOR_SOURCE_SIZE";
        private const string PIPE_VER_SOURCE_SIZE = "PIPE_VER_SOURCE_SIZE";
        private const string PF_HOR_WIN_SIZE = "PF_HOR_WIN_SIZE";
        private const string PF_VER_WIN_SIZE = "PF_VER_WIN_SIZE";

        private const string FBC_REGISTER = "FBC_REGISTER";
        private const string OVERLAY_ENABLE = "OVERLAY_ENABLE";
        private const string PF_INTERLACE_ENABLE = "PF_INTERLACE_ENABLE";
        private const string PANEL_FITTER_ENABLE = "PANEL_FITTER_ENABLE";
        private const string LATENCY_REGISTER_LSB = "LATENCY_REGISTER_LSB";
        private const string LATENCY_REGISTER_MSB = "LATENCY_REGISTER_MSB";
        private const string CURSOR_STATUS = "CURSOR_STATUS";
        private const string DISPLAY_PLANE_STATUS = "DISPLAY_PLANE_STATUS";
        private const string SPRITE_SIZE = "SPRITE_SIZE";

        private const string DISPLAY_WATERMARK_REGISTER = "DISPLAY_WATERMARK_REGISTER";
        private const string SPRITE_WATERMARK_REGISTER = "SPRITE_WATERMARK_REGISTER";
        private const string CURSOR_WATERMARK_REGISTER = "CURSOR_WATERMARK_REGISTER";
        private const string ENABLE = "_ENABLE";
        private const string DISPLAY = "_DISPLAY";
        private const string CURSOR = "_CURSOR";
        private const string SPRITE = "_SPRITE";
        #endregion

        const uint SKL_TRANSITION_MINIMUM = 14, SKL_TRANSITION_AMOUNT = 20;

        public object GetMethod(object argMessage)
        {
            bool status = true;
            Watermark_Params watermarkPar = argMessage as Watermark_Params;
            DisplayType display = watermarkPar.DisplayType;
            Platform platform = base.MachineInfo.PlatformDetails.Platform;

            DisplayParameters displayParams = GetDisplayParameters(platform, watermarkPar);

            if (platform == Platform.HSW || platform == Platform.BDW)
            {
                status = PerformPipeWatermarkCheck(display, displayParams);

                status &= CheckLowPowerWatermark(displayParams);
            }
            else
            {
                status = SKLWaterMarkCalculate(platform, display, displayParams);
            }
            return status;
        }
        private List<GENERIC_PLANE> GetValidPlanes(Platform platform, DisplayHierarchy hierarchy)
        {
            List<GENERIC_PLANE> validPlanes = new List<GENERIC_PLANE>();

            validPlanes.Add(GENERIC_PLANE.PLANE_1);
            validPlanes.Add(GENERIC_PLANE.PLANE_2);
            validPlanes.Add(GENERIC_PLANE.PLANE_3);

            if (platform == Platform.CNL)
                validPlanes.Add(GENERIC_PLANE.PLANE_4);

            return validPlanes;
        }

        private List<SCALAR> GetValidScalers(Platform platform, DisplayHierarchy hierarchy)
        {
            List<SCALAR> validPlanes = new List<SCALAR>();

            validPlanes.Add(SCALAR.Plane_Scalar_1);
            validPlanes.Add(SCALAR.Plane_Scalar_2);

            if (platform == Platform.SKL && hierarchy == DisplayHierarchy.Display_3)
                validPlanes.Remove(SCALAR.Plane_Scalar_2);

            return validPlanes;
        }

        private DisplayParameters GetDisplayParameters(Platform platform, Watermark_Params watermarkPar)
        {
            DisplayParameters displayParams = new DisplayParameters();
            displayParams.DisplayDataList = new Dictionary<DisplayType, DisplayData>();

            displayParams.displayConfig = watermarkPar.CurrentConfig;
            if (platform == Platform.HSW || platform == Platform.BDW)
            {
                displayParams.latencyValues = ComputeLatencyValue();
                displayParams.IsFBCEnabled = VerifyRegisters(FBC_REGISTER, PIPE.PIPE_A, PLANE.NONE, PORT.NONE);
            }
            else
            {
                displayParams.SklMemoryLatencyValues = CalculateSklMemoryLatency();
            }

            displayParams.displayConfig.CustomDisplayList.ForEach(display =>
                {
                    DisplayData tempDisplayData = new DisplayData();
                    PlanesStatus tempPlanesStatus = new PlanesStatus();
                    
                    PipePlaneParams pipePlaneParam = watermarkPar.DisplayParametersList[display].pipePlaneParams;
                    tempDisplayData.pipePlaneParams = pipePlaneParam;

                    Log.Message("Fetching info. for {0} with resolution {1}", display, watermarkPar.DisplayParametersList[display].displayMode.ToString());

                    DisplayMode resolution = watermarkPar.DisplayParametersList[display].displayMode;
                    DotClockValues dotClockValues = GetDotClock(displayParams.displayConfig, pipePlaneParam, resolution);

                    WatermarkParams watermarkParams = new WatermarkParams();
                    watermarkParams.DotClockinMhz = dotClockValues.DotClock;
                    watermarkParams.HTotal = dotClockValues.HTotal;
                    watermarkParams.ColorDepth = resolution.Bpp;
                    watermarkParams.IsSinglePipe = displayParams.displayConfig.ConfigType == DisplayConfigType.SD ? true : false;
                    tempDisplayData.watermarkParams = watermarkParams;
                    
                    if (platform == Platform.HSW || platform == Platform.BDW)
                    {
                        tempPlanesStatus = GetPlanesEnableStatus(pipePlaneParam);
                        tempDisplayData.planesStatus = tempPlanesStatus;

                        SurfaceWidth tempSurfaceWidth = new SurfaceWidth();
                        tempSurfaceWidth.DisplaySurfaceWidth = resolution.HzRes;

                        if (tempPlanesStatus.CursorPlane == true || tempPlanesStatus.SpritePlane == true)
                        {
                            uint spriteSurfaceWidth = 0, cursorSurfaceWidth = 0;

                            GetSurfaceWidth(pipePlaneParam, ref spriteSurfaceWidth, ref cursorSurfaceWidth);
                            tempSurfaceWidth.CursorSurfaceWidth = cursorSurfaceWidth;
                            tempSurfaceWidth.SpriteSurfaceWidth = spriteSurfaceWidth;
                        }
                        tempDisplayData.surfaceWidth = tempSurfaceWidth;
                    }
                    //SKL Data.
                    else if (platform == Platform.SKL || platform == Platform.CNL)
                        tempDisplayData.SklPlaneParams = GetSklPlaneParameters(platform, displayParams.displayConfig, pipePlaneParam, dotClockValues.DotClock);
                    
                    displayParams.DisplayDataList.Add(display, tempDisplayData);
                });

            return displayParams;
        }
        List<SKLPlaneParameters> GetSklPlaneParameters(Platform platform, DisplayConfig displayConfig, PipePlaneParams pipePlaneParam, double AdjustedPipePixelRate)
        {
            List<SKLPlaneParameters> SklPlaneParamsList = new List<SKLPlaneParameters>();
            DisplayHierarchy hierarchy = displayConfig.GetDispHierarchy(pipePlaneParam.DisplayType);

            foreach(GENERIC_PLANE currentPlane in GetValidPlanes(platform, hierarchy))
            {
                SKLPlaneParameters param = new SKLPlaneParameters();
                param.plane = currentPlane;
             
                string eventName = currentPlane.ToString() +"_CTL";
                uint planeCtlValue = 0;
                uint planeOffset = GetOffsetFromEvent(eventName, pipePlaneParam.Pipe, pipePlaneParam.Plane, PORT.NONE);
                ReadRegister(planeOffset, ref planeCtlValue);

                param.IsEnabled = ((planeCtlValue & 0x80000000)==0x80000000);
                if(param.IsEnabled ==true)
                {
                    param.ColorDepthInBytes = GetPlaneBppInBytes(planeCtlValue);
                    param.tileFormat = GetTilingFormat(planeCtlValue);
                    param.planeBufferAllocation = GetPlaneBufferAllocation(pipePlaneParam, currentPlane, planeCtlValue);
                    param.angle = GetPlaneRotationAngle(planeCtlValue);
                    param.planePixelFormat = GetPlanePixelFormat(planeCtlValue);

                    param.AdjustedPlanePixelRate = GetAdjustedPlanePixelRate(platform, displayConfig, pipePlaneParam, currentPlane, AdjustedPipePixelRate);
                    ComputePlaneSizeValues(pipePlaneParam, currentPlane, ref param);

                    SklPlaneParamsList.Add(param);
                }
            }
            return SklPlaneParamsList;
        }

        private double GetAdjustedPlanePixelRate(Platform platform, DisplayConfig displayConfig, PipePlaneParams pipePlaneParams, GENERIC_PLANE plane, double AdjustedPipePixelRate)
        {
            ulong downScalingAmount = 1000000;
            ulong tempPixelRate = 1;

            SCALAR scaler = GetCurrentScalar(platform, displayConfig, pipePlaneParams, false, plane);
            if (scaler != SCALAR.NONE)
            {
                ulong xScaling = 0, yScaling = 0;

                string eventName = plane.ToString() + "_Size";
                uint plane_Size = ReadRegister(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
                uint SrcSizeX = GetRegisterValue(plane_Size, 0, 12) + 1;
                uint SrcSizeY = GetRegisterValue(plane_Size, 16, 27) + 1;
                
                eventName = scaler.ToString() + "_Win_Size";
                uint window_Size = ReadRegister(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
                uint DestSizeX = GetRegisterValue(window_Size, 16, 29);
                uint DestSizeY = GetRegisterValue(window_Size, 0, 12);

                    SrcSizeX *= 1000;
                    SrcSizeY *= 1000;
                    
                    xScaling = SrcSizeX / DestSizeX;
                    yScaling = SrcSizeY / DestSizeY;

                    if (xScaling <= 1000)
                        xScaling = 1000;
                    
                    if (yScaling <= 1000)
                        yScaling = 1000;
                    
                    downScalingAmount = xScaling * yScaling;
            }

            tempPixelRate = (ulong)(downScalingAmount * AdjustedPipePixelRate);

            tempPixelRate = tempPixelRate / 1000000;
            return tempPixelRate;
        }

        private void ComputePlaneSizeValues(PipePlaneParams pipePlaneParam, GENERIC_PLANE currentPlane, ref SKLPlaneParameters param)
        {
            uint planeSize = 0;
            string eventName = default(string);

            eventName = currentPlane.ToString() + "_Size";
            planeSize = ReadRegister(eventName, pipePlaneParam.Pipe, pipePlaneParam.Plane, PORT.NONE);
            param.horizontalSurfaceSize = (planeSize & 0x00001FFF) + 1;
            //param.verticalSurfaceSize = (planeSize & 0x1FFF0000) + 1;
        }

        private PlanePixelFormat GetPlanePixelFormat(uint planeData)
        {
            PlanePixelFormat pixelFormat = PlanePixelFormat.RGB_8_8_8_8;
            uint pixelFormatVal = (planeData & 0x0F000000)>>24;
            pixelFormat = (PlanePixelFormat)pixelFormatVal;

            return pixelFormat;
        }

        private RotationAngle GetPlaneRotationAngle(uint planeData)
        {
            RotationAngle angle = RotationAngle.ROTATION_0;
            uint A1 = planeData & 0x00000003;

            angle = (RotationAngle)A1;

            return angle;
        }

        private uint GetPlaneBufferAllocation(PipePlaneParams pipePlaneParam, GENERIC_PLANE currentPlane, uint planeData)
        {
            uint uPlaneBufAllocation = 0;
            uint uBufferConfig = 0;
            string eventName = default(string);

            //check this condition with harpreet or Soorya.
            if ((planeData & 0x0F000000) != 0x01000000)
            {
                eventName = currentPlane.ToString() + "_BUF_CFG";
            }
            else
            {
                eventName = currentPlane.ToString() + "_NV12_BUF_CFG";                
            }

            uBufferConfig=ReadRegister(eventName, pipePlaneParam.Pipe, pipePlaneParam.Plane, PORT.NONE);
            uPlaneBufAllocation = (uint)Math.Abs((int)((uBufferConfig & 0x03FF0000) >> 16) - (int)(uBufferConfig & 0x000003FF)) + 1;

            return uPlaneBufAllocation;
        }

        private uint GetPlaneBppInBytes(uint planeData)
        {
            uint BPP = 4;
            uint A1 = (planeData & 0x0F000000) >> 24;

            if (A1 == 1 || A1 == 12)
                BPP = 1;
            else if (A1 == 0 || A1 == 14)
                BPP = 2;
            else if (A1 == 6)
                BPP = 8;

            return BPP;
        }

        private TileFormat GetTilingFormat(uint planeData)
        {
            TileFormat tilingFormat = TileFormat.Invalid;
            uint A1 = (planeData & 0x00001C00) >> 10;

            switch(A1)
            {
                case 0:
                    tilingFormat = TileFormat.Linear_Memory;
                    break;
                case 1:
                    tilingFormat = TileFormat.Tile_X_Memory;
                    break;
                case 4:
                    tilingFormat = TileFormat.Tile_Y_Legacy_Memory;
                    break;
                case 5:
                    tilingFormat = TileFormat.Tile_Y_F_Memory;
                    break;
            }

            return tilingFormat;
        }

        #region PipeWatermarkCode

        private bool PerformPipeWatermarkCheck(DisplayType display, DisplayParameters displayParams)
        {
            bool status = true;
            uint expectedWMDisplay = 0, expectedWMSprite = 0, expectedWMcursor = 0;
            WatermarkParams watermarkParams = new WatermarkParams();
            PlanesStatus planesStatus = new PlanesStatus();

            watermarkParams = displayParams.DisplayDataList[display].watermarkParams;
            planesStatus = displayParams.DisplayDataList[display].planesStatus;

            if (planesStatus.DisplayPlane == true)
            {
                watermarkParams.SurfaceWidth = displayParams.DisplayDataList[display].surfaceWidth.DisplaySurfaceWidth;
                ComputeWatermark(displayParams, watermarkParams, PlaneType.DISPLAY, WatermarkType.WM_PIPE, WatermarkLevel.Level_0, ref expectedWMDisplay);

                uint displayWatermarkByDriver = ReadRegister(DISPLAY_WATERMARK_REGISTER, PIPE.NONE, displayParams.DisplayDataList[display].pipePlaneParams.Plane, PORT.NONE);
                if (displayWatermarkByDriver == expectedWMDisplay)
                {
                    Log.Message("Display Watermark Values Matched. Value: " + expectedWMDisplay);
                }
                else if (Math.Abs(displayWatermarkByDriver - expectedWMDisplay) <= 2)
                {
                    Log.Sporadic("Display Watermark Values Mismatched. Expected from Formula: {0}. Observed from Driver: {1}", expectedWMDisplay, displayWatermarkByDriver);
                }
                else
                {
                    Log.Fail("Display Watermark Values Mismatched. Expected from Formula: {0}. Observed from Driver: {1}", expectedWMDisplay, displayWatermarkByDriver);
                    status = false;
                }
            }
            else
            {
                status = false;
                Log.Fail("Display planes are not enabled");
            }

            if (planesStatus.SpritePlane == true)
            {
                watermarkParams.SurfaceWidth = displayParams.DisplayDataList[display].surfaceWidth.SpriteSurfaceWidth;
                ComputeWatermark(displayParams, watermarkParams, PlaneType.SPRITE, WatermarkType.WM_PIPE, WatermarkLevel.Level_0, ref expectedWMSprite);

                uint spriteWatermarkByDriver = ReadRegister(SPRITE_WATERMARK_REGISTER, PIPE.NONE, displayParams.DisplayDataList[display].pipePlaneParams.Plane, PORT.NONE);
                if (spriteWatermarkByDriver == expectedWMSprite)
                {
                    Log.Message("Sprite Watermark Values Matched. Value: " + expectedWMSprite);
                }
                else if (Math.Abs(spriteWatermarkByDriver - expectedWMSprite)<=2)
                {
                    Log.Sporadic("Sprite Watermark Values Mismatched. Expected from Formula: {0}. Observed from Driver: {1}", expectedWMSprite, spriteWatermarkByDriver);
                }
                else
                {
                    Log.Fail("Sprite Watermark Values Mismatched. Expected from Formula: {0}. Observed from Driver: {1}", expectedWMSprite, spriteWatermarkByDriver);
                    status = false;
                }
            }

            if (planesStatus.CursorPlane == true)
            {
                watermarkParams.SurfaceWidth = displayParams.DisplayDataList[display].surfaceWidth.CursorSurfaceWidth;
                watermarkParams.ColorDepth = CONSTANT_CURSOR_BPPVALUE;
                ComputeWatermark(displayParams, watermarkParams, PlaneType.CURSOR, WatermarkType.WM_PIPE, WatermarkLevel.Level_0, ref expectedWMcursor);

                uint cursorWatermarkByDriver = ReadRegister(CURSOR_WATERMARK_REGISTER, PIPE.NONE, displayParams.DisplayDataList[display].pipePlaneParams.Plane, PORT.NONE);
                if (cursorWatermarkByDriver == expectedWMcursor)
                {
                    Log.Message("Cursor Watermark Values Matched. Value: " + expectedWMcursor);
                }
                else if (Math.Abs(cursorWatermarkByDriver - expectedWMcursor)<=2)
                {
                    Log.Sporadic("PIPE Cursor Watermark Values Mismatched. Expected from Formula: {0}. Observed from Driver: {1}", expectedWMcursor, cursorWatermarkByDriver);
                }
                else
                {
                    Log.Fail("PIPE Cursor Watermark Values Mismatched. Expected from Formula: {0}. Observed from Driver: {1}", expectedWMcursor, cursorWatermarkByDriver);
                    status = false;
                }
            }

            if (status)
                Log.Success("PIPE Watermark Values Matched for display: " + display);
            else
                Log.Fail("PIPE Watermark Values not Matched for display: " + display);

            return status;
        }

        #endregion

        #region LPWatermarkCode

        private bool CalculateLPWatermark(DisplayParameters displayParams, WatermarkType watermarkType, WatermarkLevel level, ref WatermarkValues watermarkValues)
        {
            bool IsFIFOExceeded = false;
            watermarkValues.PrimaryWatermark = 0;
            watermarkValues.CursorWatermark = 0;
            watermarkValues.SpriteWatermark = 0;

            Log.Message("Calculating {0} Watermark with {1}", watermarkType, level);
            
            List<AllPlanes> DisplayPlanes = GetEnabledPlanesList(displayParams.DisplayDataList);

            foreach (AllPlanes tempPlane in DisplayPlanes)
            {
                uint finalWatermark = 0;
                DisplayType display = GetDisplayToPlaneMapping(displayParams.displayConfig, tempPlane);
                PlaneType planeType = GetPlaneType(tempPlane);

                WatermarkParams watermarkParams = new WatermarkParams();
                watermarkParams = displayParams.DisplayDataList[display].watermarkParams;

                if (planeType == PlaneType.DISPLAY)
                {
                    watermarkParams.SurfaceWidth = displayParams.DisplayDataList[display].surfaceWidth.DisplaySurfaceWidth;
                }

                if (planeType == PlaneType.SPRITE)
                {
                    watermarkParams.SurfaceWidth = displayParams.DisplayDataList[display].surfaceWidth.SpriteSurfaceWidth;
                }

                if (planeType == PlaneType.CURSOR)
                {
                    watermarkParams.SurfaceWidth = displayParams.DisplayDataList[display].surfaceWidth.CursorSurfaceWidth;
                    watermarkParams.ColorDepth = CONSTANT_CURSOR_BPPVALUE;
                }

                if (ComputeWatermark(displayParams, watermarkParams, planeType, watermarkType, level, ref finalWatermark))
                {
                    IsFIFOExceeded = true;
                    Log.Message(string.Format("FIFO Exceeded for {0} in {1} for {2}, {3}", tempPlane, displayParams.displayConfig.ToString(), watermarkType, level));
                }
                else
                {
                    if (planeType == PlaneType.DISPLAY)
                        watermarkValues.PrimaryWatermark = Math.Max(finalWatermark, watermarkValues.PrimaryWatermark);
                    else if (planeType == PlaneType.CURSOR)
                        watermarkValues.CursorWatermark = Math.Max(finalWatermark, watermarkValues.CursorWatermark);
                    else if (planeType == PlaneType.SPRITE)
                        watermarkValues.SpriteWatermark = Math.Max(finalWatermark, watermarkValues.SpriteWatermark);
                }
            }

            return IsFIFOExceeded;
        }

        private bool CheckLowPowerWatermark(DisplayParameters displayParams)
        {
            bool IsFIFOExceeded = false;
            bool status = true;

            for (int i = 1; i <= 3; i++)//LP1 to LP3
            {
                WatermarkType watermarkType = (WatermarkType)Enum.Parse(typeof(WatermarkType), i.ToString());
                WatermarkLevel watermarkLevel = (WatermarkLevel)Enum.Parse(typeof(WatermarkLevel), i.ToString());
                WatermarkValues watermarkValues = new WatermarkValues();
                string eventName = watermarkType.ToString() + ENABLE;

                if (watermarkType == WatermarkType.WM_LP2 || watermarkType == WatermarkType.WM_LP3)
                {
                    watermarkLevel = WatermarkLevel.Level_4;
                    IsFIFOExceeded = CalculateLPWatermark(displayParams, watermarkType, watermarkLevel, ref watermarkValues);

                    //if exceeded maximum
                    if (watermarkType == WatermarkType.WM_LP2)
                    {
                        if (IsFIFOExceeded)
                        {
                            watermarkLevel = WatermarkLevel.Level_2;
                            Log.Message("MaxFIFO exceeded. So, calculating watermark with " + watermarkLevel);
                        }
                        else
                        {
                            watermarkLevel = WatermarkLevel.Level_3;
                            Log.Message("MaxFIFO does not exceeded. So, calculating watermark with " + watermarkLevel);
                        }
                    }
                    else if (watermarkType == WatermarkType.WM_LP3)
                    {
                        if (IsFIFOExceeded)
                        {
                            watermarkLevel = WatermarkLevel.Level_3;
                            Log.Message("MaxFIFO exceeded. So, calculating watermark with " + watermarkLevel);
                        }
                        else
                        {
                            watermarkLevel = WatermarkLevel.Level_4;
                            Log.Message("MaxFIFO does not exceeded. So, calculating watermark with " + watermarkLevel);
                        }
                    }
                }

                //Log.Message(String.Format("Calculating watermark for {0} with {1}", watermarkType, watermarkLevel));

                IsFIFOExceeded = CalculateLPWatermark(displayParams, watermarkType, watermarkLevel, ref watermarkValues);

                bool LP_Status = VerifyRegisters(eventName, PIPE.NONE, PLANE.PLANE_A, PORT.NONE);

                if (IsFIFOExceeded)
                {
                    //LP* should be disabled
                    if (LP_Status != true)
                    {
                        Log.Message(string.Format("Watermark {0} disabled as expected for {1}", watermarkType, eventName));
                    }
                    else
                    {
                        status = false;
                        Log.Fail(string.Format("Watermark {0} is still enabled which is not expected for {1}", watermarkType, eventName));
                    }
                }
                else
                {
                    uint primaryWatermark = ReadRegister(watermarkType + DISPLAY, PIPE.NONE, PLANE.PLANE_A, PORT.NONE);
                    
                    //LP* Should be enabled with the finalWatermark
                    if (LP_Status == true)
                    {
                        Log.Success(string.Format("Watermark {0} enabled as expected for {1}", watermarkType, eventName));
                    }
                    else
                    {
                        status = false;
                        Log.Fail(string.Format("Watermark {0} is still disabled which is not expected for {1}", watermarkType, eventName));
                    }
                    
                     if (primaryWatermark == watermarkValues.PrimaryWatermark)
                        Log.Success(string.Format("{0} Watermark values matched for Display Plane: {1}", watermarkType, primaryWatermark));
                    else if (Math.Abs(primaryWatermark - watermarkValues.PrimaryWatermark)<=2)
                         Log.Sporadic(string.Format("{0} Watermark values mismatched for Display Plane. Expected: {1}, Programmed: {2}", watermarkType, watermarkValues.PrimaryWatermark, primaryWatermark));
                    else
                    {
                        status = false;
                        Log.Fail(string.Format("{0} Watermark values mismatched for Display Plane. Expected: {1}, Programmed: {2}", watermarkType, watermarkValues.PrimaryWatermark, primaryWatermark));
                    }

                    if (true == IsCursorPlaneEnabled(displayParams.DisplayDataList))
                    {
                        uint cursorWatermark = ReadRegister(watermarkType + CURSOR, PIPE.NONE, PLANE.PLANE_A, PORT.NONE);
                        if (cursorWatermark == watermarkValues.CursorWatermark)
                            Log.Success(string.Format("{0} Watermark values matched for Cursor: {1}", watermarkType, cursorWatermark));
                        else if (Math.Abs(cursorWatermark - watermarkValues.CursorWatermark)<=2)
                            Log.Sporadic(string.Format("{0} Watermark values mismatched for Cursor. Expected: {1}, Programmed: {2}", watermarkType, watermarkValues.CursorWatermark, cursorWatermark));
                        else
                        {
                            status = false;
                            Log.Fail(string.Format("{0} Watermark values mismatched for Cursor. Expected: {1}, Programmed: {2}", watermarkType, watermarkValues.CursorWatermark, cursorWatermark));
                        }
                    }
                    else
                        Log.Verbose("Cursor Plane not enabled.");

                    if (true == IsSpritePlaneEnabled(displayParams.DisplayDataList))
                    {
                        uint spriteWatermark = ReadRegister(watermarkType + SPRITE, PIPE.NONE, PLANE.PLANE_A, PORT.NONE);
                        
                        if (spriteWatermark == watermarkValues.SpriteWatermark)
                            Log.Success(string.Format("{0} Watermark values matched for sprite: {1}", watermarkType, spriteWatermark));
                        else if (Math.Abs(spriteWatermark - watermarkValues.SpriteWatermark) <= 2)
                            Log.Sporadic(string.Format("{0} Watermark values mismatched for sprite. Expected: {1}, Programmed: {2}", watermarkType, watermarkValues.SpriteWatermark, spriteWatermark));
                        else
                        {
                            status = false;
                            Log.Fail(string.Format("{0} Watermark values mismatched for sprite. Expected: {1}, Programmed: {2}", watermarkType, watermarkValues.SpriteWatermark, spriteWatermark));
                        }
                    }
                    else
                        Log.Verbose("Sprite Plane not enabled.");

                }//else end of FIFO not exceeded.

            }//End of LP* loop for loop.

            return status;
        }

        private List<AllPlanes> GetEnabledPlanesList(Dictionary<DisplayType, DisplayData> DisplayDataList)
        {
            List<AllPlanes> DisplayPlanes = new List<AllPlanes>();

            for (int i = 0; i < DisplayDataList.Count; i++)
            {
                DisplayData dispData = DisplayDataList.Values.ElementAt(i);
                if (dispData.planesStatus.DisplayPlane == true)
                {
                    AllPlanes tempPlane = (AllPlanes)Enum.Parse(typeof(AllPlanes), i.ToString());
                    DisplayPlanes.Add(tempPlane);
                }

                if (dispData.planesStatus.SpritePlane == true)
                {
                    AllPlanes tempPlane = (AllPlanes)Enum.Parse(typeof(AllPlanes), (3 + i).ToString());
                    DisplayPlanes.Add(tempPlane);
                }

                if (dispData.planesStatus.CursorPlane == true)
                {
                    AllPlanes tempPlane = (AllPlanes)Enum.Parse(typeof(AllPlanes), (6 + i).ToString());
                    DisplayPlanes.Add(tempPlane);
                }
            }

            return DisplayPlanes;
        }

        private PlaneType GetPlaneType(AllPlanes plane)
        {
            PlaneType planeType = PlaneType.DISPLAY;

            switch (plane)
            {
                case AllPlanes.PLANE_A:
                case AllPlanes.PLANE_B:
                case AllPlanes.PLANE_C:
                    planeType = PlaneType.DISPLAY;
                    break;
                case AllPlanes.CursorA:
                case AllPlanes.CursorB:
                case AllPlanes.CursorC:
                    planeType = PlaneType.CURSOR;
                    break;
                case AllPlanes.SpriteA:
                case AllPlanes.SpriteB:
                case AllPlanes.SpriteC:
                    planeType = PlaneType.SPRITE;
                    break;
                default:
                    break;
            }

            return planeType;
        }

        private DisplayType GetDisplayToPlaneMapping(DisplayConfig displayConfig, AllPlanes plane)
        {
            DisplayType display = DisplayType.None;

            switch (plane)
            {
                case AllPlanes.PLANE_A:
                case AllPlanes.CursorA:
                case AllPlanes.SpriteA:
                    display = displayConfig.CustomDisplayList[0];
                    break;
                case AllPlanes.PLANE_B:
                case AllPlanes.CursorB:
                case AllPlanes.SpriteB:
                    display = displayConfig.CustomDisplayList[1];
                    break;
                case AllPlanes.PLANE_C:
                case AllPlanes.CursorC:
                case AllPlanes.SpriteC:
                    display = displayConfig.CustomDisplayList[2];
                    break;
                default:
                    break;
            }

            return display;
        }
        #endregion

        #region CommonMethods

        private bool ComputeWatermark(DisplayParameters displayParams, WatermarkParams watermarkParam, PlaneType planeType, WatermarkType watermarkType, WatermarkLevel watermarkLevel, ref uint finalWatermarkValue)
        {
            uint FIFOBuffer = 0;
            bool bComputeSmallBuffer = true, bComputeLargeBuffer = true;
            uint smallBufferValue = 0, largeBufferValue = 0;
            finalWatermarkValue = 0;
            bool IsFIFOExceeded = false;

            bool IsSpriteEnabled = IsSpritePlaneEnabled(displayParams.DisplayDataList);
            uint latency = GetPlaneLatencyValue(displayParams.latencyValues, watermarkLevel);

            Log.Verbose("Calculating Watermark for PlaneType= {0}, WatermarkType={1}, WatermarkLevel={2}", planeType, watermarkType, watermarkLevel);

            if (planeType == PlaneType.CURSOR)
                bComputeSmallBuffer = false;

            if (planeType == PlaneType.DISPLAY && watermarkType == WatermarkType.WM_PIPE)
                bComputeLargeBuffer = false;

            if (bComputeSmallBuffer)
            {
                smallBufferValue = (uint)(watermarkParam.DotClockinMhz * (watermarkParam.ColorDepth / BPP_CONSTANT) * latency) / WATERMARK_CONSTANT;

                if (smallBufferValue < MINIMUM_WATERMARK)
                    smallBufferValue = MINIMUM_WATERMARK;

                FIFOBuffer = smallBufferValue;
                Log.Verbose("DotClock= {0}, ColorDepth={1}, latency={2}, SmallBuffer={3}", watermarkParam.DotClockinMhz, watermarkParam.ColorDepth, latency, smallBufferValue);
            }

            if (bComputeLargeBuffer)
            {
                uint linetime = 0;
                if (true)
                {
                    linetime = (uint)((watermarkParam.HTotal * WATERMARK_CONSTANT) / watermarkParam.DotClockinMhz);
                    largeBufferValue = ((latency / linetime) + WATERMARK_DATA) * watermarkParam.SurfaceWidth * (watermarkParam.ColorDepth / BPP_CONSTANT);
                }
                else
                {
                    linetime = (uint)(watermarkParam.HTotal / watermarkParam.DotClockinMhz);
                    largeBufferValue = ((latency / linetime / WATERMARK_CONSTANT) + WATERMARK_DATA) * watermarkParam.SurfaceWidth * (watermarkParam.ColorDepth / BPP_CONSTANT);
                }
                if (largeBufferValue < MINIMUM_WATERMARK)
                    largeBufferValue = MINIMUM_WATERMARK;

                FIFOBuffer = largeBufferValue;
                Log.Verbose("DotClock= {0}, HTotal={1}, LineTime={2}, latency={3}, SurfaceWidth={4}, ColorDepth={5}, LargeBuffer={6}",
                    watermarkParam.DotClockinMhz, watermarkParam.HTotal, linetime, latency, watermarkParam.SurfaceWidth, watermarkParam.ColorDepth, largeBufferValue);
            }

            if (bComputeSmallBuffer && bComputeLargeBuffer)
            {
                FIFOBuffer = Math.Min(smallBufferValue, largeBufferValue);
            }

            FIFOBuffer += CLOCK_CROSS;

            if (FIFOBuffer > GetMaxWatermarkValue(watermarkType, planeType, watermarkParam.IsSinglePipe, IsSpriteEnabled, displayParams.IsFBCEnabled))
                IsFIFOExceeded = true;
            Log.Verbose(string.Format("After Addition of Clock_Gross amount: {0} results to {1}", CLOCK_CROSS, FIFOBuffer));
            finalWatermarkValue = (((FIFOBuffer % INCREMENT_VALUE) == 0) ? (FIFOBuffer / INCREMENT_VALUE) : (FIFOBuffer / INCREMENT_VALUE) + 1);
            Log.Verbose(string.Format("Dividing the final value with {0} results to {1}", INCREMENT_VALUE, finalWatermarkValue));

            return IsFIFOExceeded;
        }

        /// <summary>
        /// Obtains the DotClock for the Display
        /// </summary>
        /// <param name="presentResolution">Resolition to which DotClock to be Calculated</param>
        /// <param name="display">Display to which DotClock to be Calculated</param>
        private DotClockValues GetDotClock(DisplayConfig displayConfig, PipePlaneParams pipePlaneParam, DisplayMode presentResolution)
        {
            DotClockValues dotClockValues = new DotClockValues();

            dotClockValues.HTotal = GetHTotal(pipePlaneParam);

            dotClockValues.DotClock = presentResolution.InterlacedFlag == 0 ? presentResolution.pixelClock : (presentResolution.pixelClock / 2);
            Log.Verbose(string.Format("DotClock Value is : {0}", dotClockValues.DotClock));

            bool PFInterlaced = VerifyRegisters(PF_INTERLACE_ENABLE, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE);
            if (PFInterlaced == true)
            {
                dotClockValues.DotClock = dotClockValues.DotClock * 2;
                Log.Message(string.Format("DotClock when Progressive Fetch - Interlace Display enabled : {0}", dotClockValues.DotClock));
            }
            else
            {
                Log.Verbose("Progressive Fetch - Interlace Display  is not Enabled");
            }

            // Computing DownScaling.
            bool scalerEnabled = false;
            uint DestSizeX = 0;
            uint DestSizeY = 0;

            if (base.MachineInfo.PlatformDetails.Platform == Platform.HSW || base.MachineInfo.PlatformDetails.Platform == Platform.BDW)
            {
                scalerEnabled = VerifyRegisters(PANEL_FITTER_ENABLE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
                if (scalerEnabled == true)
                {
                    DestSizeX = ReadRegister(PF_HOR_WIN_SIZE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
                    DestSizeY = ReadRegister(PF_VER_WIN_SIZE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
                }
            }
            else if (base.MachineInfo.PlatformDetails.Platform == Platform.SKL || base.MachineInfo.PlatformDetails.Platform == Platform.CNL)
            {
                dotClockValues.DotClock *= 1000;
                SCALAR scaler = GetCurrentScalar(base.MachineInfo.PlatformDetails.Platform, displayConfig, pipePlaneParam, true, GENERIC_PLANE.NONE);

                if (scaler != SCALAR.NONE)
                {
                    scalerEnabled = true;
                    string eventName = scaler.ToString() + "_Win_Size";
                    uint window_Size = ReadRegister(eventName, pipePlaneParam.Pipe, pipePlaneParam.Plane, PORT.NONE);

                    DestSizeX = GetRegisterValue(window_Size, 16, 29);
                    DestSizeY = GetRegisterValue(window_Size, 0, 12);
                }
            }
            else
            {
                Log.Abort("Platform: {0} not supported.", base.MachineInfo.PlatformDetails.Platform);
            }

            if (scalerEnabled == true)
            {
                ulong xScaling = 0, yScaling = 0;
                UInt64 downScalingAmount = 1;
                Log.Verbose("Panel Fitter is Enabled");

                uint SrcSizeX = ReadRegister(PIPE_HOR_SOURCE_SIZE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE) + 1;
                uint SrcSizeY = ReadRegister(PIPE_VER_SOURCE_SIZE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE) + 1;
                SrcSizeX *= 1000;
                SrcSizeY *= 1000;

                xScaling = SrcSizeX / DestSizeX;
                yScaling = SrcSizeY / DestSizeY;

                if (xScaling <= 1000)
                    xScaling = 1000;
                if (yScaling <= 1000)
                    yScaling = 1000;

                downScalingAmount = xScaling * yScaling;
                dotClockValues.DotClock = dotClockValues.DotClock * downScalingAmount;

                dotClockValues.DotClock = dotClockValues.DotClock / 1000000;
            }
            else
            {
                Log.Message("Panel Fitter is not Enabled");
            }

            Log.Message(string.Format("The Values of DotClock = {0} HTOTAL = {1}",
                dotClockValues.DotClock, dotClockValues.HTotal));

            return dotClockValues;
        }

        private SCALAR GetCurrentScalar(Platform platform, DisplayConfig displayConfig, PipePlaneParams pipePlaneParams, bool IsPipeCall, GENERIC_PLANE plane)
        {
            SCALAR scaler = SCALAR.NONE;

            Dictionary<SCALAR, SCALAR_MAP> ScalarMapper = new Dictionary<SCALAR, SCALAR_MAP>();
            DisplayHierarchy hierarchy = displayConfig.GetDispHierarchy(pipePlaneParams.DisplayType);

            foreach (SCALAR currScalar in GetValidScalers(platform, hierarchy))
            {
                string eventName = currScalar + "_Enable";
                if (VerifyRegisters(eventName, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE))
                {
                    bool status = IsScalerEnabled(pipePlaneParams, currScalar, IsPipeCall, plane);
                    if (status == true)
                    {
                        scaler = currScalar;

                        if (IsPipeCall)
                            Log.Verbose("{0} is enabled and mapped for Pipe for {1}", currScalar, pipePlaneParams.DisplayType);
                        else
                            Log.Verbose("{0} is enabled and mapped for {1} for {2}", currScalar, plane, pipePlaneParams.DisplayType);
                    }

                }
                else
                    Log.Verbose("{0} is not enabled for {1}", currScalar, pipePlaneParams.DisplayType);
            }

            return scaler;
        }

        private bool IsScalerEnabled(PipePlaneParams pipePlaneObject, SCALAR currentScalar, bool IsPipeCall, GENERIC_PLANE plane)
        {
            bool status = false;
            IsPipeCall = false;
            plane = GENERIC_PLANE.NONE;
            SCALAR_MAP currentScalarMap = SCALAR_MAP.NONE;

            string eventName = currentScalar.ToString() + "_Binding";
            uint scalarVal = ReadRegister(eventName, pipePlaneObject.Pipe, pipePlaneObject.Plane, PORT.NONE);
            currentScalarMap = (SCALAR_MAP)scalarVal;

            if (IsPipeCall == true)
            {
                if (currentScalarMap == SCALAR_MAP.PIPE)
                {
                    status = true;
                }
            }
            else
            {
                switch (currentScalarMap)
                {
                    case SCALAR_MAP.PLANE_1:
                        if (plane == GENERIC_PLANE.PLANE_1)
                            status = true;
                        break;

                    case SCALAR_MAP.PLANE_2:
                        if (plane == GENERIC_PLANE.PLANE_2)
                            status = true;
                        break;

                    case SCALAR_MAP.PLANE_3:
                        if (plane == GENERIC_PLANE.PLANE_3)
                            status = true;
                        break;

                    case SCALAR_MAP.PLANE_4:
                        if (plane == GENERIC_PLANE.PLANE_4)
                            status = true;
                        break;
                }
            }
            return status;
        }

        private uint GetHTotal(PipePlaneParams pipePlaneParam)
        {
            uint uHtotal = 0;
            uint lane_cnt = 0, bpp = 0;
            uint HActive, HSync, HFPorch, HBPorch, HSyncStart, HSyncEnd = 0;

            // To calculate HTotal for MIPI in BXT MIPI  

            if (base.MachineInfo.PlatformDetails.Platform == Platform.BXT && pipePlaneParam.DisplayType == DisplayType.MIPI)
            {
                uint uMIPIA_PortCtrl = 0, uMIPIC_PortCtrl = 0, uMIPIACtrl = 0, uMIPICCtrl = 0, uMIPI_HSync = 0,
                    uMIPI_HFrontPorch = 0, uMIPI_HBackPorch = 0, uMIPI_HActive = 0, uMIPIA_DSI = 0, uMIPIC_DSI = 0,
                    uMIPIA_VideoMode = 0, uMIPIC_VideoMode = 0, uMIPIA_VTotal = 0, uMIPIC_VTotal = 0;

                uint monitorID = base.EnumeratedDisplays.Where(item => item.DisplayType == pipePlaneParam.DisplayType).FirstOrDefault().CUIMonitorID;

                ReadRegister((uint)0x6B0C0, ref uMIPIA_PortCtrl);
                ReadRegister((uint)0x6B8C0, ref uMIPIC_PortCtrl);
                ReadRegister((uint)0x6B104, ref uMIPIACtrl);
                ReadRegister((uint)0x6B904, ref uMIPICCtrl);
                ReadRegister((uint)0x6B028, ref uMIPI_HSync);
                ReadRegister((uint)0x6B02C, ref uMIPI_HFrontPorch);
                ReadRegister((uint)0x6B030, ref uMIPI_HBackPorch);
                ReadRegister((uint)0x6B034, ref uMIPI_HActive);
                ReadRegister((uint)0x6B00C, ref uMIPIA_DSI);
                ReadRegister((uint)0x6B80C, ref uMIPIC_DSI);
                ReadRegister((uint)0x6B058, ref uMIPIA_VideoMode);
                ReadRegister((uint)0x6B858, ref uMIPIC_VideoMode);
                ReadRegister((uint)0x6B100, ref uMIPIA_VTotal);
                ReadRegister((uint)0x6B900, ref uMIPIC_VTotal);


                // if ((((uMIPIA_PortCtrl & 0x80000000) == 0x80000000) && (((uMIPIACtrl & 0x00000380) >> 7) == pipeCount))) // CHeck for MIPI A enabld and pipe select
                if (((uMIPIA_PortCtrl & 0x80000000) == 0x80000000) && (monitorID == 0x41104))
                {
                    uint A1 = 0;
                    A1 = (uMIPIA_DSI & 0x00000780) >> 7;

                    if (A1 == 1)
                        bpp = 16;
                    else if (A1 == 3)
                        bpp = 18;
                    else if (A1 == 4)
                        bpp = 24;

                    lane_cnt = uMIPIA_DSI & 0x00000007;

                }
                // if ((((uMIPIC_PortCtrl & 0x80000000) == 0x80000000) && (((uMIPIACtrl & 0x00000380) >> 7) == pipeCount))) // CHeck for MIPI C enabld and pipe select
                if (((uMIPIC_PortCtrl & 0x80000000) == 0x80000000) && (monitorID == 0x41104))
                {
                    uint A1 = 0;
                    A1 = (uMIPIC_DSI & 0x00000780) >> 7;

                    if (A1 == 1)
                        bpp = 16;
                    else if (A1 == 3)
                        bpp = 18;
                    else if (A1 == 4)
                        bpp = 24;

                    lane_cnt = uMIPIC_DSI & 0x00000007;
                }


                // To convert bytclk to pixelclk

                //ulValue = (ulPixelCount * pThis->m_ucBitsPerPixel) / (pThis->m_ucLaneCount * 8);

                HActive = (uint)Math.Ceiling(((double)uMIPI_HActive * lane_cnt * 8)) / bpp;

                HSync = (uint)Math.Ceiling(((double)uMIPI_HSync * lane_cnt * 8)) / bpp;

                HFPorch = (uint)Math.Ceiling(((double)uMIPI_HFrontPorch * lane_cnt * 8)) / bpp;

                HBPorch = (uint)Math.Ceiling(((double)uMIPI_HBackPorch * lane_cnt * 8)) / bpp;

                // HSyncStart = HFrontPorch + HActive
                HSyncStart = HFPorch + HActive;

                // HSyncEnd = HSync + (HSyncStart - 1)

                HSyncEnd = HSync + HSyncStart - 1;

                //Htotal = HBackPorch + HSyncEnd + 1

                uHtotal = HBPorch + HSyncEnd + 1;

                Log.Verbose("\nMIPI HTotal calculated:" + (uHtotal));

            }
            else
            {
                uHtotal = ReadRegister(HTOTAL, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE) + 1;
            }

            return uHtotal;
        }

        /// <summary>
        /// Returns the SurfaceDepth of the corresponding plane of the display
        /// </summary>
        /// <param name="display"></param>
        private void GetSurfaceWidth(PipePlaneParams pipePlaneParam, ref uint spriteSurfaceWidth, ref uint cursorSurfaceWidth)
        {
            spriteSurfaceWidth = ReadRegister(SPRITE_SIZE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE) + 1;
            //spriteSurfaceWidth = (spriteSurfaceWidth + 1) * SURFACEWIDTH_ADDON; Refer this from softbios code.

            uint tempCursorValue = ReadRegister(CURSOR_STATUS, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
            if (tempCursorValue == 2 || tempCursorValue == 34 || tempCursorValue == 37)
            {
                cursorSurfaceWidth = 128;
            }
            else if (tempCursorValue == 3 || tempCursorValue == 35 || tempCursorValue == 38)
            {
                cursorSurfaceWidth = 256;
            }
            else if (tempCursorValue == 4 || tempCursorValue == 5 || tempCursorValue == 6 || tempCursorValue == 7 || tempCursorValue == 36 || tempCursorValue == 39)
            {
                cursorSurfaceWidth = 64;
            }
        }
        public uint GetMaxWatermarkValue(WatermarkType watermarkType, PlaneType planeType, bool IsSinglePipe, bool isSpriteEnabled, bool IsDBPEnabled)
        {
            uint maxWaterMark = 0;

            if (base.AppManager.MachineInfo.PlatformDetails.Platform == Platform.BDW)
            {
                maxWaterMark = GetBDWMaxWatermarkValue(watermarkType, planeType, IsSinglePipe, isSpriteEnabled, IsDBPEnabled);
            }
            else
            {
                maxWaterMark = GetHSWMaxWatermarkValue(watermarkType, planeType, IsSinglePipe, isSpriteEnabled, IsDBPEnabled);
            }
            return maxWaterMark;
        }

        public uint GetHSWMaxWatermarkValue(WatermarkType watermarkType, PlaneType planeType, bool IsSinglePipe, bool isSpriteEnabled, bool IsDBPEnabled)
        {
            uint maxWaterMark = 0;

            if (watermarkType == WatermarkType.WM_PIPE)
            {
                if (planeType == PlaneType.DISPLAY)
                {
                    maxWaterMark = 8128;//127;
                }
                else if (planeType == PlaneType.CURSOR)
                {
                    maxWaterMark = 4032;// 63;
                }
                else if (planeType == PlaneType.SPRITE)
                {
                    maxWaterMark = 8128;// 127;
                }
            }
            else//For WM_LP*
            {
                if (IsSinglePipe)//Single pipe
                {
                    if (planeType == PlaneType.DISPLAY)
                    {
                        if (isSpriteEnabled == true)
                        {
                            if (IsDBPEnabled)
                                maxWaterMark = 8192;//128;
                            else
                                maxWaterMark = 24576;//384;
                        }
                        else
                            maxWaterMark = 49152;// 768;
                    }
                    else if (planeType == PlaneType.CURSOR)
                    {
                        maxWaterMark = 16320;// 255;
                    }
                    else if (planeType == PlaneType.SPRITE)
                    {
                        if (IsDBPEnabled)
                            maxWaterMark = 40960;//640;
                        else
                            maxWaterMark = 24576;//384;
                    }
                    else if (planeType == PlaneType.FBC)
                    {
                        maxWaterMark = 960;// 15;
                    }
                }
                else//multipipe
                {
                    if (planeType == PlaneType.DISPLAY)
                    {
                        if (isSpriteEnabled == true)
                            maxWaterMark = 8192;//128;
                        else
                            maxWaterMark = 16384;// 256;
                    }
                    else if (planeType == PlaneType.CURSOR)
                    {
                        maxWaterMark = 4096;// 64;
                    }
                    else if (planeType == PlaneType.SPRITE)
                    {
                        maxWaterMark = 8192;//128;
                    }
                    else if (planeType == PlaneType.FBC)
                    {
                        maxWaterMark = 960;// 15;
                    }
                }
            }

            return maxWaterMark;
        }

        public uint GetBDWMaxWatermarkValue(WatermarkType watermarkType, PlaneType planeType, bool IsSinglePipe, bool isSpriteEnabled, bool IsDBPEnabled)
        {
            uint maxWaterMark = 0;

            if (watermarkType == WatermarkType.WM_PIPE)
            {
                if (planeType == PlaneType.DISPLAY)
                {
                    maxWaterMark = 16320;//255;
                }
                else if (planeType == PlaneType.CURSOR)
                {
                    maxWaterMark = 4032;// 63;
                }
                else if (planeType == PlaneType.SPRITE)
                {
                    maxWaterMark = 16320;//255 ;
                }
            }
            else//For WM_LP*
            {
                if (IsSinglePipe)//Single pipe
                {
                    if (planeType == PlaneType.DISPLAY)
                    {
                        if (isSpriteEnabled == true)
                        {
                            if (IsDBPEnabled)
                                maxWaterMark = 32768;//512;
                            else
                                maxWaterMark = 98304;//1536;
                        }
                        else
                            maxWaterMark = 131008;// 2047;
                    }
                    else if (planeType == PlaneType.CURSOR)
                    {
                        maxWaterMark = 16384;// 255;
                    }
                    else if (planeType == PlaneType.SPRITE)
                    {
                        if (IsDBPEnabled)
                            maxWaterMark = 131008;//2047;
                        else
                            maxWaterMark = 98304;//384;
                    }
                    else if (planeType == PlaneType.FBC)
                    {
                        maxWaterMark = 1984;// 31;
                    }
                }
                else//multipipe
                {
                    if (planeType == PlaneType.DISPLAY)
                    {
                        if (isSpriteEnabled == true)
                            maxWaterMark = 32768;//512;
                        else
                            maxWaterMark = 65536;// 1024;
                    }
                    else if (planeType == PlaneType.CURSOR)
                    {
                        maxWaterMark = 4096;// 64;
                    }
                    else if (planeType == PlaneType.SPRITE)
                    {
                        maxWaterMark = 32768;//512;
                    }
                    else if (planeType == PlaneType.FBC)
                    {
                        maxWaterMark = 1984;// 31;
                    }
                }
            }

            return maxWaterMark;
        }

        //private uint GetMaxWatermarkValue(WatermarkType watermarkType, PlaneType planeType, bool IsSinglePipe, bool isSpriteEnabled, bool IsDBPEnabled)
        //{
        //    uint maxWaterMark = 0;

        //    if (watermarkType == WatermarkType.WM_PIPE)
        //    {
        //        if (planeType == PlaneType.DISPLAY)
        //        {
        //            maxWaterMark = 8128;//127;
        //        }
        //        else if (planeType == PlaneType.CURSOR)
        //        {
        //            maxWaterMark = 4032;// 63;
        //        }
        //        else if (planeType == PlaneType.SPRITE)
        //        {
        //            maxWaterMark = 8128;// 127;
        //        }
        //    }
        //    else//For WM_LP*
        //    {
        //        //bool IsDBPEnabled = VerifyRegisters(FBC_REGISTER, PIPE.PIPE_A, PLANE.NONE, PORT.NONE); //optimize this    //Check if DataBufferPartitioning is Enabled
        //        if (IsSinglePipe)//Single pipe
        //        {
        //            if (planeType == PlaneType.DISPLAY)
        //            {
        //                if (isSpriteEnabled == true)
        //                {
        //                    if (IsDBPEnabled)
        //                        maxWaterMark = 8192;//128;
        //                    else
        //                        maxWaterMark = 24576;//384;
        //                }
        //                else
        //                    maxWaterMark = 49152;// 768;
        //            }
        //            else if (planeType == PlaneType.CURSOR)
        //            {
        //                maxWaterMark = 16320;// 255;
        //            }
        //            else if (planeType == PlaneType.SPRITE)
        //            {
        //                if (IsDBPEnabled)
        //                    maxWaterMark = 40960;//640;
        //                else
        //                    maxWaterMark = 24576;//384;
        //            }
        //            else if (planeType == PlaneType.FBC)
        //            {
        //                maxWaterMark = 960;// 15;
        //            }
        //        }
        //        else//multipipe
        //        {
        //            if (planeType == PlaneType.DISPLAY)
        //            {
        //                if (isSpriteEnabled == true)
        //                    maxWaterMark = 8192;//128;
        //                else
        //                    maxWaterMark = 16384;// 256;
        //            }
        //            else if (planeType == PlaneType.CURSOR)
        //            {
        //                maxWaterMark = 4096;// 64;
        //            }
        //            else if (planeType == PlaneType.SPRITE)
        //            {
        //                maxWaterMark = 8192;//128;
        //            }
        //            else if (planeType == PlaneType.FBC)
        //            {
        //                maxWaterMark = 960;// 15;
        //            }
        //        }
        //    }

        //    return maxWaterMark;
        //}

        private LatencyValues ComputeLatencyValue()
        {
            LatencyValues latencyValues = new LatencyValues();

            uint LatencyLSB = ReadRegister(LATENCY_REGISTER_LSB, PIPE.PIPE_A, PLANE.NONE, PORT.NONE);
            uint LatencyMSB = ReadRegister(LATENCY_REGISTER_MSB, PIPE.PIPE_A, PLANE.NONE, PORT.NONE);

            latencyValues.LatencyDisplay = GetRegisterValue(LatencyMSB, 24, 31) * LATENCY_CONSTANT_100;
            if (latencyValues.LatencyDisplay == 0)
                latencyValues.LatencyDisplay = GetRegisterValue(LatencyLSB, 0, 3) * LATENCY_CONSTANT_100;

            latencyValues.LatencyLP4 = GetRegisterValue(LatencyMSB, 0, 8) * LATENCY_CONSTANT_500;
            latencyValues.LatencyLP3 = GetRegisterValue(LatencyLSB, 20, 28) * LATENCY_CONSTANT_500;
            latencyValues.LatencyLP2 = GetRegisterValue(LatencyLSB, 12, 19) * LATENCY_CONSTANT_500;
            latencyValues.LatencyLP1 = GetRegisterValue(LatencyLSB, 4, 11) * LATENCY_CONSTANT_500;

            return latencyValues;
        }
        private Dictionary<WatermarkLevel, uint> CalculateSklMemoryLatency()
        {
            UInt32 uMailbox_Data0 = 0;
            UInt32 uMailbox_Data1 = 0;
            UInt32 uMailbox_Interface = 0x80000006;     //As per Bspec with Error code =06h and Run/busy=1
            UInt32 uLatency_Data0 = 0;
            UInt32 uLatency_Data1 = 0;
            //uint[] Latency = { 0, 0, 0, 0, 0, 0, 0, 0 };
            Dictionary<WatermarkLevel, uint> Latency = new Dictionary<WatermarkLevel, uint>();

            Log.Verbose("Computing SKL Memory Latency Values.");

            //Write the Mailbox register value

            WriteRegister(0x138128, uMailbox_Data0);
            WriteRegister(0x13812C, uMailbox_Data1);
            WriteRegister(0x138124, uMailbox_Interface);

            ReadRegister((uint)0x138124, ref uMailbox_Interface);
            ReadRegister((uint)0x138124, ref uMailbox_Interface);

            //Read the Set One Latency Value
            ReadRegister((uint)0x138128, ref uLatency_Data0);

            uMailbox_Data0 = 1;
            uMailbox_Data1 = 0;
            uMailbox_Interface = 0x80000006;

            //Write the Mailbox register value

            WriteRegister(0x138128, uMailbox_Data0);
            WriteRegister(0x13812C, uMailbox_Data1);
            WriteRegister(0x138124, uMailbox_Interface);

            ReadRegister((uint)0x138124, ref uMailbox_Interface);
            ReadRegister((uint)0x138124, ref uMailbox_Interface);


            //Read the Set One Latency Value
            ReadRegister((uint)0x138128, ref uLatency_Data1);

            Latency[WatermarkLevel.Level_0] = (uLatency_Data0 & 0x000000FF);
            Latency[WatermarkLevel.Level_1] = ((uLatency_Data0 & 0x0000FF00) >> 8);
            Latency[WatermarkLevel.Level_2] = ((uLatency_Data0 & 0x00FF0000) >> 16);
            Latency[WatermarkLevel.Level_3] = ((uLatency_Data0 & 0xFF000000) >> 24);
            Latency[WatermarkLevel.Level_4] = (uLatency_Data1 & 0x000000FF);
            Latency[WatermarkLevel.Level_5] = ((uLatency_Data1 & 0x0000FF00) >> 8);
            Latency[WatermarkLevel.Level_6] = ((uLatency_Data1 & 0x00FF0000) >> 16);
            Latency[WatermarkLevel.Level_7] = ((uLatency_Data1 & 0xFF000000) >> 24);

            //Check for BXT whether it is valid or not

            if (Latency[0] == 0)
            {
                Latency[WatermarkLevel.Level_0] = (Latency[WatermarkLevel.Level_0] + 2);
                Latency[WatermarkLevel.Level_1] = (Latency[WatermarkLevel.Level_1] + 2);
                Latency[WatermarkLevel.Level_2] = (Latency[WatermarkLevel.Level_2] + 2);
                Latency[WatermarkLevel.Level_3] = (Latency[WatermarkLevel.Level_3] + 2);
                Latency[WatermarkLevel.Level_4] = (Latency[WatermarkLevel.Level_4] + 2);
                Latency[WatermarkLevel.Level_5] = (Latency[WatermarkLevel.Level_5] + 2);
                Latency[WatermarkLevel.Level_6] = (Latency[WatermarkLevel.Level_6] + 2);
                Latency[WatermarkLevel.Level_7] = (Latency[WatermarkLevel.Level_7] + 2);
            }

            return Latency;
        }

        public bool SKLWaterMarkCalculate(Platform platform, DisplayType display, DisplayParameters displayParams)
        {
            bool bFinalResult = true;
            List<uint> uMem_Latency = new List<uint>();
            UInt64 uAdjustedPipePixelRate = 1;
            uint uMethod1Value = 0, uMethod2Value = 0, uPlaneBytesPerLine = 1;    // Changing the code making uPlaneBytesPerline = 1 for removing the exception
            uint uYTileMinimum = 0, uPlaneBufferAlocation = 0;
            uint uResultBytes = 0, uResultBlocks = 0, uResultLines = 0;
            uint PlaneBlockperline = 0;
            bool Transtion_WM_Status = false;
            uint Trans_Result_Block = 0, Trans_Result_Line = 0, Trans_Y_Tile = 0, Trans_Offset_Block = 0;

            PipePlaneParams pipePlaneParams = displayParams.DisplayDataList[display].pipePlaneParams;
            uint HTotal = displayParams.DisplayDataList[display].watermarkParams.HTotal;

            //Retrieve memory latency values //Need to change with dictionary.
            uMem_Latency = displayParams.SklMemoryLatencyValues.Values.ToList();

            int pipeIndex = (int)displayParams.displayConfig.GetDispHierarchy(display);

            uAdjustedPipePixelRate = (ulong)(displayParams.DisplayDataList[display].watermarkParams.DotClockinMhz);
            Log.Verbose("Adjusted pipe pixel rate " + uAdjustedPipePixelRate + " for display: " + display.ToString());

            uint wm_linetime = ((10 * (8 * 1000 * HTotal)) + (5 * ((uint)uAdjustedPipePixelRate))) / (10 * ((uint)uAdjustedPipePixelRate));
            if (!Check_WM_LINETIME(pipePlaneParams, wm_linetime))
            {
                bFinalResult = false;
            }

            //for calculating enabled planes per pipe
            for (int eachPlane = 0; eachPlane < displayParams.DisplayDataList[display].SklPlaneParams.Count; eachPlane++)
            {
                uint BPP = 0;
                uint uWMPlanePipeLatencyLevel = 0;
                uint uWM_Plane_Transition_Value = 0;
                UInt64 uAdjustedPlanePixelRate = 0;

                SKLPlaneParameters planeParameters = displayParams.DisplayDataList[display].SklPlaneParams[eachPlane];
                GENERIC_PLANE currentPlane = displayParams.DisplayDataList[display].SklPlaneParams[eachPlane].plane;

                Log.Verbose("Plane: {0}, Tiling: {1}, Angle: {2} PixelFormat: {3}, ColorDepthInBytes: {4}",
                    planeParameters.plane, planeParameters.tileFormat, planeParameters.angle, planeParameters.planePixelFormat, planeParameters.ColorDepthInBytes);

                Log.Verbose("Plane: {0}, PlanePixelRate: {1}, HorizontalSurfaceSize: {2} planeBufferAllocation: {3}.",
                    planeParameters.plane, planeParameters.AdjustedPlanePixelRate, planeParameters.horizontalSurfaceSize, planeParameters.planeBufferAllocation);

                uAdjustedPlanePixelRate = (ulong)planeParameters.AdjustedPlanePixelRate;
                BPP = planeParameters.ColorDepthInBytes;

                //Reading the driver Watermark offset Value
                uint planeWatermarkBaseOffset = GetOffsetFromEvent(currentPlane + "_WM_BASE", pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
                uint planeWatermarkTransitionOffset = GetOffsetFromEvent(currentPlane + "_WM_TRANS", pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);

                //for calculations involving each memory latency values per plane
                for (int k = 0; k < 8; k++)
                {
                    //Log.Verbose("\n BPP : " + BPP + "\n Plane register : " + Temp100 + "\n PSize" + uPlane_SZ[j] + "\n Value of A :"+ A1 );

                    Log.Verbose("\n Memory Latency[{0}]: {1}", k, uMem_Latency[k]);
                    uMethod1Value = (uMem_Latency[k] * ((uint)uAdjustedPlanePixelRate) * (BPP)) / 5120;  //Considering the Pixel clock in Khz

                    Log.Verbose("\n Method1: " + uMethod1Value);
                    uPlaneBytesPerLine = (planeParameters.horizontalSurfaceSize) * (BPP);

                    //Calculate Blocks per line 
                    if (planeParameters.tileFormat == TileFormat.Linear_Memory || planeParameters.tileFormat == TileFormat.Tile_X_Memory)  //Check for Linear or X-tiling
                        PlaneBlockperline = ((uint)Math.Ceiling(uPlaneBytesPerLine / 512.0)) * 100;
                    else
                        PlaneBlockperline = ((uint)Math.Ceiling(((4 * uPlaneBytesPerLine) / 512.0)) * 100) / 4;


                    uint Temp1 = (uint)Math.Ceiling((uMem_Latency[k] * (uAdjustedPlanePixelRate) * 1.0) / (HTotal * 1.0 * 1000));
                    Log.Verbose("\n Temp1: " + Temp1 + "\t" + (uMem_Latency[k] * (uAdjustedPlanePixelRate / 1000) * 1.00) + "\t" + (HTotal * 1.00));
                    uMethod2Value = (uint)(Temp1 * PlaneBlockperline);
                    Log.Verbose("\n Method2Value:" + uMethod2Value);
                    uPlaneBufferAlocation = planeParameters.planeBufferAllocation;
                    Log.Verbose("\n uPlaneBufferAlocation:" + uPlaneBufferAlocation);
                    
                    if (planeParameters.tileFormat == TileFormat.Linear_Memory || planeParameters.tileFormat == TileFormat.Tile_X_Memory)  //Check for Linear or X-tiling
                    {
                        //Code add to remove DividebyZero exception
                        if (uPlaneBytesPerLine == 0)
                            uPlaneBytesPerLine = 1;
                        if ((uPlaneBufferAlocation * 512 / uPlaneBytesPerLine) >= 1)
                        {
                            uResultBytes = Math.Min(uMethod1Value, uMethod2Value);
                        }
                        else
                        {
                            uResultBytes = uMethod1Value;
                        }
                    }
                    else//y-tiling on the current plane enabled
                    {
                        if (planeParameters.angle == RotationAngle.ROTATION_90 || planeParameters.angle == RotationAngle.ROTATION_270)//90 or 270 rotated plane
                        {
                            if (planeParameters.planePixelFormat == PlanePixelFormat.NV12_4_2_0)//NV12
                            {
                                uYTileMinimum = 16 * PlaneBlockperline;
                            }
                            else if (planeParameters.planePixelFormat == PlanePixelFormat.YUV_4_2_2)//YUV 422
                            {
                                uYTileMinimum = 8 * PlaneBlockperline;
                            }
                            else
                            {
                                uYTileMinimum = 4 * PlaneBlockperline;
                            }
                        }
                        else
                        {
                            //Log.Verbose("\nPipe " + (i + 1) + " , plane " + (j + 1) + " is not rotated");
                            uYTileMinimum = 4 * PlaneBlockperline;
                        }
                        Log.Verbose("\n YTileMinimum:" + uYTileMinimum);
                        uResultBytes = Math.Max(uMethod2Value, uYTileMinimum);
                    }

                    uResultBlocks = (uint)Math.Ceiling((double)uResultBytes / 100) + 1;
                    uResultLines = (uint)Math.Ceiling((double)uResultBytes / PlaneBlockperline);

                    if (k > 0 & k < 8)
                    {
                        if (platform == Platform.SKL)
                        {
                            if (planeParameters.tileFormat == TileFormat.Linear_Memory || planeParameters.tileFormat == TileFormat.Tile_X_Memory)  //Check for Linear or X-tiling
                                uResultBlocks = uResultBlocks + 1;
                            else
                                uResultLines = uResultLines + 4;
                        }
                    }


                    //Calculation for Transition Watermark
                    if (k == 0)
                    {
                        Trans_Offset_Block = SKL_TRANSITION_MINIMUM + SKL_TRANSITION_AMOUNT;
                        Trans_Y_Tile = 2 * uYTileMinimum * uMem_Latency[0];
                        if (planeParameters.tileFormat == TileFormat.Linear_Memory || planeParameters.tileFormat == TileFormat.Tile_X_Memory)  //Check for Linear or X-tiling
                        {
                            Trans_Result_Block = uResultBlocks + Trans_Offset_Block;
                        }
                        else
                        {
                            Trans_Result_Block = Math.Max(uResultBlocks, Trans_Y_Tile) + Trans_Offset_Block;
                        }

                        Trans_Result_Block = (uint)Math.Ceiling(Trans_Result_Block / 1.0) + 1;

                    }

                    //Reading the PlaneWatermarkBase Register.
                    ReadRegister(planeWatermarkBaseOffset + (uint)(4 * k), ref uWMPlanePipeLatencyLevel);
                    if (k == 0)
                        ReadRegister(planeWatermarkTransitionOffset, ref uWM_Plane_Transition_Value);

                    //Compare against maximum and check programmed values
                    if ((uResultBlocks >= uPlaneBufferAlocation) || (uResultLines > 31))
                    {
                        if (k == 0)//check if level 0 is exceeding max and still plane enabled.
                        {
                            Log.Fail("\nERROR: Plane:" + currentPlane + " was not supposed to be enabled since max value exceeded for level 0. Terminating test!");
                            bFinalResult = false;
                        }
                        if ((uWMPlanePipeLatencyLevel & 0x80000000) != 0)
                        {
                            Log.Fail("\nERROR: Latency level:" + (k) + " enabled for pipe:" + (pipeIndex + 1) + " and plane:" + (eachPlane + 1) + " even though max value exceeded");
                            bFinalResult = false;
                        }
                    }
                    else
                    {
                        if ((uWMPlanePipeLatencyLevel & 0x80000000) == 0x80000000)
                        {
                            Log.Message("\nInfo: Latency level:" + (k) + " is enabled for pipe:" + (pipeIndex + 1) + " and plane:" + (eachPlane + 1));
                            if ((uWMPlanePipeLatencyLevel & 0x40000000) == 0)
                            {
                                if (uResultLines != ((uWMPlanePipeLatencyLevel & 0x0007C000) >> 14))
                                {
                                    Log.Fail("\nERROR: Lines programmed: " + ((uWMPlanePipeLatencyLevel & 0x0007C000) >> 14) + " while expected: " + (uResultLines));
                                    bFinalResult = false;
                                }
                                else
                                {
                                    Log.Success("\nSUCCESS: Lines programmed: " + ((uWMPlanePipeLatencyLevel & 0x0007C000) >> 14) + " while expected: " + (uResultLines));
                                }
                            }
                            else
                            {
                                Log.Message("\nInfo: Line watermark value is ignored and Block watermark value is used for pipe:" + (pipeIndex + 1) + " , plane:" + (eachPlane + 1) + " and Latency level:" + (k));
                            }
                            if (uResultBlocks != (uWMPlanePipeLatencyLevel & 0x000003FF))
                            {
                                Log.Fail("\nERROR: Blocks programmed: " + (uWMPlanePipeLatencyLevel & 0x000003FF) + " while expected: " + (uResultBlocks));
                                bFinalResult = false;
                            }
                            else if ((Trans_Result_Block != (uWM_Plane_Transition_Value & 0x000003FF)) && Transtion_WM_Status == true && k == 0)
                            {
                                Log.Fail("\nERROR: Transition Blocks programmed: " + (uWM_Plane_Transition_Value & 0x000003FF) + " while expected: " + (uResultBlocks));
                                bFinalResult = false;
                            }
                            else
                            {
                                Log.Success("\nSUCCESS: Blocks programmed: " + (uWMPlanePipeLatencyLevel & 0x000003FF) + " while expected: " + (uResultBlocks));
                            }
                        }
                        else
                        {
                            Log.Fail("Watermark not enabled for level {0}.", k);
                        }
                    }
                }
            }

            return bFinalResult;
        }

        private bool Check_WM_LINETIME(PipePlaneParams pipePlaneParams, uint WM_LineTime)
        {
            uint uDriverWMLineTime = 0;
            uDriverWMLineTime = ReadRegister(WM_LINETIME, pipePlaneParams.Pipe, pipePlaneParams.Plane, PORT.NONE);
            if (WM_LineTime == uDriverWMLineTime)
            {
                Log.Success("\nSUCCESS: WM_LINETIME matches for pipe " + pipePlaneParams.DisplayType +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return true;
            }
            else if ((WM_LineTime - 1) == uDriverWMLineTime)
            {
                Log.Success("\nSUCCESS: WM_LINETIME matches for pipe " + pipePlaneParams.DisplayType +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return true;
            }
            else if ((WM_LineTime + 1) == uDriverWMLineTime)
            {
                Log.Success("\nSUCCESS: WM_LINETIME matches for pipe " + pipePlaneParams.DisplayType +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return true;
            }
            else
            {
                Log.Fail("\nERROR: WM_LINETIME does not match for pipe " + pipePlaneParams.DisplayType +
                    ". Driver programmed: " + uDriverWMLineTime + " for expected value: " + WM_LineTime);
                return false;

            }
        }

        private void ReadRegister(uint offset, ref uint regValue)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = offset;

            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIORead, driverData);
            DriverEscape escape = new DriverEscape();

            if (!escape.SetMethod(driverParams))
                Log.Fail("Failed to read Register with offset as {0}", driverData.input);
            else
            {
                Log.Message("Offset: {0} Value from registers = {1}", offset, driverData.output.ToString("X"));
                regValue = driverData.output;
            }
        }

        private void WriteRegister(uint offset, uint regValue)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = offset;
            driverData.output = regValue;

            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIOWrite, driverData);
            DriverEscape escape = new DriverEscape();

            if (!escape.SetMethod(driverParams))
                Log.Fail("Failed to write Register with offset {0} and value: {1}", driverData.input.ToString("X"), driverData.output.ToString("X"));
            else
                Log.Message("Written Offset: {0} with Value: {1}", offset.ToString("X"), driverData.output.ToString("X"));
        }

        private uint GetRegisterValue(uint RegisterValue, int start, int end)
        {
            uint value = RegisterValue << (31 - end);
            value >>= (31 - end + start);
            return value;
        }

        private uint GetPlaneLatencyValue(LatencyValues latencyValues, WatermarkLevel level)
        {
            uint latencyValue = 0;

            switch (level)
            {
                case WatermarkLevel.Level_0:
                    latencyValue = latencyValues.LatencyDisplay;
                    break;
                case WatermarkLevel.Level_1:
                    latencyValue = latencyValues.LatencyLP1;
                    break;
                case WatermarkLevel.Level_2:
                    latencyValue = latencyValues.LatencyLP2;
                    break;
                case WatermarkLevel.Level_3:
                    latencyValue = latencyValues.LatencyLP3;
                    break;
                case WatermarkLevel.Level_4:
                    latencyValue = latencyValues.LatencyLP4;
                    break;
            }

            return latencyValue;
        }


        private PlanesStatus GetPlanesEnableStatus(PipePlaneParams pipePlaneParam)
        {
            PlanesStatus planesStatus = new PlanesStatus();

            planesStatus.SpritePlane = VerifyRegisters(OVERLAY_ENABLE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
            planesStatus.CursorPlane = !VerifyRegisters(CURSOR_STATUS, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
            planesStatus.DisplayPlane = VerifyRegisters(DISPLAY_PLANE_STATUS, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);

            return planesStatus;
        }

        private bool IsSpritePlaneEnabled(Dictionary<DisplayType, DisplayData> DisplayDataList)
        {
            bool status = false;
            foreach (DisplayData dispData in DisplayDataList.Values)
            {
                status |= dispData.planesStatus.SpritePlane;
            }
            return status;
        }

        private bool IsCursorPlaneEnabled(Dictionary<DisplayType, DisplayData> DisplayDataList)
        {
            bool status = false;
            foreach (DisplayData dispData in DisplayDataList.Values)
            {
                status |= dispData.planesStatus.CursorPlane;
            }
            return status;
        }

        private uint GetOffsetFromEvent(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            Log.Verbose("Reading Register for event : {0}", pRegisterEvent);
            uint offset = 0;
            EventRegisterInfo eventRegister = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            eventRegister.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegister.GetMethod(eventInfo);

            if (returnEventInfo.listRegisters.Count == 0)
                Log.Abort("Unable to fetch registers for event " + pRegisterEvent);
            else
            {
                RegisterInf reginfo = returnEventInfo.listRegisters[0];
                offset = Convert.ToUInt32(reginfo.Offset, 16);
            }

            return offset;
        }

        private uint ReadRegister(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            Log.Verbose("Reading Register for event : {0}", pRegisterEvent);

            EventRegisterInfo eventRegister = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            eventRegister.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegister.GetMethod(eventInfo);

            if (returnEventInfo.listRegisters.Count == 0)
                Log.Fail("Unable to fetch registers for event " + pRegisterEvent);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                uint bitmap = Convert.ToUInt32(reginfo.Bitmap, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIORead, driverData);
                DriverEscape escape = new DriverEscape();

                if (!escape.SetMethod(driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    Log.Message("Offset: {0} Bitmap: {1}  Value from registers = {2}", reginfo.Offset, reginfo.Bitmap, driverData.output.ToString("X"));

                return GetRegisterValue(driverData.output, bitmap);
            }

            return 0;
        }
        /// <summary>
        /// Gets the Register Value 
        /// </summary>
        /// <param name="regValue">Value of Register to be AND with the Bitmap</param>
        /// <param name="regBitmap">Bitmap Value of Register to be AND with the Register Value</param>
        /// <returns></returns>
        private uint GetRegisterValue(uint regValue, uint regBitmap)
        {
            int count = 0;
            string bitvalue = regBitmap.ToString("X");
            while (bitvalue.EndsWith("0") != false)
            {
                bitvalue = bitvalue.Substring(0, bitvalue.Length - 1);
                count++;
            }

            regValue &= regBitmap;
            string currentValue = regValue.ToString("X");
            if (currentValue != "0")
                currentValue = currentValue.Substring(0, currentValue.Length - count);

            return Convert.ToUInt32(currentValue, 16);
        }

        private bool VerifyRegisters(string pRegisterEvent, PIPE pPipe, PLANE pPlane, PORT pPort)
        {
            Log.Verbose("Verifying Register for event : {0}", pRegisterEvent);
            bool regValueMatched = true;
            EventRegisterInfo eventRegister = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pPipe;
            eventInfo.plane = pPlane;
            eventInfo.port = pPort;
            eventInfo.eventName = pRegisterEvent;
            eventRegister.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegister.GetMethod(eventInfo);

            if (returnEventInfo.listRegisters.Count == 0)
                Log.Fail("Unable to fetch registers for event " + pRegisterEvent);

            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                //Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIORead, driverData);
                DriverEscape escape = new DriverEscape();

                if (!escape.SetMethod(driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else if (!CompareRegisters(driverData.output, reginfo))
                {
                    Log.Message("Register with offset {0} doesnot match required values", reginfo.Offset);
                    regValueMatched = false;
                }
            }

            return regValueMatched;
        }

        private bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            Log.Message("Offset = {0} Bitmap = {1}, expected value = {2} Value from registers = {3}", argRegInfo.Offset, argRegInfo.Bitmap, argRegInfo.Value, argDriverData.ToString("X"));
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            //Log.Verbose("value from reg read in ubit = {0}", hex);
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

        #region DontDelete

        //List<Register> DotClockRegisterList = new List<Register>();
        // eventName = "DOTCLOCK_VALUES";
        //Log.Verbose("Fetching registers for " + eventName);
        //DotClockRegisterList = RegisterManager.Instance.GetRegisters(RegisterManager.Instance.TestName, eventName, pipe.ToString());
        //foreach (Register register in DotClockRegisterList)
        //{
        //if (register.Name.ToUpper().Contains("HTOTAL"))
        //{
        //if (RegisterModule.Instance.ReadRegister(Convert.ToUInt32(register.Offset, 16), ref value))
        //{

        //dotClockValues.HTotal = ReadRegister(HTOTAL, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE);//GetRegisterValue(value, Convert.ToUInt32(register.Bitmap, 16));
        //    dotClockValues.HTotal = dotClockValues.HTotal + 1;
        //}
        //}
        //else if (register.Name.ToUpper().Contains("VTOTAL"))
        //{
        //    //if (RegisterModule.Instance.ReadRegister(Convert.ToUInt32(register.Offset, 16), ref value))
        //{
        //dotClockValues.VTotal = ReadRegister(SOURCE_PIPE_IMAGE, pipePlaneParam.Pipe, PLANE.NONE, PORT.NONE); //GetRegisterValue(value, Convert.ToUInt32(register.Bitmap, 16));
        //    dotClockValues.VTotal = dotClockValues.VTotal + 1;
        //}
        //}
        //else
        //{
        //    Log.Fail("No Valid Registers Found for the event : DOTCLOCK_VALUES");
        //    Log.Verbose(string.Format("Failed in GetDotClock .. Unable to retrieve DotClock Values of the display {0}", display));
        //}
        //}

        //DisplayConfig displayConfig = new DisplayConfig();
        //    Config config = new Config();
        //    config.EnumeratedDisplays = base.EnumeratedDisplays;
        //    displayConfig = (DisplayConfig)config.Get;

        //    displayParams.displayConfig = displayConfig;

        //    displayConfig.CustomDisplayList.ForEach(display =>
        //        {
        //            Modes mode = new Modes();
        //            DisplayMode resolution = new DisplayMode();
        //            PlanesStatus tempPlanesStatus = new PlanesStatus();

        //            PipePlaneParams pipePlaneParam = GetPipePlaneParams(display);
        //            displayParams.pipePlaneParams.Add(pipePlaneParam);

        //            DisplayInfo displayInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
        //            mode.EnumeratedDisplays = base.EnumeratedDisplays;
        //            resolution = (DisplayMode)mode.GetMethod(displayInfo);

        //This method is not required. Can be used it for sprite/display/cursor enabling status.
        ///// <summary>
        ///// Calculates the Latency Values of all Planes of the given Display
        ///// </summary>
        ///// <param name="display">Display to which Latencies to be calculated</param>

        //public LatencyValues GetLatencyValues(DisplayType display)
        //{
        //    LatencyValues latencyValues = ComputeLatencyValue();
        //    bool cursorEnable = false, spriteEnable = false, displayEnable = false;

        //    PipePlane p = new PipePlane();
        //    PipePlaneParams pipePlaneParam = new PipePlaneParams(display);

        //    p.GetMethod(pipePlaneParam);

        //    spriteEnable = VerifyRegisters(OVERLAY_ENABLE, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
        //    cursorEnable = !VerifyRegisters(CURSOR_STATUS, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);
        //    displayEnable = VerifyRegisters(DISPLAY_PLANE_STATUS, PIPE.NONE, pipePlaneParam.Plane, PORT.NONE);

        //    return latencyValues;
        //}

        //private PipePlaneParams GetPipePlaneParams(DisplayType display)
        //{
        //    PipePlane p = new PipePlane();
        //    PipePlaneParams pipePlaneParam = new PipePlaneParams(display);
        //    p.MachineInfo = base.MachineInfo;
        //    p.EnumeratedDisplays = base.EnumeratedDisplays;

        //    p.GetMethod(pipePlaneParam);

        //    return pipePlaneParam;
        //}
        #endregion
    }
}
