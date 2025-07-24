namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Threading;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;
    using System.Collections.Generic;

    public class LaunchCharmWindow : FunctionalBase, ISetNoArgs, ISet,ISetMethod
    {
        private List<KeyCode> listKeyCode = new List<KeyCode>();
        KeyPress keyPress = new KeyPress();

        public object Set
        {
            set
            {
                Log.Verbose("Launching Charm Window (Windows Automation UI)");
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
            listKeyCode.Add(KeyCode.LWIN);
            listKeyCode.Add(KeyCode.KEY_P);
            keyPress.SetMethod(listKeyCode);
            Thread.Sleep(2000);
        }
        private void Tab()
        {
            Log.Verbose("Sending TAB command");
            keyPress.SetMethod(new List<KeyCode> { KeyCode.TAB });
        }
        private void Enter()
        {
            Log.Verbose("Sending Enter command");
            keyPress.SetMethod(new List<KeyCode> { KeyCode.ENTER });
            keyPress.SetMethod(new List<KeyCode> { KeyCode.ESC });
        }
        public bool SetMethod(object argMessage)
        {
            Log.Verbose("Launching Charm Window (Windows Automation UI)");

            Log.Verbose("Sending WinP command");
            listKeyCode.Add(KeyCode.LWIN);
            listKeyCode.Add(KeyCode.KEY_C);
            keyPress.SetMethod(listKeyCode);
            Thread.Sleep(2000);

            return true;
        }
    }
}
