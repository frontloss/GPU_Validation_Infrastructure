namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;

    public static class TestPostProcessing
    {
        public static Dictionary<TestCleanUpType, object> RegisterCleanupRequest;

        private static Dictionary<TestCleanUpType, System.Action> CleanupHandle;
        public static void Init()
        {
            RegisterCleanupRequest = new Dictionary<TestCleanUpType, object>();
        }

        public static void RegisterPlayersProcess(Process playerProcess)
        {
            if (TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.Players))
            {
                List<Process> playersList = (List<Process>)TestPostProcessing.RegisterCleanupRequest[TestCleanUpType.Players];
                if (playersList == null)
                {
                    playersList = new List<Process>();
                }
                if (!playersList.Select(eachPlayer => eachPlayer.Id).ToList().Contains(playerProcess.Id))
                {
                    playersList.Add(playerProcess);
                    TestPostProcessing.RegisterCleanupRequest[TestCleanUpType.Players] = playersList;
                }
            }
            else
            {
                TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.Players, new List<Process> { playerProcess });
            }
        }
    }
}
