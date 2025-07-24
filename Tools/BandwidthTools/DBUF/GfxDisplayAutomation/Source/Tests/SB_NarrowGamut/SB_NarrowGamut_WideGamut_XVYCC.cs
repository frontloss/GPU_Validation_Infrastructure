using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Microsoft.Win32;
namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_NarrowGamut_WideGamut_XVYCC : SB_NarrowGamut_Base
    {
        protected DisplayType _wGDisplay = DisplayType.DP;
        protected DisplayType _nGDisplay = DisplayType.EDP;
        protected DisplayType _xvycc_YcbcrDisplay = DisplayType.HDMI;
        protected WideGamutLevel _wGLevel = WideGamutLevel.LEVEL3;        
        protected ColorType _colorType = ColorType.XvYCC;
        protected Dictionary<DisplayType, string> _availableEDIDMap = null;
        public SB_NarrowGamut_WideGamut_XVYCC()
        {
            _availableEDIDMap = new Dictionary<DisplayType, string>();
            _availableEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL_U2711_XVYCC.EDID");
            _availableEDIDMap.Add(DisplayType.HDMI_2, "HDMI_DELL_U2711_XVYCC.EDID");

            _availableEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
            _availableEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
        }
        public Dictionary<WideGamutLevel, string> WideGamutEvents
        {
            get
            {
                Dictionary<WideGamutLevel, string> wideGamutLevel = new Dictionary<WideGamutLevel, string>() { 
                { WideGamutLevel.NATURAL, "WB_SLIDER_LEVEL1" }, 
            { WideGamutLevel.LEVEL2, "WB_SLIDER_LEVEL2" },
            { WideGamutLevel.LEVEL3, "WB_SLIDER_LEVEL3" },
            {WideGamutLevel.LEVEL4, "WB_SLIDER_LEVEL4"  },
           // {WideGamutLevel.VIVID, "WB_SLIDER_LEVEL1"}
            };
                return wideGamutLevel;
            }
        }
        public Dictionary<DisplayType, int> wideGamutInfValue
        {
            get
            {
                Dictionary<DisplayType, int> _wideGamutInfValue = new Dictionary<DisplayType, int>() {{DisplayType.EDP,1},
            {DisplayType.DP,2},{DisplayType.HDMI,4}};
                return _wideGamutInfValue;
            }
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != 3)
            {
                Log.Abort("Test supports only TDC/TED ,Current config {0}");
            }
            if (!base.CurrentConfig.DisplayList.Contains(_nGDisplay))
                Log.Abort("Display list does not contain Narrow Gamut Display {0}",_nGDisplay);
            if (!base.CurrentConfig.DisplayList.Contains(_wGDisplay))
                Log.Abort("Display list does not contain Wide Gamut Display {0}", _wGDisplay);
            if (!base.CurrentConfig.DisplayList.Contains(_xvycc_YcbcrDisplay))
                Log.Abort("Display list does not contain XVYCC/YCBCR Display {0}", _xvycc_YcbcrDisplay);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            PerformINFChanges(NarrowGamutOption.EnableINF);
            base.InstallDriver();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            PerformINFChanges(NarrowGamutOption.VerifyINF);             
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            WideGamutDriver(wideGamutInfValue[_wGDisplay]);            
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            base.InitializeHotplugFramework();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    base.HotPlug(curDisp, _availableEDIDMap[curDisp]);
                    _pluggableDisplaySim.Add(curDisp);
                }
            });
            base.ApplyConfig(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {            
            base.SetWideGamut(_wGDisplay, _wGLevel);
            base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            {
                base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.EnableNarrowGamut);
            });
            VerifyWideGamut(_wGDisplay, _wGLevel);
            VerifyColor(_xvycc_YcbcrDisplay);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            if (base.MachineInfo.PlatformDetails.Platform != Platform.CHV)
            { // csc is always enabled in chv , hence disbale state is not being checked.
                base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
                {
                    base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.DisbaleNarrowGamut);
                });
            }
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            _pluggableDisplaySim.ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
            base.CleanUpHotplugFramework();
            PerformINFChanges(NarrowGamutOption.ResetINF);
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            WideGamutDriver(0);
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Make changes in Registry for Disabling Narrow Gamut");
            RegistryParams registryParams = new RegistryParams();
            registryParams.value = 0;

            registryParams.infChanges = InfChanges.ModifyInf;

            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "NarrowGamutFeatureEnable";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);

            Log.Message(true, "Make changes in Registry for Disabling over ride chromaticity ");
            RegistryParams registryParams1 = new RegistryParams();
            registryParams1.value = 0;
            registryParams1.infChanges = InfChanges.RevertInf;
            registryParams1.registryKey = Registry.LocalMachine;
            registryParams1.keyName = "OverRideChromaticityData";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams1);
        }
        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            base.NarrowGamutSupportedDisplays.Intersect(base.CurrentConfig.DisplayList).ToList().ForEach(curDisp =>
            {
                base.SetNarrowGamutStatus(curDisp, NarrowGamutOption.EnableNarrowGamut, false);
            });
        }
        protected void PerformINFChanges(NarrowGamutOption argNarrowGamutOption)
        {
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.ProdDriverPath)
                  || Directory.GetFiles(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "Setup.exe").Count().Equals(0))
                Log.Abort("Setup file(s) in {0} path not found!", base.ApplicationManager.ApplicationSettings.ProdDriverPath);

            string infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");
            if (!Directory.Exists(infPath) || Directory.GetFiles(infPath, "*.inf").Count().Equals(0))
                Log.Abort("INF file in {0} path not found", infPath);

            Log.Message(true, "Make changes in INF file to enable Narrow Gamut and Wide Gamut");
            infPath = string.Concat(base.ApplicationManager.ApplicationSettings.ProdDriverPath, "\\Graphics");

            NarrowGamutParams NGParam = new NarrowGamutParams()
            {
                INFFilePath = infPath,
                narrowGamutOption = argNarrowGamutOption,
                DisplayType = _nGDisplay
            };
            AccessInterface.SetFeature<NarrowGamutParams>(Features.NarrowGamut, Action.Set, Source.AccessAPI, NGParam);                   
        }
        private void VerifyWideGamut(DisplayType argDispType, WideGamutLevel argWideGamutLevel)
        {
            Log.Message(true, "Verifying wide gamut for level {0} on {1}", argWideGamutLevel, argDispType);
            PipePlaneParams pipePlane1 = new PipePlaneParams(argDispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argDispType, pipePlane1.Pipe, pipePlane1.Plane);

            if (VerifyRegisters(WideGamutEvents[argWideGamutLevel], PIPE.NONE, pipePlane1.Plane, PORT.NONE))
            {
                Log.Success("WideGamut level {0} is verified for {1}", argWideGamutLevel, argDispType);
            }
            else
            {
                Log.Fail("WB Slider value is not set to level {0} for {1}", argWideGamutLevel, argDispType);
            }

            if (VerifyRegisters("PIPE_CSC", PIPE.NONE, pipePlane1.Plane, PORT.NONE))
            {
                Log.Success("csc is verified for {0}", argDispType);
            }
            else
            {
                Log.Fail("csc is not verified");
            }
        }
        protected virtual void VerifyColor(DisplayType argDispType)
        {
            Log.Message(true, "Verify {0} for {1}", _colorType, _xvycc_YcbcrDisplay);
            XvYccYcbXr xvyccObject = new XvYccYcbXr()
            {
                displayType = DisplayType.HDMI,
                currentConfig = base.CurrentConfig,
                colorType = ColorType.XvYCC,
                isEnabled = 1
            };
            if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.XvYcc, Action.SetMethod, xvyccObject))
            {
                Log.Success("xvycc is enabled on hdmi");
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.HDMI).FirstOrDefault();

                base.RegisterCheck(displayInfo.DisplayType, displayInfo, "XVYCC_ENABLE");

            }
            else
                Log.Fail("xvycc is not enabled on hdmi");
        }
        protected void WideGamutDriver(int argValue)
        {
            Log.Message(true, "Make changes in Registry for  Wide Gamut");
            RegistryParams registryParams = new RegistryParams();
            registryParams.value = argValue;
            if (argValue == 0)
                registryParams.infChanges = InfChanges.RevertInf;
            else
                registryParams.infChanges = InfChanges.ModifyInf;

            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "WideGamutFeatureEnable";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
    }
}