using System;
using System.Collections.Generic;
using System.IO;
namespace Intel.VPG.Display.Automation
{
    public class StaticFormArgs
    {
        public const string DEFAULT_IMAGE = "Desktop.jpg";

        public bool ShowForm { get; set; }
        public DisplayType displayType { get; set; }
        public DisplayConfig currentConfig { get; set; }

        private string imageFilePath;
        public string ImageFilePath
        {
            get { return imageFilePath; }
            set { imageFilePath = string.Concat(Directory.GetCurrentDirectory(), @"\", value); }
        }

        public StaticFormArgs(bool argShowForm, string img = DEFAULT_IMAGE)
        {
            this.ShowForm = argShowForm;
            this.imageFilePath = img;
        }
    }
}
