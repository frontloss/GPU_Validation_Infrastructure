using System;
using System.IO;
namespace Intel.VPG.Display.Automation
{
    public class SetUpDesktopArgs
    {
        
        public const string DEFAULT_IMAGE = "Desktop.jpg";
        private string imageFilePath;
        private string metadataFilePath;
        private uint bpc;

        public string ImageFilePath
        {
            get { return imageFilePath; }
            set { imageFilePath = value; }
        }

        public string MetadataFilePath
        {
            get { return metadataFilePath; }
            set { metadataFilePath = value; }
        }

        public uint BPC
        {
            get { return bpc; }
            set { bpc = value; }
        }

        public enum SetUpDesktopOperation
        {
            ChangeDesktopBackground,
            ShowTaskBar,
            HideTaskBar,
            ShowCursor,
            HideCursor,
            PrepareDesktop,
            RestoreDesktop,
            BallonNotifications,
            ShowMMIOFlip,
            HideMMIOFlip,
            TenPlayerHDR,

        }
        public SetUpDesktopOperation FunctionName { get; set; }

        public SetUpDesktopArgs(SetUpDesktopOperation argFuncName, string img = DEFAULT_IMAGE)
        {
            this.FunctionName = argFuncName;
            this.imageFilePath = string.Concat(Directory.GetCurrentDirectory(), @"\", img) ;
        }
        public DisplayType display { get; set; }
        public UInt64 pGmmBlock { get; set; }
        public DisplayConfig currentConfig { get; set; }
        public DisplayMode displayMode { get; set; }
    }
}
