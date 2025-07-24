using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    public partial class Form1 : Form
    {
        public Size MonitorSize = SystemInformation.PrimaryMonitorSize;
        public Point FormLocation = new Point(0, 0);
        public bool lostFocus = false;
        Bitmap map = null;
        //Relative path for the Golden Image used in capturing CRCs
        public const string GoldenImagePath = "CrcImage\\GoldenImage.jpg";

        public Form1()
        {
            InitializeComponent();
        }

        public void PrintMonitorSize()
        {
            Log.Message(String.Format("Width:{0} Height:{1}", MonitorSize.Width, MonitorSize.Height));
            Log.Message(String.Format("Location - X={0},Y={1}", FormLocation.X, FormLocation.Y));
        }

        public void ChangeBackground()
        {
            this.BackgroundImage = null;

            if (map != null)
            {
                map.Dispose();
                map = null;
            }

            this.Dispose(true);
        }

        public void SetLostFocus(bool value)
        {
            lostFocus = value;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            map = new Bitmap(GoldenImagePath);
            this.BackgroundImage = map;
            this.FormBorderStyle = FormBorderStyle.None;
            this.BackgroundImageLayout = ImageLayout.None;
            this.Width = MonitorSize.Width;
            this.Height = MonitorSize.Height;
            this.Location = FormLocation;
            this.WindowState = FormWindowState.Maximized;
            System.Threading.Thread.Sleep(100);
        }

        private void Form1_LostFocus(object sender, EventArgs e)
        {
            lostFocus = true;
            this.Focus();
        }
       
    }
}
