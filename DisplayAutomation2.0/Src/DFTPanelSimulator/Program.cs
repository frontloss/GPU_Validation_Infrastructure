using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace Intel.VPG.Display.Automation
{
    public struct PortsCollection
    {
        public List<string> PortsList;
    }

    class Program
    {
        static void Main(string[] args)
        {
            DIVA_PORT_TYPE_CLR portType = DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR;
            bool IsPlugCall = true;
            bool IsLowPower = false;
            string EdidPath = default(string);
            string DpcdPath = default(string);

            Helper.EnableULT(true);
            Helper.EnableFeature(true, DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM);

            if ((args.Length == 1 && (args[0].Contains("/?") || args[0].Contains("help"))) || args.Length == 0)
            {
                Help();
                return;
            }
            else if ((args.Length == 1 && (args[0].ToLower() == "listallports")))
            {
                List<string> availablePorts = Helper.GetAvailablePorts();
                WriteToXML(availablePorts);

                availablePorts.ForEach(eachPort => Console.WriteLine(eachPort));
                return;
            }
            else if ((args.Length == 1 && (args[0].ToLower() == "listfreeports")))
            {
                List<string> availablePorts = Helper.GetFreePorts();
                WriteToXML(availablePorts);

                availablePorts.ForEach(eachPort => Console.WriteLine(eachPort));
                return;
            }
            else if (args.Length < 2)
            {
                Console.WriteLine("Insufficient arguments passed.");
                Help();
                return;
            }

            if (args.Length >= 1)
            {
                if (args[0].ToLower().Equals("plug"))
                {
                    IsPlugCall = true;
                }
                else if (args[0].ToLower().Equals("unplug"))
                {
                    IsPlugCall = false;
                }
                else
                {
                    Console.WriteLine("Invalid Plug/unplug parameter specified.");
                    Help();
                    return;
                }
            }

            if (args.Length >= 2)
            {
                portType = ConvertToPort(args[1]);
                if (portType == DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR)
                {
                    Console.WriteLine("Invalid PortType {0} passed.", args[1]);
                    Help();
                    return;
                }
            }

            if (IsPlugCall == true)
            {
                if (args.Length >= 3)
                {
                    EdidPath = args[2];
                    if (!File.Exists(EdidPath))
                    {
                        Console.WriteLine("Invalid EdidPath {0}.", args[2]);
                        Help();
                        return;
                    }
                }

                if (args.Length >= 4 && Helper.IsDP(portType))
                {
                    DpcdPath = args[3];
                    if (!File.Exists(DpcdPath))
                    {
                        Console.WriteLine("Invalid DpcdPath {0}.", args[3]);
                        Help();
                        return;
                    }
                }
            }

            foreach (string st in args)
            {
                if (st.ToLower().Equals("lowpower"))
                    IsLowPower = true;
            }

            DIVA_DISPLAY_DETAILS_ARGS_CLR displayDetails = Helper.GetDisplayDetailsFromPort(portType);

            if (displayDetails.PortType == DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR)
            {
                Console.WriteLine("Unable to find free port.");
            }
            else
            {
                if (portType == DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR && displayDetails.DisplayUID == 0)
                {
                    displayDetails.DisplayUID = 0x40F07;
                }

                bool status = Helper.ULT_FW_PlugDisplay(IsPlugCall, portType, displayDetails.DisplayUID, EdidPath, DpcdPath, IsLowPower);

                if (status)
                {
                    Console.WriteLine("{0} of {1} is successful.", args[0], args[1]);
                }
                else
                {

                    Console.WriteLine("{0} of {1} is Not successful.", args[0], args[1]);
                }
            }
        }

        private static void WriteToXML(List<string> Ports)
        {
            XmlSerializer sxml = null;
            XmlTextWriter writer = null;
            PortsCollection collection = new PortsCollection();
            collection.PortsList = new List<string>();

            collection.PortsList.AddRange(Ports);

            writer = new XmlTextWriter("PortsList.xml", null);
            writer.Formatting = Formatting.Indented;
            writer.Indentation = 4;
            writer.WriteStartDocument();

            sxml = new XmlSerializer(collection.GetType());
            sxml.Serialize(writer, collection);
            writer.Flush();
            writer.Close();
        }

        private static DIVA_PORT_TYPE_CLR ConvertToPort(string connecterInfo)
        {
            DIVA_PORT_TYPE_CLR portType = DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR;
            switch(connecterInfo.ToUpper())
            {
                case "DP_A":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR;
                    break;

                case "DP_B":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTDPB_PORT_CLR;
                    break;
                case "DP_C":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTDPC_PORT_CLR;
                    break;
                case "DP_D":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTDPD_PORT_CLR;
                    break;
                case "DP_E":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTDPE_PORT_CLR;
                    break;
                case "DP_F":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTDPF_PORT_CLR;
                    break;
                case "HDMI_B":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_DVOB_PORT_CLR;
                    break;
                case "HDMI_C":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_DVOC_PORT_CLR;
                    break;
                case "HDMI_D":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_DVOD_PORT_CLR;
                    break;
                case "HDMI_E":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_DVOE_PORT_CLR;
                    break;
                case "HDMI_F":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_DVOF_PORT_CLR;
                    break;

                case "MIPI_A":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTMIPIA_PORT_CLR;
                    break;
                case "MIPI_C":
                    portType = DIVA_PORT_TYPE_CLR.DIVA_INTMIPIC_PORT_CLR;
                    break;
            }

            return portType;
        }

        private static void Help()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("#######################################################################################################################").Append(Environment.NewLine);
            sb.Append("#Version : 1.1").Append(Environment.NewLine);
            sb.Append("#Date : WW30_5").Append(Environment.NewLine).Append(Environment.NewLine);
            sb.Append("#..\\>DFTPanelSimulator.exe <ListAllPorts/ ListFreePorts>").Append(Environment.NewLine);
            sb.Append("#..\\>DFTPanelSimulator.exe <Plug/Unplug> <Port> <EDID_Path> <DPCD_Path> <LowPower>").Append(Environment.NewLine);
            sb.Append("#..\\>DFTPanelSimulator.exe Plug DP_B DP_3011.EDID DP_3011_DPCD.txt ").Append(Environment.NewLine);
            sb.Append(@"#..\\>DFTPanelSimulator.exe Plug HDMI_C C:\HDMI_Dell_3011.EDID LowPower").Append(Environment.NewLine);
            sb.Append(@"#..\\>DFTPanelSimulator.exe Unplug HDMI_C").Append(Environment.NewLine);
            sb.Append("#").Append(Environment.NewLine);
            sb.Append("#port = <Encoder_Type>_<DDI>(Info. obtained from cmd \"ListPorts\") -> DP_A .... DP_F, HDMI_B....HDMI_F, MIPI_A,MIPI_C").Append(Environment.NewLine);
            sb.Append("#EDID_File = sample.bin or sample.edid").Append(Environment.NewLine);
            sb.Append("#DPCD = sample.bin -> Required only for DP/EDP.").Append(Environment.NewLine);
            sb.Append("#LowPower = is Optional argument ").Append(Environment.NewLine);
            sb.Append("#Note : DP_A == eDP ").Append(Environment.NewLine);
            sb.Append("#######################################################################################################################").Append(Environment.NewLine);
            Console.WriteLine(sb.ToString());
            return;
        }
    }
}
