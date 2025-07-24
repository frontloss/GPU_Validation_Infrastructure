/*------------------------------------------------------------------------------------------------*
 *
 * @file     Program.cs
 * @brief    This file contains implementation of command line based tool for generating 
 *           combination of supported displays which fulfulls the DRAM BW restrictions and DBUF
 *           allocation requirements.
 *           Please refer the READ_ME.txt file for details on dependencies.
 *           E.g. command line: DRAM_BW.exe TigerLake
 * @author   Suraj Gaikwad
 *
 *-----------------------------------------------------------------------------------------------*/


using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using System.Xml;
using System.Xml.Linq;

namespace DRAM_BW_Check
{
    public enum RM_PIXELFORMAT
    {
        // IF ANY NEW FORMAT IS ADDED HERE, PLEASE UPDATE ALL THE BELOW MACORS.
        _8BPP_INDEXED = 0,
        B5G6R5X0,
        B8G8R8X8,
        R8G8B8X8,
        B10G10R10X2,
        R10G10B10X2,
        R10G10B10X2_XR_BIAS,
        R16G16B16X16F,
        YUV422_8,
        YUV422_10,
        YUV422_12,
        YUV422_16,
        YUV444_8,
        YUV444_10,
        YUV444_12,
        YUV444_16,
        NV12YUV420,
        P010YUV420,
        P012YUV420,
        P016YUV420,
        MAX_PIXELFORMAT,
        TRY_ALL_POSSIBLE = -1,

    };

    public enum RM_STATUS
    {
        // Start with Generic erro codes
        RM_UNSUCCESSFUL = unchecked((int)0x80000000),
        RM_NO_MEMORY,
        RM_INVALID_PARAM,
        RM_NULL_PARAM,
        RM_TIMEOUT,
        RM_BUFFER_TOO_SMALL,
        RM_BUFFER_OVERFLOW,
        RM_ERROR_UNKNOWN,
        RM_BUSY,
        RM_NOT_SUPPORTED,
        RM_INVALID_CONTEXT,

        // Rm functionality specific codes
        RM_FUNCTIONAL_RANGE_START = unchecked((int)0x90000000), // -2147483648
        RM_NUM_PLANE_EXCEEDS_LIMIT,
        RM_NUM_SCALARS_EXCEEDS_LIMIT,
        RM_INVALID_PIXEL_FORMAT,
        RM_INVALID_PLANE_INDEX,
        RM_ASYNC_FLIP_NOT_SUPPORTED,
        RM_ASYNC_FLIP_HW_RESTRICTION_NOT_MET,
        RM_ALPHA_BLEND_NOT_SUPPORTED,
        RM_SURF_WIDTH_HEIGHT_HW_RESTRICTION_NOT_MET,
        RM_SURF_SIZE_HW_RESTRICTION_NOT_MET,
        RM_AUX_SURF_HW_RESTRICTION_NOT_MET,
        RM_SURF_OFFSET_HW_RESTRICTION_NOT_MET,
        RM_VFLIP_NOT_SUPPORTED,
        RM_VFLIP_HW_RESTRICTION_NOT_MET,
        RM_HFLIP_NOT_SUPPORTED,
        RM_HFLIP_HW_RESTRICTION_NOT_MET,
        RM_ROTATION_NOT_SUPPORTED,
        RM_ROTATION_DISABLED_FOR_RGB_SW_POLICY,
        RM_ROTATION_HW_RESTRICTION_NOT_MET,
        RM_SCALE_NOT_SUPPORTED,
        RM_SCALE_HW_RESTRICTION_NOT_MET,
        RM_HIGH_Q_SCALE_NOT_SUPPORTED,
        RM_BILINEAR_SCALE_NOT_SUPPORTED,
        RM_HORZ_STRETCH_FACTOR_EXCEEDS_LIMIT,
        RM_HORZ_SHRINK_FACTOR_EXCEEDS_LIMIT,
        RM_VERT_STRETCH_FACTOR_EXCEEDS_LIMIT,
        RM_VERT_SHRINK_FACTOR_EXCEEDS_LIMIT,
        RM_HW_WA_RESTRICTION_NOT_MET,
        RM_COLOR_CONFIG_NOT_SUPPORTED,
        RM_WM_EXCEEDED_FIFO,
        RM_DBUF_EXCEEDED_PIPE_ALLOC,
        RM_PIPE_NOT_AVAILABLE,
        RM_BANDWIDTH_EXCEEDED,
        RM_CUS_HW_RESTRICTION_NOT_MET,
        RM_CUS_MAX_PLANE_SIZE_EXCEEDS_LIMIT,

