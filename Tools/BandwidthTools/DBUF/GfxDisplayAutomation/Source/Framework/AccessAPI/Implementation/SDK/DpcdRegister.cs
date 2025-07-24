using System;
using System.Text;
using System.Linq;

namespace Intel.VPG.Display.Automation
{
    class DpcdRegister : FunctionalBase, IGetMethod, IParse
    {
        public object GetMethod(object argMessage)
        {
            DpcdInfo args = argMessage as DpcdInfo;
            SdkExtensions sdkExtn = base.CreateInstance<SdkExtensions>(new SdkExtensions());
            ISDK sdkDpcd = sdkExtn.GetSDKHandle(SDKServices.DpcdRegister);
            return (DpcdInfo)sdkDpcd.Get(args);
        }

        public void Parse(string[] args)
        {
            uint range = 1;

            if (args.Length == 5 && args[3].ToLower().Contains("range"))
            {
                range = Convert.ToUInt32(args[4]);
            }

            if (args.Length >= 3 && args[0].ToLower().Contains("get"))
            {
                DisplayType display = (DisplayType)Enum.Parse(typeof(DisplayType), args[1], true);
                
                DpcdInfo argMessage = new DpcdInfo();
                argMessage.DispInfo = base.EnumeratedDisplays.Where(dI => dI.DisplayType == display).FirstOrDefault();

                for (uint count = 0; count < range; count++)
                {
                    argMessage.Offset = Convert.ToUInt32(args[2], 16) + count;

                    GetMethod(argMessage);

                    Log.Message("DPCD Value for {0} is {1}", argMessage.Offset.ToString("X"), argMessage.Value.ToString("X"));
                }
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe dpcdregister get DisplayType <inputvalue> range <count>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe dpcdregister get DP 0x00000 range 10");
            sb.Append("For register read : Execute.exe dpcdregister get EDP 0x00000");
            Log.Message(sb.ToString());
        }
    }
}
