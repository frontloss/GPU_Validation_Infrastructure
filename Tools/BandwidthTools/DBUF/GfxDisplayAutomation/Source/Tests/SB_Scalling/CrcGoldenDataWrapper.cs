using System;
using System.IO;
using System.Collections.Generic;
using System.Xml;

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
    }

    public struct MasterGoldenDataCollection
    {
        public string display;
        public List<ModeCRC> GoldenCRC;
    }

    class CrcGoldenDataWrapper
    {
        static XmlSerializer sxml = null;
        static XmlTextWriter writer = null;
        string goldenDataFileName = default(string);

        static MasterGoldenDataCollection GD;

        public CrcGoldenDataWrapper(string platform, DisplayInfo dispInfo, OSType OS)
        {
            GD = new MasterGoldenDataCollection();

            //goldenDataFileName = "GoldenCRCsCollection\\" + platform + "_" + dispInfo.DisplayType + "_" + dispInfo.SerialNum;
            goldenDataFileName = platform + "_" + OS + "_" + dispInfo.DisplayType + "_" + dispInfo.SerialNum;

            goldenDataFileName += ".xml";
            LoadXMLData(platform, dispInfo);
        }

        private void LoadXMLData(string platform, DisplayInfo dispInfo)
        {
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
                GD.GoldenCRC = new List<ModeCRC>();
                GD.display = dispInfo.DisplayType.ToString();
            }
        }

        public void AddToXML(ModeCRC mode, DisplayInfo dispInfo)
        {
            if (!CheckDataIfAlreadyPresent(mode))
            {
                GD.GoldenCRC.Add(mode);

                Log.Verbose(String.Format("writing in to xml :Resolution:{0},Refresh rate:{1} Hz,CD:{2},Scaling:{3},HS:{4},VS:{5},Rotation:{6}",
                                                      mode.resolution, mode.refreshRate, mode.colorDepth, mode.scaling,
                                                      mode.customHorizontalScaling, mode.customVerticalScaling, mode.rotationAngle));
               
                writer = new XmlTextWriter(goldenDataFileName, null);
                writer.Formatting = Formatting.Indented;
                writer.Indentation = 4;
                writer.WriteStartDocument();

                sxml = new XmlSerializer(GD.GetType());
                sxml.Serialize(writer, GD);
                writer.Flush();
                writer.Close();
            }
        }

        public uint GetCRCFromFile(ModeCRC mode)
        {
            uint crc = 0;
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
                                                crc = map.CRC;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            return crc;
        }

        bool CheckDataIfAlreadyPresent(ModeCRC mode)
        {
            bool flag = false;
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

                                                flag = true;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            return flag;
        }

    }
}
