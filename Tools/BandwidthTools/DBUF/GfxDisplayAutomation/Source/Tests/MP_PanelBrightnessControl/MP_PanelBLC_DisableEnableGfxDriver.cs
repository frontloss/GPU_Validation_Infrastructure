using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_PanelBLC_DisableEnableGfxDriver : MP_PanelBLC_Base
    {
        internal List<PanelBLCData> PanelBLCData;
        private List<PanelBLCFunctions> FunctionCallSequence;
        private List<NotifyEvent> NotifyEventSequence;
        private Dictionary<PanelBLCFunctions, System.Action> ActionMapper;
        private int testStep = 0;
        private int notifyEventIndex = 0;

        private ushort initialBrightnessValue = 0;
        private ushort testCompletionBrightnessValue = 0;
        private GetBrightnessParam PanelBrightnessGetParam;

        public MP_PanelBLC_DisableEnableGfxDriver()
        {
            #region Allocate Memory
            NotifyEventSequence = new List<NotifyEvent>();
            ActionMapper = new Dictionary<PanelBLCFunctions, System.Action>();
            PanelBrightnessGetParam = new GetBrightnessParam();
            #endregion

            #region Define Function call Delegate
            ActionMapper.Add(PanelBLCFunctions.NotifyEvent, ParseNotifyEvent);
            ActionMapper.Add(PanelBLCFunctions.AuxAccessStatus, ParseAuxAccess);
            ActionMapper.Add(PanelBLCFunctions.PanelBlcPathEnableStatus, ParseDriverLoadStatus);
            #endregion
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Test Pre Condition");
            SetEnvironment();
            PanelBrightnessGetParam.ServiceType = PanelGetService.GetCurrentBrightness;
            initialBrightnessValue = AccessInterface.GetFeature<ushort, GetBrightnessParam>(Features.PanelBrightnessControl, Action.GetMethod, Source.AccessAPI, PanelBrightnessGetParam);
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
        public void DisableEnableDriver()
        {
            Log.Message(true, "Disable & Enabke GFX driver");
            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.DisableDriver, Action.SetMethod, DriverAdapterType.Intel))
                Log.Success("Successfully disabled Gfx Driver");
            else
                Log.Fail("Failed to disabled Gfx Driver");

            Thread.Sleep(10000);

            if (AccessInterface.SetFeature<bool, DriverAdapterType>(Features.EnableDriver, Action.SetMethod, DriverAdapterType.Intel))
                Log.Success("Successfully enable Gfx Driver");
            else
                Log.Fail("Failed to enable Gfx Driver");

            if(!base.DisablePanelDriver())
                Log.Abort("Failed to Disable Panel Brightness Control Stub Driver");
            if(!base.EnablePanelDriver())
                Log.Abort("Failed to Enabe Panel Brightness Control Stub Driver");
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void ParsePanelData()
        {
            PanelBLCData = base.ParsePanelBrightnessControl();
            SetTestProperty();

            foreach (PanelBLCFunctions FT in FunctionCallSequence)
            {
                if (ActionMapper.ContainsKey(FT))
                    ActionMapper[FT]();
                else
                    Log.Fail("Function Name {0} Not Defined", FT);
            }
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
            Log.Message(true, "Parsing Notify Event Function Call");
            if (PanelBLCData[testStep].PanelNotifyEvent != null)
            {
                NotifyEvent NE = PanelBLCData[testStep++].PanelNotifyEvent;
                if (NE.EventName == NotifyEventSequence[notifyEventIndex].EventName &&
                    NE.EventType == NotifyEventSequence[notifyEventIndex].EventType)
                {
                    Log.Success("Notify Event Sequence Expected, Event Name {0} Event Type {1} Time Stamp {2}", NE.EventName, NE.EventType, NE.TimeStamp);
                }
                else
                {
                    Log.Fail("Notify Event Sequence Dosen't Expected");
                    Log.Verbose("Expected Event Name {0} and Event Type {1}", NE.EventName, NE.EventType);
                    Log.Verbose("Actual Event Name {0} and Event Type {1}", NotifyEventSequence[notifyEventIndex].EventName, NotifyEventSequence[notifyEventIndex].EventType);
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
            if (base.MachineInfo.PlatformDetails.Platform == Platform.CHV)
                return;

            Log.Message(true, "Parsing Aux Access Status");
            if (PanelBLCData[testStep].PanelAuxAccess != null)
            {
                AuxAccessStatus status = PanelBLCData[testStep++].PanelAuxAccess;
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

        private void ParseDriverLoadStatus()
        {
            Log.Message(true, "Parsing Driver Load Status");
            if (PanelBLCData[testStep].PathEnableStatus != null)
            {
                PanelBlcPathEnableStatus PathEnable = PanelBLCData[testStep++].PathEnableStatus;
                if (PathEnable.Status == true)
                {
                    Log.Success("Arrival of GFX Driver Reported to panel Driver");
                }
                else
                {
                    Log.Fail("Arrival of GFX Driver dosen't Reported to Panel Driver");
                }
            }
            else
            {
                Log.Fail("Stub Driver Logger dosen't have Driver Load Entry");
            }
        }

        private void SetTestProperty()
        {
            #region Fill test Call Sequence
            if (base.PanelBacklightOff == false)
            {
                FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.PanelBlcPathEnableStatus };
            }
            else
            {
                FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.PanelBlcPathEnableStatus };
            }
            #endregion

            #region Fill Notify Event Sequence
            if (base.PanelBacklightOff == false)
            {
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_DRIVER_UNLOAD, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_DRIVER_LOADED, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
            }
            else
            {
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_DRIVER_UNLOAD, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
                NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_DRIVER_LOADED, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
            }
            #endregion
        }

    }
}
