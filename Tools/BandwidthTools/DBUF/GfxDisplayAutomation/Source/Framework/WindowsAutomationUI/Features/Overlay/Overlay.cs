namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Text;
    using System.Linq;
    class Overlay : FunctionalBase, ISet ,IParse
    {
        private Dictionary<OverlayPlaybackOptions, Action<Process>> _playBackOptions = null;
        private Dictionary<OSType, PlayerBase> _player = null;
        protected OverlayParams _overlayParam = null;
        public object Set
        {
            set
            {
                _overlayParam = value as OverlayParams;
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
                _playBackOptions.Add(Automation.OverlayPlaybackOptions.ChangeFormat, argPlayer.ChangeFormat);
            }
        }
        private PlayerBase GetPlayer
        {
            get
            {
                Dictionary<OverlayApp, PlayerBase> player = new Dictionary<OverlayApp, PlayerBase>()
                {
                    {OverlayApp.ArcSoft,new ArcSoft()},
                    {OverlayApp.MovingWorld,new MovingWorld()},
                    {OverlayApp.MPlayer,new MPlayerC()}
                };
                if (null == this._player)
                {
                    this._player = new Dictionary<OSType, PlayerBase>();
                    this._player.Add(OSType.WIN7, new MPlayerC());
                    this._player.Add(OSType.Default, new MovingWorld());
                }
                    if (_overlayParam.overlayApp != OverlayApp.None)
                        return player[_overlayParam.overlayApp];
                    if (this._player.ContainsKey(base.MachineInfo.OS.Type))
                        return this._player[base.MachineInfo.OS.Type];

                    return this._player[OSType.Default];
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