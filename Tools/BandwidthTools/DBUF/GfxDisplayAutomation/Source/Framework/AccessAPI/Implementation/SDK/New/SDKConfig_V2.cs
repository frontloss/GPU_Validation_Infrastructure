namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using igfxSDKLib;
    using System.Threading;

    /*  Get set display config through CUI SDK 8.0 */
    class SdkConfig_v2 : FunctionalBase, ISDK
    {
        protected DisplayConfig argDispConfig;
        private DisplayConfiguration Config;

        public object Get(object args)
        {
            DisplayConfig dispConfig = new DisplayConfig();
            dispConfig.EnumeratedDisplays = base.EnumeratedDisplays;
            GfxSDKClass sdk = new GfxSDKClass();
            Config = sdk.Display.Configuration;
            Config.Get();

            if (Config.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                int noOfDisplays = Config.Displays.Length;
                Array DisplayList = Config.Displays;
                if (noOfDisplays == 1 && Config.IsCollage == false)
                {
                    dispConfig.ConfigType = DisplayConfigType.SD;

                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(0)).DisplayID)).DisplayType;
                    dispConfig.SecondaryDisplay = DisplayType.None;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }
                else if (noOfDisplays == 2 && Config.IsCollage == false)
                {
                    dispConfig.ConfigType =
                        (((DisplayConfigDetails)DisplayList.GetValue(0)).SourceID) ==
                        (((DisplayConfigDetails)DisplayList.GetValue(1)).SourceID)
                        ? DisplayConfigType.DDC : DisplayConfigType.ED;

                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(0)).DisplayID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(1)).DisplayID)).DisplayType;
                    dispConfig.TertiaryDisplay = DisplayType.None;
                }
                else if (noOfDisplays == 3 && Config.IsCollage == false)
                {
                    dispConfig.ConfigType =
                        ((((DisplayConfigDetails)DisplayList.GetValue(0)).SourceID) ==
                        (((DisplayConfigDetails)DisplayList.GetValue(1)).SourceID)) &&
                        ((((DisplayConfigDetails)DisplayList.GetValue(1)).SourceID) ==
                        (((DisplayConfigDetails)DisplayList.GetValue(2)).SourceID))
                        ? DisplayConfigType.TDC : DisplayConfigType.TED;

                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(0)).DisplayID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(1)).DisplayID)).DisplayType;
                    dispConfig.TertiaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(2)).DisplayID)).DisplayType;
                }
                else if (Config.IsCollage)
                {
                    dispConfig.ConfigType =
                        Config.Collage.ArrangeDisplaysInCollageMatrix.GetUpperBound(0) <
                        Config.Collage.ArrangeDisplaysInCollageMatrix.GetUpperBound(1) ? DisplayConfigType.Horizontal : DisplayConfigType.Vertical;

                    dispConfig.PrimaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(0)).DisplayID)).DisplayType;
                    dispConfig.SecondaryDisplay = dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(1)).DisplayID)).DisplayType;
                    dispConfig.TertiaryDisplay = (noOfDisplays == 3) ?
                        dispConfig.EnumeratedDisplays.Find(
                        id => id.WindowsMonitorID.Equals(((DisplayConfigDetails)DisplayList.GetValue(2)).DisplayID)).DisplayType : DisplayType.None;
                }
            }

            else
            {
                Log.Fail("Failed to Get Configuration through SDK ErrorCode: {0} ", Config.Error);
            }
            return dispConfig;
        }

        public object Set(object args)
        {
            argDispConfig = args as DisplayConfig;
            if (argDispConfig.EnumeratedDisplays == null)
            {
                argDispConfig.EnumeratedDisplays = base.EnumeratedDisplays;
            }
            DisplayConfiguration displayConfig = new DisplayConfiguration();
            FillOpmode(displayConfig);
            return SwitchDisplayConfig(displayConfig);
        }

        private void FillOpmode(DisplayConfiguration displayConfig)
        {
            int dispCount = 0;
            int displayIndx = 0;
            uint sourceId = 0;

            dispCount = argDispConfig.CustomDisplayList.Count;
            var displayList = new DisplayConfigDetails[dispCount];
            for (displayIndx = 0; displayIndx < dispCount; displayIndx++)
                displayList[displayIndx] = new DisplayConfigDetails();

            displayConfig.Displays = displayList;
            displayConfig.PrimaryDisplayID = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.PrimaryDisplay)).WindowsMonitorID;

            if (DisplayExtensions.GetUnifiedConfig(argDispConfig.ConfigType) == DisplayUnifiedConfig.Collage)
            {
                displayConfig.IsCollage = true;
                if (argDispConfig.ConfigType == DisplayConfigType.Horizontal)
                {
                    var CollageDispList = new CollageBezelDetails[1, dispCount];
                    for (uint index = 0; index < dispCount; index++)
                    {
                        CollageDispList[0, index] = new CollageBezelDetails();
                        CollageDispList[0, index].IndexInDisplaysArray = index;
                    }
                    displayConfig.Collage.ArrangeDisplaysInCollageMatrix = CollageDispList;
                }
                else if (argDispConfig.ConfigType == DisplayConfigType.Vertical)
                {
                    var CollageDispList = new CollageBezelDetails[dispCount, 1];
                    for (uint index = 0; index < dispCount; index++)
                    {
                        CollageDispList[index, 0] = new CollageBezelDetails();
                        CollageDispList[index, 0].IndexInDisplaysArray = index;
                    }
                    displayConfig.Collage.ArrangeDisplaysInCollageMatrix = CollageDispList;
                }
                for (displayIndx = 0; displayIndx < dispCount; displayIndx++)
                {
                    DisplayInfo display = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.CustomDisplayList.ElementAt(displayIndx)));
                    ((DisplayConfigDetails)(displayConfig.Displays.GetValue(displayIndx))).DisplayID = display.WindowsMonitorID;
                    ((DisplayConfigDetails)(displayConfig.Displays.GetValue(displayIndx))).SourceID = 0;
                }
            }

            else if (DisplayExtensions.GetUnifiedConfig(argDispConfig.ConfigType) == DisplayUnifiedConfig.Clone)
            {
                DisplayMode resolution = new DisplayMode() { HzRes = 1024, VtRes = 768, RR = 60, Bpp = 32, InterlacedFlag = 0 };
                for (displayIndx = 0; displayIndx < dispCount; displayIndx++)
                {
                    DisplayInfo display = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.CustomDisplayList.ElementAt(displayIndx)));
                    ((DisplayConfigDetails)displayConfig.Displays.GetValue(displayIndx)).SourceID = sourceId;
                    ((DisplayConfigDetails)displayConfig.Displays.GetValue(displayIndx)).DisplayID = display.WindowsMonitorID;
                }
            }
            else
            {
                for (displayIndx = 0; displayIndx < dispCount; displayIndx++)
                {
                    DisplayInfo display = argDispConfig.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(argDispConfig.CustomDisplayList.ElementAt(displayIndx)));
                    ((DisplayConfigDetails)displayConfig.Displays.GetValue(displayIndx)).SourceID = sourceId++;
                    ((DisplayConfigDetails)displayConfig.Displays.GetValue(displayIndx)).DisplayID = display.WindowsMonitorID;
                }
            }
        }

        private bool SwitchDisplayConfig(DisplayConfiguration _DisplayConfig)
        {
            GfxSDKClass sdk = new GfxSDKClass();
            DisplayConfiguration displayConfig = sdk.Display.Configuration;
            bool status = false;

            DisplayInfo priDisplayInfo = base.EnumeratedDisplays.Where(cI => cI.DisplayType == argDispConfig.PrimaryDisplay).FirstOrDefault();

            if (argDispConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone
                && base.MachineInfo.PlatformDetails.IsLowpower
                && priDisplayInfo.IsPortraitPanel == true
                && (!base.AppManager.MachineInfo.OS.IsGreaterThan(OSType.WINTHRESHOLD))
                && priDisplayInfo.displayExtnInformation.Equals(DisplayExtensionInfo.Internal))
            {
                Log.Alert("{0} This Configuration Is Not Applicable", argDispConfig);
                return true;
            }

            displayConfig = _DisplayConfig;
            displayConfig.Set();
            Thread.Sleep(7000);
            if (displayConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                Log.Message("Config {0} applied Successfully through CUI SDK", argDispConfig.GetCurrentConfigStr());
                status = true;
            }
            else
            {
                Log.Message("Failed to apply Config {0} through SDK", argDispConfig.GetCurrentConfigStr());
                status = false;
            }
            return status;
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
