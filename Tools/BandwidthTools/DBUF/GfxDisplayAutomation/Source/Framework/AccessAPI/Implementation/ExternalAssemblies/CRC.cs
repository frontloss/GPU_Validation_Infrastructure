namespace Intel.VPG.Display.Automation
{    
    using System.Linq;
    using System.Collections.Generic;
    using System;
    using System.Text;

    internal class CRC : FunctionalBase, IGetMethod, IParse
    {
        public struct CrcOffset
        {
            public uint CRCControlRegister;
            public uint enableCRCValue;
            public uint disableCRCValue;
            public uint scrambleOffset;
            public uint scrambleValue;
            public uint CRCResult;
            
            public uint PipeCRCControlRegister;
            public uint enablePipeCRC;
            public uint disablePipeCRC;
            public uint PipeCRCResult;            
        };

        [ParseAttribute(InterfaceName = InterfaceType.IGetMethod, InterfaceData = new string[] { "DisplayType:DisplayType" }, Comment = "Gets the Port CRC for display")]
        public void Parse(string[] args)
        {
            if (args.Length == 2 && args[0].ToLower().Contains("get"))
            {
                DisplayType display = (DisplayType)Enum.Parse(typeof(DisplayType), args[1], true);
                CRCArgs crcargs=new CRCArgs();
                crcargs.displayType= display;

                GetMethod(crcargs);
                Log.Message("For {0}=> Port CRC={1}", display, crcargs.CRCValue);
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe CRC get DisplayType").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe CRC get DP");
            Log.Message(sb.ToString());
        }

        public object GetMethod(object argMessage)
        {
            uint reg_offset, reg_value = 0;
            bool isCRCDone = false;
            CRCArgs args = argMessage as CRCArgs;

            CrcOffset crcParams = new CrcOffset();
            PORT currentPort = base.EnumeratedDisplays.Where(dispInfo => dispInfo.DisplayType == args.displayType).First().Port;
            FindRegisterOffsets(args.displayType, currentPort, ref crcParams);

            if (args.ComputePipeCRC != true)
            {
                //Enable scramble register for DP
                if (args.displayType == DisplayType.DP || args.displayType == DisplayType.EDP)
                {
                    reg_offset = crcParams.scrambleOffset;
                    ReadRegister(reg_offset, ref reg_value);
                    Log.Verbose(String.Format(" Reading {0} Scramble register Offset: 0x{1}, Value: 0x{2} ", args.displayType, reg_offset.ToString("X"), reg_value.ToString("X")));
                    reg_value = reg_value | 0x1;
                    WriteRegister(reg_offset, reg_value);
                    Log.Verbose(String.Format(" Written {0} Scramble register Offset: 0x{2}, Value: 0x{2} ", args.displayType, reg_offset.ToString("X"), reg_value.ToString("X")));
                }

                #region commentedcode
                ////Disable PortCRC
                //reg_offset = crcParams.CRCControlRegister;
                //reg_value = crcParams.disableCRCValue;
                //WriteRegister(reg_offset, reg_value);
                //Log.Message(String.Format(" Reseting PORT CRC, Offset: {0}, Value: {1} ", reg_offset.ToString("X"), reg_value.ToString("X")));
                #endregion

                //enable CRC Control Register
                reg_offset = crcParams.CRCControlRegister;
                reg_value = crcParams.enableCRCValue;
                Log.Verbose(String.Format(" Enable PORT CRC, Offset: {0}, Value: {1} ", reg_offset.ToString("X"), reg_value.ToString("X")));
                WriteRegister(reg_offset, reg_value);

                for (int w = 0; w < 6; w++)
                {
                    //Wait for CRC Done bit to be 1. then read from CRC_RES register.
                    reg_offset = crcParams.CRCControlRegister;
                    ReadRegister(reg_offset, ref reg_value);
                    reg_value |= 0x1000000;
                    WriteRegister(reg_offset, reg_value);

                    isCRCDone = false;
                    for (int y = 0; y < 300; y++)
                    {
                        ReadRegister(reg_offset, ref reg_value);
                        //SimpleLogger.Debug(String.Format(" Checking CRC Done, Iteration {0}, Offset: {1}, Value: {2} ", y, reg_offset.ToString("X"), reg_value.ToString("X")));
                        if ((reg_value & 0x1000000) == 0x1000000)
                        {
                            isCRCDone = true;
                            Log.Verbose("CRC Done bit is 1");
                            break;
                        }
                    }
                    if (isCRCDone == true)
                    {
                        //Read from CRC_RES register.
                        reg_offset = crcParams.CRCResult;
                        ReadRegister(reg_offset, ref reg_value);
                        args.CRCValue = reg_value;
                    }
                    else
                    {
                        Log.Verbose("CRC Done bit not set to 1. Assigning 0 for CRCValue.");
                        args.CRCValue = 0;
                    }
                    Log.Verbose(String.Format(" Platform PORT CRC,  Offset: {0}, CRC_Result: {1} ", reg_offset.ToString("X"), reg_value.ToString("X")));
                }
            }

            #region ComputingPipeCRC
            if (args.ComputePipeCRC == true)
            {
                //enable Pipe CRC Control Register
                reg_offset = crcParams.PipeCRCControlRegister;
                reg_value = crcParams.enablePipeCRC;
                Log.Verbose(String.Format(" Enable PIPE CRC, Offset: {0}, Value: {1} ", reg_offset.ToString("X"), reg_value.ToString("X")));
                WriteRegister(reg_offset, reg_value);

                for (int w = 0; w < 6; w++)
                {
                    //Wait for CRC Done bit to be 1. then read from PIPE_CRC_RES register.
                    reg_offset = crcParams.PipeCRCControlRegister;
                    ReadRegister(reg_offset, ref reg_value);
                    reg_value |= 0x1000000;
                    WriteRegister(reg_offset, reg_value);

                    isCRCDone = false;
                    for (int y = 0; y < 300; y++)
                    {
                        ReadRegister(reg_offset, ref reg_value);
                        //SimpleLogger.Debug(String.Format(" Checking CRC Done, Iteration {0}, Offset: {1}, Value: {2} ", y, reg_offset.ToString("X"), reg_value.ToString("X")));
                        if ((reg_value & 0x1000000) == 0x1000000)
                        {
                            isCRCDone = true;
                            Log.Verbose("CRC Done bit is 1");
                            break;
                        }
                    }
                    if (isCRCDone == true)
                    {
                        //Read from CRC_RES register.
                        reg_offset = crcParams.PipeCRCResult;
                        ReadRegister(reg_offset, ref reg_value);
                        args.CRCValue = reg_value;
                    }
                    else
                    {
                        Log.Verbose("CRC Done bit not set to 1. Assigning 0 for PipeCRCValue.");
                        args.CRCValue = 0;
                    }
                    Log.Verbose(String.Format(" Pipe CRC,  Offset: {0}, CRC_Result: {1} ", reg_offset.ToString("X"), reg_value.ToString("X")));
                }
            }

            #endregion

            return args;
        }

        public bool ReadRegister(uint reg_offset, ref uint reg_value)
        {
            DriverEscape driverEscape = new DriverEscape();
            DriverEscapeData<uint, uint> registerData = new DriverEscapeData<uint, uint>();
            registerData.input = reg_offset;

            if (driverEscape.ParseRegisterRead(registerData))
            {
                reg_value = registerData.output;
            }
            else
            {
                Log.Fail("Register read failed offset:0x{0}", reg_offset);
                return false;
            }
            return true;
        }

        public void WriteRegister(uint reg_offset, uint reg_value)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = reg_offset;
            driverData.output = reg_value;

            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.DIVAMMIOWrite, driverData);
            DriverEscape escape = new DriverEscape();

            if (!escape.SetMethod(driverParams))
                Log.Abort("Failed to Write Register with offset: 0x{0}", driverData.input);
            else
                Log.Verbose("Offset:0x{0},  Data written:0x{1}", driverData.input.ToString("X"), driverData.output.ToString("X"));
        }
        public bool FindRegisterOffsets(DisplayType display,PORT port, ref CrcOffset offsetCRC)
        {

             uint displacement = 256 * ((uint) port -1);
             PipePlaneParams pipePlane = new PipePlaneParams(display);
             PipePlane pPlane = base.CreateInstance<PipePlane>(new PipePlane());
             pipePlane = (PipePlaneParams)pPlane.GetMethod(pipePlane);

             RegisterInf registerInfo = FetchRegisters("CRC_CTRL", PIPE.NONE, PLANE.NONE, PORT.NONE);
             offsetCRC.CRCControlRegister =Convert.ToUInt32(registerInfo.Offset,16)+displacement;
             offsetCRC.enableCRCValue = Convert.ToUInt32(registerInfo.Bitmap, 16);
             offsetCRC.disableCRCValue = 0;

             registerInfo = FetchRegisters("CRC_SCRAMBLE", PIPE.NONE, PLANE.NONE, PORT.NONE);
             offsetCRC.scrambleOffset = Convert.ToUInt32(registerInfo.Offset, 16) + displacement;
             offsetCRC.scrambleValue = Convert.ToUInt32(registerInfo.Bitmap, 16);

             registerInfo = FetchRegisters("CRC_RES", PIPE.NONE, PLANE.NONE, PORT.NONE);
             offsetCRC.CRCResult = Convert.ToUInt32(registerInfo.Offset, 16) + displacement;

            //Pipe CRC
             registerInfo = FetchRegisters("PIPE_CRC_CTRL", PIPE.NONE, pipePlane.Plane, PORT.NONE);
             offsetCRC.PipeCRCControlRegister = Convert.ToUInt32(registerInfo.Offset, 16);
             offsetCRC.enablePipeCRC = Convert.ToUInt32(registerInfo.Bitmap, 16);
             offsetCRC.disablePipeCRC = 0;

             registerInfo = FetchRegisters("PIPE_CRC_RES", PIPE.NONE, pipePlane.Plane, PORT.NONE);
             offsetCRC.PipeCRCResult = Convert.ToUInt32(registerInfo.Offset, 16);

            return true;
        }


        public RegisterInf FetchRegisters(string registerEvent, PIPE pipe, PLANE plane, PORT port)
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

            return returnEventInfo.listRegisters[0];
        }
    }
}