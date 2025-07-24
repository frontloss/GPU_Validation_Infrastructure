using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    class MP_PanelBLC_AC_DC_Switch : MP_PanelBLC_Base
    {
        internal List<PanelBLCData> panelBLCData;

        internal List<PanelBLCFunctions> SKL_FunctionCallSequence;
        internal List<PanelBLCFunctions> CHV_FunctionCallSequence;
        internal List<NotifyEvent> SKL_NotifyEventSequence;

        internal Dictionary<Platform, List<PanelBLCFunctions>> FunctionCallsSequenceKV;
        internal Dictionary<Platform, List<NotifyEvent>> NotifyEventCallSequenceKV;

        internal Dictionary<PanelBLCFunctions, System.Action> ActionMapper;

        internal List<PanelBLCFunctions> TestFunctionCallSequence;
        internal List<NotifyEvent> TestNotifyEventCallSequence;
        private GetBrightnessParam PanelBrightnessGetParam;

        private int testStep = 0;
        private int notifyEventIndex = 0;

        private ushort ReducedBrightness;
        private ushort CurrentBrightness;
        private ushort BrightnessAfterEvent;

        public MP_PanelBLC_AC_DC_Switch()
        {
            #region Allocate Memory
            NotifyEventCallSequenceKV = new Dictionary<Platform, List<NotifyEvent>>();
            FunctionCallsSequenceKV = new Dictionary<Platform, List<PanelBLCFunctions>>();
            SKL_NotifyEventSequence = new List<NotifyEvent>();
            ActionMapper = new Dictionary<PanelBLCFunctions, System.Action>();
            PanelBrightnessGetParam = new GetBrightnessParam();
            #endregion

            #region Define Function call Delegate
            ActionMapper.Add(PanelBLCFunctions.NotifyEvent, ParseNotifyEvent);
            ActionMapper.Add(PanelBLCFunctions.AuxAccessStatus, ParseAuxAccess);
            ActionMapper.Add(PanelBLCFunctions.SetBrighthness, ParseSetBrightnessEvent);
            #endregion
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Test Pre Condition");
            ACDCSwitch(PowerLineStatus.Online);

            SetEnvironment();
            SetTestProperty();
            FunctionCallsSequenceKV.TryGetValue(base.MachineInfo.PlatformDetails.Platform, out TestFunctionCallSequence);
            NotifyEventCallSequenceKV.TryGetValue(base.MachineInfo.PlatformDetails.Platform, out TestNotifyEventCallSequence);

            PanelBrightnessGetParam.ServiceType = PanelGetService.GetCurrentBrightness;
            CurrentBrightness = AccessInterface.GetFeature<ushort, GetBrightnessParam>(Features.PanelBrightnessControl, Action.GetMethod, Source.AccessAPI, PanelBrightnessGetParam);
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void SetDisplayConfig()
        {
            Log.Message(true, "Set Current config via OS call");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SwitchPowerSource()
        {
            Log.Message(true, "Swith to DC Power Source and verify panel Driver Data");
            ACDCSwitch(PowerLineStatus.Offline);
            ParsePanelData();
            Log.Message(true, "Swith to AC Power Source and verify panel Driver Data");
            ACDCSwitch(PowerLineStatus.Online);
            ParsePanelData();
            ValidateSetBrightness();
        }

        [Test(Type = TestType.PostCondition, Order = 3)]
        public void TestCleanUP()
        {
            Log.Message(true, "Test Post Condition");
            base.EnableDisablePanelBLCInterface(0);
        }

        private void ParseNotifyEvent()
        {
            Log.Message(true, "Parsing Notify Event Function Call");
            if (panelBLCData[testStep].PanelNotifyEvent != null)
            {
                NotifyEvent NE = panelBLCData[testStep++].PanelNotifyEvent;

                if (NE.EventName == TestNotifyEventCallSequence[notifyEventIndex].EventName &&
                    NE.EventType == TestNotifyEventCallSequence[notifyEventIndex].EventType)
                {
                    Log.Success("Notify Event Sequence Expected, Event Name {0} Event Type {1} Time Stamp {2}", NE.EventName, NE.EventType, NE.TimeStamp);
                }
                else
                {
                    Log.Fail("Notify Event Sequence Dosen't Expected");
                    Log.Verbose("Expected Event Name {0} and Event Type {1}", NE.EventName, NE.EventType);
                    Log.Verbose("Actual Event Name {0} and Event Type {1}", TestNotifyEventCallSequence[notifyEventIndex].EventName, TestNotifyEventCallSequence[notifyEventIndex].EventType);
                }
                notifyEventIndex++;
            }
            else
            {
                Log.Fail("Stub Driver Logger dosen't have Notify Event Entry");
            }
        }

        private void ParseAuxAccess()
        {
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

        private void ParseSetBrightnessEvent()
        {
            ushort value;
            if (panelBLCData[testStep].PanelSetBrightness != null)
            {
                if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) == PowerLineStatus.Offline)
                {
                    ReducedBrightness = (ushort)panelBLCData[testStep].PanelSetBrightness.BrightnessValue;
                }
                if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) == PowerLineStatus.Online)
                {
                    BrightnessAfterEvent = (ushort)panelBLCData[testStep].PanelSetBrightness.BrightnessValue;
                }
                value = (ushort)panelBLCData[testStep++].PanelSetBrightness.BrightnessValue;
                Log.Verbose("Panel Brightness Control Set Brightness Value is {0}", value);
            }
        }

        private void ValidateSetBrightness()
        {
            if (CurrentBrightness == BrightnessAfterEvent)
                Log.Success("Brightness values are same ( {0} ) before and after DC to AC Switch", CurrentBrightness);
            else
            {
                Log.Fail("Brightness Values are different before and after DC to AC Switch");
                Log.Verbose("Brightness value before DC Switch {0}", CurrentBrightness);
                Log.Verbose("Brightness value after AC Switch {0}", BrightnessAfterEvent);
            }
        }

        private void ParsePanelData()
        {
            Thread.Sleep(10000);
            panelBLCData = base.ParsePanelBrightnessControl();
            testStep = 0;
            notifyEventIndex = 0;
            foreach (PanelBLCFunctions FT in TestFunctionCallSequence)
            {
                if (ActionMapper.ContainsKey(FT))
                    ActionMapper[FT]();
                else
                    Log.Fail("Function Name {0} Not Defined", FT);
            }
        }

        private void ACDCSwitch(PowerLineStatus powerSource)
        {
            string powerOption = powerSource == PowerLineStatus.Online ? "AC" : "DC";
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) != powerSource)
            {
                if (!AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Abort("Switch to {0} power option failed", powerOption);
                else
                    Log.Verbose(false, "System is in {0} power mode", powerOption);
            }
            else
                Log.Verbose(false, "System is in {0} power mode", powerOption);
        }

        private void SetTestProperty()
        {
            #region Fill test Call Sequence
            SKL_FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.SetBrighthness,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent, };

            FunctionCallsSequenceKV.Add(Platform.SKL, SKL_FunctionCallSequence);

            CHV_FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.SetBrighthness
            };

            FunctionCallsSequenceKV.Add(Platform.CHV, CHV_FunctionCallSequence);

            #endregion

            #region Fill Notify Event Sequence
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            NotifyEventCallSequenceKV.Add(Platform.SKL, SKL_NotifyEventSequence);
            #endregion
        }
    }
}
