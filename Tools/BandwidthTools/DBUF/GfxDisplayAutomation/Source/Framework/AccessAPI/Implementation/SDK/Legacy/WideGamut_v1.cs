namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using IgfxExtBridge_DotNet;

    class WideGamut_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
        private string errorDesc = "";
        private WideGamutParams wideGamutParams;
        public object Set(object args)
        {
            wideGamutParams = args as WideGamutParams;
            Log.Message("Applying widegamut {0} to {1}", wideGamutParams.WideGamutLevel, wideGamutParams.DisplayType);
            if (base.MachineInfo.PlatformDetails.IsLowpower)
                return SetWideGamutForLP();
            else
                return SetWideGamutForGen();
        }

        public object Get(object args)
        {
            wideGamutParams = args as WideGamutParams;
            if (base.MachineInfo.PlatformDetails.IsLowpower)
                GetWideGamutForLP();
            else
                GetWideGamutForGen();
            return 0;
        }

        private void GetWideGamutForLP()
        {
            IGFX_SOURCE_DISPLAY_CSC_DATA data = new IGFX_SOURCE_DISPLAY_CSC_DATA();
            data.ulReserved = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            data.dwFlag = 1;

            APIExtensions.DisplayUtil.GetCSCData(ref data, out igfxErrorCode, out errorDesc);
            Log.Message("Wide Gammut is Supported = {0} is Enable = {1} and 601 count = {2}", data.dwIsSupported, data.bEnable, data.CSCMatrix.fLFPCSCMatrix_601.Count());
            data.CSCMatrix.fLFPCSCMatrix_601.ToList().ForEach(curValue =>
            {
                Log.Message("\t {0}", curValue);
            });

            Log.Message("Wide Gamut 709 count = {0}", data.CSCMatrix.fLFPCSCMatrix_709.Count());
            data.CSCMatrix.fLFPCSCMatrix_709.ToList().ForEach(curValue =>
            {
                Log.Message("\t {0}", curValue);
            });
        }

        private void GetWideGamutForGen()
        {
            IGFX_GAMUT_EXPANSION gamut = new IGFX_GAMUT_EXPANSION();

            gamut.dwDeviceID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            gamut.versionHeader.dwVersion = 1;
            APIExtensions.DisplayUtil.GetGamutData(ref gamut, out igfxErrorCode, out errorDesc);

            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
            {
                Log.Fail("WideGamut feature not supported for display {0}", wideGamutParams.DisplayType);
                wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
            }
            else if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Fail("Unable to fetch widegamut level - {0}:{1}", errorDesc, igfxErrorCode.ToString());
                wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
            }
            else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                wideGamutParams.WideGamutLevel = (WideGamutLevel)Enum.Parse(typeof(WideGamutLevel), gamut.dwGamutExpansionLevel.ToString());
            }
        }

        private bool SetWideGamutForGen()
        {
            bool status = false;
            IGFX_GAMUT_EXPANSION gamut = new IGFX_GAMUT_EXPANSION();
            float[] CSCMatrixRow1 = new float[3];
            float[] CSCMatrixRow2 = new float[3];
            float[] CSCMatrixRow3 = new float[3];

            gamut.dwDeviceID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            gamut.versionHeader.dwVersion = 1;

            APIExtensions.DisplayUtil.GetGamutData(ref gamut, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
            {
                Log.Fail("WideGamut feature not supported for display {0}", wideGamutParams.DisplayType);
                wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
            }
            else if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Fail("Unable to fetch widegamut level - {0}:{1}", errorDesc, igfxErrorCode.ToString());
                wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
            }
            else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                gamut.dwGamutExpansionLevel = (uint)wideGamutParams.WideGamutLevel;
                APIExtensions.DisplayUtil.SetGamutData(ref gamut, CSCMatrixRow1, CSCMatrixRow2, CSCMatrixRow3, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Fail("Unable to set widegamut level for {0}- {1}:{2}", wideGamutParams.DisplayType, errorDesc, igfxErrorCode.ToString());
                    wideGamutParams.WideGamutLevel = WideGamutLevel.Unsupported;
                }
                else if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Success("widegamut level set to {0} for {1}", wideGamutParams.WideGamutLevel, wideGamutParams.DisplayType);
                    status = true;
                }
            }
            return status;
        }

        private bool SetWideGamutForLP()
        {
            bool status = false;
            IGFX_SOURCE_DISPLAY_CSC_DATA data = new IGFX_SOURCE_DISPLAY_CSC_DATA();
            data.ulReserved = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            data.dwFlag = 1;
            APIExtensions.DisplayUtil.GetCSCData(ref data, out igfxErrorCode, out errorDesc);

            data.bEnable = 1;
            data.CSCMatrix.fLFPCSCMatrix_601[0] = (float)1.0;
            data.CSCMatrix.fLFPCSCMatrix_601[1] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_601[2] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_601[3] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_601[4] = (float)1.0;
            data.CSCMatrix.fLFPCSCMatrix_601[5] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_601[6] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_601[7] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_601[8] = (float)1.0;

            data.CSCMatrix.fLFPCSCMatrix_709[0] = (float)0.5;
            data.CSCMatrix.fLFPCSCMatrix_709[1] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_709[2] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_709[3] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_709[4] = (float)0.4;
            data.CSCMatrix.fLFPCSCMatrix_709[5] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_709[6] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_709[7] = (float)0.0;
            data.CSCMatrix.fLFPCSCMatrix_709[8] = (float)0.7;

            data.CSCMatrix.flag = 1;
            data.dwFlag = 1;

            APIExtensions.DisplayUtil.SetCSCData(ref data, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                status = true;
                Log.Success("Wide gamut successfully enabled");
            }
            else
                Log.Fail("Failed to enable wide gamut, Error Code: {0}", igfxErrorCode);
            return status;
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
