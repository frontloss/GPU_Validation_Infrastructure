namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading;
    using igfxSDKLib;

    /*  Set independent rotation through CUI SDK 8.0 */
    class SdkIndependentRotation_v2 : FunctionalBase, ISDK
    {
        private DisplayConfiguration SDKConfig;
        public object Set(object args)
        {
            int dispCount = 0;

            List<DisplayMode> modeList = (List<DisplayMode>)args;
            GfxSDKClass sdk = new GfxSDKClass();
            SDKConfig = sdk.Display.Configuration;
            SDKConfig.Get();

            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkConfig = sdkExtn.GetSDKHandle(SDKServices.Config);
            DisplayConfig currentConfig = (DisplayConfig)sdkConfig.Get(null);

            if (modeList.Count < 2)
            {
                Log.Verbose("Minimum two mode list required to set independent rotation");
                return false;
            }

            if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                dispCount = SDKConfig.Displays.Length;
                SDKConfig.PrimaryDisplayID = base.EnumeratedDisplays.Find(DT => DT.DisplayType.Equals(modeList.First().display)).WindowsMonitorID;

                int currentIndex = (int)DisplayExtensions.GetDispHierarchy(currentConfig, modeList.First().display);
                if (SDKConfig.IsCollage)
                {
                    if (SDKConfig.Collage.ArrangeDisplaysInCollageMatrix.GetUpperBound(0) <
                        SDKConfig.Collage.ArrangeDisplaysInCollageMatrix.GetUpperBound(1)) //Horizontal collage
                    {
                        var CollageDispList = new CollageBezelDetails[1, dispCount];
                        for (uint index = 0; index < dispCount; index++)
                        {
                            CollageDispList[0, index] = new CollageBezelDetails();
                            CollageDispList[0, index].IndexInDisplaysArray = index;
                        }
                        SDKConfig.Collage.ArrangeDisplaysInCollageMatrix = CollageDispList;
                    }
                    else //Vertical Collage
                    {
                        var CollageDispList = new CollageBezelDetails[dispCount, 1];
                        for (uint index = 0; index < dispCount; index++)
                        {
                            CollageDispList[index, 0] = new CollageBezelDetails();
                            CollageDispList[index, 0].IndexInDisplaysArray = index;
                        }
                        SDKConfig.Collage.ArrangeDisplaysInCollageMatrix = CollageDispList;
                    }
                }

                for (int indexIn = 0; indexIn < SDKConfig.Displays.Length; indexIn++)
                {
                    DisplayMode mode = modeList[indexIn];
                    uint ResX = mode.HzRes;
                    uint ResY = mode.VtRes;
                    if (DisplayExtensions.CanFlip(mode))
                        DisplayExtensions.SwapValue(ref ResX, ref ResY);

                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ResolutionSourceX = ResX;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ResolutionSourceY = ResY;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.ColorBPP = MODE_BPP.BPP_32_BIT;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.RefreshRate = mode.RR;
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Mode.IsInterlaced = (mode.InterlacedFlag == 0) ? false : true;

                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Scaling = SdkExtensions.GetSDKScaling_v2((ScalingOptions)mode.ScalingOptions.First());
                    ((DisplayConfigDetails)(SDKConfig.Displays.GetValue(indexIn))).Rotation = SdkExtensions.GetSDKOrientation_v2(mode.Angle);
                }

                SDKConfig.Set();
                if (SDKConfig.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
                {
                    Log.Message("Independent rotation applied Successfully through CUI SDK");
                    Thread.Sleep(5000);
                    return true;
                }
                else
                {
                    Log.Message("Failed to apply independent rotation through SDK");
                }
            }
            else
            {
                Log.Fail("Failed to GetConfiguration through SDK ErrorCode: {0} ", SDKConfig.Error);
            }
            return false;
        }

        public object Get(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}