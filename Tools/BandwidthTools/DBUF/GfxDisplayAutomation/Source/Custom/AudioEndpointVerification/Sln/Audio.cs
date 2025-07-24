using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using IgfxExtBridge_DotNet;
using System.Diagnostics;
using System.IO;

namespace AudioEndpointVerification
{
    public partial class Audio : Form
    {
        public Audio()
        {
            InitializeComponent();
            Image image = Image.FromFile(Directory.GetCurrentDirectory() + @"\Mapper\Logo.png");
            pictureBoxLogo.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBoxLogo.Image = image;

            GetEndpointbutton.Enabled = false;
            PlayBkAudTextBox.Enabled = false;
            ReadExtnReg.Enabled = false;
            ResetRegReadBtn.Enabled = false;
            groupBoxRegisterControl.Enabled = false;

            CommonExtension.Init();
            CommonExtension.DriverStatus();
            if (CommonExtension.driverInfo.GfxDriver.Status.ToLower() != DriverState.Running.ToString().ToLower())
                CommonExtension.ErrorMessage("Gfx Driver is not Enable!", ErrorCode.Error, true);
            if (CommonExtension.driverInfo.AudioDriver.Status.ToLower().Trim() != "ok")
                CommonExtension.ErrorMessage("Audio Driver is not Enable!", ErrorCode.Error, true);
            TextBox_Platform.Text = CommonExtension.GetplatformID();
            TextBox_Bios.Text = CommonExtension.GetBIOSVersion();
            TextBox_Gfx_Ver.Text = CommonExtension.driverInfo.GfxDriver.Version;
            TextBox_Audio_Ver.Text = CommonExtension.GetAudioDriverVersion();
            if (string.IsNullOrEmpty(TextBox_Audio_Ver.Text))
            {
                CommonExtension.ErrorMessage("External displays are not active!", ErrorCode.Error, true);
            }
            else
                GetEndpointbutton.Enabled = true;
            GetAudTopology();
        }

        public static void KillProcess(string argProcessName)
        {
            Process.GetProcessesByName(argProcessName).Where(p => p.ProcessName.ToLower().Equals(argProcessName.ToLower())).ToList().ForEach(p =>
            {
                p.Kill();
            });
        }

        private void GetAudTopology()
        {
            IGFX_ERROR_CODES igfxError = IGFX_ERROR_CODES.IGFX_SUCCESS;
            string errorDec = string.Empty;
            IGFX_AUDIO_FEATURE_INFO audFeture = new IGFX_AUDIO_FEATURE_INFO();
            audFeture.versionHeader.dwVersion = 1;
            APIExtensions.DisplayUtil.GetAudioTopology(ref audFeture, out igfxError, out errorDec);
            if (igfxError == IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                if (audFeture.dwAudioConfig > 1 && audFeture.dwNumberofAudio > 1)
                {
                    AudTopologytextBox.Text = "Multi Source";
                    SetAudioEndPntCB.SetItemChecked(1, true);
                }
                else if (audFeture.dwAudioConfig == 0 && audFeture.dwNumberofAudio == 0)
                {
                    AudTopologytextBox.Text = "Single Display";
                }
                else
                {
                    AudTopologytextBox.Text = "Single Source";
                    SetAudioEndPntCB.SetItemChecked(0, true);
                }

            }
            else
            {
                AudTopologytextBox.Text = "None";
                SetAudioEndPntCB.SetItemChecked(0, false);
                SetAudioEndPntCB.SetItemChecked(1, false);
            }
        }

        private void GetEndpointbutton_Click(object sender, EventArgs e)
        {
            if (CommonExtension.DriverStatus(true) == false)
            {
                RegOffsetTextBox.Text = null;
                AUD_PIN_ELD_RegTextBox.Text = null;
                RegDataGridView.DataSource = null;
                return;
            }
            PlayBkAudTextBox.Enabled = true;
            groupBoxRegisterControl.Enabled = true;
            RegDataGridView.DataSource = null;
            Thread.Sleep(2000);
            GetAudTopology();
            AudioEndpointData endpointData = new AudioEndpointData();
            PlayBkAudTextBox.Lines = endpointData.playBackDevices.ToArray();
            PlayBkAudTextBox.Show();

            List<AudioRegDataWrapper> regObj = new List<AudioRegDataWrapper>();
            GetAudioRegInfo regInfoData = new GetAudioRegInfo();
            regObj = regInfoData.ValidateRegister();

            RegOffsetTextBox.Text = regInfoData.offset;
            AUD_PIN_ELD_RegTextBox.Text = regInfoData.AUD_PIN_ELD_Reg_Value;

            RegDataGridView.DataSource = regObj;
            RegDataGridView.Show();

        }

        private void ApplyBtn_Click(object sender, EventArgs e)
        {
            if (CommonExtension.DriverStatus(true) == false)
            {
                PlayBkAudTextBox.Text = null;
                AudTopologytextBox.Text = null;
                SetAudioEndPntCB.SetItemChecked(0, false);
                SetAudioEndPntCB.SetItemChecked(1, false);
                return;
            }
            IGFX_ERROR_CODES igfxError = IGFX_ERROR_CODES.IGFX_SUCCESS;
            string errorDec = string.Empty;
            IGFX_AUDIO_FEATURE_INFO audFeture = new IGFX_AUDIO_FEATURE_INFO();
            audFeture.versionHeader.dwVersion = 1;
            if (SetAudioEndPntCB.SelectedIndex == 0)
                audFeture.dwAudioConfig = 1;
            else
                audFeture.dwAudioConfig = 2;
            APIExtensions.DisplayUtil.SetAudioTopology(ref audFeture, out igfxError, out errorDec);
            GetAudTopology();
        }

        private void SetAudioEndPntCB_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (SetAudioEndPntCB.SelectedIndex == 0)
                SetAudioEndPntCB.SetItemChecked(1, false);
            else
                SetAudioEndPntCB.SetItemChecked(0, false);
        }

        private void ReadExtnReg_Click(object sender, EventArgs e)
        {
            if (CommonExtension.DriverStatus(true) == false)
            {
                textBoxRegOffset.Text = null;
                textBoxRegReadValue.Text = null;
                return;
            }
            if (string.IsNullOrEmpty(textBoxRegOffset.Text))
            {
                MessageBox.Show("Please Specify register offset value");
                return;
            }
            DriverEscape driverEscape = new DriverEscape();
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = Convert.ToUInt32(textBoxRegOffset.Text.Trim(), 16);
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            if (!driverEscape.SetMethod(driverParams))
                MessageBox.Show("Failed to read Register with offset as " + driverData.input);
            else
            {
                textBoxRegReadValue.Text = driverData.output.ToString();
            }
        }

        private void ResetRegReadBtn_Click(object sender, EventArgs e)
        {
            textBoxRegOffset.Text = string.Empty;
            textBoxRegReadValue.Text = string.Empty;
        }

        private void CloseBtn_Click(object sender, EventArgs e)
        {
            System.Windows.Forms.Application.Exit();
        }

        private void textBoxRegOffset_TextChanged(object sender, EventArgs e)
        {
            ReadExtnReg.Enabled = true;
            ResetRegReadBtn.Enabled = true;
        }

    }
}
