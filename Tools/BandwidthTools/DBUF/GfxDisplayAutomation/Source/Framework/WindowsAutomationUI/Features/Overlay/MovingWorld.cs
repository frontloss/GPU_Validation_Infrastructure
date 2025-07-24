namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System.Windows.Automation;
    using System.Collections.Generic;
    internal class MovingWorld : PlayerBase
    {
        Dictionary<ColorFormat, List<string>> _colorFormat = new Dictionary<ColorFormat, List<string>>() { {ColorFormat.RGB,new List<string>(){"D3DFMT_X8R8G8B8","D3DFMT_A8R8G8B8"}},
        {ColorFormat.YUV,new List<string>(){"D3DFMT_UYVY","D3DFMT_YUY2"}}};
        string playerName = "dx9_overlay.exe";
        internal override Process Instance(IApplicationSettings argAppSettings, int argCurrMethodIdx)
        {
            base.AppSettings = argAppSettings;
            base.CurrMethodIdx = argCurrMethodIdx;

            
            if (string.IsNullOrEmpty(base.OverlayParams.Player))
                base.OverlayParams.Player = string.Format("{0}\\{1}", base.AppSettings.DisplayToolsPath, playerName);
            if (!File.Exists(base.OverlayParams.Player))
                Log.Abort("{0} does not exist!", base.OverlayParams.Player);

            Process playerProcess = Process.GetProcessesByName(playerName.Substring(0, playerName.IndexOf("."))).FirstOrDefault();
            if (null == playerProcess)
            {
                Log.Message(true, "Launching {0} ", playerName);
                playerProcess = CommonExtensions.StartProcess(base.OverlayParams.Player, string.Empty, 0, base.AppSettings.DisplayToolsPath);
            }
            else
                playerProcess.StartInfo.FileName = base.OverlayParams.Player;

            //Used for cleanup of the overlay player during test cleanup.
            TestPostProcessing.RegisterPlayersProcess(playerProcess);
            
            return playerProcess;
        }
        internal override void Stop(Process argProcess)
        {
            base.StopPlayback(argProcess, "o");
        }
        internal override void Move(Process argProcess)
        {
            if (base.IsMoveApplicable())
            {
                base.Move(argProcess);
                Thread.Sleep(15000);
            }
        }
        internal override void FullScreen(Process argProcess)
        {
            Thread.Sleep(3000);
            base.FullScreenPlayback(argProcess, "{F2}");
            
        }
        internal override void Close(Process argProcess)
        {
            Log.Message(true,"Closing Moving World");
            base.Close(argProcess);
        }
        internal override void ChangeFormat(Process argProcess)
        {
            Log.Message(true, "Chaning Moving World format to {0}",base.OverlayParams.colorFormat);
            this.SetWindowFocus(argProcess);
            Thread.Sleep(3000);
            SendKeys.SendWait("{F9}");
            Thread.Sleep(3000);


            ColorFormat cp = base.OverlayParams.colorFormat;
            if (_colorFormat.Keys.ToList().Contains(cp))
            {
                List<string> options = _colorFormat[cp];
                UIABaseHandler uiaBaseHandler = new UIABaseHandler();
                bool match = false;
               
                options.ForEach(curString =>
                    {
                        if (!match)
                        {
                            AutomationElement element = UIABaseHandler.SelectElementNameControlType(curString, ControlType.MenuItem);
                            if (element != null)
                            {
                                Log.Message("Selecting the element {0}",curString);
                                uiaBaseHandler.Invoke(element);
                                match = true;
                            }
                            else
                                Log.Message("element {0} is null",curString);
                        }
                    });
            }                                       
        }
        internal override void Play(Process argProcess)
        {
            if (null != argProcess)
            {
                base.Close(argProcess);
                Thread.Sleep(2000);
            }

            argProcess = CommonExtensions.StartProcess(this.GetFilePath(), string.Empty, 0, base.AppSettings.DisplayToolsPath);

            if (!this.IsPlayerLoaded())
                Log.Abort("{0} did not launch.", playerName);
            
        }

        private Process GetPlayerProcess()
        {
            return Process.GetProcessesByName(playerName.Substring(0, playerName.IndexOf("."))).FirstOrDefault();
        }
        private bool IsPlayerLoaded()
        {
            bool isLoaded = (null != this.GetPlayerProcess());

            if (!isLoaded)
            {
                try
                {
                    Thread.Sleep(5000);
                    isLoaded = (null != this.GetPlayerProcess());
                }
                catch (Exception ex)
                {
                    Log.Sporadic(false, "Moving World:: {0}", ex.Message);
                    Log.Verbose("{0}", ex.StackTrace);
                }
            }

            return isLoaded;
        }       
        private string GetFilePath()
        {
            return string.Format("{0}\\{1}", base.AppSettings.DisplayToolsPath, playerName);
        }
    }
}
