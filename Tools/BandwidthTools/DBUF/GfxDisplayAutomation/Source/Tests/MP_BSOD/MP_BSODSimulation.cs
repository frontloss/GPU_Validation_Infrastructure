namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Diagnostics;
    using System.Text.RegularExpressions;

    [Test(Type = TestType.HasReboot)]
    class MP_BSODSimulation : TestBase
    {
        private string _bsodRebootFilePath = String.Concat(Directory.GetCurrentDirectory(), "\\BSODReboot{0}.tmp");
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            //Log.Message(true, "Set the type of memory dump");
            //CommonExtensions.StartProcess("wmic", "recoveros set DebugInfoType = 1");
            //Log.Message(true, "Enable Automatic Restart");
            //CommonExtensions.StartProcess("wmic", "recoveros set AutoReboot = true");            
        }
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Disabling Driver Signature Enforcement");
            SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");
        }
        [Test(Type = TestType.PreCondition, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Verify Disabling Driver Signature Enforcement");
            CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Connect all the displays planned in the grid.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
            }
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Install the driver that does BSOD");
            //check it
            //CommonExtensions.WriteRebootInfo(4);
            _bsodRebootFilePath = String.Format(_bsodRebootFilePath, 4);
            Log.Message("reboot file path {0}", _bsodRebootFilePath);
            File.WriteAllText(_bsodRebootFilePath, "4");
            string ddriverInfPath = null;
            string osVersion = MachineInfo.OS.Architecture;
            if (osVersion.Contains("32"))
                ddriverInfPath = " DDriverInf\\x86\\DDriver.inf";
            else
                ddriverInfPath = "DDriverInf\\x64\\DDriver.inf";
            Log.Verbose("ddriver path {0}", ddriverInfPath);
            AccessInterface.SetFeature(Features.InstallDDriver, Action.Set, ddriverInfPath);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Check if BSOD happened and it was manually initiated");
            Log.Verbose("Check if there exixts a Dump file in C:\\Windows\\Minidumps folder");
            Log.Message("in step 5 {0}", _bsodRebootFilePath);
            File.Delete(Directory.GetFiles(Directory.GetCurrentDirectory(), "BSODReboot*.tmp").FirstOrDefault());
            if (File.Exists(String.Format(_bsodRebootFilePath, 4)))
                Log.Fail("bsod reboot file didnot get deleted");
            string result = null;
            int flag = 0;
            string bugCheckLine = "Bugcheck code 000000E2";
            string normalisedBugCheckLine = Regex.Replace(bugCheckLine, @"\s+", String.Empty);
            string dumpFileName = Directory.GetFiles(Directory.GetCurrentDirectory(), "*.dmp").FirstOrDefault();

            Process dumpchk = CommonExtensions.StartProcess("dumpchk.exe ", dumpFileName);

            while (!dumpchk.StandardOutput.EndOfStream)
            {
                result = dumpchk.StandardOutput.ReadLine();
                string normalisedResult = Regex.Replace(result, @"\s+", String.Empty);
                if (String.Equals(normalisedResult, normalisedBugCheckLine, StringComparison.OrdinalIgnoreCase))
                    flag = 1;
            }
            if (flag == 1)
                Log.Success("BSOD was MANUALLY_INITIATED_CRASH");
            else
                Log.Fail(false, "BSOD was not manually_initiated");
            Log.Message(false, "Delete Dump file");
            if (File.Exists(dumpFileName))
                File.Delete(dumpFileName);
        }
    }
}