using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AudioEndpointVerification
{
    public class GetAudioRegInfo
    {
        private List<DisplayInfo> displayInfo { get; set; }
        public string offset { get; set; }
        public string AUD_PIN_ELD_Reg_Value { get; set; }
        private int count = 0;
        private Dictionary<PLANE, string> RegValuePipeMap;

        public GetAudioRegInfo()
        {
            RegValuePipeMap = new Dictionary<PLANE, string>();
            displayInfo = new List<DisplayInfo>();
            DisplayEnumeration enumerate = new DisplayEnumeration();
            displayInfo = enumerate.GetAll;
        }
        public List<AudioRegDataWrapper> ValidateRegister()
        {
            List<DisplayType> dispTypeInfo = new List<DisplayType>();
            Config dispConfig = new Config(displayInfo);
            DisplayConfig currentConfig = dispConfig.GetConfig();
            List<AudioRegDataWrapper> regWrapper = new List<AudioRegDataWrapper>();
            PipePlane pipeplaneInfo = new PipePlane();
            Platform plat = (Platform)Enum.Parse(typeof(Platform), CommonExtension.PlatformID);

            EventRegisterInfo regCheck = new EventRegisterInfo();
            DriverEscape driverEscape = new DriverEscape();
            count = 0;
            foreach (DisplayInfo DI in displayInfo)
            {
                dispTypeInfo.Add(DI.DisplayType);
            }
            foreach (DisplayType type in dispTypeInfo.Except(currentConfig.CustomDisplayList))
            {
                displayInfo.Remove(displayInfo.Where(DT => DT.DisplayType == type).First());
            }
            foreach (DisplayInfo disp in displayInfo)
            {
                AudioRegDataWrapper temp = new AudioRegDataWrapper();
                EventInfo eventInfo = new EventInfo();

                PipePlaneParams pipePlaneObject = new PipePlaneParams(disp.DisplayType);
                pipePlaneObject = pipeplaneInfo.GetMethod(plat, disp.DisplayType, disp.Port) as PipePlaneParams;
                temp.Pipe = pipePlaneObject.Pipe.ToString();

                temp.DisplayType = disp.DisplayType;
                temp.AudioSupport = (disp.isAudioCapable == true) ? "Yes" : "No";
                temp.DisplayHierarchy = currentConfig.dispListParam.Where(K => K.Value == disp.DisplayType).Select(P => P.Key).First().ToString();
                eventInfo.plane = pipePlaneObject.Plane;


                if (disp.isAudioCapable)
                    eventInfo.eventName = "AUDIO_ENABLE";
                else
                    eventInfo.eventName = "AUDIO_DISABLE";
                EventInfo returnEventInfo = regCheck.GetMethod(eventInfo) as EventInfo;
                foreach (RegisterInf reginfo in returnEventInfo.listRegisters)
                {
                    offset = reginfo.Offset;
                    DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                    driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                    DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                    if (!driverEscape.SetMethod(driverParams))
                        MessageBox.Show("Failed to read Register with offset as " + driverData.input);
                    else
                    {
                        if (CompareRegisters(driverData.output, reginfo, temp))
                            temp.Status = "SUCCESS";
                        else
                            temp.Status = "FAIL";
                    }
                    if (RegValuePipeMap.Count == 0)
                    {
                        string[] data = AUD_PIN_ELD_Reg_Value.Split('-');
                        RegValuePipeMap.Add(PLANE.PLANE_C, data[0]);
                        RegValuePipeMap.Add(PLANE.PLANE_B, data[1]);
                        RegValuePipeMap.Add(PLANE.PLANE_A, data[2]);
                    }

                    string value = RegValuePipeMap.Where(K => K.Key == pipePlaneObject.Plane).Select(P => P.Value).First().ToString();

                    temp.RegValue = Convert.ToInt32(value.Remove(0, 1), 2);
                    regWrapper.Add(temp);
                    count++;
                }

            }
            return regWrapper;
        }
        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo, AudioRegDataWrapper argregWrapper)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            AUD_PIN_ELD_Reg_Value = BitMerge(Convert.ToString(argDriverData, 2));
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            string valu = String.Format("{0:X}", hex & bit);
            if (argregWrapper.AudioSupport.ToLower().Equals("no"))
            {
                if ((Convert.ToInt32(valu) & 01) == 1)
                    return false;
                else
                    return true;
            }
            else if (String.Equals(valu, argRegInfo.Value))
                return true;
            return false;
        }

        private string BitMerge(string argData, bool isValidbit = false)
        {
            char[] dataBit = new char[14];
            for (int count = 0; count < dataBit.Length; count++)
            {
                if (count == 4 || count == 9)
                {
                    dataBit[4] = '-';
                    dataBit[9] = '-';
                }
                else
                {
                    if (!isValidbit)
                        dataBit[count] = '0';
                    else
                        dataBit[count] = '*';
                }
            }
            int index = dataBit.Length;
            for (int i = argData.Length - 1; i >= 0; i--)
            {
                if (dataBit[--index] == '-')
                {
                    i++;
                    continue;
                }
                dataBit[index] = argData[i];
            }
            string text = new string(dataBit);
            if (!string.IsNullOrEmpty(argData))
                return text;
            return string.Empty;
        }
    }
}
