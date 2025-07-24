using System;
using System.IO;
using System.Collections.Generic;
using System.Xml;
using System.Linq;
using System.Xml.Serialization;
using System.Runtime.InteropServices;


namespace Intel.VPG.Display.Automation
{
    public struct ModeCRC
    {
        public string resolution;
        public uint refreshRate;
        public uint IsInterlaced;
        public uint colorDepth;
        public uint rotationAngle;
        public string scaling;
        public double customHorizontalScaling;
        public double customVerticalScaling;
        public uint CRC;
        public uint PipeCRC;
        public bool HDREnable;
    }

    public struct MasterGoldenDataCollection
    {
        public string display;
        public List<ModeCRC> GoldenCRC;
    }

    internal class CrcGoldenData : FunctionalBase, IGetMethod
    {
        private bool LoadXMLData(CrcGoldenDataArgs crcGoldenDataArgs, ref MasterGoldenDataCollection GD)
        {
            bool status=true;
 			string fileName ,goldenDataFileName ;
           
			DisplayInfo displayInfo = crcGoldenDataArgs.displayInfo;
            string stPlatform = base.MachineInfo.PlatformDetails.Platform.ToString();
            if (crcGoldenDataArgs.IsHDRContent == true)
               fileName = stPlatform + "_" + base.MachineInfo.OS.Type + "_" + displayInfo.DisplayType + "_" + displayInfo.SerialNum + "_HDR" + ".xml";
            else
               fileName = stPlatform + "_" + base.MachineInfo.OS.Type + "_" + displayInfo.DisplayType + "_" + displayInfo.SerialNum + ".xml";
           
            if (crcGoldenDataArgs.IsPipeCRC)
                fileName = "PIPE_" + fileName;
            else
                fileName = "PORT_" + fileName;

            goldenDataFileName = base.AppSettings.GoldenCRCPath + "\\GoldenCRCsCollection\\" + fileName;


      
            Log.Verbose("Loading XML from {0}", goldenDataFileName);
            if (File.Exists(goldenDataFileName))
            {
                TextReader reader = new StreamReader(goldenDataFileName);
                XmlSerializer serializer = new XmlSerializer(typeof(MasterGoldenDataCollection));
                GD = (MasterGoldenDataCollection)serializer.Deserialize(reader);
                reader.Close();
            }
            else
            {
                status = false; 
            }
            return status;
        }

        public bool GetCRCFromFile(CrcGoldenDataArgs crcGoldenDataArgs, ref uint goldenCRC)
        {
            bool status = false;
            goldenCRC = 0;
            MasterGoldenDataCollection GD = default(MasterGoldenDataCollection);

                if (LoadXMLData(crcGoldenDataArgs, ref GD)!=true)
                return false;

                ModeCRC mode = ConvertToCRCMode(crcGoldenDataArgs);
            
            foreach (ModeCRC map in GD.GoldenCRC)
            {
                if (map.resolution.Equals(mode.resolution))
                {
                    if (map.refreshRate == mode.refreshRate)
                    {
                        if (map.IsInterlaced == mode.IsInterlaced)
                        {
                            if (map.colorDepth.Equals(mode.colorDepth))
                            {
                                if (map.rotationAngle.Equals(mode.rotationAngle))
                                {
                                    if (map.scaling.Equals(mode.scaling))
                                    {
                                        if (map.customHorizontalScaling == mode.customHorizontalScaling)
                                        {
                                            if (map.customVerticalScaling == mode.customVerticalScaling)
                                            {
                                                if (map.HDREnable == mode.HDREnable)
                                                {
                                                   
                                                    goldenCRC = map.CRC;
                                                    status = true;
                                                    break;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            return status;
        }

        private ModeCRC ConvertToCRCMode(CrcGoldenDataArgs crcGoldenDataArgs)
        {
            DisplayMode displayMode = crcGoldenDataArgs.displayMode;
            ModeCRC modeCRC = new ModeCRC();

            modeCRC.resolution = displayMode.HzRes + "x" + displayMode.VtRes;
            modeCRC.refreshRate = displayMode.RR;
            modeCRC.IsInterlaced = displayMode.InterlacedFlag;
            modeCRC.colorDepth = displayMode.Bpp;
            modeCRC.scaling = ((ScalingOptions)displayMode.ScalingOptions.First()).ToString();
            modeCRC.customHorizontalScaling = 0;
            modeCRC.customVerticalScaling = 0;
            modeCRC.HDREnable = crcGoldenDataArgs.IsHDREnable;

            return modeCRC;
        }
        public object GetMethod(object argMessage)
        {
            uint tempCRC = 0;
            CrcGoldenDataArgs crcGoldenDataArgs = argMessage as CrcGoldenDataArgs;

            crcGoldenDataArgs.IsCRCPresent = GetCRCFromFile(crcGoldenDataArgs,ref tempCRC);

            crcGoldenDataArgs.CRCValue = tempCRC;
            return crcGoldenDataArgs;
        }
    }
}
