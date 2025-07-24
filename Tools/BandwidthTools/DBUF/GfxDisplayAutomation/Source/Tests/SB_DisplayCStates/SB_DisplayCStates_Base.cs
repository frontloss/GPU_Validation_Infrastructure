namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Runtime.InteropServices;
    using System.Diagnostics;

    class SB_DisplayCStates_Base : TestBase
    {
        protected uint DC5CounterInitial = 0;
        protected uint DC5CounterFinal = 0;
        protected uint DC6CounterInitial = 0;
        protected bool DC5Status = false;
        protected bool DC6_DC9Status = false;
        protected bool CommandMode = false;
        protected enum DCStateOutput
        {
            DC5,
            DC6,
            DC9
        }

        protected uint DC6CounterFinal = 0;
        [DllImport("user32.dll", EntryPoint = "FindWindow", SetLastError = true)]
        static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        [DllImport("user32.dll", EntryPoint = "SendMessage", SetLastError = true)]
        static extern IntPtr SendMessage(IntPtr hWnd, Int32 Msg, IntPtr wParam, IntPtr lParam);
        const int WM_COMMAND = 0x111;
        const int MIN_ALL = 419;
        const int MIN_ALL_UNDO = 416;
        protected List<DCStateOutput> DisplayCStateEDP(bool argIsBXT, bool argIsIdle, bool argIsMinimize)
        {
            List<DCStateOutput> outputDCState = new List<DCStateOutput>();

            Int32 bitmap = 0x00000003;
            int value = 2;
            if (argIsBXT)
            {
                bitmap = 0x00000001;
                value = 1;
            }
            List<uint> DisplayCStateRegisters = new List<uint>();
            Log.Message(true, "Get initial values for DC3_DC5_Counter and DC5_DC6_Counter");
            DC5CounterInitial = GetRegisterValue("DC5_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);
            if (!argIsBXT)
                DC6CounterInitial = GetRegisterValue("DC6_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);

            MonitorTurnOffParam monitorTurnOffParam = new MonitorTurnOffParam();
            if (argIsIdle)
            {
                Log.Message(true, "Keep the system idle for 2 minutes");
                if (argIsMinimize)
                {
                    monitorTurnOffParam.onOffParam = MonitorOnOff.On;
                    IntPtr LhWND = FindWindow("Shell_TrayWnd", null);
                    SendMessage(LhWND, WM_COMMAND, (IntPtr)MIN_ALL, IntPtr.Zero);
                }
            }
            else
            {
                Process.Start("monitoroff.exe");
            }
            monitorTurnOffParam.waitingTime = 120;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam);
            var startTime = DateTime.UtcNow;
            while (DateTime.UtcNow - startTime < TimeSpan.FromSeconds(180))
            {

                //if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam))
                //{

                DisplayCStateRegisters = GetRegisterValueList("DC_STATE", PIPE.NONE, PLANE.NONE, PORT.NONE);
                Log.Message("DC_States Register Value at {0} --> DC_STATE_DEBUG = {1}, DC_STATE_ENABLE = {2}, DC_STATE_SELECT = {3}, POWER_WELL_CONTROL = {4}", DateTime.Now.ToString(), DisplayCStateRegisters[0], DisplayCStateRegisters[1], DisplayCStateRegisters[2], DisplayCStateRegisters[3]);
                if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && ((DisplayCStateRegisters[2] & bitmap) == value))
                {
                    DC5Status = true;
                }
                if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && (DisplayCStateRegisters[1] == 0xffffffff) && (DisplayCStateRegisters[2] == 0xffffffff))
                //if (((DisplayCStateRegisters[0] & 0x00000002) == 2))
                {
                    DC6_DC9Status = true;
                }
                //}
            }
            monitorTurnOffParam.onOffParam = MonitorOnOff.On;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam);
            DisplayConfig displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = DisplayType.EDP
            };
            if (base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
            {
                displayConfig.PrimaryDisplay = DisplayType.MIPI;
            }
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            Log.Message(true, "Get final values for DC3_DC5_Counter and DC5_DC6_Counter");
            DC5CounterFinal = GetRegisterValue("DC5_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);

            if (!argIsBXT)
                DC6CounterFinal = GetRegisterValue("DC6_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message("DC5_Counter_Initial = {0}, DC5_Counter_Final = {1}, DC6_Counter_Initial = {2}, DC6_Counter_Final = {3}", DC5CounterInitial, DC5CounterFinal, DC6CounterInitial, DC6CounterFinal);

            if (argIsIdle)
            {
                if ((DC5CounterFinal != DC5CounterInitial) || (DC5Status))
                {
                    Log.Success("The system entered DC5");
                    outputDCState.Add(DCStateOutput.DC5);
                }
            }
            else
            {
                if (DC5CounterFinal != DC5CounterInitial || (DC5Status))
                {
                    Log.Success("The system entered DC5");
                    outputDCState.Add(DCStateOutput.DC5);
                }
                if (DC6CounterFinal != DC6CounterInitial || (DC6_DC9Status == true))
                {
                    Log.Success("The system entered DC6");
                    outputDCState.Add(DCStateOutput.DC6);
                }

            }
            if (argIsBXT)
            {
                if (DC6_DC9Status)
                {
                    Log.Success("The system entered DC9");
                    outputDCState.Add(DCStateOutput.DC9);
                }

            }
            return outputDCState;
        }
        protected List<DCStateOutput> DisplayCStateEDP(bool argIsBXT, bool argIsIdle)
        {
            List<DCStateOutput> outputDCState = new List<DCStateOutput>();
            Int32 bitmap = 0x00000003;
            int value = 2;
            if (argIsBXT)
            {
                bitmap = 0x00000001;
                value = 1;
            }
            List<uint> DisplayCStateRegisters = new List<uint>();
            Log.Message(true, "Get initial values for DC3_DC5_Counter and DC5_DC6_Counter");
            DC5CounterInitial = GetRegisterValue("DC5_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);
            if (!argIsBXT)
                DC6CounterInitial = GetRegisterValue("DC6_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);
           
            MonitorTurnOffParam monitorTurnOffParam = new MonitorTurnOffParam();
            if (argIsIdle)
            {
                Log.Message(true, "Keep the system idle for 2 minutes");
                monitorTurnOffParam.onOffParam = MonitorOnOff.On;
                IntPtr LhWND = FindWindow("Shell_TrayWnd", null);
                SendMessage(LhWND, WM_COMMAND, (IntPtr)MIN_ALL, IntPtr.Zero);
            }
            else
            {
                Process.Start("monitoroff.exe");
            }
            monitorTurnOffParam.waitingTime = 120;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam);
            var startTime = DateTime.UtcNow;
            while (DateTime.UtcNow - startTime < TimeSpan.FromSeconds(180))
            {
            
                //if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam))
                //{

                    DisplayCStateRegisters = GetRegisterValueList("DC_STATE", PIPE.NONE, PLANE.NONE, PORT.NONE);
                    Log.Message("DC_States Register Value at {0} --> DC_STATE_DEBUG = {1}, DC_STATE_ENABLE = {2}, DC_STATE_SELECT = {3}, POWER_WELL_CONTROL = {4}", DateTime.Now.ToString(), DisplayCStateRegisters[0], DisplayCStateRegisters[1], DisplayCStateRegisters[2], DisplayCStateRegisters[3]);
                    if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && ((DisplayCStateRegisters[2] & bitmap) == value))
                    {
                        DC5Status = true;
                    }
                    if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && (DisplayCStateRegisters[1] == 0xffffffff) && (DisplayCStateRegisters[2] == 0xffffffff))
                        //if (((DisplayCStateRegisters[0] & 0x00000002) == 2))
                    {
                        DC6_DC9Status = true;
                    }
                //}
            }
            monitorTurnOffParam.onOffParam = MonitorOnOff.On;
            AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam);
            DisplayConfig displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = DisplayType.EDP
            };
            if (base.CurrentConfig.CustomDisplayList.Contains(DisplayType.MIPI))
            {
                displayConfig.PrimaryDisplay = DisplayType.MIPI;
            }
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Success("Config applied successfully");
            else
            
            
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            Log.Message(true, "Get final values for DC3_DC5_Counter and DC5_DC6_Counter");
            DC5CounterFinal = GetRegisterValue("DC5_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);

            if (!argIsBXT)
                DC6CounterFinal = GetRegisterValue("DC6_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message("DC5_Counter_Initial = {0}, DC5_Counter_Final = {1}, DC6_Counter_Initial = {2}, DC6_Counter_Final = {3}", DC5CounterInitial, DC5CounterFinal, DC6CounterInitial, DC6CounterFinal);

            if (argIsIdle)
            {
                if ((DC5CounterFinal != DC5CounterInitial) || (DC5Status))
                {
                    Log.Success("The system entered DC5");
                    outputDCState.Add(DCStateOutput.DC5);
                }
            }
            else
            {
                if (DC5CounterFinal != DC5CounterInitial || (DC5Status))
                {
                    Log.Success("The system entered DC5");
                    outputDCState.Add(DCStateOutput.DC5);
                }
                if (DC6CounterFinal != DC6CounterInitial || (DC6_DC9Status == true))
                {
                    Log.Success("The system entered DC6");
                    outputDCState.Add(DCStateOutput.DC6);
                }

            }
            if (argIsBXT)
            {
                if (DC6_DC9Status)
                {
                    Log.Success("The system entered DC9");
                    outputDCState.Add(DCStateOutput.DC9);
                }
               
            }
            return outputDCState;
        }
        protected List<DCStateOutput> DisplayCStateMIPI(bool argIsVideoMode, bool argIsIdle)
        {
            List<DCStateOutput> outputDCState = new List<DCStateOutput>();
            Int32 bitmap = 0x00000008;
            int value = 8;
            List<uint> DisplayCStateRegisters = new List<uint>();
            Log.Message(true, "Get initial values for DC3_DC5_Counter and DC5_DC6_Counter");
            DC5CounterInitial = GetRegisterValue("DC5_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);
            if (VerifyRegisters("COMMAND_VIDEO_MODE", PIPE.NONE, PLANE.NONE, PORT.NONE, false))
            {
                if (argIsVideoMode)
                    Log.Abort("The test requires Video Mode..MIPI panel is in Command Mode");
                else
                    Log.Success("The Panel is in Command Mode");
            }
            else
            {
                if (argIsVideoMode)
                    Log.Success("The Panel is in Video Mode");
                else
                    Log.Abort("The test requires Command Mode..MIPI panel is in Video Mode");
            }
            List<uint> BLCRegisters = new List<uint>();
            BLCRegisters = GetRegisterValueList("PWM", PIPE.NONE, PLANE.NONE, PORT.NONE);
            if (((BLCRegisters[0] & 0x80000000) == 80000000) && ((BLCRegisters[1] & 0x80000000) == 80000000))
            {
                Log.Message("MIPI is in DisplayPWM");
                MonitorTurnOffParam monitorTurnOffParam = new MonitorTurnOffParam();
                if (argIsIdle)
                {
                    Log.Message(true, "Keep the system idle for 2 minutes");
                    monitorTurnOffParam.onOffParam = MonitorOnOff.On;
                }
                else
                {
                    Log.Message(true, "Turn off Monitor for 2 minutes");
                    monitorTurnOffParam.onOffParam = MonitorOnOff.OffOn;
                }
                monitorTurnOffParam.waitingTime = 120;
                if (AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorTurnOffParam))
                {
                    var startTime = DateTime.UtcNow;
                    while (DateTime.UtcNow - startTime < TimeSpan.FromSeconds(120))
                    {
                        DisplayCStateRegisters = GetRegisterValueList("DC_STATE", PIPE.NONE, PLANE.NONE, PORT.NONE);
                        Log.Message("DC_States Register Value at {0} --> DC_STATE_DEBUG = {1}, DC_STATE_ENABLE = {2}, DC_STATE_SELECT = {3}, POWER_WELL_CONTROL = {4}", DateTime.Now.ToString(), DisplayCStateRegisters[0], DisplayCStateRegisters[1], DisplayCStateRegisters[2], DisplayCStateRegisters[3]);
                        if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && ((DisplayCStateRegisters[1] & bitmap) == value))
                        {
                            DC5Status = true;
                        }
                        if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && (DisplayCStateRegisters[1] == 0xffffffff) && (DisplayCStateRegisters[2] == 0xffffffff))
                        {
                            DC6_DC9Status = true;
                        }
                    }
                }
            }
            else
            {
                Log.Message("MIPI is in PanelPWM");
                if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && ((DisplayCStateRegisters[1] & bitmap) == value) && ((DisplayCStateRegisters[4] & 0x80000000)== 0 ) && ((DisplayCStateRegisters[5] & 0x80000000)== 0))
                {
                    DC5Status = true;
                }
                if (((DisplayCStateRegisters[0] & 0x00000002) == 2) && (DisplayCStateRegisters[1] == 0xffffffff) && (DisplayCStateRegisters[2] == 0xffffffff))
                {
                    DC6_DC9Status = true;
                }
            }
            Log.Message(true, "Get final values for DC3_DC5_Counter");
            DC5CounterFinal = GetRegisterValue("DC5_COUNTER", PIPE.NONE, PLANE.NONE, PORT.NONE);

            Log.Message("DC5_Counter_Initial = {0}, DC5_Counter_Final = {1}", DC5CounterInitial, DC5CounterFinal);

            if ((DC5CounterFinal != DC5CounterInitial) && (DC5Status))
            {
                Log.Success("The system entered DC5");
                outputDCState.Add(DCStateOutput.DC5);
            }
            if (DC6_DC9Status)
            {
                    Log.Success("The system entered DC9");
                    outputDCState.Add(DCStateOutput.DC9);              
            }
            return outputDCState;


        }
        protected new uint GetRegisterValue(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            uint resList = 0;
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Verbose("Offset being checked = {0} Bitmap {1}", reginfo.Offset, reginfo.Bitmap);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input.ToString("X"));
                else
                {
                    resList = Convert.ToUInt32(driverData.output);
                }
            }
            return resList;
        }
        protected List<uint> GetRegisterValueList(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            List<uint> resList = new List<uint>();
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;

            Log.Verbose("Event being checked = {0}", eventInfo.eventName);
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
            foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
            {
                Log.Verbose("Offset being checked = {0} Bitmap {1}", reginfo.Offset, reginfo.Bitmap);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input.ToString("X"));
                else
                {
                    uint bit = Convert.ToUInt32(driverData.output);
                    resList.Add(bit);
                }
            }
            return resList;
        }
      
   }
}
