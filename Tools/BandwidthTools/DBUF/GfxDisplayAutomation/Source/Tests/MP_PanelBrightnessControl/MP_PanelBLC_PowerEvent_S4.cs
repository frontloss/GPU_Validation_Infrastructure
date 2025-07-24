using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_PanelBLC_PowerEvent_S4 : MP_PanelBLC_PowerEvent_S3
    {
        public MP_PanelBLC_PowerEvent_S4()
        {
            #region S4 Event Data Property
            powerParams = new PowerParams() { Delay = 60, };
            powerParams.PowerStates = PowerStates.S4;
            #endregion
        }

        internal override void SetTestProperty()
        {
            #region Fill test Call Sequence
            if (base.FastModeSet)
            {
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
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent };
            }
            else
            {
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
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.AuxAccessStatus,
                PanelBLCFunctions.NotifyEvent };
            }

            FunctionCallsSequenceKV.Add(Platform.SKL, SKL_FunctionCallSequence);
            
            CHV_FunctionCallSequence = new List<PanelBLCFunctions>{
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.SetBrighthness,
                PanelBLCFunctions.NotifyEvent,
                PanelBLCFunctions.NotifyEvent };

            FunctionCallsSequenceKV.Add(Platform.CHV, CHV_FunctionCallSequence);
            #endregion

            #region Fill Notify Event Sequence

            if (base.FastModeSet)
            {
                //Sleep Sequence
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT, Optional = true });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT, Optional = true });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_SYSTEM_D3_D4, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });

                //Wake Sequence
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_SYSTEM_D0, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

                NotifyEventCallSequenceKV.Add(Platform.SKL, SKL_NotifyEventSequence);
            }
            else
            {
                //Sleep Sequence
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT, Optional = true });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT, Optional = true });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_SYSTEM_D3_D4, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });

                //Wake Sequence
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_SYSTEM_D0, EventType = PanelBLCEventType.IGD_EVENT_TYPE_SINGLE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT, Optional = true });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT, Optional = true });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
                SKL_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

                NotifyEventCallSequenceKV.Add(Platform.SKL, SKL_NotifyEventSequence);
            }

            //Sleep Sequence
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_PANEL_POWER_OFF, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            //Wake Sequence
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_PRE_EVENT });
            CHV_NotifyEventSequence.Add(new NotifyEvent { EventName = PanelBLCEventName.IGD_BACKLIGHT_ON, EventType = PanelBLCEventType.IGD_EVENT_TYPE_POST_EVENT });

            NotifyEventCallSequenceKV.Add(Platform.CHV, CHV_NotifyEventSequence);
            #endregion
        }
    }
}
