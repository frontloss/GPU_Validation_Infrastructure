using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_PanelBLC_PowerEvent_S3 : MP_PanelBLC_Base
    {
        protected PowerParams powerParams;
        internal List<PanelBLCData> PanelBLCData;
        internal List<PanelBLCData> ActualPanelBLCData;
        internal List<PanelBLCFunctions> SKL_FunctionCallSequence;
        internal List<PanelBLCFunctions> CHV_FunctionCallSequence;
        internal List<NotifyEvent> SKL_NotifyEventSequence;
        internal List<NotifyEvent> CHV_NotifyEventSequence;

        internal Dictionary<Platform, List<PanelBLCFunctions>> FunctionCallsSequenceKV;
        internal Dictionary<Platform, List<NotifyEvent>> NotifyEventCallSequenceKV;

        internal Dictionary<PanelBLCFunctions, System.Action> ActionMapper;

        internal List<PanelBLCFunctions> TestFunctionCallSequence;
        internal List<NotifyEvent> TestNotifyEventCallSequence;

        private int testStep = 0;
        private int notifyEventIndex = 0;
        private int setBrightnessValuBeforPowerEvent = -1;
        private int setBrightnessValueAfterPowerEvent = -1;
        private bool SystemPowerOffState = false;
        private bool PowerOnFollowedByOff = false;
        private ushort initialBrightnessValue = 0;
        private ushort testCompletionBrightnessValue = 0;
        private GetBrightnessParam PanelBrightnessGetParam;

        public MP_PanelBLC_PowerEvent_S3()
        {
            #region S3 Event Data Property
            powerParams = new PowerParams() { Delay = 45, };
            powerParams.PowerStates = PowerStates.S3;
            #endregion

            #region Allocate Memory
            NotifyEventCallSequenceKV = new Dictionary<Platform, List<NotifyEvent>>();
            FunctionCallsSequenceKV = new Dictionary<Platform, List<PanelBLCFunctions>>();
            SKL_NotifyEventSequence = new List<NotifyEvent>();
            CHV_NotifyEventSequence = new List<NotifyEvent>();
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
            SetEnvironment();
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
        public void GotopowerState()
        {
            PanelBrightnessGetParam.ServiceType = PanelGetService.GetCurrentBrightness;
            initialBrightnessValue = AccessInterface.GetFeature<ushort, GetBrightnessParam>(Features.PanelBrightnessControl, Action.GetMethod, Source.AccessAPI, PanelBrightnessGetParam);
            Log.Message(true, "Put the system into {0} state & resume", powerParams.PowerStates.ToString());
            base.EventResult(powerParams.PowerStates, base.InvokePowerEvent(powerParams, powerParams.PowerStates));
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void ParsePanelData()
        {
            PanelBLCData = base.ParsePanelBrightnessControl();
            RemoveMultipleSetCall();
            ActualPanelBLCData = PreParser();
            
            SetTestProperty();
            FunctionCallsSequenceKV.TryGetValue(base.MachineInfo.PlatformDetails.Platform, out TestFunctionCallSequence);
            NotifyEventCallSequenceKV.TryGetValue(base.MachineInfo.PlatformDetails.Platform, out TestNotifyEventCallSequence);

            foreach (PanelBLCFunctions FT in TestFunctionCallSequence)
            {
                if (ActionMapper.ContainsKey(FT))
                    ActionMapper[FT]();
                else
                    Log.Fail("Function Name Not Defined");
            }

            ValidateSetBrightnessAfterPE();
        }

        [Test(Type = TestType.PostCondition, Order = 4)]
        public void TestCleanUP()
        {
            testCompletionBrightnessValue = AccessInterface.GetFeature<ushort, GetBrightnessParam>(Features.PanelBrightnessControl, Action.GetMethod, Source.AccessAPI, PanelBrightnessGetParam);
            if (initialBrightnessValue != testCompletionBrightnessValue)
            {
                Log.Fail("Initial Brightness value {0} and test completion brightness value {1} are not same", initialBrightnessValue, testCompletionBrightnessValue);
            }
            Log.Message(true, "Test Post Condition");
            base.EnableDisablePanelBLCInterface(0);
        }

        private void ParseNotifyEvent()
        {
            #region Check for IGD_BACKLIGHT_OFF Event Entry which is optional
            if (PowerOnFollowedByOff == true)
            {
                NotifyEvent NE = TestNotifyEventCallSequence[notifyEventIndex];
                if (NE.Optional == true &&
                    ((NE.EventName == PanelBLCEventName.IGD_BACKLIGHT_OFF) && ActualPanelBLCData[testStep].PanelNotifyEvent.EventName != NE.EventName))
                {
                        notifyEventIndex++;
                        return;
                }
            }
            #endregion

            Log.Message(true, "Parsing Notify Event Function Call");
            if (ActualPanelBLCData[testStep].PanelNotifyEvent != null)
            {
                NotifyEvent NE = ActualPanelBLCData[testStep++].PanelNotifyEvent;
                if (NE.EventName == PanelBLCEventName.IGD_SYSTEM_D3_D4)
                    SystemPowerOffState = true;

                if (NE.EventName == PanelBLCEventName.IGD_SYSTEM_D0)
                {
                    if (SystemPowerOffState == true)
                    {
                        PowerOnFollowedByOff = true;
                    }
                    SystemPowerOffState = false;
                }

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
            Log.Message(true, "Parsing Aux Access Status");
            if (ActualPanelBLCData[testStep].PanelAuxAccess != null)
            {
                AuxAccessStatus status = ActualPanelBLCData[testStep++].PanelAuxAccess;

                if (SystemPowerOffState == true && status.AuxStatus != PanelBLCIGDStatus.IGD_SUCCESS)
                {
                    Log.Success("Aux Access as expected, IGD Status {0}, system in low power state", status.AuxStatus);
                }
                
                else if (status.AuxStatus == PanelBLCIGDStatus.IGD_SUCCESS)
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
            Log.Message(true, "Parsing Set Brightness");
            if (ActualPanelBLCData[testStep].PanelSetBrightness != null)
            {
                int value = ActualPanelBLCData[testStep++].PanelSetBrightness.BrightnessValue;
                if (SystemPowerOffState == true)
                    setBrightnessValuBeforPowerEvent = value;
                else
                    setBrightnessValueAfterPowerEvent = value;
                Log.Verbose("Panel Brightness Control Set Brightness Value is {0}", value);
            }
            else
            {
                Log.Fail("Stub Driver Logger dosen't have Set Brightness Entry");
            }
        }

        private void RemoveMultipleSetCall()
        {
            List<PanelBLCData> temp = new List<PanelBLCData>();
            bool duplicateSetCall = false;
            for (int idx = 0; idx < PanelBLCData.Count; idx++)
            {
                duplicateSetCall = false;
                PanelBLCData data = PanelBLCData[idx];
                if (data.PanelSetBrightness != null)
                {
                    PanelBLCData NextSetdata = PanelBLCData[idx + 1];
                    if (NextSetdata.PanelSetBrightness != null && duplicateSetCall == false)
                    {
                        duplicateSetCall = true;
                        temp.Add(data);
                    }
                    else if (duplicateSetCall == false)
                    {
                        temp.Add(data);
                    }
                }
                else
                {
                    temp.Add(data);
                    duplicateSetCall = false;
                }
            }
            PanelBLCData.Clear();
            PanelBLCData.AddRange(temp);
        }

        /* This function will return whether data enty is valid or not
         * On win 10 we are getting multiple on off call */
        private List<PanelBLCData> PreParser()
        {
            int nextOnCallIndex = 0 ;

            List<PanelBLCData> temp = new List<PanelBLCData>();
            for (int idx = 0; idx < PanelBLCData.Count; idx++)
            {
                PanelBLCData data = PanelBLCData[idx];
                if (data.PanelSetBrightness != null)
                {

                }
                if (ValidateMultipleOnOffCall(idx, ref nextOnCallIndex) == false)
                {
                    temp.Add(data);
                }
                else
                {
                    idx += nextOnCallIndex; 
                }
            }
            return temp;
        }

        private bool ValidateMultipleOnOffCall(int idx, ref int nextOnCallIndex)
        {
            if (idx < (PanelBLCData.Count - 1))
            {
                NotifyEvent OnCall = PanelBLCData[idx].PanelNotifyEvent;
                NotifyEvent OffCall = PanelBLCData[idx + 1].PanelNotifyEvent;
                if (OnCall != null && OffCall != null)
                {
                    if (OnCall.EventName == PanelBLCEventName.IGD_SYSTEM_D0 &&
                        OffCall.EventName == PanelBLCEventName.IGD_SYSTEM_D3_D4)
                    {
                        nextOnCallIndex = FindNextPowerOnCall(idx);
                        return true;
                    }
                    return false;
                }
            }
            return false;
        }

        private int FindNextPowerOnCall(int idx)
        {
            int nextPowerOnIndex = 0;
            for (int index = idx + 1; index < (PanelBLCData.Count - 1); index++)
            {
                NotifyEvent OnCall = PanelBLCData[index].PanelNotifyEvent;
                if (OnCall != null)
                {
                    if (OnCall.EventName == PanelBLCEventName.IGD_SYSTEM_D0)
                        break;
                    else
                        nextPowerOnIndex++;
                }
                else
                    nextPowerOnIndex++;
            }
            return nextPowerOnIndex;
        }

        private void ValidateSetBrightnessAfterPE()
        {
            if (setBrightnessValuBeforPowerEvent != -1 && setBrightnessValueAfterPowerEvent != -1)
            {
                if (setBrightnessValuBeforPowerEvent == setBrightnessValueAfterPowerEvent)
                    Log.Success("Brightness values are same ( {0} ) before and after power event {1}", setBrightnessValuBeforPowerEvent, powerParams.PowerStates.ToString());
                else
                {
                    Log.Fail("Brightness Values are different before and after power event {0}", powerParams.PowerStates.ToString());
                    Log.Verbose("Brightness value before power event is {0}", setBrightnessValuBeforPowerEvent);
                    Log.Verbose("Brightness value after power event is {0}", setBrightnessValueAfterPowerEvent);
                }

            }
        }

        internal virtual void SetTestProperty()
        {
            #region Fill test Call Sequence
            SKL_FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.SetBrighthness,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent };

            FunctionCallsSequenceKV.Add(Platform.SKL, SKL_FunctionCallSequence);

            CHV_FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.SetBrighthness,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent };

            FunctionCallsSequenceKV.Add(Platform.CHV, CHV_FunctionCallSequence);
            #endregion

            #region Fill Notify Event Sequence
            //Sleep Sequence
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_SYSTEM_D3_D4, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });

            //Wake Sequence
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_SYSTEM_D0, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            NotifyEventCallSequenceKV.Add(Platform.SKL, SKL_NotifyEventSequence);

            //Sleep Sequence
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            //Wake Sequence
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            NotifyEventCallSequenceKV.Add(Platform.CHV, CHV_NotifyEventSequence);
            #endregion
        }
    }
}
