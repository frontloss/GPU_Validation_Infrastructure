namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Threading;
    using System.Windows.Forms;

    using Ranorex;

    public class LaunchCharmWindow : FunctionalBase, ISetNoArgs, ISet
    {
        public object Set
        {
            set
            {
                this.LaunchCharm();
                for (int idx = 0; idx < (int)value; idx++)
                    this.Tab();
                this.Enter();
            }
        }
        public bool SetNoArgs()
        {
            this.Tab();
            this.Enter();
            return true;
        }

        private void LaunchCharm()
        {
            Log.Verbose("Sending WinP command");
            Keyboard.Press("{LWin down}{P down}{P up}{LWin up}");
            Thread.Sleep(2000);
        }
        private void Tab()
        {
            Log.Verbose("Sending TAB command");
            SendKeys.SendWait("{TAB}");
            Thread.Sleep(2000);
        }
        private void Enter()
        {
            Log.Verbose("Sending Enter command");
            SendKeys.SendWait("~");
            Thread.Sleep(8000);
        }
    }
}
