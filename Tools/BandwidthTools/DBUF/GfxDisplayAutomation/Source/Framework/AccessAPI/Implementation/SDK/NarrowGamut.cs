using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
namespace Intel.VPG.Display.Automation
{
    class NarrowGamut : FunctionalBase, ISet
    {
        public Dictionary<NarrowGamutOption, System.Action> PerformChanges
        {
            get
            {
                Dictionary<NarrowGamutOption, System.Action> performChanges = new Dictionary<NarrowGamutOption, System.Action>() { 
                {NarrowGamutOption.EnableNarrowGamut,SetNarrowGamutStatus},
                {NarrowGamutOption.DisbaleNarrowGamut,SetNarrowGamutStatus},
                {NarrowGamutOption.EnableINF,EnableINF},
                {NarrowGamutOption.ResetINF,ResetINF},
                {NarrowGamutOption.VerifyINF,VerifyINF}};
                return performChanges;
            }
        }
        private NarrowGamutParams narrowGamut;
        public NarrowGamutParams NarrowGamutData
        {
            get { return narrowGamut; }
            set { narrowGamut = value; }
        }
        public Dictionary<string, List<string>> ChangesInInf
        { 
            get
            {
                Dictionary<string, List<string>> _changesInInf = new Dictionary<string, List<string>>() {
          
            { ";<-NarrowGamut_AddSwSettings->", new List<string>(){"[ChromaticityOverride_AddSwSettings]",
                ";override chromaticity data. 10 bytes of EDID Chromaticity data are overriden using this section",
                "HKR,, OverRideChromaticityData,%REG_BINARY%,37,AC,A3,59,57,9B,25,0D,51,59",
                "[NarrowGamutFeature_AddSwSettings]",
                "HKR,, NarrowGamutFeatureEnable,%REG_DWORD%, 0x01 ; 0x01- Enable 0- Disable ,0x2 - Dont care"} },                
            {"<-NarrowGamut_DelSwSettings>",new List<string>(){"[ChromaticityOverride_DelSwSettings]",
                                                              "HKR,, OverRideChromaticityData",
                                                              "[NarrowGamutFeature_DelSwSettings]",
                                                              "HKR,, NarrowGamutFeatureEnable"}}};
               GetFieldName().ForEach(field =>
              _changesInInf.Add(field, new List<string>() {  "AddReg =  ChromaticityOverride_AddSwSettings", "AddReg =  NarrowGamutFeature_AddSwSettings" , "DelReg =  ChromaticityOverride_DelSwSettings",
                                                         "DelReg =  NarrowGamutFeature_DelSwSettings"}));
                return _changesInInf;
            }
        }
        public object Set
        {
            set
            {
                NarrowGamutData = value as NarrowGamutParams;
                PerformChanges[narrowGamut.narrowGamutOption]();
            }
        }
        private void SetNarrowGamutStatus()
        {
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkGamut = sdkExtn.GetSDKHandle(SDKServices.NarrowGamut);
            sdkGamut.Set(NarrowGamutData);
        }
        private void EnableINF()
        {
            Log.Message(true,"Changing .inf to enable Narrow Gamut");
            string fileName = "\\igdlh64.inf";
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            ChangesInInf.Keys.ToList().ForEach(curKey =>
            {
                StringBuilder newfile = new StringBuilder();
                string[] data = File.ReadAllLines(string.Concat(NarrowGamutData.INFFilePath, fileName));
                for (int i = 0; i < data.Length; i++)
                {
                    string line = data.ElementAt(i);
                    if (line.Contains(curKey))
                    {
                        newfile.Append(line + "\r\n");
                        string nextLine = data.ElementAt(i + 1);
                        List<string> linesToBeAdded = ChangesInInf[curKey];
                        linesToBeAdded.ForEach(curLine =>
                        {
                            if (!data.Any(dI => dI.Equals(curLine)))
                                newfile.Append(curLine + "\r\n");
                        });
                        continue;
                    }
                    newfile.Append(line + "\r\n");
                }
                File.WriteAllText(string.Concat(NarrowGamutData.INFFilePath, fileName), newfile.ToString());
            });
        }
        private void ResetINF()
        {
            Log.Message(true, "Changing .inf to disable Narrow Gamut");
            List<string> changes = new List<string>();
            ChangesInInf.Keys.ToList().ForEach(curKey =>
            {
                List<string> data = ChangesInInf[curKey];
                data.ForEach(curData =>
                {
                    changes.Add(curData);
                });
            });
            string fileName = "\\igdlh64.inf";
            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            StringBuilder newfile = new StringBuilder();
            string[] fileData = File.ReadAllLines(string.Concat(NarrowGamutData.INFFilePath, fileName));

            fileData.ToList().ForEach(curLine =>
            {
                if (!changes.Contains(curLine))
                {
                    newfile.Append(curLine + "\r\n");
                }
                else
                {
                    Log.Message("{0}",curLine);
                }
            });
            File.WriteAllText(string.Concat(NarrowGamutData.INFFilePath, fileName), newfile.ToString());
        }
        private void VerifyINF()
        {
            Log.Message(true, "Verifying .inf chnages  to enable Narrow Gamut");
            List<string> changes = new List<string>();
            ChangesInInf.Keys.ToList().ForEach(curKey =>
            {
                List<string> data = ChangesInInf[curKey];
                data.ForEach(curData =>
                {
                    changes.Add(curData);
                });
            });
            string fileName = "\\igdlh64.inf";

            if (MachineInfo.OS.Architecture.Contains("32"))
                fileName = "\\igdlh.inf";

            string[] fileData = File.ReadAllLines(string.Concat(NarrowGamutData.INFFilePath, fileName));

            changes.ForEach(curLine =>
            {
                if (!fileData.Contains(curLine))
                {
                    Log.Fail(".INF changes for narrow gamut is not complete, missing seeting {0}", curLine);
                }
            });
        }
        private List<string> GetFieldName()
        {
            List<string> fieldNames = new List<string>();

            switch(base.MachineInfo.PlatformDetails.Platform)
            {
                case Platform.HSW:
                    fieldNames.Add("HSWM");
                    fieldNames.Add("HSWD");
                    break;
                case Platform.CHV:
                    fieldNames.Add("CHVM");
                    fieldNames.Add("CHVMF");
                    break;
                case Platform.BDW:
                    fieldNames.Add("BDWM");
                    break;
                default:
                    fieldNames.Add(base.MachineInfo.PlatformDetails.Platform + "D");
                    break;

            }

            Dictionary<OSType, uint> osInfo = new Dictionary<OSType, uint>() {
            {OSType.WIN7,7},
            {OSType.WIN8,8},
            {OSType.WINBLUE,81},
            {OSType.WINTHRESHOLD,10}};

            for (int i = 0; i < fieldNames.Count; i++)
            {
                string key = "[i" + fieldNames[i] + "_w";
                if (osInfo.Keys.ToList().Contains(base.MachineInfo.OS.Type))
                    key = key + osInfo[base.MachineInfo.OS.Type];
                else
                    Log.Fail("cannot find entry {0} in Dictionary:osInfo ", base.MachineInfo.OS.Type);
                
                key = key + "]";
                
                fieldNames[i] = key;
            }
           return fieldNames;
        }
    }
}
