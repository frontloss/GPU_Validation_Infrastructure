namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text;

    class Overlay : FunctionalBase, ISet ,IParse
    {
        private Dictionary<OverlayPlaybackOptions, Action<Process>> _playBackOptions = null;
        private Dictionary<string, PlayerBase> _player = null;

        public object Set
        {
            set
            {
                PlayerBase player = this.GetPlayer;
                this.PlaybackOptions(player);
                player.GetMode = base.GetDisplayModeByDisplayType;
                player.OverlayParams = value as OverlayParams;
                this._playBackOptions[player.OverlayParams.PlaybackOptions](player.Instance(base.AppSettings, base.CurrentMethodIndex));
            }
        }

        private void PlaybackOptions(PlayerBase argPlayer)
        {
            if (null == this._playBackOptions)
            {
                _playBackOptions = new Dictionary<OverlayPlaybackOptions, Action<Process>>();
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.ClosePlayer, argPlayer.Close);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.FullScreen, argPlayer.FullScreen);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.MaximizePlayer, argPlayer.Maximize);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.MinimizePlayer, argPlayer.Minimize);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.MovePlayer, argPlayer.Move);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.PauseVideo, argPlayer.Pause);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.PlayVideo, argPlayer.Play);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.RestorePlayer, argPlayer.Restore);
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.StopVideo, argPlayer.Stop);
            }
        }
        private PlayerBase GetPlayer
        {
            get
            {
                string DEFAULT = "Default";
                if (null == this._player)
                {
                    this._player = new Dictionary<string, PlayerBase>();
                    this._player.Add(OSInfo.WIN7, new MPlayerC());
                    this._player.Add(DEFAULT, new ArcSoft());
                }
                if (this._player.ContainsKey(base.MachineInfo.OS.Type))
                    return this._player[base.MachineInfo.OS.Type];
                return this._player[DEFAULT];
            }
        }

        #region IParse Members

        public void Parse(string[] args)
        {
            if (args.Length >= 2 && args[0].ToLower().Contains("set"))
            {
                OverlayParams tempParams = new OverlayParams();
                OverlayPlaybackOptions tempOptions;

                if (Enum.TryParse<OverlayPlaybackOptions>(args[1], true, out tempOptions))
                {
                    tempParams.PlaybackOptions = tempOptions;
                    tempParams.DisplayHierarchy = DisplayHierarchy.Display_1;
                    tempParams.CurrentConfig = base.CurrentConfig;
                }
                else
                {
                    this.HelpText();
                }


                PlayerBase player = this.GetPlayer;
                this.PlaybackOptions(player);
                player.GetMode = base.GetDisplayModeByDisplayType;
                player.OverlayParams = tempParams;
                this._playBackOptions[player.OverlayParams.PlaybackOptions](player.Instance(base.AppSettings, base.CurrentMethodIndex));
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Problem with Commandline Parameters. \n Please type : Execute.exe Overlay set <ClosePlayer/PlayVideo/StopVideo>").Append(Environment.NewLine);
            sb.Append("For example : Execute.exe Overlay set ClosePlayer");
            Log.Message(sb.ToString());
        }

        #endregion
    }
}