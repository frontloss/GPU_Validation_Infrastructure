using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AudioEndpointVerification
{
    class PipePlane
    {
        const uint CPT_TRANSCODER_A_VALUE = 0;
        const uint CPT_TRANSCODER_B_VALUE = 20000000;
        const uint CPT_TRANSCODER_C_VALUE = 40000000;

        const uint IVB_DP_PORT_B = 0;
        const uint IVB_DP_PORT_C = 20000000;
        const uint IVB_DP_PORT_D = 40000000;

        const uint HSW_Port_B = 10000000;
        const uint HSW_Port_C = 20000000;
        const uint HSW_Port_D = 30000000;
        const uint HSW_Port_E = 40000000;
        const string VLV_Pipe_A = "80000000";
        const string VLV_Pipe_B = "C0000000";

        public object GetMethod(Platform argPlatform, DisplayType argDisplay, PORT argPort)
        {
            bool result = false;
            PIPE pipe = PIPE.NONE;
            PLANE plane = PLANE.NONE;
            PipePlaneParams pipePlane = new PipePlaneParams(argDisplay);
            result = GetPipe(argPlatform, argDisplay, argPort, ref pipe);
            if (result)
                pipePlane.Pipe = pipe;

            result = GetPlane(argPlatform, argDisplay, pipe, ref plane);
            if (result)
                pipePlane.Plane = plane;
            return pipePlane;
        }

        private bool GetPipe(Platform currentPlatform, DisplayType display, PORT port, ref PIPE pipe)
        {
            bool result = false;

            switch (currentPlatform)
            {
                case Platform.IVBM:
                    result = GetPipeByDefault(currentPlatform, display, port, ref pipe);
                    break;
                case Platform.HSWDT:
                case Platform.HSWM:
                case Platform.HSWU:
                case Platform.BDW:
                case Platform.SKL:
                case Platform.CNL:
                    result = GetPipeforHSW_Plus(display, port, ref pipe);
                    break;
                case Platform.VLV:
                    result = GetPipeForVLV(display, port, ref pipe);
                    break;
                case Platform.CHV:
                    result = GetPipeForCHV(display, port, ref pipe);
                    break;
                default: Console.WriteLine("Wrong platform Passed: {0}", currentPlatform);
                    break;
            }

            return result;
        }

        private bool GetPipeByDefault(Platform platform, DisplayType displayType, PORT port, ref PIPE pipe)
        {
            bool result = false;
            String currentValue = "";
            String registerName = displayType.ToString() + "_" + "ENABLED";

            if (displayType == DisplayType.DP)
            {
                Console.WriteLine(String.Format("Using transcoder registers to find pipe"));

                uint portValue = GetPortValue(platform, port);
                foreach (PIPE tempPipe in Enum.GetValues(typeof(PIPE)))
                {
                    if (tempPipe == PIPE.NONE)
                        continue;

                    RegisterInf pipeRegister = FetchRegisters(registerName, tempPipe, PLANE.NONE, PORT.NONE)[0];
                    if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
                    {
                        if (Convert.ToUInt32(currentValue) == portValue)
                        {
                            pipe = tempPipe;
                            result = true;
                            break;
                        }
                    }
                }
            }
            else
            {
                RegisterInf portRegister = FetchRegisters(registerName, PIPE.NONE, PLANE.NONE, port)[0];
                if (GetBitMappedValue(portRegister.Offset, portRegister.Bitmap, ref currentValue))
                {
                    if (Convert.ToUInt32(currentValue) == CPT_TRANSCODER_A_VALUE)
                    {
                        pipe = PIPE.PIPE_A;
                        result = true;
                    }
                    else if (Convert.ToUInt32(currentValue) == CPT_TRANSCODER_B_VALUE)
                    {
                        pipe = PIPE.PIPE_B;
                        result = true;
                    }
                    else if (Convert.ToUInt32(currentValue) == CPT_TRANSCODER_C_VALUE)
                    {
                        pipe = PIPE.PIPE_C;
                        result = true;
                    }
                }
            }

            if (result)
                Console.WriteLine(String.Format("Display {0} driven by {1}", displayType, pipe.ToString()));
            else
                Console.WriteLine(string.Format("Unable to fetch pipe for display {0}", displayType));

            return result;
        }
        private bool GetPipeForCHV(DisplayType displayType, PORT port, ref PIPE pipe)
        {
            bool result = false;
            String currentValue = "";

            string CHV_Pipe_A = "";
            string CHV_Pipe_B = "";
            string CHV_Pipe_C = "";

            if (displayType == DisplayType.HDMI)
            {
                CHV_Pipe_A = "80000000";
                CHV_Pipe_B = "81000000";
                CHV_Pipe_C = "82000000";
            }
            else if (displayType == DisplayType.EDP)
            {
                CHV_Pipe_B = "80000000";
            }
            else if (displayType == DisplayType.DP)
            {
                CHV_Pipe_A = "80000000";
                CHV_Pipe_B = "80010000";
                CHV_Pipe_C = "80020000";
            }
            else if (displayType == DisplayType.MIPI)
            {
                CHV_Pipe_A = "80000000";
            }
            RegisterInf pipeRegister = FetchRegisters(displayType + "_PIPE_SELECT", PIPE.NONE, PLANE.NONE, port)[0];

            if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
            {
                //uint value = Convert.ToUInt32(currentValue, 16);              
                if (currentValue == CHV_Pipe_A)
                {
                    pipe = PIPE.PIPE_A;
                    result = true;
                }
                if (currentValue == CHV_Pipe_B)
                {
                    pipe = PIPE.PIPE_B;
                    result = true;
                }
                else if (currentValue == CHV_Pipe_C)
                {
                    pipe = PIPE.PIPE_C;
                    result = true;
                }
                else
                {
                    Console.WriteLine("cannot find match for {0} with value {1}", displayType, currentValue);
                }
            }
            if (result)
                Console.WriteLine(String.Format("Display {0} driven by {1}", displayType, pipe.ToString()));
            else
                Console.WriteLine(string.Format("Unable to fetch pipe for display {0}", displayType));

            return result;
        }
        private bool GetPipeForVLV(DisplayType displayType, PORT port, ref PIPE pipe)//added for VLV
        {
            bool result = false;
            String currentValue = "";

            RegisterInf pipeRegister = FetchRegisters(displayType + "_PIPE_SELECT", PIPE.NONE, PLANE.NONE, port)[0];

            if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
            {
                if (currentValue == VLV_Pipe_B)
                {
                    pipe = PIPE.PIPE_B;
                    result = true;
                }
                else if (currentValue == VLV_Pipe_A)
                {
                    pipe = PIPE.PIPE_A;
                    result = true;
                }
            }
            if (result)
                Console.WriteLine(String.Format("Display {0} driven by {1}", displayType, pipe.ToString()));
            else
                Console.WriteLine(string.Format("Unable to fetch pipe for display {0}", displayType));

            return result;
        }

        private bool GetPipeforHSW_Plus(DisplayType display, PORT port, ref PIPE pipe)
        {
            String currentValue = "";
            bool result = false;

            if (display == DisplayType.EDP && port == PORT.PORTA)
            {
                pipe = PIPE.PIPE_EDP;
                return true;
            }

            uint portValue = GetPortValue(Platform.HSWM, port);
            foreach (PIPE tempPipe in Enum.GetValues(typeof(PIPE)))
            {
                if (tempPipe == PIPE.NONE)
                    continue;

                RegisterInf pipeRegister = FetchRegisters("PIPE_SELECT", tempPipe, PLANE.NONE, PORT.NONE)[0];
                if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
                {
                    if (Convert.ToUInt32(currentValue) == portValue)
                    {
                        pipe = tempPipe;
                        result = true;
                        break;
                    }
                }
            }

            if (result)
                Console.WriteLine(String.Format("Display {0} driven by {1}", display, pipe.ToString()));
            else
                Console.WriteLine(string.Format("Unable to fetch pipe for display {0}", display));

            return result;
        }
        private bool GetPlane(Platform platform, DisplayType display, PIPE pipe, ref PLANE plane)
        {
            String currentValue = "";
            bool result = false;

            if (!(pipe == PIPE.PIPE_EDP && (GetPlatformInfo() == "HSW" || GetPlatformInfo() == "BDW" || GetPlatformInfo() == "SKL" || GetPlatformInfo() == "CNL")))
            {
                //plane = (PLANE)Enum.Parse(typeof(PLANE), "PLANE_" + pipe.ToString().Substring(5));
                switch (pipe)
                {
                    case PIPE.PIPE_A:
                        plane = PLANE.PLANE_A;
                        break;
                    case PIPE.PIPE_B:
                        plane = PLANE.PLANE_B;
                        break;
                    case PIPE.PIPE_C:
                        plane = PLANE.PLANE_C;
                        break;
                    default:
                        Console.WriteLine(string.Format("Invalid pipe value {0} passed for the display {1}", pipe, display));
                        break;
                }

                return true;
            }

            foreach (PLANE tempPlane in Enum.GetValues(typeof(PLANE)))
            {
                if (tempPlane == PLANE.NONE)
                    continue;

                RegisterInf pipeRegister = FetchRegisters("PLANE_SELECT", PIPE.NONE, tempPlane, PORT.NONE)[0];

                if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
                {
                    if (String.Equals(pipeRegister.Value, currentValue))
                    {
                        plane = tempPlane;
                        result = true;
                        break;
                    }
                }
            }

            if (result)
                Console.WriteLine(String.Format("Display {0} driven by {1}", display, plane));
            else
                Console.WriteLine(string.Format("Unable to fetch plane for display {0}", display));

            return result;
        }

        public DisplayType GetDisplayType(DisplayType display)
        {
            DisplayType displayType = DisplayType.None;
            switch (display)
            {
                case DisplayType.CRT:
                    displayType = DisplayType.CRT;
                    break;
                case DisplayType.DP:
                case DisplayType.DP_2:
                    displayType = DisplayType.DP;
                    break;
                case DisplayType.EDP:
                    displayType = DisplayType.EDP;
                    break;
                case DisplayType.MIPI:
                    displayType = DisplayType.MIPI;
                    break;
                case DisplayType.HDMI:
                case DisplayType.HDMI_2:
                    displayType = DisplayType.HDMI;
                    break;
                default:
                    break;
            }
            return displayType;
        }

        public List<RegisterInf> FetchRegisters(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = new EventRegisterInfo();
            Console.WriteLine("Fetching Registers for event:{0} with factors:{1},{2},{3}", registerEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            //base.CopyOver(eventRegisterInfo);
            //eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);

            return returnEventInfo.listRegisters;
        }

        private uint GetPortValue(Platform platform, PORT port)
        {
            uint portValue = 0;
            if (platform == Platform.IVBM)
            {
                if (port == PORT.PORTB)
                    portValue = IVB_DP_PORT_B;
                else if (port == PORT.PORTC)
                    portValue = IVB_DP_PORT_B;
                else if (port == PORT.PORTD)
                    portValue = IVB_DP_PORT_D;
            }
            else
            {
                if (port == PORT.PORTB)
                    portValue = HSW_Port_B;
                else if (port == PORT.PORTC)
                    portValue = HSW_Port_C;
                else if (port == PORT.PORTD)
                    portValue = HSW_Port_D;
                else if (port == PORT.PORTE)
                    portValue = HSW_Port_E;
            }
            return portValue;
        }

        public bool GetBitMappedValue(String registerOffset, String bitmap, ref String currentValue)
        {
            uint regValue = 0;
            DriverEscape driverEscape = new DriverEscape();
            DriverEscapeData<uint, uint> registerData = new DriverEscapeData<uint, uint>();
            registerData.input = Convert.ToUInt32(registerOffset, 16);

            if (driverEscape.ParseRegisterRead(registerData))
            {
                regValue = registerData.output & Convert.ToUInt32(bitmap, 16);
                currentValue = regValue.ToString("X");
                return true;
            }
            else
            {
                Console.WriteLine("Register read failed");
                return false;
            }
        }
        private string GetPlatformInfo()
        {
            string platform = "";
            switch (CommonExtension.PlatformID)
            {
                case "HSWM":
                case "HSWDT":
                case "HSWU":
                    platform = "HSW";
                    break;
                case "IVBM":
                    platform = "IVB";
                    break;
                case "BDW":
                    platform = "BDW";
                    break;
                case "VLV":
                    platform = "VLV";
                    break;
                case "SKL":
                    platform = "SKL";
                    break;
                case "CNL":
                    platform = "CNL";
                    break;
            }
            return platform;
        }
    }
}
