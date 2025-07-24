using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_PanelBLC_Hotplug_UnPlug : MP_PanelBLC_Base
    {
        internal List<PanelBLCData> PanelData;
        private List<PanelBLCData> TempPanelData;
        internal List<PanelBLCFunctions> TestFunctionCallSequence;
        internal List<NotifyEvent> TestNotifyEventCallSequence;

        internal Dictionary<PanelBLCFunctions, System.Action> ActionMapper;
        private int testStep = 0;
        private int notifyEventIndex = 0;

        public MP_PanelBLC_Hotplug_UnPlug()
        {
            #region Allocate Memory
            ActionMapper = new Dictionary<PanelBLCFunctions, System.Action>();
            TestNotifyEventCallSequence = new List<NotifyEvent>();
            #endregion

            #region Fill test Call Sequence
            TestFunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent };
            #endregion

            #region Fill Notify Event Sequence
            //Sleep Sequence
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            TestNotifyEventCallSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            #endregion

            #region Define Function call Delegate
            ActionMapper.Add(PanelBLCFunctions.NotifyEvent, ParseNotifyEvent);
            ActionMapper.Add(PanelBLCFunctions.AuxAccessStatus, ParseAuxAccess);
            #endregion
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Test Pre Condition");
            if (base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
            {
                Log.Abort("Test is invalid for this platform");
            }
            SetEnvironment();
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void PerformAction()
        {
            if (base.CurrentConfig.PluggableDisplayList.Count == 0)
            {
                Log.Abort("No Pluggable Display Found");
            }
            Log.Message(true, "Hotplug Unplug External Display");
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Verbose("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);
                    ParsePanelData();

                    Log.Verbose("Unplugging display {0}", DT);
                    if (base.HotUnPlug(DT))
                    {
                        Log.Success("Successfully able to hot unplug display {0}", DT);
                        ParsePanelData();
                    }
                    else
                        Log.Fail("Unable to hot unplug display {0}", DT);
                }
                else
                {
                    Log.Fail("Unable to hot plug display {0}", DT);
                }
            }
        }

        [Test(Type = TestType.PostCondition, Order = 2)]
        public void TestCleanUP()
        {
            Log.Message(true, "Test Post Condition");
            base.EnableDisablePanelBLCInterface(0);
        }

        internal void ParsePanelData()
        {
            testStep = 0;
            notifyEventIndex = 0;
            TempPanelData = base.ParsePanelBrightnessControl();
            PreParser();
            foreach (PanelBLCFunctions FT in TestFunctionCallSequence)
            {
                if (ActionMapper.ContainsKey(FT))
                    ActionMapper[FT]();
                else
                    Log.Fail("Function Name {0} Not Defined", FT);
            }
        }

        private void PreParser()
        {
            int startIndex;
            PanelData = new List<PanelBLCData>();
            for (startIndex = 0; startIndex < TempPanelData.Count; startIndex++)
            {
                if (TempPanelData[startIndex].PanelNotifyEvent != null)
                {
                    if (TempPanelData[startIndex].PanelNotifyEvent.EventName == PanelBLCEventName.IGD_BACKLIGHT_OFF)
                    {
                        break;
                    }
                }
            }
            for (int Index = startIndex; Index < TempPanelData.Count; Index++)
            {
                PanelData.Add(TempPanelData[Index]);
            }
        }

        private void ParseNotifyEvent()
        {
            Log.Message(true, "Parsing Notify Event Function Call");
            if (PanelData[testStep].PanelNotifyEvent != null)
            {
                NotifyEvent NE = PanelData[testStep++].PanelNotifyEvent;
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
            if (PanelData[testStep].PanelAuxAccess != null)
            {
                AuxAccessStatus status = PanelData[testStep++].PanelAuxAccess;
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
