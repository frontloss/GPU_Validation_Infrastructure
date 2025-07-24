using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_PanelBLC_SmoothBrightness : MP_PanelBLC_Base
    {
        internal List<PanelBLCData> panelBLCData;
        internal List<PanelBLCFunctions> TestFunctionCallSequence;
        private GetBrightnessParam PanelBrightnessGetParam;
        private SetBrightnessParam PanelBrightnessSetParam;
        private ulong timeOutInSec = 1;
        private ushort MaxBrightnessValue = 100;
        private ushort MinBrightnessValue = 0;

        internal Dictionary<PanelBLCFunctions, System.Action> ActionMapper;
        private int testStep = 0;
        private bool IsIncremental;
        private bool IsDecremental;
        private ushort prevBrightnessValue;

        public MP_PanelBLC_SmoothBrightness()
        {
            #region Allocate Memory
            ActionMapper = new Dictionary<PanelBLCFunctions, System.Action>();
            TestFunctionCallSequence = new List<PanelBLCFunctions>();

            PanelBrightnessGetParam = new GetBrightnessParam();
            PanelBrightnessSetParam = new SetBrightnessParam();
            #endregion

            #region Define Function call Delegate
            ActionMapper.Add(PanelBLCFunctions.SetBrighthness, ParseSetBrightness);
            ActionMapper.Add(PanelBLCFunctions.AuxAccessStatus, ParseAuxAccess);
            #endregion
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Test Pre Condition");
            base.ApplicationManager.VerifyTDR = false;
            DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.GetInternalDisplay() };
            Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Message("Config (SD {0}) applied successfully", displayConfig.PrimaryDisplay);
            else
            {
                Log.Abort("Config (SD {0}) not applied!", displayConfig.PrimaryDisplay);
            }
            SetDefaultBrightness();
            SetEnvironment();
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void DecreasePanelBrightness()
        {
            int currentBrightness = GetCurrentBrightness();
            Log.Message(true, "Change Panel Brightness from {0} to {0} Percent", currentBrightness, MinBrightnessValue);
            for (ushort brightness = 99; brightness >= 1; brightness--)
            {
                SetPanelBrightnessLevel(brightness);
                if (brightness == 0) break;
            }
            prevBrightnessValue = 99;
            IsDecremental = true;
            ParsePanelData();
            IsDecremental = false;
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void IncreasePanelBrightness()
        {
            int currentBrightness = GetCurrentBrightness();
            Log.Message(true, "Change Panel Brightness from {0} to {0} Percent", currentBrightness, MaxBrightnessValue);
            for (ushort brightness = 2; brightness <= 100; brightness++)
            {
                SetPanelBrightnessLevel(brightness);
            }
            prevBrightnessValue = 2;
            IsIncremental = true;
            ParsePanelData();
            IsIncremental = false;
        }

        [Test(Type = TestType.PostCondition, Order = 3)]
        public void TestCleanUP()
        {
            Log.Message(true, "Test Post Condition");
            base.EnableDisablePanelBLCInterface(0);
        }

        private void ParsePanelData()
        {
            panelBLCData = base.ParsePanelBrightnessControl();
            SetTestProperty();
            foreach (PanelBLCFunctions FT in TestFunctionCallSequence)
            {
                if (ActionMapper.ContainsKey(FT))
                    ActionMapper[FT]();
                else
                    Log.Fail("Function Name {0} Not Defined", FT);
            }
        }

        private bool SetPanelBrightnessLevel(ushort argBrightnessValue)
        {
            Log.Verbose("Change Panel Brightness to {0} percent", argBrightnessValue);
            PanelBrightnessSetParam.ServiceType = PanelSetService.SerBrightness;
            PanelBrightnessSetParam.Brightness = argBrightnessValue;
            PanelBrightnessSetParam.Timeout = timeOutInSec;
            if (AccessInterface.SetFeature<bool, SetBrightnessParam>(Features.PanelBrightnessControl, Action.SetMethod, Source.AccessAPI, PanelBrightnessSetParam))
            {
                return true;
            }
            else
            {
                Log.Fail("Unable to Set Panel Brightness to {0} Percent", PanelBrightnessSetParam.Brightness);
                Log.Verbose("Current Brightness Value is {0}", GetCurrentBrightness());
                return false;
            }
        }

        private ushort GetCurrentBrightness()
        {
            return AccessInterface.GetFeature<ushort, GetBrightnessParam>(Features.PanelBrightnessControl, Action.GetMethod, Source.AccessAPI, PanelBrightnessGetParam);
        }

        private void SetDefaultBrightness()
        {
            PanelBrightnessGetParam.ServiceType = PanelGetService.GetCurrentBrightness;
            if (MaxBrightnessValue != GetCurrentBrightness())
            {
                SetPanelBrightnessLevel(MaxBrightnessValue);
            }
        }

        private void SetTestProperty()
        {
            TestFunctionCallSequence.Clear();
            testStep = 0;
            if (panelBLCData.Count == 0)
            {
                Log.Fail("No Valid Panel Brightness Data Found");
            }
            else
            {
                foreach (PanelBLCData PD in panelBLCData)
                {
                    if (PD.PanelSetBrightness != null)
                        TestFunctionCallSequence.Add(PanelBLCFunctions.SetBrighthness);
                    else if (PD.PanelAuxAccess != null)
                        TestFunctionCallSequence.Add(PanelBLCFunctions.AuxAccessStatus);
                    else
                    {
                        Log.Abort("Invalid Function Call Entry found.");
                    }
                }
            }
        }

        private void ParseSetBrightness()
        {
            bool Status = true;
            if (panelBLCData[testStep].PanelSetBrightness != null)
            {
                ushort value = (ushort)panelBLCData[testStep++].PanelSetBrightness.BrightnessValue;
                Log.Verbose("Panel Brightness Control Set Brightness Value is {0}", value);
                if (IsDecremental)
                {
                    if (value == prevBrightnessValue)
                    {
                        Log.Verbose("Panle Brightness Value {0}", value);
                        prevBrightnessValue--;
                    }
                    else
                    {
                        Log.Alert("Panel Brightness Value {0}", value);
                        Status = false;
                        prevBrightnessValue = (ushort)(GetCurrentBrightness() - 1);
                    }
                }
                if (IsIncremental)
                {
                    if (value == prevBrightnessValue)
                    {
                        Log.Verbose("Panle Brightness Value {0}", value);
                        prevBrightnessValue++;
                    }
                    else
                    {
                        Log.Alert("Panel Brightness Value {0}", value);
                        Status = false;
                        prevBrightnessValue = (ushort)(GetCurrentBrightness() + 1);
                    }
                }

                if (Status == true)
                {
                    Log.Success("Set Brightness Call Sequence as expected");
                }
                else
                {
                    Log.Fail("Set Brightness Call Sequence is not as expected");
                }
            }
            else
            {
                Log.Fail("Stub Driver Logger dosen't have Set Brightness Entry");
            }
        }

        private void ParseAuxAccess()
        {
            if (base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
                return;
            Log.Verbose("Parsing Aux Access Status");
            if (panelBLCData[testStep].PanelAuxAccess != null)
            {
                AuxAccessStatus status = panelBLCData[testStep++].PanelAuxAccess;
                if (status.AuxStatus == PanelBLCIGDStatus.IGD_SUCCESS)
                {
                    Log.Success("Aux Access Success, IGD Status {0}", status.AuxStatus);
                }
                else
                {
                    Log.Fail("Aux Access Failed, IGD Status {0}", status.AuxStatus);
                }
            }
            else
            {
                Log.Fail("Stub Driver Logger dosen't have Aux Access Entry");
            }
        }
    }
}
