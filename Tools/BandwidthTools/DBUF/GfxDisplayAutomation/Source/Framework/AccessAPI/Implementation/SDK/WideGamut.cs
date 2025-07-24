namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Collections.Generic;
    using IgfxExtBridge_DotNet;
    using System.Text;
    using System.IO;
    public class WideGamut : FunctionalBase, ISet, IGetMethod, IParse
    {
        public Dictionary<WideGamutOption, System.Action> PerformChanges
        {
            get
            {
                Dictionary<WideGamutOption, System.Action> changes = new Dictionary<WideGamutOption, System.Action>() {
            {WideGamutOption.SetWideGamut,SetWideGamut},
            {WideGamutOption.ChangeINF,EnableINFChanges},
            {WideGamutOption.VerifyINF,VerifyInfValue}
            };
                return changes;
            }
        }
        private WideGamutParams wideGamutParams;
        public WideGamutParams WideGamutParams
        {
            get { return wideGamutParams; }
            set { wideGamutParams = value; }
        }
        public object Set
        {
            set
            {
                WideGamutParams = value as WideGamutParams;
                PerformChanges[wideGamutParams.option]();
            }
        }

        private void SetWideGamut()
        {
            if (base.MachineInfo.PlatformDetails.IsLowpower) //platform.HCV
            {
                SetWideGamutForLowPower(wideGamutParams);

            }
            else
            {
                SetWideGamutForGen(wideGamutParams);
            }
        }
        private void SetWideGamutForGen(WideGamutParams wideGamutParams)
        {
            Log.Message(true, "Applying widegamut {0} to {1}", wideGamutParams.WideGamutLevel, wideGamutParams.DisplayType);
            IGFX_GAMUT_EXPANSION gamut = new IGFX_GAMUT_EXPANSION();
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";
            float[] CSCMatrixRow1 = new float[3];
            float[] CSCMatrixRow2 = new float[3];
            float[] CSCMatrixRow3 = new float[3];

            gamut.dwDeviceID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            gamut.versionHeader.dwVersion = 1;

            APIExtensions.DisplayUtil.GetGamutData(ref gamut, out igfxErrorCode, out errorDesc);

            if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
            {
                Log.Fail(String.Format("WideGamut feature not supported for display {0}", wideGamutParams.DisplayType));
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
                }
            }

        }

        public void SetWideGamutForLowPower(WideGamutParams argWideGamutParams)
        {
            Log.Message(true, "Applying Wide Gamut to {0}", argWideGamutParams.DisplayType);
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";

            IGFX_SOURCE_DISPLAY_CSC_DATA data = new IGFX_SOURCE_DISPLAY_CSC_DATA();
            data.ulReserved = base.EnumeratedDisplays.Where(dI => dI.DisplayType == argWideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            data.dwFlag = 1;

            APIExtensions.DisplayUtil.GetCSCData(ref data, out igfxErrorCode, out errorDesc);
            Log.Message("The output of getCSC data is {0}", igfxErrorCode);


            data.bEnable = 1;
            data.ulReserved = base.EnumeratedDisplays.Where(dI => dI.DisplayType == argWideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();

            Log.Message("The cui id is {0}", data.ulReserved);

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
                Log.Success("Wide gamut is enabled {0}, enable status is {1}", igfxErrorCode, data.bEnable);
            }
            else
                Log.Fail("Failed to enable wide gamut , {0}", igfxErrorCode);
        }
        public object GetMethod(object argMessage)
        {
            WideGamutParams wideGamutParams = argMessage as WideGamutParams;
            if (base.MachineInfo.PlatformDetails.IsLowpower) //platform.HCV
            {
                GetWideGamutForLowPower(wideGamutParams);

            }
            else
            {
                IGFX_GAMUT_EXPANSION gamut = new IGFX_GAMUT_EXPANSION();
                IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
                string errorDesc = "";

                gamut.dwDeviceID = base.EnumeratedDisplays.Where(dI => dI.DisplayType == wideGamutParams.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
                gamut.versionHeader.dwVersion = 1;

                APIExtensions.DisplayUtil.GetGamutData(ref gamut, out igfxErrorCode, out errorDesc);

                if (igfxErrorCode == IGFX_ERROR_CODES.IGFX_UNSUPPORTED_FEATURE)
                {
                    Log.Verbose(String.Format("WideGamut feature not supported for display {0}", wideGamutParams.DisplayType));
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
            return wideGamutParams;
        }
        protected void GetWideGamutForLowPower(WideGamutParams argWideGamutParam)
        {
            Log.Message("\n Get Wide Gamut Data");
            IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
            string errorDesc = "";

            IGFX_SOURCE_DISPLAY_CSC_DATA data = new IGFX_SOURCE_DISPLAY_CSC_DATA();
            data.ulReserved = base.EnumeratedDisplays.Where(dI => dI.DisplayType == argWideGamutParam.DisplayType).Select(dI => dI.CUIMonitorID).FirstOrDefault();
            data.dwFlag = 1;

            APIExtensions.DisplayUtil.GetCSCData(ref data, out igfxErrorCode, out errorDesc);
            Log.Message("The output of getCSC data is {0}", igfxErrorCode);
            Log.Message("bEnable {0}", data.bEnable);
            Log.Message("dwlsSupported {0}", data.dwIsSupported);
            Log.Message("ulReserved {0}", data.ulReserved);

            Log.Message("601 {0}", data.CSCMatrix.fLFPCSCMatrix_601.Count());
            data.CSCMatrix.fLFPCSCMatrix_601.ToList().ForEach(curValue =>
            {
                Log.Message("\t {0}", curValue);
            });

            Log.Message("\n 709 {0}", data.CSCMatrix.fLFPCSCMatrix_709.Count());
            data.CSCMatrix.fLFPCSCMatrix_709.ToList().ForEach(curValue =>
            {
                Log.Message("\t {0}", curValue);
            });
        }
        public void Parse(string[] args)
        {
            WideGamutParams wideGamutParams = new WideGamutParams();
            DisplayType tempDisplay;
            WideGamutLevel tempLevel = WideGamutLevel.Unsupported;

            if (args.Length == 3 && args[0].ToLower().Contains("set"))
            {
                if (Enum.TryParse<DisplayType>(args[1], true, out tempDisplay) && Enum.TryParse<WideGamutLevel>(args[2], true, out tempLevel))
                {
                    wideGamutParams.DisplayType = tempDisplay;
                    wideGamutParams.WideGamutLevel = tempLevel;
                    Log.Verbose("Setting WideGamut level:{0} for display {1}", wideGamutParams.WideGamutLevel, wideGamutParams.DisplayType);
                    Set = wideGamutParams;
                }
                else
                {
                    this.HelpText();
                }
            }
            else if (args.Length == 2 && args[0].ToLower().Contains("get"))
            {
                if (Enum.TryParse<DisplayType>(args[1], true, out tempDisplay))
                {
                    wideGamutParams.DisplayType = tempDisplay;
                    GetMethod(wideGamutParams);
                    Log.Message("WideGamut level for display {0} is {1}", wideGamutParams.DisplayType, wideGamutParams.WideGamutLevel);
                }
                else
                {
                    this.HelpText();
                }
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe WideGamut set DisplayType <NATURAL/LEVEL2/LEVEL3/LEVEL4/VIVID>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe WideGamut set HDMI LEVEL2");
            sb.Append("For example : Execute.exe WideGamut get DP");
            sb.Append("For example : Execute.exe WideGamut set EDP VIVID");
            Log.Message(sb.ToString());
        }
        private bool INFFileChanges(string infPath, string argStartsWith, string toBeReplaced)
        {
            Log.Message(true,"Making Changes to .INF File to enable WideGamut");
            //HKR,, WideGamutFeatureEnable,%REG_DWORD%, 0x01 	; 0x01- Enable for LFP, 0x02 - Enable for DP, 0x04 - Enable for HDMI... 
            string fileName = "\\igdlh64.inf";
            StringBuilder newfile = new StringBuilder();
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            Log.Verbose("{0}", string.Concat(infPath, fileName));
            string[] file = File.ReadAllLines(string.Concat(infPath, fileName));

            string temp = "";
            foreach (string line in file)
            {
                if (line.Contains(argStartsWith))
                {
                    string oldString = line.Split(';').First();
                    //if (oldString.Equals(toBeReplaced))
                    //{
                    //    Log.Message("driver nneed not be reinstalled");
                    //    return false;
                    //}
                    //else
                    //{
                    temp = line.Replace(oldString, toBeReplaced);
                    newfile.Append(temp + "\r\n");
                    //}
                    continue;
                }
                newfile.Append(line + "\r\n");
            }
            File.WriteAllText(string.Concat(infPath, fileName), newfile.ToString());
            return true;
        }
        private void EnableINFChanges()
        {
            string str = "HKR,, WideGamutFeatureEnable,%REG_DWORD%, ";
            INFFileChanges(WideGamutParams.INFPath, str, str + "0x0" + wideGamutParams.INFValue + " \t");
        }
        protected void VerifyInfValue()
        {
            Log.Message(true, "Verifying Changes made in .INF File to enable WideGamut");
            string argStartsWith = "HKR,, WideGamutFeatureEnable,%REG_DWORD%, ";
            string fileName = "\\igdlh64.inf";
            StringBuilder newfile = new StringBuilder();
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            Log.Verbose("{0}", string.Concat(WideGamutParams.INFPath, fileName));
            string[] file = File.ReadAllLines(string.Concat(WideGamutParams.INFPath, fileName));

            foreach (string line in file)
            {
                if (line.Contains(argStartsWith))
                {
                    string oldString = line.Split(';').First();
                    if (oldString.Trim().EndsWith(WideGamutParams.INFValue.ToString()))
                    {
                        Log.Success("Inf change {0} is success", WideGamutParams.INFValue);
                    }
                    else
                    {
                        Log.Abort("Failed to change Inf value to {0}, current Inf value {1}", WideGamutParams.INFValue, oldString);

                    }
                }
            }
        }
    }
}