using System;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using System.Xml.Linq;
namespace Intel.VPG.Display.Automation
{
    class YTiling : FunctionalBase, IGetMethod
    {
        private bool _nv12Buf, _cursorEnabled;
        private uint _buffStart, _buffEnd;
        public bool CursorEnabled
        {
            get { return _cursorEnabled; }
            set { _cursorEnabled = value; }
        }
        public bool Nv12Buf
        {
            get { return _nv12Buf; }
            set { _nv12Buf = value; }
        }
        public uint BuffEnd
        {
            get { return _buffEnd; }
            set { _buffEnd = value; }
        }

        public uint BuffStart
        {
            get { return _buffStart; }
            set { _buffStart = value; }
        }
        private Dictionary<string, Dictionary<uint, string>> _featureMapper;
        public List<string> YTilingEvents
        {
            get
            {
                List<string> _yTilingEvents = new List<string>() { "PLANE_1_A", "PLANE_1_B", "PLANE_1_C", "PLANE_2_A", "PLANE_2_B", "PLANE_2_C", "PLANE_3_A", "PLANE_3_B", "PLANE_3_C" };
                return _yTilingEvents;
            }
        }
        public object GetMethod(object argMessage)
        {
            GetYTilingDataDFromXML();
            MMIORW mmioData = argMessage as MMIORW;
            Log.Message("the event is {0} in ytiling.cs", mmioData.FeatureName);
            DBufInfo dbuf = new DBufInfo();
            if (YTilingEvents.Contains(mmioData.FeatureName))
                dbuf = GetYTilingInfo(mmioData);
            return dbuf;
        }
        private string ReadMMIORW(string argOffset, bool argPrintRegValue)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = Convert.ToUInt32(argOffset, 16);
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            DriverEscape driverEscapeObj = new DriverEscape();
            bool status = driverEscapeObj.SetMethod(driverParams);
            string hexValue = driverData.output.ToString("X");
            Log.Message("The {0} : {1}", argOffset, hexValue);

            return hexValue;

