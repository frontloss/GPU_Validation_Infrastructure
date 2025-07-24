using System.Diagnostics;
using System.Reflection;
using System.IO;
namespace AudioEndpointVerification
{
    partial class Audio
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
            KillProcess("AudioEndpointVerification");
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            string ToolV = FileVersionInfo.GetVersionInfo(Assembly.GetExecutingAssembly().Location).FileVersion;
            this.components = new System.ComponentModel.Container();
            this.groupBox_Control = new System.Windows.Forms.GroupBox();
            this.ReadExtnReg = new System.Windows.Forms.Button();
            this.textBoxRegReadValue = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.textBoxRegOffset = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.GetSetAudioTopology = new System.Windows.Forms.GroupBox();
            this.label3 = new System.Windows.Forms.Label();
            this.SetAudioEndPntCB = new System.Windows.Forms.CheckedListBox();
            this.PlayBkAudTextBox = new System.Windows.Forms.TextBox();
            this.AudTopologytextBox = new System.Windows.Forms.TextBox();
            this.AudioTopology = new System.Windows.Forms.Label();
            this.ApplyBtn = new System.Windows.Forms.Button();
            this.groupBoxRegisterControl = new System.Windows.Forms.GroupBox();
            this.RegDataGridView = new System.Windows.Forms.DataGridView();
            this.DisplayHierarchy = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.AudioSupport = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.AUD_PIN_ELD_RegTextBox = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.RegOffsetTextBox = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.CloseBtn = new System.Windows.Forms.Button();
            this.GetEndpointbutton = new System.Windows.Forms.Button();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.TextBox_Audio_Ver = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.TextBox_Gfx_Ver = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.TextBox_Bios = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.TextBox_Platform = new System.Windows.Forms.TextBox();
            this.label12 = new System.Windows.Forms.Label();
            this.ResetRegReadBtn = new System.Windows.Forms.Button();
            this.pictureBoxLogo = new System.Windows.Forms.PictureBox();
            this.displayTypeDataGridViewTextBoxColumn1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.pipeDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.regValueDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.statusDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.audioRegDataWrapperBindingSource = new System.Windows.Forms.BindingSource(this.components);
            this.audioDispInfoBindingSource = new System.Windows.Forms.BindingSource(this.components);
            this.groupBox_Control.SuspendLayout();
            this.GetSetAudioTopology.SuspendLayout();
            this.groupBoxRegisterControl.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.RegDataGridView)).BeginInit();
            this.groupBox3.SuspendLayout();
            this.groupBox4.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxLogo)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.audioRegDataWrapperBindingSource)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.audioDispInfoBindingSource)).BeginInit();
            this.SuspendLayout();
            // 
            // groupBox_Control
            // 
            this.groupBox_Control.Controls.Add(this.ResetRegReadBtn);
            this.groupBox_Control.Controls.Add(this.ReadExtnReg);
            this.groupBox_Control.Controls.Add(this.textBoxRegReadValue);
            this.groupBox_Control.Controls.Add(this.label2);
            this.groupBox_Control.Controls.Add(this.textBoxRegOffset);
            this.groupBox_Control.Controls.Add(this.label1);
            this.groupBox_Control.Controls.Add(this.GetSetAudioTopology);
            this.groupBox_Control.Controls.Add(this.groupBoxRegisterControl);
            this.groupBox_Control.Location = new System.Drawing.Point(14, 115);
            this.groupBox_Control.Margin = new System.Windows.Forms.Padding(2);
            this.groupBox_Control.Name = "groupBox_Control";
            this.groupBox_Control.Padding = new System.Windows.Forms.Padding(2);
            this.groupBox_Control.Size = new System.Drawing.Size(656, 263);
            this.groupBox_Control.TabIndex = 0;
            this.groupBox_Control.TabStop = false;
            this.groupBox_Control.Text = "AudioInformation";
            // 
            // ReadExtnReg
            // 
            this.ReadExtnReg.Location = new System.Drawing.Point(454, 91);
            this.ReadExtnReg.Name = "ReadExtnReg";
            this.ReadExtnReg.Size = new System.Drawing.Size(96, 23);
            this.ReadExtnReg.TabIndex = 15;
            this.ReadExtnReg.Text = "Read Register";
            this.ReadExtnReg.UseVisualStyleBackColor = true;
            this.ReadExtnReg.Click += new System.EventHandler(this.ReadExtnReg_Click);
            // 
            // textBoxRegReadValue
            // 
            this.textBoxRegReadValue.Location = new System.Drawing.Point(533, 52);
            this.textBoxRegReadValue.Name = "textBoxRegReadValue";
            this.textBoxRegReadValue.Size = new System.Drawing.Size(119, 20);
            this.textBoxRegReadValue.TabIndex = 14;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(451, 57);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(79, 13);
            this.label2.TabIndex = 13;
            this.label2.Text = "Register Value:";
            // 
            // textBoxRegOffset
            // 
            this.textBoxRegOffset.Location = new System.Drawing.Point(533, 26);
            this.textBoxRegOffset.Name = "textBoxRegOffset";
            this.textBoxRegOffset.Size = new System.Drawing.Size(119, 20);
            this.textBoxRegOffset.TabIndex = 12;
            this.textBoxRegOffset.TextChanged += new System.EventHandler(this.textBoxRegOffset_TextChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(450, 29);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(80, 13);
            this.label1.TabIndex = 11;
            this.label1.Text = "Register Offset:";
            // 
            // GetSetAudioTopology
            // 
            this.GetSetAudioTopology.Controls.Add(this.label3);
            this.GetSetAudioTopology.Controls.Add(this.SetAudioEndPntCB);
            this.GetSetAudioTopology.Controls.Add(this.PlayBkAudTextBox);
            this.GetSetAudioTopology.Controls.Add(this.AudTopologytextBox);
            this.GetSetAudioTopology.Controls.Add(this.AudioTopology);
            this.GetSetAudioTopology.Controls.Add(this.ApplyBtn);
            this.GetSetAudioTopology.Location = new System.Drawing.Point(4, 19);
            this.GetSetAudioTopology.Margin = new System.Windows.Forms.Padding(2);
            this.GetSetAudioTopology.Name = "GetSetAudioTopology";
            this.GetSetAudioTopology.Padding = new System.Windows.Forms.Padding(2);
            this.GetSetAudioTopology.Size = new System.Drawing.Size(441, 103);
            this.GetSetAudioTopology.TabIndex = 10;
            this.GetSetAudioTopology.TabStop = false;
            this.GetSetAudioTopology.Text = "Get/Set AudioTopology";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.ForeColor = System.Drawing.Color.Tomato;
            this.label3.Location = new System.Drawing.Point(194, 10);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(93, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "PlaybackDevices:";
            // 
            // SetAudioEndPntCB
            // 
            this.SetAudioEndPntCB.FormattingEnabled = true;
            this.SetAudioEndPntCB.Items.AddRange(new object[] {
            "Single Source",
            "Multiple Source"});
            this.SetAudioEndPntCB.Location = new System.Drawing.Point(8, 17);
            this.SetAudioEndPntCB.Margin = new System.Windows.Forms.Padding(2);
            this.SetAudioEndPntCB.Name = "SetAudioEndPntCB";
            this.SetAudioEndPntCB.Size = new System.Drawing.Size(112, 34);
            this.SetAudioEndPntCB.TabIndex = 8;
            this.SetAudioEndPntCB.UseTabStops = false;
            this.SetAudioEndPntCB.SelectedIndexChanged += new System.EventHandler(this.SetAudioEndPntCB_SelectedIndexChanged);
            // 
            // PlayBkAudTextBox
            // 
            this.PlayBkAudTextBox.Location = new System.Drawing.Point(197, 27);
            this.PlayBkAudTextBox.Multiline = true;
            this.PlayBkAudTextBox.Name = "PlayBkAudTextBox";
            this.PlayBkAudTextBox.Size = new System.Drawing.Size(235, 47);
            this.PlayBkAudTextBox.TabIndex = 5;
            // 
            // AudTopologytextBox
            // 
            this.AudTopologytextBox.Location = new System.Drawing.Point(89, 79);
            this.AudTopologytextBox.Margin = new System.Windows.Forms.Padding(2);
            this.AudTopologytextBox.Name = "AudTopologytextBox";
            this.AudTopologytextBox.Size = new System.Drawing.Size(183, 20);
            this.AudTopologytextBox.TabIndex = 7;
            // 
            // AudioTopology
            // 
            this.AudioTopology.AutoSize = true;
            this.AudioTopology.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.AudioTopology.Location = new System.Drawing.Point(4, 82);
            this.AudioTopology.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.AudioTopology.Name = "AudioTopology";
            this.AudioTopology.Size = new System.Drawing.Size(81, 13);
            this.AudioTopology.TabIndex = 6;
            this.AudioTopology.Text = "AudioTopology:";
            // 
            // ApplyBtn
            // 
            this.ApplyBtn.Location = new System.Drawing.Point(129, 20);
            this.ApplyBtn.Margin = new System.Windows.Forms.Padding(2);
            this.ApplyBtn.Name = "ApplyBtn";
            this.ApplyBtn.Size = new System.Drawing.Size(58, 26);
            this.ApplyBtn.TabIndex = 9;
            this.ApplyBtn.Text = "Apply";
            this.ApplyBtn.UseVisualStyleBackColor = true;
            this.ApplyBtn.Click += new System.EventHandler(this.ApplyBtn_Click);
            // 
            // groupBoxRegisterControl
            // 
            this.groupBoxRegisterControl.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.groupBoxRegisterControl.Controls.Add(this.RegDataGridView);
            this.groupBoxRegisterControl.Controls.Add(this.AUD_PIN_ELD_RegTextBox);
            this.groupBoxRegisterControl.Controls.Add(this.label6);
            this.groupBoxRegisterControl.Controls.Add(this.label5);
            this.groupBoxRegisterControl.Controls.Add(this.RegOffsetTextBox);
            this.groupBoxRegisterControl.Controls.Add(this.label4);
            this.groupBoxRegisterControl.Location = new System.Drawing.Point(5, 126);
            this.groupBoxRegisterControl.Margin = new System.Windows.Forms.Padding(2);
            this.groupBoxRegisterControl.Name = "groupBoxRegisterControl";
            this.groupBoxRegisterControl.Padding = new System.Windows.Forms.Padding(2);
            this.groupBoxRegisterControl.Size = new System.Drawing.Size(647, 135);
            this.groupBoxRegisterControl.TabIndex = 1;
            this.groupBoxRegisterControl.TabStop = false;
            this.groupBoxRegisterControl.Text = "RegisterVerification (AUD_PIN_ELD_CP_VLD)";
            // 
            // RegDataGridView
            // 
            this.RegDataGridView.AllowUserToAddRows = false;
            this.RegDataGridView.AllowUserToDeleteRows = false;
            this.RegDataGridView.AutoGenerateColumns = false;
            this.RegDataGridView.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.RegDataGridView.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.DisplayedCells;
            this.RegDataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.RegDataGridView.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.displayTypeDataGridViewTextBoxColumn1,
            this.DisplayHierarchy,
            this.AudioSupport,
            this.pipeDataGridViewTextBoxColumn,
            this.regValueDataGridViewTextBoxColumn,
            this.statusDataGridViewTextBoxColumn});
            this.RegDataGridView.DataSource = this.audioRegDataWrapperBindingSource;
            this.RegDataGridView.Location = new System.Drawing.Point(0, 46);
            this.RegDataGridView.Name = "RegDataGridView";
            this.RegDataGridView.Size = new System.Drawing.Size(642, 83);
            this.RegDataGridView.TabIndex = 5;
            // 
            // DisplayHierarchy
            // 
            this.DisplayHierarchy.DataPropertyName = "DisplayHierarchy";
            this.DisplayHierarchy.HeaderText = "DisplayHierarchy";
            this.DisplayHierarchy.Name = "DisplayHierarchy";
            // 
            // AudioSupport
            // 
            this.AudioSupport.DataPropertyName = "AudioSupport";
            this.AudioSupport.HeaderText = "AudioSupport";
            this.AudioSupport.Name = "AudioSupport";
            // 
            // AUD_PIN_ELD_RegTextBox
            // 
            this.AUD_PIN_ELD_RegTextBox.Location = new System.Drawing.Point(233, 21);
            this.AUD_PIN_ELD_RegTextBox.Name = "AUD_PIN_ELD_RegTextBox";
            this.AUD_PIN_ELD_RegTextBox.Size = new System.Drawing.Size(183, 20);
            this.AUD_PIN_ELD_RegTextBox.TabIndex = 4;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.ForeColor = System.Drawing.Color.DarkViolet;
            this.label6.Location = new System.Drawing.Point(157, 24);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(76, 13);
            this.label6.TabIndex = 3;
            this.label6.Text = "RegisterValue:";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(167, 18);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(0, 13);
            this.label5.TabIndex = 2;
            // 
            // RegOffsetTextBox
            // 
            this.RegOffsetTextBox.Location = new System.Drawing.Point(82, 20);
            this.RegOffsetTextBox.Name = "RegOffsetTextBox";
            this.RegOffsetTextBox.Size = new System.Drawing.Size(69, 20);
            this.RegOffsetTextBox.TabIndex = 1;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.ForeColor = System.Drawing.Color.BlueViolet;
            this.label4.Location = new System.Drawing.Point(5, 24);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(77, 13);
            this.label4.TabIndex = 0;
            this.label4.Text = "RegisterOffset:";
            // 
            // CloseBtn
            // 
            this.CloseBtn.Location = new System.Drawing.Point(135, 381);
            this.CloseBtn.Name = "CloseBtn";
            this.CloseBtn.Size = new System.Drawing.Size(52, 23);
            this.CloseBtn.TabIndex = 16;
            this.CloseBtn.Text = "Close";
            this.CloseBtn.UseVisualStyleBackColor = true;
            this.CloseBtn.Click += new System.EventHandler(this.CloseBtn_Click);
            // 
            // GetEndpointbutton
            // 
            this.GetEndpointbutton.Location = new System.Drawing.Point(12, 381);
            this.GetEndpointbutton.Name = "GetEndpointbutton";
            this.GetEndpointbutton.Size = new System.Drawing.Size(117, 23);
            this.GetEndpointbutton.TabIndex = 0;
            this.GetEndpointbutton.Text = "CheckAudioEndpoint";
            this.GetEndpointbutton.UseVisualStyleBackColor = true;
            this.GetEndpointbutton.Click += new System.EventHandler(this.GetEndpointbutton_Click);
            // 
            // groupBox3
            // 
            this.groupBox3.BackColor = System.Drawing.SystemColors.Info;
            this.groupBox3.Controls.Add(this.pictureBoxLogo);
            this.groupBox3.Controls.Add(this.groupBox4);
            this.groupBox3.Location = new System.Drawing.Point(12, 12);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(658, 98);
            this.groupBox3.TabIndex = 3;
            this.groupBox3.TabStop = false;
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.TextBox_Audio_Ver);
            this.groupBox4.Controls.Add(this.label9);
            this.groupBox4.Controls.Add(this.TextBox_Gfx_Ver);
            this.groupBox4.Controls.Add(this.label8);
            this.groupBox4.Controls.Add(this.TextBox_Bios);
            this.groupBox4.Controls.Add(this.label7);
            this.groupBox4.Controls.Add(this.TextBox_Platform);
            this.groupBox4.Controls.Add(this.label12);
            this.groupBox4.Location = new System.Drawing.Point(5, 15);
            this.groupBox4.Margin = new System.Windows.Forms.Padding(2);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Padding = new System.Windows.Forms.Padding(2);
            this.groupBox4.Size = new System.Drawing.Size(534, 77);
            this.groupBox4.TabIndex = 11;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "SystemInfo";
            // 
            // TextBox_Audio_Ver
            // 
            this.TextBox_Audio_Ver.Location = new System.Drawing.Point(383, 49);
            this.TextBox_Audio_Ver.Name = "TextBox_Audio_Ver";
            this.TextBox_Audio_Ver.Size = new System.Drawing.Size(146, 20);
            this.TextBox_Audio_Ver.TabIndex = 7;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label9.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.label9.Location = new System.Drawing.Point(279, 48);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(97, 15);
            this.label9.TabIndex = 6;
            this.label9.Text = "Audio Driver Ver:";
            // 
            // TextBox_Gfx_Ver
            // 
            this.TextBox_Gfx_Ver.Location = new System.Drawing.Point(382, 18);
            this.TextBox_Gfx_Ver.Name = "TextBox_Gfx_Ver";
            this.TextBox_Gfx_Ver.Size = new System.Drawing.Size(146, 20);
            this.TextBox_Gfx_Ver.TabIndex = 5;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.label8.Location = new System.Drawing.Point(279, 21);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(84, 15);
            this.label8.TabIndex = 4;
            this.label8.Text = "Gfx Driver Ver:";
            // 
            // TextBox_Bios
            // 
            this.TextBox_Bios.Location = new System.Drawing.Point(59, 47);
            this.TextBox_Bios.Name = "TextBox_Bios";
            this.TextBox_Bios.Size = new System.Drawing.Size(214, 20);
            this.TextBox_Bios.TabIndex = 3;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.label7.Location = new System.Drawing.Point(6, 49);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(34, 15);
            this.label7.TabIndex = 2;
            this.label7.Text = "Bios:";
            // 
            // TextBox_Platform
            // 
            this.TextBox_Platform.Location = new System.Drawing.Point(59, 21);
            this.TextBox_Platform.Name = "TextBox_Platform";
            this.TextBox_Platform.Size = new System.Drawing.Size(97, 20);
            this.TextBox_Platform.TabIndex = 1;
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label12.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.label12.Location = new System.Drawing.Point(6, 22);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(56, 15);
            this.label12.TabIndex = 0;
            this.label12.Text = "Platform:";
            // 
            // ResetRegReadBtn
            // 
            this.ResetRegReadBtn.Location = new System.Drawing.Point(556, 91);
            this.ResetRegReadBtn.Name = "ResetRegReadBtn";
            this.ResetRegReadBtn.Size = new System.Drawing.Size(91, 23);
            this.ResetRegReadBtn.TabIndex = 16;
            this.ResetRegReadBtn.Text = "Reset";
            this.ResetRegReadBtn.UseVisualStyleBackColor = true;
            this.ResetRegReadBtn.Click += new System.EventHandler(this.ResetRegReadBtn_Click);
            // 
            // pictureBoxLogo
            // 
            this.pictureBoxLogo.Location = new System.Drawing.Point(544, 19);
            this.pictureBoxLogo.Name = "pictureBoxLogo";
            this.pictureBoxLogo.Size = new System.Drawing.Size(100, 73);
            this.pictureBoxLogo.TabIndex = 12;
            this.pictureBoxLogo.TabStop = false;
            // 
            // displayTypeDataGridViewTextBoxColumn1
            // 
            this.displayTypeDataGridViewTextBoxColumn1.DataPropertyName = "DisplayType";
            this.displayTypeDataGridViewTextBoxColumn1.HeaderText = "DisplayType";
            this.displayTypeDataGridViewTextBoxColumn1.Name = "displayTypeDataGridViewTextBoxColumn1";
            // 
            // pipeDataGridViewTextBoxColumn
            // 
            this.pipeDataGridViewTextBoxColumn.DataPropertyName = "Pipe";
            this.pipeDataGridViewTextBoxColumn.HeaderText = "Pipe";
            this.pipeDataGridViewTextBoxColumn.Name = "pipeDataGridViewTextBoxColumn";
            // 
            // regValueDataGridViewTextBoxColumn
            // 
            this.regValueDataGridViewTextBoxColumn.DataPropertyName = "RegValue";
            this.regValueDataGridViewTextBoxColumn.HeaderText = "RegValue";
            this.regValueDataGridViewTextBoxColumn.Name = "regValueDataGridViewTextBoxColumn";
            // 
            // statusDataGridViewTextBoxColumn
            // 
            this.statusDataGridViewTextBoxColumn.DataPropertyName = "Status";
            this.statusDataGridViewTextBoxColumn.HeaderText = "Status";
            this.statusDataGridViewTextBoxColumn.Name = "statusDataGridViewTextBoxColumn";
            // 
            // audioRegDataWrapperBindingSource
            // 
            this.audioRegDataWrapperBindingSource.DataSource = typeof(AudioEndpointVerification.AudioRegDataWrapper);
            // 
            // audioDispInfoBindingSource
            // 
            this.audioDispInfoBindingSource.DataSource = typeof(AudioEndpointVerification.AudioDispInfo);
            // 
            // Audio
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(677, 410);
            this.Controls.Add(this.CloseBtn);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox_Control);
            this.Controls.Add(this.GetEndpointbutton);
            this.Margin = new System.Windows.Forms.Padding(2);
            this.Name = "Audio";
            this.Text = "Audio" + " (" + ToolV + ")";
            this.groupBox_Control.ResumeLayout(false);
            this.groupBox_Control.PerformLayout();
            this.GetSetAudioTopology.ResumeLayout(false);
            this.GetSetAudioTopology.PerformLayout();
            this.groupBoxRegisterControl.ResumeLayout(false);
            this.groupBoxRegisterControl.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.RegDataGridView)).EndInit();
            this.groupBox3.ResumeLayout(false);
            this.groupBox4.ResumeLayout(false);
            this.groupBox4.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxLogo)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.audioRegDataWrapperBindingSource)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.audioDispInfoBindingSource)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox_Control;
        private System.Windows.Forms.GroupBox groupBoxRegisterControl;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Button GetEndpointbutton;
        private System.Windows.Forms.TextBox PlayBkAudTextBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox AUD_PIN_ELD_RegTextBox;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox RegOffsetTextBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.DataGridView RegDataGridView;
        private System.Windows.Forms.BindingSource audioDispInfoBindingSource;
        private System.Windows.Forms.BindingSource audioRegDataWrapperBindingSource;
        private System.Windows.Forms.TextBox AudTopologytextBox;
        private System.Windows.Forms.Label AudioTopology;
        private System.Windows.Forms.GroupBox GetSetAudioTopology;
        private System.Windows.Forms.Button ApplyBtn;
        private System.Windows.Forms.CheckedListBox SetAudioEndPntCB;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.TextBox TextBox_Audio_Ver;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox TextBox_Gfx_Ver;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.TextBox TextBox_Bios;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox TextBox_Platform;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.TextBox textBoxRegReadValue;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox textBoxRegOffset;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button CloseBtn;
        private System.Windows.Forms.Button ReadExtnReg;
        private System.Windows.Forms.DataGridViewTextBoxColumn displayTypeDataGridViewTextBoxColumn1;
        private System.Windows.Forms.DataGridViewTextBoxColumn DisplayHierarchy;
        private System.Windows.Forms.DataGridViewTextBoxColumn AudioSupport;
        private System.Windows.Forms.DataGridViewTextBoxColumn pipeDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn regValueDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn statusDataGridViewTextBoxColumn;
        private System.Windows.Forms.Button ResetRegReadBtn;
        private System.Windows.Forms.PictureBox pictureBoxLogo;
    }
}