        // All success cases goes here
        RM_SUCCESS = 0,
    }

    public partial class DRAM_BW
    {
        XElement ConfigFile = null;
        XElement TimingFile = null;
        IntPtr RmExpContext = IntPtr.Zero;
        List<String> ConfigList = new List<string>();
        String LastKnownGoodConfig = null;

        Boolean IsInterlaced = false;
        String XRes, YRes, RR = null;
        //String ResultText = null;
        String PlatformSelection, ConfigSelection = null;
        List<String> PlatformsList = new List<string>();
        List<String> ConfigsList = new List<string>();
        List<String> DisplayTimingsList = new List<string>();

        List<List<String>> DisplayCombinations = new List<List<string>>();


        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern IntPtr SetUpRMExport(UInt32 Platform);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS InitializeRMExport(IntPtr RmCtxt);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS CleanUpRMExport(IntPtr RmCtxt);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS UpdateMmioSimulationStore(IntPtr RmCtxt, UInt32 Offset, UInt32 Data);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS UpdatePcuMailBoxSimulationStore(IntPtr RmCtxt, UInt32 MailBoxCmd, UInt32 CmdParam1, UInt32 CmdParam2, UInt32 CmdData, UInt32 CmdData1, UInt32 ReadResult, UInt32 ReadResult2, UInt32 ResponseCode);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS RmExportAddDisplay(IntPtr RmCtxt, ref RM_EXP_TIMING_INFO TimingInfo, RM_EXP_USER_PREFERENCE Prefference);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS RmExportClearAllDisplays(IntPtr RmCtxt);
        [DllImport("RmExport.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern RM_STATUS RmExportGenerateTiming(UInt32 XRes, UInt32 YRes, UInt32 RRate, UInt32 IsInterLaced, ref RM_EXP_TIMING_INFO TimingInfo);


        [StructLayout(LayoutKind.Sequential)]
        public struct RM_EXP_TIMING_INFO
        {
            public UInt32 DotClockInHz;     // Pixel clock in Hz
            public UInt32 HTotal;           // Horizontal total in pixels
            public UInt32 HActive;          // Active in pixels
            public UInt32 HBlankStart;      // From start of active in pixels
            public UInt32 HBlankEnd;        // From start of active in pixels
            public UInt32 HSyncStart;       // From start of active in pixels
            public UInt32 HSyncEnd;         // From start of active in pixels
            public UInt32 HRefresh;         // Refresh Rate
            public UInt32 VTotal;           // Vertical total in lines
            public UInt32 VActive;          // Active lines
            public UInt32 VBlankStart;      // From start of active lines
            public UInt32 VBlankEnd;        // From start of active lines
            public UInt32 VSyncStart;       // From start of active lines
            public UInt32 VSyncEnd;         // From start of active lines
            public UInt32 VRoundedRR;       // Refresh Rate
            public byte IsInterlaced;       // 1 = Interlaced Mode
            public byte HSyncPolarity;      // 1 = H. Sync Polarity is Negative going pulse
            public byte VSyncPolarity;      // 1 = V. Sync Polarity is Negative going pulse
            public RM_EXP_TIMING_INFO(XElement Timing)
            {
                DotClockInHz = GetValueFromString(Timing.Element("Pixel_Clock").Value);
                HTotal = GetValueFromString(Timing.Element("H_Total").Value);
                HActive = GetValueFromString(Timing.Element("H_Active").Value);
                HBlankStart = GetValueFromString(Timing.Element("H_Blank_Start").Value);
                HBlankEnd = GetValueFromString(Timing.Element("H_BlankEnd").Value);
                HSyncStart = GetValueFromString(Timing.Element("H_SyncStart").Value);
                HSyncEnd = GetValueFromString(Timing.Element("H_SyncEnd").Value);
                HRefresh = GetValueFromString(Timing.Element("H_Frequency").Value);
                VTotal = GetValueFromString(Timing.Element("V_Total").Value);
                VActive = GetValueFromString(Timing.Element("V_Active").Value);
                VBlankStart = GetValueFromString(Timing.Element("V_Blank_Start").Value);
                VBlankEnd = GetValueFromString(Timing.Element("V_BlankEnd").Value);
                VSyncStart = GetValueFromString(Timing.Element("V_SyncStart").Value);
                VSyncEnd = GetValueFromString(Timing.Element("V_SyncEnd").Value);
                VRoundedRR = GetValueFromString(Timing.Element("Refresh_Rate").Value);
                IsInterlaced = Convert.ToByte(Timing.Element("IsInterlaced").Value);
                HSyncPolarity = 0;
                VSyncPolarity = 0;
            }
        }


        [StructLayout(LayoutKind.Sequential)]
        public struct RM_EXP_USER_PREFERENCE
        {
            public RM_PIXELFORMAT PixelFmt;
            public UInt32 NumPlanes;
        }


        public DRAM_BW()
        {
            try
            {
                // Load the configs from the xml
                ConfigFile = XElement.Load("PlatformConfig.xml");
                TimingFile = XElement.Load("Timings.xml");
                LoadPlatforms();
                LoadTimings();
            }
            catch (Exception Ex)
            {
                Console.WriteLine("Unable to load the config files...");
                return;
            }
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Get Value From String
        * Description      This function extracts integer value from string
        * @param[In]       Value String to extra interger value
        * @return          Return Integer value of string
        *---------------------------------------------------------------------------------------*/
        public static UInt32 GetValueFromString(string Value)
        {
            try
            {
                String UpperValue = Value.ToUpper();
                if (UpperValue.StartsWith("0X"))
                {
                    return Convert.ToUInt32(UpperValue, 16);
                }
                // Check if its a decimal value and treat it as base 10 number
                else if (Regex.IsMatch(UpperValue, @"^\d+"))
                {
                    return Convert.ToUInt32(UpperValue, 10);
                }
                else if (UpperValue.Equals("TRUE"))
                {
                    return 1;
                }
                else if (UpperValue.Equals("FALSE"))
                {
                    return 0;
                }
                else
                {
                    Debug.Assert(false, "Invalid conversion");
                }
            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
            }
            return 0;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Build Error Message
        * Description      This function builds error message from the RM_STATUS enum
        * @param[In]       Status RM_STATUS enum
        * @return          Return String of error message
        *---------------------------------------------------------------------------------------*/
        String BuildErrorMessage(RM_STATUS Status)
        {
            String Message;
            switch (Status)
            {
                case RM_STATUS.RM_BANDWIDTH_EXCEEDED:
                    Message = "DRAM Bandwith Exceeded";
                    break;
                case RM_STATUS.RM_DBUF_EXCEEDED_PIPE_ALLOC:
                    Message = "DBuf not Sufficient for the plane combination";
                    break;
                case RM_STATUS.RM_WM_EXCEEDED_FIFO:
                    Message = "DBuf not Sufficient for single plane itself";
                    break;
                case RM_STATUS.RM_PIPE_NOT_AVAILABLE:
                    Message = "Run out of Pipes. Check Max pipes supported by Platform";
                    break;
                case RM_STATUS.RM_SUCCESS:
                    Message = "Succeeded";
                    break;
                default:
                    Message = String.Format("Error Code {0}", Status);
                    break;
            }
            // Error code in Hex representation
            Message += String.Format(" : (0x{0:X})", Status);
            return Message;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Configure MMIO Simulation
        * Description      This function configures the MMIO simulation data to be used in 
        *                  calculations for validating topology
        * @param[In]       Config RAM Config  from the PlatformConfig.xml
        * @return          Return True if load successful; False otherwise
        *---------------------------------------------------------------------------------------*/
        Boolean ConfigureMmioSimulation(XElement Config)
        {
            Boolean IsInitialized = false;
            try
            {
                // Gather the verifcations required on thie trigger
                IEnumerable<XElement> Elementlist = from el in Config.Elements("SimulationData").Elements("MmioData") select el;

                if (Elementlist.Count() == 0)
                {
                    // Nothing to process. Return early
                    return false;
                }
                foreach (XElement MmioElmt in Elementlist)
                {
                    // e.Attribute("name").Value.ToString()
                    UInt32 Offset = GetValueFromString(MmioElmt.Attribute("Offset").Value);
                    UInt32 Data = GetValueFromString(MmioElmt.Attribute("Data").Value);
                    // Call the dll with the simulation value
                    UpdateMmioSimulationStore(RmExpContext, Offset, Data);
                }

            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
                return false;
            }
            return IsInitialized;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Configure PCU MailBox Simulation
        * Description      This function configures the PCU MailBox simulation data to be used in 
        *                  calculations for validating topology
        * @param[In]       Config RAM Config  from the PlatformConfig.xml
        * @return          Return True if load successful; False otherwise
        *---------------------------------------------------------------------------------------*/
        Boolean ConfigurePcuMailBoxSimulation(XElement Config)
        {
            Boolean IsInitialized = false;
            try
            {
                // Gather the verifcations required on thie trigger
                IEnumerable<XElement> Elementlist = from el in Config.Elements("SimulationData").Elements("PcuMailBoxData") select el;

                if (Elementlist.Count() == 0)
                {
                    // Nothing to process. Return early
                    return false;
                }
                foreach (XElement MmioElmt in Elementlist)
                {
                    UInt32 MailBoxCmd = GetValueFromString(MmioElmt.Attribute("MailBoxCmd").Value);
                    UInt32 CmdParam1 = GetValueFromString(MmioElmt.Attribute("CmdParam1").Value);
                    UInt32 CmdParam2 = GetValueFromString(MmioElmt.Attribute("CmdParam2").Value);
                    UInt32 CmdData = GetValueFromString(MmioElmt.Attribute("CmdData").Value);
                    UInt32 CmdData1 = GetValueFromString(MmioElmt.Attribute("CmdData1").Value);
                    UInt32 ReadResult = GetValueFromString(MmioElmt.Attribute("ReadResult").Value);
                    UInt32 ReadResult2 = GetValueFromString(MmioElmt.Attribute("ReadResult2").Value);
                    // Call the dll with the simulation value
                    UpdatePcuMailBoxSimulationStore(RmExpContext, MailBoxCmd, CmdParam1, CmdParam2, CmdData, CmdData1, ReadResult, ReadResult2, 0);
                }

            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
                return false;
            }
            return IsInitialized;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Load Timings
        * Description      This function parses the Timings.xml file and creates a list of 
        *                  supported Display Timings
        * @param[In]       void
        * @return          Return True if load successful; False otherwise
        *---------------------------------------------------------------------------------------*/
        Boolean LoadTimings()
        {
            Boolean IsInitialized = false;
            try
            {

                IEnumerable<XElement> PlatformList = from el in TimingFile.Elements("Timing") select el;
                foreach (XElement Platform in PlatformList)
                {
                    String TimingName = Platform.Element("Name").Value.ToString();
                    if (DisplayTimingsList.Contains(TimingName))
                    {
                        // Skipping the duplicate
                        continue;
                    }
                    DisplayTimingsList.Add(TimingName);
                    IsInitialized = true;
                }
            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
                return false;
            }

            return IsInitialized;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Load Platform
        * Description      This function parses the PlatformConfig.xml file and creates a list of 
        *                  supported platforms
        * @param[In]       void
        * @return          Return True if load successful; False otherwise
        *---------------------------------------------------------------------------------------*/
        Boolean LoadPlatforms()
        {
            Boolean IsInitialized = false;
            try
            {

                IEnumerable<XElement> PlatformList = from el in ConfigFile.Elements("Platform") select el;
                foreach (XElement Platform in PlatformList)
                {
                    String PlatformName = Platform.Element("Name").Value.ToString();
                    if (PlatformsList.Contains(PlatformName))
                    {
                        // Skipping the duplicate platform
                        continue;
                    }
                    PlatformsList.Add(PlatformName);
                    IsInitialized = true;
                }
            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
                return false;
            }
            return IsInitialized;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Setup Platform
        * Description      This function tries to setup the RmExport.dll and configure the MailBox 
        *                  register values from xml
        * @param[In]       PlatformName Platform Name
        * @param[In]       ConfigName RAM config details
        * @return          Return True if setup successful; False otherwise
        *---------------------------------------------------------------------------------------*/
        Boolean SetUpPlatform(String PlatformName, String ConfigName)
        {
            Boolean IsInitialized = false;
            
            RM_STATUS Status;
            try
            {
                // Cleanup any existing context
                if (IntPtr.Zero != RmExpContext)
                {
                    CleanUpRMExport(RmExpContext);
                }
                IEnumerable<XElement> PlatformList = from el in ConfigFile.Elements("Platform") where (string)el.Element("Name") == PlatformName select el;
                foreach (XElement Config in PlatformList)
                {
                    //RmExpContext = SetUpRMExport(6);
                    RmExpContext = SetUpRMExport(GetValueFromString(Config.Element("Enum").Value));
                    break;
                }
                // Set the Platform
                IEnumerable<XElement> ConfigList = from el in PlatformList.Elements("Config") where (string)el.Element("Name") == ConfigName select el;
                if (ConfigList.Count() > 1)
                {
                    Console.WriteLine("More than one config with same name !!!");
                }
                foreach (XElement Config in ConfigList)
                {
                    ConfigureMmioSimulation(Config);
                    ConfigurePcuMailBoxSimulation(Config);
                    break;
                }
                // Init the platform
                Status = InitializeRMExport(RmExpContext);
                
            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
                return false;
            }
            return IsInitialized;
        }
        
        
        /**---------------------------------------------------------------------------------------*
        * @brief           Add Display
        * Description      This function tries to add a new display to the supported displays list
        *                  and validates the new combination of displays
        * @param[In]       TimingSelection Display Timing to be checked and to be added to the 
        *                  supported displays list
        * @return          Return True if display is added and validated; False otherwise
        *---------------------------------------------------------------------------------------*/
        private Boolean AddDisplay(String TimingSelection)
        {
            Boolean status = false;

            Boolean IsValidTopology = false;
            RM_EXP_TIMING_INFO TimingInfo = new RM_EXP_TIMING_INFO();
            RM_EXP_USER_PREFERENCE Preference = new RM_EXP_USER_PREFERENCE();
            Preference.NumPlanes = 0;
            Preference.PixelFmt = RM_PIXELFORMAT.TRY_ALL_POSSIBLE;

            try
            {

                IEnumerable<XElement> TimingList = from el in TimingFile.Elements("Timing") where (string)el.Element("Name") == TimingSelection select el;
                if (TimingList.Count() > 1)
                {
                    Console.WriteLine("More than one Timing with same name !!!. Picking the first one");
                }

                foreach (XElement Timing in TimingList)
                {
                    TimingInfo = new RM_EXP_TIMING_INFO(Timing);

                    break;
                }
                
                RM_STATUS Status = RmExportAddDisplay(RmExpContext, ref TimingInfo, Preference);
                if (RM_STATUS.RM_SUCCESS != Status)
                {
                    Console.WriteLine("Failed to add the Display to the topology. {0}", BuildErrorMessage(Status));
                    return false;
                }
                else
                {
                    IsValidTopology = true;
                }
            }
            catch (Exception Ex)
            {
                Debug.Assert(false, Ex.Message);
                return false;
            }

            if (IsValidTopology)
            {
                status = true;
                // Show the result in the text block
                string Line;
                LastKnownGoodConfig = null;
                // Read the file and display it line by line.  
                StreamReader ReportFile = new StreamReader(@"RM_Report.txt");
                while ((Line = ReportFile.ReadLine()) != null)
                {
                    Line += "\n";
                    LastKnownGoodConfig += Line;
                }

                ReportFile.Close();
            }
            return status;
        }

        /**---------------------------------------------------------------------------------------*
        * @brief           Clear Displays
        * Description      This function clears the list of supported displays (Last known good config)
        *---------------------------------------------------------------------------------------*/
        private void ClearDisplays()
        {
            RmExportClearAllDisplays(RmExpContext);
            LastKnownGoodConfig = null;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Combination Repetition Util
        * Description      This function generates comabinations of Strings from array with repetition
        * @param[In]       chosen Temp array to track index of chosen element
        * @param[In]       arr List of string containing all the displays from Timings.xml
        * @param[In]       n Size of arr
        * @param[In]       r Size of combination required (Currently 4 displays only supported)
        * @return          Return void
        *---------------------------------------------------------------------------------------*/
        void CombinationRepetitionUtil(int[] chosen, List<String> arr, int index, int r, int start, int end)
        { 
            if (index == r)
            {
                List<String> temp = new List<string>();
                for (int i = 0; i < r; i++)
                {
                    temp.Add(arr[chosen[i]]);
                }
                // Update the DisplayCombinations
                DisplayCombinations.Add(temp);
                return;
            }

            // One by one choose all elements (without considering the fact whether element is already chosen or not)  
            // and recur  
            for (int i = start; i <= end; i++)
            {
                chosen[index] = i;
                CombinationRepetitionUtil(chosen, arr, index + 1, r, i, end);
            }
            return;
        }


        /**---------------------------------------------------------------------------------------*
        * @brief           Generate Displays Combination
        * Description      This function generates displays combination (with repetition)
        * @param[In]       arr List of string containing all the displays from Timings.xml
        * @param[In]       n Size of arr
        * @param[In]       r Size of combination required (Currently 4 displays only supported)
        * @return          Return String with Platform name mapping to PlatformConfig.xml
        *---------------------------------------------------------------------------------------*/
        void GenerateDisplaysCombination(List<String> arr, int n, int r)
        {
            // Allocate memory  
            int[] chosen = new int[r + 1];

            // Call the recursice function  
            CombinationRepetitionUtil(chosen, arr, 0, r, 0, n - 1);
        }


        /**--------------------------------------------------------------------------------------*
        * @brief           Parse Platform
        * Description      This function prase the command line argument to get the Platform name
        * @param[In]       args List of string containing the commandline arguments
        * @return          Return String with Platform name mapping to PlatformConfig.xml
        *---------------------------------------------------------------------------------------*/
        static String ParsePlatform(string[] args, List<String> platformslist)
        {
            if (platformslist.Contains(args[0]))
            {
                return args[0];
            }
            else
                return "";
            
        }


        /**--------------------------------------------------------------------------------------*
        * @brief           Get Config
        * Description      This function parse the PlatformConfig.XMl for the supported RAM 
        *                  configs and prompts the user t select one config out of that
        * @param[In]       platform List of string containing the commandline arguments
        * @return          Return String with Ram type mapping to PlatformConfig.xml
        *---------------------------------------------------------------------------------------*/
        String GetConfig(string platform)
        {
            String config = "";
            IEnumerable<XElement> ConfigList;
            IEnumerable<XElement> PlatformList = from el in ConfigFile.Elements("Platform") where (string)el.Element("Name") == platform select el;
            foreach (XElement Platform in PlatformList)
            {
                ConfigList = from el in Platform.Elements("Config") select el;

                foreach (XElement Config in ConfigList)
                {
                    String ConfigName = Config.Element("Name").Value.ToString();
                    if (ConfigsList.Contains(ConfigName))
                    {
                        // Skipping the duplicate platform
                        continue;
                    }
                    ConfigsList.Add(ConfigName);
                }
            }

            Console.WriteLine("\nSupported Configs for " + platform + " are :");

            for (int i = 0; i < ConfigsList.Count(); i++)
            {
                Console.WriteLine(i+1 + "\t"+ ConfigsList[i]);
            }

            Console.WriteLine("\nSelect the config: ");
            int input = Convert.ToInt32(Console.ReadLine());

            if((input<ConfigsList.Count()) && (input>0)) 
            {
                config = ConfigsList[input - 1].ToString();
            }

            return config;
        }


        /**--------------------------------------------------------------------------------------*
        * @brief           Main Function
        * Description      Main function of the code
        * @param[In]       args List of string containing the commandline arguments
        * @return          Return void
        *---------------------------------------------------------------------------------------*/
        static void Main(string[] args)
        {
            DRAM_BW BW_Check = new DRAM_BW();

            BW_Check.PlatformSelection = DRAM_BW.ParsePlatform(args, BW_Check.PlatformsList);

            if (BW_Check.PlatformSelection == "")
            {
                Console.WriteLine("Platform Not Supported. Please check the PlatformConfig.xml");
                return;
            }

            BW_Check.ConfigSelection = BW_Check.GetConfig(BW_Check.PlatformSelection);

            if (BW_Check.ConfigSelection == "")
            {
                Console.WriteLine("Config Not Supported. Please check the PlatformConfig.xml");
                return;
            }

            Console.WriteLine("Selected Platform: "+ BW_Check.PlatformSelection+"\t Selected Config: "+BW_Check.ConfigSelection);

            BW_Check.GenerateDisplaysCombination(BW_Check.DisplayTimingsList, BW_Check.DisplayTimingsList.Count, 4);

            BW_Check.SetUpPlatform(BW_Check.PlatformSelection, BW_Check.ConfigSelection);

            HashSet<String> SupportedDisp = new HashSet<string>();
            HashSet<String> GoodConfig = new HashSet<string>();
            foreach (List<String> displist in BW_Check.DisplayCombinations)
            {
                String temp = "";
                BW_Check.ClearDisplays();
                foreach (String disp in displist)
                {
                    Boolean status = false;

                    status = BW_Check.AddDisplay(disp);
                    Console.WriteLine(disp + "\t -> " + status);
                    if (status == false)
                    {
                        BW_Check.ClearDisplays();
                        Console.WriteLine("==========");
                        break;
                    }
                    temp = temp + disp + ", ";
                }
                Console.WriteLine("======---------======");

                String LastGoodConfig = "";
                string Line;

                StreamReader ReportFile = new StreamReader(@"RM_Report.txt");
                while ((Line = ReportFile.ReadLine()) != null)
                {
                    Line += "\n";
                    LastGoodConfig += Line;
                }

                GoodConfig.Add(LastGoodConfig);

                ReportFile.Close();

                if (temp != "")
                {
                    SupportedDisp.Add(temp);
                }

            }

            var path = @"SupportedConfigs.txt";
            var sw = new StreamWriter(path);

            foreach (String displist in GoodConfig)
            {
                sw.WriteLine(displist);
            }

            sw.Close();
        }
    }

}