            //Process regValue = CommonExtensions.StartProcess("MMIORW.exe", " r " + argOffset);//6C05C  70080           
            //string data = regValue.StandardOutput.ReadLine();  //Value:0x
            //if (argPrintRegValue)
            //    Log.Verbose("Reg {0} : {1}", argOffset, data);
            //data = data.Substring(8, (data.Length - 8));
            //return data;
        }
        private uint CompareRegValue(string argRegValue, string argBitmap)
        {
            uint regValue = Convert.ToUInt32(argRegValue, 16);
            uint bitmap = Convert.ToUInt32(argBitmap, 16);


            string regValueBinary = Convert.ToString(regValue, 2);
            while (regValueBinary.Count() < 32)
            {
                regValueBinary = "0" + regValueBinary;
            }

            string bitmapBinary = Convert.ToString(bitmap, 2);
            while (bitmapBinary.Count() < 32)
            {
                bitmapBinary = "0" + bitmapBinary;
            }

            int startIndex = bitmapBinary.IndexOf('1');
            int lastIndex = bitmapBinary.LastIndexOf('1');

            string value = regValueBinary.Substring(startIndex, lastIndex - startIndex + 1);
            return Convert.ToUInt32(value, 2);
            //  return regValue & bitmap;
        }
        protected DBufInfo GetYTilingInfo(MMIORW argMMIORW)
        {
            Log.Message(true, "{0}", argMMIORW.FeatureName);
            RegisterInf yTileEnable = argMMIORW.RegInfList.First();
            string yTileEnableValue = ReadMMIORW(yTileEnable.Offset, true);
            uint yTileEnableValueInt = CompareRegValue(yTileEnableValue, yTileEnable.Bitmap);
            RegisterInf regInf;
            DBufInfo dbuf = new DBufInfo();
            if (yTileEnableValueInt == 1)
            {
                dbuf.Enabled = true;
                Nv12Buf = false;
                regInf = argMMIORW.RegInfList.ElementAt(1);
                dbuf.SourcePixelFormat = GetYTileSource(regInf);
                regInf = argMMIORW.RegInfList.ElementAt(2);
                dbuf.TileFormat = GetYTileFormat(regInf);
                regInf = argMMIORW.RegInfList.ElementAt(3);
                dbuf.RotationAngle = GetRotation(regInf);

                BuffEnd = 0;
                regInf = argMMIORW.RegInfList.ElementAt(4);
                GetBuffEnd(regInf);
                BuffStart = 0;
                regInf = argMMIORW.RegInfList.ElementAt(5);
                GetBuffStart(regInf);
                Log.Message("\t PLANE_BUF_CFG start block: {0} end block: {1} Total Block Count: {2},", BuffStart, BuffEnd, BuffEnd - BuffStart + 1);
                dbuf.PlaneBufCFGTotalBlock = BuffEnd - BuffStart + 1;
                dbuf.NVBuf = Nv12Buf;
                if (Nv12Buf)
                {
                    BuffEnd = 0;
                    regInf = argMMIORW.RegInfList.ElementAt(6);
                    GetBuffEnd(regInf);
                    BuffStart = 0;
                    regInf = argMMIORW.RegInfList.ElementAt(7);
                    GetBuffStart(regInf);
                    Log.Message("\t PLANE_NV12_BUF start block: {0} end block: {1} Total Block Count: {2},", BuffStart, BuffEnd, BuffEnd - BuffStart + 1);
                }
                CursorEnabled = false;
                regInf = argMMIORW.RegInfList.ElementAt(8);
                dbuf.CursorMode = GetcursorEnable(regInf);
                if (CursorEnabled)
                {
                    dbuf.HWCursorEnable = true;
                    BuffEnd = 0;
                    regInf = argMMIORW.RegInfList.ElementAt(9);
                    GetBuffEnd(regInf);
                    BuffStart = 0;
                    regInf = argMMIORW.RegInfList.ElementAt(10);
                    GetBuffStart(regInf);
                    Log.Message("\t CUR_BUF_CFG start block: {0} end block: {1} Total Block Count: {2},", BuffStart, BuffEnd, BuffEnd - BuffStart + 1);
                    dbuf.CursorBufTotalBlock = BuffEnd - BuffStart + 1;
                }
                Log.Message("The hActive Register is offset {0} bitmap {1}", argMMIORW.RegInfList.ElementAt(11).Offset, argMMIORW.RegInfList.ElementAt(11).Bitmap);
                regInf = argMMIORW.RegInfList.ElementAt(11);
                dbuf.DisplaySurfaceWidth = GetHActive(regInf);
                Log.Message("the regList count is {0}", argMMIORW.RegInfList.Count());
                if (argMMIORW.RegInfList.Count() == 14)
                {
                    Log.Message("in new code");
                    uint hActiveValue = dbuf.DisplaySurfaceWidth;
                    uint laneCount = 0; uint bpp = 0;
                    regInf = argMMIORW.RegInfList.ElementAt(12);
                    laneCount = GetLaneCount(regInf);
                    regInf = argMMIORW.RegInfList.ElementAt(13);
                    bpp = GetMipiBpp(regInf);

                    // dbuf.DisplaySurfaceWidth = ((laneCount * 8) * hActiveValue) / bpp;
                    uint product1 = laneCount * 8; Log.Message("the product1 {0}", product1);
                    uint product2 = product1 * hActiveValue; Log.Message("the product2 {0}", product2);
                    uint divide = product2 / bpp; Log.Message("the divide {0}", divide);
                    dbuf.DisplaySurfaceWidth = divide;
                    Log.Message("Mipi HActive final value : {0}", dbuf.DisplaySurfaceWidth);
                }
            }
            else
            {
                Log.Message("YTile is not enabled");
                dbuf.Enabled = false;
            }
            return dbuf;
        }

        private string GetYTileSource(RegisterInf argRegInf)
        {
            string yTileSource = ReadMMIORW(argRegInf.Offset, false);
            uint yTileSourceValue = CompareRegValue(yTileSource, argRegInf.Bitmap);
            string sourcePixelFormatStr = "";
            Dictionary<uint, string> sourcePixelFormat = _featureMapper["YTileSource"];
            if (sourcePixelFormat.Keys.Contains(yTileSourceValue))
            {
                Log.Message("\t Source Pixel Format: {0}", sourcePixelFormat[yTileSourceValue]);
                sourcePixelFormatStr = sourcePixelFormat[yTileSourceValue];
                if (yTileSourceValue == 1)
                {
                    Nv12Buf = true;
                }
                else
                {
                    Nv12Buf = false;
                }
            }
            else
            {
                sourcePixelFormatStr = "None";
            }
            return sourcePixelFormatStr;
        }
        private TileFormat GetYTileFormat(RegisterInf argRegInf)
        {
            string yTileFormat = ReadMMIORW(argRegInf.Offset, false);
            uint yTileFormatValue = CompareRegValue(yTileFormat, argRegInf.Bitmap);
            Dictionary<uint, TileFormat> tiledSurface = new Dictionary<uint, TileFormat>()
            {
                {0x0,TileFormat.Linear_Memory},{0x1,TileFormat.Tile_X_Memory},{0x4,TileFormat.Tile_Y_Legacy_Memory},{0x5,TileFormat.Tile_Y_F_Memory}
            };
            if (tiledSurface.Keys.Contains(yTileFormatValue))
            {
                Log.Message("\t Tile Format: {0}", tiledSurface[yTileFormatValue]);
                return tiledSurface[yTileFormatValue];
            }
            return TileFormat.Invalid;
        }
        private string GetRotation(RegisterInf argRegInf)
        {
            string rotation = ReadMMIORW(argRegInf.Offset, false);
            uint rotationValue = CompareRegValue(rotation, argRegInf.Bitmap);
            Dictionary<uint, string> planeRotation = _featureMapper["Rotation"];
            if (planeRotation.Keys.Contains(rotationValue))
            {
                Log.Message("\t  Rotation: {0}", planeRotation[rotationValue]);
                return planeRotation[rotationValue];
            }
            return "No Rotation";
        }
        private void GetBuffEnd(RegisterInf argRegInf)
        {
            string buffEnd = ReadMMIORW(argRegInf.Offset, false);
            BuffEnd = CompareRegValue(buffEnd, argRegInf.Bitmap);
        }
        private void GetBuffStart(RegisterInf argRegInf)
        {
            string buffStart = ReadMMIORW(argRegInf.Offset, false);
            BuffStart = CompareRegValue(buffStart, argRegInf.Bitmap);
        }

