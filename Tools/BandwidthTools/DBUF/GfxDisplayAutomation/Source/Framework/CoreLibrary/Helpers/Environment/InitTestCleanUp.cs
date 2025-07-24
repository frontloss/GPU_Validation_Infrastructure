namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using System.Diagnostics;

    class InitTestCleanUp : InitEnvironment
    {
        private IApplicationManager _appManager = null;
        private TestBase _context = null;
        private static Dictionary<TestCleanUpType, System.Action> CleanupHandle;

        public InitTestCleanUp(IApplicationManager argManager)
            : base(argManager)
        {
            this._appManager = argManager;
            CleanupHandle = new Dictionary<TestCleanUpType, System.Action>();

            //add your own cleanup function here.
            CleanupHandle.Add(TestCleanUpType.SimulatedBattery, CleanupSimulatedBattery);
            CleanupHandle.Add(TestCleanUpType.LANConnection, EnableLANConnection);
            CleanupHandle.Add(TestCleanUpType.SimulatedDisplay, CleanUpSimulatedDisplay);
            CleanupHandle.Add(TestCleanUpType.Players, CleanUpPlayers);
            CleanupHandle.Add(TestCleanUpType.Underrun, CleanUpUnderrun);
            CleanupHandle.Add(TestCleanUpType.WiGig, CleanUpWiGig);
            CleanupHandle.Add(TestCleanUpType.ValidatePowerScheme, CleanUpPowerScheme);
        }
        public override void DoWork()
        {
            _context = _context.Load(base.Manager.ParamInfo[ArgumentType.TestName] as string);
            if (_context == null)
                return;
            Log.Message(true, "Test Clean Up, and Release All Resources");
            this.Cleanup();
        }

        private void Cleanup()
        {
            List<TestCleanUpType> keyList = new List<TestCleanUpType>(TestPostProcessing.RegisterCleanupRequest.Keys);
            foreach (TestCleanUpType FT in keyList)
            {
                Log.Verbose("Cleaning up {0}", FT.ToString());
                if (CleanupHandle.ContainsKey(FT))
                    CleanupHandle[FT]();
            }
        }

        private void CleanupSimulatedBattery()
        {
            CommonExtensions.StartProcess(@"cscript", "SimulatedBattery_Control.vbs /cleanup", 0).WaitForExit();
            Thread.Sleep(6000);
        }

        private void EnableLANConnection()
        {
            NetParam netParam;
            netParam = new NetParam();
            netParam.adapter = Adapter.LAN;
            netParam.netWorkState = NetworkState.Enable;
            NetworkExtensions.SetNetworkConnection(netParam);
        }

        private void CleanUpSimulatedDisplay()
        {
            EnvPreparedness.RunTask(_appManager, Features.InitCleanupSimulatedDisplays);
        }

        private void CleanUpPlayers()
        {
             List<Process> playersList = (List<Process>)TestPostProcessing.RegisterCleanupRequest[TestCleanUpType.Players];

            if(playersList !=null)
            {
                playersList.ForEach(eachPlayer =>
                {
                    if(!eachPlayer.HasExited)
                    {
                        eachPlayer.Kill();
                    }
                });
            }
        }

        private void CleanUpUnderrun()
        {
            AccessInterface.SetFeature<bool>(Features.VerifyUnderrun, Action.SetMethod, false);
        }
        private void CleanUpWiGig()
        {
            WiGigParams inputParam = new WiGigParams();
            inputParam.wigigSyncInput = WIGIG_SYNC.RF_Kill;
            AccessInterface.SetFeature<bool, WiGigParams>(Features.WIGIG, Action.SetMethod, inputParam);
        }
        private void CleanUpPowerScheme()
        {
            DisplayExtensions.ValidatePowerScheme();
        }
    }
}
