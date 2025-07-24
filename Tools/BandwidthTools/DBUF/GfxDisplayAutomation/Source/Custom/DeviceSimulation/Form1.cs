using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

/*
  Author: Chandrakanth, pabolu 
*/


namespace Intel.VPG.Display.Automation
{
    public struct Details
    {
        public DIVA_PORT_TYPE_CLR Port;
        public uint ulDisplayUID;
        public bool Plug;
        public bool IsLowPower;
        public string EDIDFileName;
    }

    public partial class DeviceSimulationTool : Form
    {
        public List<Details> GlobalDetails = new List<Details>();

        public List<DIVA_DISPLAY_DETAILS_ARGS_CLR> EnumeratedDisplays = new List<DIVA_DISPLAY_DETAILS_ARGS_CLR>();

        public DeviceSimulationTool()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            loadForm();
        }

        private void loadForm()
        {
            Image image = Image.FromFile(Directory.GetCurrentDirectory() + @"\Logo.png");
            pictureBoxLogo.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBoxLogo.Image = image;

            Helper.EnableULT(true);
            Helper.EnableFeature(true, DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM);
            Helper.FetchEnumeratedDisplays(ref EnumeratedDisplays);

            if(!EnumeratedDisplays.Any(item=> item.DisplayUID == 0x40f04))
            {
                DIVA_DISPLAY_DETAILS_ARGS_CLR dispDetails = new DIVA_DISPLAY_DETAILS_ARGS_CLR();
                dispDetails.DisplayUID = 0x40f04;
                dispDetails.PortType = DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR;
                dispDetails.DisplayType = DIVA_DISPLAY_TYPE_CLR.DIVA_LFP_TYPE_CLR;

                EnumeratedDisplays.Add(dispDetails);
            }

            EnumeratedDisplays.ForEach(item =>
            {
                if ((item.DisplayType != DIVA_DISPLAY_TYPE_CLR.DIVA_NULL_DISPLAY_TYPE_CLR) && !cbPort.Items.Contains(item.PortType))
                {
                    cbPort.Items.Add(item.PortType);
                }
            });

            if (cbPort.Items.Count == 0)
            {
                cbPort.SelectedIndex = -1;
                cbDisplayUID.Text = "";
                cbDisplayUID.Items.Clear();
                lbAttachedStatus.Text = "Device Status";

            }
            else if (cbPort.Items.Count > 0)
                cbPort.SelectedIndex = 0;
        }

        private void myToolTip()
        {
            ToolTip toolTip = new ToolTip();
            toolTip.SetToolTip(cbPort, "Specifies the displays port");
            toolTip.SetToolTip(cbDisplayUID, "Specifies the WindowsMonitorID for the selected port");
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
        }

        private void btHotplug_Click(object sender, EventArgs e)
        {
            List<bool> plugList=new List<bool>();
            List<bool> lowPowerList=new List<bool>();
            List<DIVA_PORT_TYPE_CLR> portList = new List<DIVA_PORT_TYPE_CLR>();
            List<uint> displayUIDList = new List<uint>();
            List<string> edidFileList = new List<string>();

            if (GlobalDetails.Count == 0)
            {
                MessageBox.Show("List is empty. Add something and do plug");
                return;
            }

            for (int i = 0; i < GlobalDetails.Count; i++)
            {
                plugList.Add(GlobalDetails[i].Plug);
                lowPowerList.Add(GlobalDetails[i].IsLowPower);
                portList.Add(GlobalDetails[i].Port);
                displayUIDList.Add(GlobalDetails[i].ulDisplayUID);
                edidFileList.Add(GlobalDetails[i].EDIDFileName);
            }

            Helper.ULT_FW_PlugDisplay(plugList, portList, displayUIDList, edidFileList, lowPowerList);
            
            ClearDetails();
        }

        private void btClear_Click(object sender, EventArgs e)
        {
            ClearDetails();
        }

        private void ClearDetails()
        {
            dataGridViewDetailsBindingSource.DataSource = null;
            GlobalDetails.Clear();
        }

        private void cbPort_SelectedValueChanged(object sender, EventArgs e)
        {
            cbDisplayUID.Text = "";
            cbDisplayUID.Items.Clear();

            string currentItem = cbPort.SelectedItem.ToString();

            EnumeratedDisplays.ForEach(item =>
            {
                if (item.PortType.ToString() == currentItem)
                    cbDisplayUID.Items.Add(item.DisplayUID.ToString("X"));
            });

            if (cbDisplayUID.Items.Count > 0)
                cbDisplayUID.SelectedIndex = 0;
        }

        private void cbDisplayUID_SelectedValueChanged(object sender, EventArgs e)
        {
            bool status = false;
            uint displayUID = Convert.ToUInt32(cbDisplayUID.Text, 16);
            if (displayUID != 0)
                status = Helper.GetDeviceConnectedStatus(displayUID);

            if (status)
                lbAttachedStatus.Text = "Attached";
            else
                lbAttachedStatus.Text = "Not Attached";
        }

        private void btAdd_Click(object sender, EventArgs e)
        {
            Details d = new Details();
            d.EDIDFileName = tbEDID.Text;
            d.Port = (DIVA_PORT_TYPE_CLR)Enum.Parse(typeof(DIVA_PORT_TYPE_CLR), cbPort.Text);
            d.ulDisplayUID = Convert.ToUInt32(cbDisplayUID.Text, 16);

            d.Plug = checkBoxPlug.Checked == true ? true : false;
            d.IsLowPower = checkBoxLowPower.Checked == true ? true : false;   
         
            GlobalDetails.Add(d);

            LoadDataGridView(GlobalDetails);
            
        }
        private void LoadDataGridView(List<Details> GlobalDetails)
        {
            List<DataGridViewDetails> tempDetailsList = new List<DataGridViewDetails>();
            GlobalDetails.ForEach(item =>
            {
                DataGridViewDetails tempDGVDetails = new DataGridViewDetails();
                tempDGVDetails.Port = item.Port.ToString();
                tempDGVDetails.DisplayUID = item.ulDisplayUID.ToString("X");
                tempDGVDetails.EDIDFileName = item.EDIDFileName;
                tempDGVDetails.Plug = item.Plug ? "Plug" : "UnPlug";
                tempDGVDetails.IsLowPower = item.IsLowPower ? "LowPower" : "Normal";
                
                tempDetailsList.Add(tempDGVDetails);
            });

            dataGridViewDetailsBindingSource.DataSource = tempDetailsList;
            dataGridViewDisplaySnapshot.Show();
        }
        private void btEnableULT_Click(object sender, EventArgs e)
        {
            Helper.EnableULT(true);
            Helper.EnableFeature(true, DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM);
        }

        private void btDisableULT_Click(object sender, EventArgs e)
        {
            Helper.EnableULT(false);
        }

        private void btBrowse_Click(object sender, EventArgs e)
        {
            DialogResult res = DialogBoxEDID.ShowDialog();
            tbEDID.Text = DialogBoxEDID.FileName;
        }
    }
    public class DataGridViewDetails
    {
        public string Port { get; set; }
        public string DisplayUID { get; set; }
        public string Plug { get; set; }
        public string IsLowPower { get; set; }
        public string EDIDFileName { get; set; }
    }
}