        private string GetcursorEnable(RegisterInf argRegInf)
        {
            string cursorEnable = ReadMMIORW(argRegInf.Offset, true);
            uint curEnableValue = CompareRegValue(cursorEnable, argRegInf.Bitmap);
            Dictionary<uint, string> cursorModeSelect = _featureMapper["Cursor"];
            if (cursorModeSelect.Keys.Contains(curEnableValue))
            {
                if (cursorModeSelect.Keys.First() != curEnableValue)
                {
                    CursorEnabled = true;
                    Log.Message("\t Cursor Mode Select: {0}", cursorModeSelect[curEnableValue]);
                    return cursorModeSelect[curEnableValue];
                }
            }
            return "None";
        }
        private uint GetHActive(RegisterInf argRegInf)
        {
            string value = ReadMMIORW(argRegInf.Offset, false);
            uint hActive = CompareRegValue(value, argRegInf.Bitmap);
            Log.Message("The hactive is {0}", hActive);
            return hActive;
        }
        private uint GetLaneCount(RegisterInf argRegInf)
        {
            string value = ReadMMIORW(argRegInf.Offset, false);
            uint laneCount = CompareRegValue(value, argRegInf.Bitmap);
            Log.Message("The lane count is {0}", laneCount);
            return laneCount;
        }
        private uint GetMipiBpp(RegisterInf argRegInf)
        {
            string bpp = ReadMMIORW(argRegInf.Offset, false);
            uint bppValue = CompareRegValue(bpp, argRegInf.Bitmap);
            Dictionary<uint, string> bppMap = _featureMapper["MipiBpp"];
            if (bppMap.Keys.Contains(bppValue))
            {
                Log.Message("\t  Mipi Bpp: {0}", bppMap[bppValue]);
                Log.Message("the value of bpp in decimal {0}", Convert.ToUInt32(bppMap[bppValue]));
                return Convert.ToUInt32(bppMap[bppValue]);
            }
            return 0;
        }
        private void GetYTilingDataDFromXML()
        {
            _featureMapper = new Dictionary<string, Dictionary<uint, string>>();
            string fileName = string.Concat(Directory.GetCurrentDirectory(), "\\Mapper\\YTiling.map");
            if (!File.Exists(fileName))
                Log.Abort("File {0} not found", fileName);
            XDocument doc = XDocument.Load(fileName);
            var platform = from plt in doc.Descendants("Platform")
                           where plt.Attribute("id").Value.ToString().Contains(base.MachineInfo.PlatformDetails.Platform.ToString())
                           select new
                           {
                               platformId = plt.Attribute("id").Value,
                               key = plt.Descendants("Feature")
                           };
            foreach (var currentFeature in platform.First().key)
            {
                List<DisplayConfig> DispConfigList = new List<DisplayConfig>();
                string featureName = currentFeature.Attribute("id").Value;
                var valueList = currentFeature.Descendants("Value");
                Dictionary<uint, string> featureValue = new Dictionary<uint, string>();
                foreach (var currentValue in valueList)
                {
                    string regValue = currentValue.Attribute("regValue").Value;
                    uint regValueInt = Convert.ToUInt32(regValue, 16);
                    string reg = currentValue.Value;
                    featureValue.Add(regValueInt, reg);
                }
                _featureMapper.Add(featureName, featureValue);
            }
        }
    }
}

