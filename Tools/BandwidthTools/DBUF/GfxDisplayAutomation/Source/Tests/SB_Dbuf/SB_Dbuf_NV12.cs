using System.Windows.Forms;
using System.Threading;
using System.Diagnostics;
namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_NV12:SB_Dbuf_Base
    {
         [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
             base.ApplyConfig(base.CurrentConfig);
             //base.PerformYTiling(base.CurrentConfig);       
        }
         [Test(Type = TestType.Method, Order = 1)]
         public void TestStep1()
         {
             LaunchXBox();
         }
         [Test(Type = TestType.Method, Order = 2)]
         public void TestStep2()
         {
             base.CheckDbuf(base.CurrentConfig);
             ClosePlayerNExplorer();
         }
         private void LaunchXBox()
         {
             CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.MPOClipPath);
             SendKeys.SendWait("{F11}");
             Thread.Sleep(10000);
             AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, "Wildlife");
             Thread.Sleep(15000);
         }
         private void ClosePlayerNExplorer()
         {
             SendKeys.SendWait("%{F4}");
             Thread.Sleep(1000);
             Process[] explorerProcess = Process.GetProcessesByName("explorer");
             if (explorerProcess.Length > 0)
             {
                 foreach (Process p in explorerProcess)
                     p.Kill();
             }
         }
    }
}
