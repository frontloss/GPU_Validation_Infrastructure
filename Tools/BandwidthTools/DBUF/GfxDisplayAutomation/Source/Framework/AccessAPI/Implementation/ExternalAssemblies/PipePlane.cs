using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class PipePlane: FunctionalBase, IGetMethod,IParse
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
        const uint HSW_Port_F = 50000000;
        const string VLV_Pipe_A = "80000000";
        const string VLV_Pipe_B = "C0000000";

        public object GetMethod(object argMessage)
        {
            bool result = false;
            PIPE pipe = PIPE.NONE;
            PLANE plane=PLANE.NONE;
            PipePlaneParams pipePlane = argMessage as PipePlaneParams;
            DisplayType display = pipePlane.DisplayType;
            Platform currentPlatform = base.MachineInfo.PlatformDetails.Platform;
            DisplayInfo currentDisplayInfo=base.EnumeratedDisplays.Where(dI => dI.DisplayType == display).FirstOrDefault();

            if ((currentDisplayInfo.Port == PORT.NONE) & (!(DisplayExtensions.GetDisplayType(pipePlane.DisplayType) == DisplayType.WIGIG_DP)))
            {
                Log.Fail("Port for displayType {0} is {1}", display, currentDisplayInfo.Port);
                return false;
            }
            else
            {
                display = DisplayExtensions.GetDisplayType(display);
                result = GetPipe(currentPlatform, display, currentDisplayInfo.Port, ref pipe);
                if (result)
                    pipePlane.Pipe = pipe;

                result = GetPlane(currentPlatform, display, pipe, ref plane);
                if (result)
                    pipePlane.Plane = plane;
            }
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
                case Platform.HSW:
                case Platform.BDW:              
                case Platform.CNL:
                case Platform.SKL:
                case Platform.BXT:
                case Platform.KBL:
                case Platform.GLK:
                case Platform.ICL:
                    result = GetPipeforHSW_Plus(display, port, ref pipe);
                    break;
                case Platform.VLV:
                    result = GetPipeForVLV(display, port, ref pipe);
                    break;
                case Platform.CHV:
                    result = GetPipeForCHV(display, port, ref pipe);
                    break;
                default: Log.Fail("Wrong platform Passed: {0}", currentPlatform);
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
                Log.Verbose(String.Format("Using transcoder registers to find pipe"));

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
                Log.Message(String.Format("Display {0} driven by {1}", displayType, pipe.ToString()));
            else
                Log.Fail(string.Format("Unable to fetch pipe for display {0}", displayType));

            return result;
        }
        private bool GetPipeForCHV(DisplayType displayType, PORT port, ref PIPE pipe)
        {
            bool result = false;
            String currentValue = "";

            string CHV_Pipe_A = "";
            string CHV_Pipe_B ="";
            string CHV_Pipe_C ="";

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

            RegisterInf pipeRegister = FetchRegisters(displayType + "_PIPE_SELECT", PIPE.NONE, PLANE.NONE, port)[0];

            if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
            {
                if (displayType == DisplayType.MIPI)
                {
                    if (currentValue == "80000000")
                    {
                        if (port == PORT.PORTA)
                        {
                            CHV_Pipe_A = "80000000";
                        }
                        else
                        {
                            CHV_Pipe_B = "80000000";
                        }
                    }
                    else
                    {
                        CHV_Pipe_A = "80000001";
                        CHV_Pipe_B = "80000002";
                    }
                }
             
                if (currentValue == CHV_Pipe_A)
                {
                    pipe = PIPE.PIPE_A;
                    result = true;
                }
                else if (currentValue == CHV_Pipe_B)
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
                    Log.Alert("cannot find match for {0} with value {1}",displayType , currentValue);
                }
            }
            if (result)
                Log.Message(String.Format("Display {0} driven by {1}", displayType, pipe.ToString()));
            else
                Log.Fail(string.Format("Unable to fetch pipe for display {0}", displayType));

            return result;
        }
        private bool GetPipeForVLV(DisplayType displayType, PORT port, ref PIPE pipe)//added for VLV
        {
            bool result = false;
            String currentValue = "";

            string pipeA= VLV_Pipe_A;
            string pipeB = VLV_Pipe_B;

            RegisterInf pipeRegister = FetchRegisters(displayType + "_PIPE_SELECT", PIPE.NONE, PLANE.NONE, port)[0];
           
            if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
            {
                if (displayType == DisplayType.MIPI)
                {
                    if (currentValue == "80000000")
                    {
                        if (port == PORT.PORTA)
                        {
                             pipeA= "80000000";
                        }
                        else
                        {
                            pipeB = "80000000";
                        }
                    }
                    else
                    {
                        pipeA = "80000001";
                        pipeB = "80000002";
                    }
                }
             
                Log.Verbose("Regsiter offset: {0} Bitmap:{1} Value:{2}",pipeRegister.Offset,pipeRegister.Bitmap,currentValue);
                if (currentValue == pipeB)
                {
                    pipe = PIPE.PIPE_B;
                    result = true;
                }
                else if (currentValue == pipeA)
                {
                    pipe = PIPE.PIPE_A;
                    result = true;
                }
            }
            if (result)
                Log.Message(String.Format("Display {0} driven by {1}", displayType, pipe.ToString()));
            else
                Log.Fail(string.Format("Unable to fetch pipe for display {0}", displayType));
           
            return result;
        }

        private bool GetPipeforHSW_Plus(DisplayType display, PORT port, ref PIPE pipe)
        {
            String currentValue = "";
            bool result = false;

            if (display == DisplayType.EDP && port==PORT.PORTA)
            {                
                    pipe = PIPE.PIPE_EDP;
                    return true;                
            }

            uint portValue = GetPortValue(Platform.HSW, port);
            foreach(PIPE tempPipe in Enum.GetValues(typeof(PIPE)))
            {
                if(tempPipe==PIPE.NONE)
                    continue;

                if (DisplayExtensions.GetDisplayType(display) == DisplayType.WIGIG_DP)
                {
                    if (tempPipe == PIPE.PIPE_EDP)
                        continue;
                    if ((VerifyRegister(display.ToString() +"_Transcoder_CTL_Pipe_Select", tempPipe, PLANE.NONE, PORT.NONE)))
                    {
                        result = true;
                    }
                }
                else
                {
                    RegisterInf pipeRegister = FetchRegisters("PIPE_SELECT", tempPipe, PLANE.NONE, PORT.NONE)[0];
                    if (GetBitMappedValue(pipeRegister.Offset, pipeRegister.Bitmap, ref currentValue))
                    {
                        if (Convert.ToUInt32(currentValue) == portValue)
                        {
                            result = true;
                        }
                    }
                }
                if (result)
                {
                    pipe = tempPipe;
                    break;
                }
            }

            if (result)
                Log.Message(String.Format("Display {0} driven by {1}", display, pipe.ToString()));
            else
                Log.Fail(string.Format("Unable to fetch pipe for display {0}", display));
           
            return result;
        }
       
        private bool GetPlane(Platform platform, DisplayType display, PIPE pipe, ref PLANE plane)
        {
            String currentValue = "";
            bool result = false;

            if (pipe != PIPE.PIPE_EDP)
            {
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
                        Log.Fail(string.Format("Invalid pipe value {0} passed for the display {1}", pipe, display));
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
                Log.Message(String.Format("Display {0} driven by {1}", display, plane));
            else
                Log.Fail(string.Format("Unable to fetch plane for display {0}", display));

            return result;
        }

        public List<RegisterInf> FetchRegisters(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors:{1},{2},{3}", registerEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);

            returnEventInfo.listRegisters.ForEach(cur =>
                {
                    Log.Message("Offset: 0x{0}, Bitmap: 0x{1}",cur.Offset, cur.Bitmap);
                });
            return returnEventInfo.listRegisters;
        }

        private uint GetPortValue(Platform platform,PORT port)
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
                else if (port == PORT.PORTF)
                    portValue = HSW_Port_F;
            }
            return portValue;
        }

        public bool GetBitMappedValue(String registerOffset, String bitmap, ref String currentValue)
        {
            uint regValue = 0;
            DriverEscape driverEscape = new DriverEscape();
            DriverEscapeData<uint, uint> registerData = new DriverEscapeData<uint, uint>();
            registerData.input=Convert.ToUInt32(registerOffset, 16);

            if (driverEscape.ParseRegisterRead(registerData))
            {
                regValue =registerData.output & Convert.ToUInt32(bitmap, 16);
                currentValue = regValue.ToString("X");
                Log.Verbose("Offset:{0}, bitmap:{1}, Value:{2}, Value after Bitmap:{3}", registerOffset, bitmap, registerData.output.ToString("X"), currentValue);
                return true;
            }
            else
            {
                Log.Fail("Register read failed");
                return false;
            }
        }
        
         [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" }, Comment = "Gets the Pipe and Plane information for a display")]
        public void Parse(string[] args)
        {
            if (args.Length == 2 && args[0].ToLower().Contains("get"))
            {
                DisplayType display = (DisplayType)Enum.Parse(typeof(DisplayType), args[1], true);
                PipePlaneParams pipePlaneParams = new PipePlaneParams(display);
                GetMethod(pipePlaneParams);
                Log.Message("For {0}=> Pipe={1},Plane={2}", display, pipePlaneParams.Pipe, pipePlaneParams.Plane);
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe PipePlane get DisplayType").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe PipePlane get DP");
            Log.Message(sb.ToString());
        }
        private bool VerifyRegister(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors:{1},{2},{3}", registerEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);
            return returnEventInfo.RegistersMatched;
        }
        
    }
}
