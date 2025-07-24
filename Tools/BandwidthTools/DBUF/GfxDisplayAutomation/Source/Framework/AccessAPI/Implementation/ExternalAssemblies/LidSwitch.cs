namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Runtime.InteropServices;
    using System.Collections.Generic;

    internal class LidSwitch : FunctionalBase, ISetMethod, ISet
    {
        public object Set
        {
            set
            {
                LidSwitchParams argLidSwitchParams = (LidSwitchParams)value;

                DVMU4_STATUS d = Interop.EnableLID(0x00, argLidSwitchParams.Delay, true, true);
                if (d == DVMU4_STATUS.SUCCESS)
                {
                    Log.Success("Lid Switch Successful");
                }
                else
                    Log.Message("Lid Switch Unsuccessful using DVMU. DVMU Status returned is {0}", d);
            }
        }
        public bool SetMethod(object argMessage)
        {
            LidSwitchAction argLidSwitchAction = (LidSwitchAction)argMessage;
            return (ChangeLidAction(argLidSwitchAction));
        }

        private bool ChangeLidAction(LidSwitchAction argLidSwitchAction)
        {
            int enumValue = (int)argLidSwitchAction;
            string result = null;
            string schemeGuid = null;
            string subgroupGuid = null;
            string settingGuid = null;
            Process schemeGuidProcess = CommonExtensions.StartProcess("powercfg.exe", " /List");
            while (!schemeGuidProcess.StandardOutput.EndOfStream)
            {
                result = schemeGuidProcess.StandardOutput.ReadLine();
                if (result.EndsWith("*"))
                {
                    if (result.Contains(':'))
                    {
                        result = result.Split(':').Last().TrimStart();
                    }
                    schemeGuid = result.Split(' ').First();
                    Log.Message("SchemeGUID - {0}", schemeGuid);
                }
            }
            Process guidProcess = CommonExtensions.StartProcess("powercfg.exe", " /Query");
            while (!guidProcess.StandardOutput.EndOfStream)
            {
                result = guidProcess.StandardOutput.ReadLine();
                if (result.Contains("Power buttons and lid"))
                {
                    if (result.Contains(':'))
                        result = result.Split(':').Last().TrimStart();
                    subgroupGuid = result.TrimStart().Split(' ').First();
                    Log.Message("Sub Group GUID - {0}", subgroupGuid);
                }
                if (result.Contains("Lid close action"))
                {
                    if (result.Contains(':'))
                        result = result.Split(':').Last().TrimStart();
                    settingGuid = result.TrimStart().Split(' ').First();
                    Log.Message("Setting GUID - {0}", settingGuid);
                }
            }
            string acArgument = "/setacvalueindex " + schemeGuid + " " + subgroupGuid + " " + settingGuid + " " + enumValue.ToString();
            Process guid = CommonExtensions.StartProcess("powercfg.exe", acArgument);
            string dcArgument = "/setdcvalueindex " + schemeGuid + " " + subgroupGuid + " " + settingGuid + " " + enumValue.ToString();
            guid = CommonExtensions.StartProcess("powercfg.exe", dcArgument);
            if (VerifyLidActionChange(schemeGuid, subgroupGuid, enumValue, enumValue))
                return true;
            else
                return false;
        }
        private bool VerifyLidActionChange(string argSchemeGuid, string argSubgrpGuid, int argAcExpectedValue, int argDcExpectedValue)
        {
            string result = null;
            int acValueSet, dcValueSet;
            string argument = "-query " + argSchemeGuid + " " + argSubgrpGuid;
            Process verifyProcess = CommonExtensions.StartProcess("powercfg.exe", argument);
            while (!verifyProcess.StandardOutput.EndOfStream)
            {
                result = verifyProcess.StandardOutput.ReadLine();
                string nextLine = null;
                if (result.Contains("Lid close action"))
                {
                    for (int i = 0; i < 10; i++)
                        nextLine = verifyProcess.StandardOutput.ReadLine();
                    acValueSet = Convert.ToInt32(nextLine.TrimStart().Split('x').Last());
                    nextLine = verifyProcess.StandardOutput.ReadLine();
                    dcValueSet = Convert.ToInt32(nextLine.TrimStart().Split('x').Last());
                    Log.Message("Current AC value - {0} Current DC value - {1}", acValueSet, dcValueSet);
                    if (acValueSet == argAcExpectedValue && dcValueSet == argDcExpectedValue)
                    {
                        Log.Success("The expected and Current AC and DC values match. AC value = {0}, DC value = {1}", (LidSwitchAction)acValueSet, (LidSwitchAction)dcValueSet);
                        return true;
                    }
                    else
                    {
                        Log.Fail("The expected AC value = {0} Current AC value = {1} The expected DC value = {2} Current DC value = {3}", (LidSwitchAction)argAcExpectedValue, (LidSwitchAction)acValueSet, (LidSwitchAction)argDcExpectedValue, (LidSwitchAction)dcValueSet);
                        return false;
                    }
                }
            }
            return false;
        }
    }
}