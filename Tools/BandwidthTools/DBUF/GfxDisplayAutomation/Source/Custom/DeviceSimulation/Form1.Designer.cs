namespace Intel.VPG.Display.Automation
{
    partial class DeviceSimulationTool
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
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.btClear = new System.Windows.Forms.Button();
            this.btHotplug = new System.Windows.Forms.Button();
            this.DialogBoxEDID = new System.Windows.Forms.OpenFileDialog();
            this.btEnableULT = new System.Windows.Forms.Button();
            this.btDisableULT = new System.Windows.Forms.Button();
            this.label8 = new System.Windows.Forms.Label();
            this.dataGridViewDisplaySnapshot = new System.Windows.Forms.DataGridView();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.pictureBoxLogo = new System.Windows.Forms.PictureBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.btAdd = new System.Windows.Forms.Button();
            this.label5 = new System.Windows.Forms.Label();
            this.checkBoxLowPower = new System.Windows.Forms.CheckBox();
            this.checkBoxPlug = new System.Windows.Forms.CheckBox();
            this.lbAttachedStatus = new System.Windows.Forms.Label();
            this.cbDisplayUID = new System.Windows.Forms.ComboBox();
            this.btBrowse = new System.Windows.Forms.Button();
            this.tbEDID = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.cbPort = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.label1 = new System.Windows.Forms.Label();
            this.portDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.displayUIDDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.plugDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.isLowPowerDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.eDIDFileNameDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewDetailsBindingSource = new System.Windows.Forms.BindingSource(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewDisplaySnapshot)).BeginInit();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxLogo)).BeginInit();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewDetailsBindingSource)).BeginInit();
            this.SuspendLayout();
            // 
            // btClear
            // 
            this.btClear.Location = new System.Drawing.Point(552, 149);
            this.btClear.Name = "btClear";
            this.btClear.Size = new System.Drawing.Size(109, 23);
            this.btClear.TabIndex = 8;
            this.btClear.Text = "Clear List";
            this.btClear.UseVisualStyleBackColor = true;
            this.btClear.Click += new System.EventHandler(this.btClear_Click);
            // 
            // btHotplug
            // 
            this.btHotplug.Location = new System.Drawing.Point(223, 404);
            this.btHotplug.Name = "btHotplug";
            this.btHotplug.Size = new System.Drawing.Size(142, 23);
            this.btHotplug.TabIndex = 13;
            this.btHotplug.Text = "Perform Hotplug/Unplug";
            this.btHotplug.UseVisualStyleBackColor = true;
            this.btHotplug.Click += new System.EventHandler(this.btHotplug_Click);
            // 
            // DialogBoxEDID
            // 
            this.DialogBoxEDID.FileName = "openFileDialog1";
            // 
            // btEnableULT
            // 
            this.btEnableULT.Location = new System.Drawing.Point(13, 18);
            this.btEnableULT.Margin = new System.Windows.Forms.Padding(2);
            this.btEnableULT.Name = "btEnableULT";
            this.btEnableULT.Size = new System.Drawing.Size(99, 35);
            this.btEnableULT.TabIndex = 18;
            this.btEnableULT.Text = "Enable DFT FW";
            this.btEnableULT.UseVisualStyleBackColor = true;
            this.btEnableULT.Click += new System.EventHandler(this.btEnableULT_Click);
            // 
            // btDisableULT
            // 
            this.btDisableULT.Location = new System.Drawing.Point(552, 18);
            this.btDisableULT.Margin = new System.Windows.Forms.Padding(2);
            this.btDisableULT.Name = "btDisableULT";
            this.btDisableULT.Size = new System.Drawing.Size(107, 35);
            this.btDisableULT.TabIndex = 19;
            this.btDisableULT.Text = "Disable DFT FW";
            this.btDisableULT.UseVisualStyleBackColor = true;
            this.btDisableULT.Click += new System.EventHandler(this.btDisableULT_Click);
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(581, 418);
            this.label8.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(88, 13);
            this.label8.TabIndex = 25;
            this.label8.Text = "Internal Use Only";
            // 
            // dataGridViewDisplaySnapshot
            // 
            this.dataGridViewDisplaySnapshot.AllowUserToAddRows = false;
            this.dataGridViewDisplaySnapshot.AllowUserToDeleteRows = false;
            this.dataGridViewDisplaySnapshot.AutoGenerateColumns = false;
            this.dataGridViewDisplaySnapshot.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewDisplaySnapshot.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.portDataGridViewTextBoxColumn,
            this.displayUIDDataGridViewTextBoxColumn,
            this.plugDataGridViewTextBoxColumn,
            this.isLowPowerDataGridViewTextBoxColumn,
            this.eDIDFileNameDataGridViewTextBoxColumn});
            this.dataGridViewDisplaySnapshot.DataSource = this.dataGridViewDetailsBindingSource;
            this.dataGridViewDisplaySnapshot.Location = new System.Drawing.Point(11, 17);
            this.dataGridViewDisplaySnapshot.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewDisplaySnapshot.Name = "dataGridViewDisplaySnapshot";
            this.dataGridViewDisplaySnapshot.ReadOnly = true;
            this.dataGridViewDisplaySnapshot.RowTemplate.Height = 24;
            this.dataGridViewDisplaySnapshot.Size = new System.Drawing.Size(536, 154);
            this.dataGridViewDisplaySnapshot.TabIndex = 28;
            // 
            // groupBox1
            // 
            this.groupBox1.BackColor = System.Drawing.Color.White;
            this.groupBox1.Controls.Add(this.pictureBoxLogo);
            this.groupBox1.Controls.Add(this.dataGridViewDisplaySnapshot);
            this.groupBox1.Controls.Add(this.btClear);
            this.groupBox1.Location = new System.Drawing.Point(2, 202);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(2);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(2);
            this.groupBox1.Size = new System.Drawing.Size(667, 181);
            this.groupBox1.TabIndex = 29;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Displays Snapshot ";
            // 
            // pictureBoxLogo
            // 
            this.pictureBoxLogo.Location = new System.Drawing.Point(551, 38);
            this.pictureBoxLogo.Margin = new System.Windows.Forms.Padding(2);
            this.pictureBoxLogo.Name = "pictureBoxLogo";
            this.pictureBoxLogo.Size = new System.Drawing.Size(109, 81);
            this.pictureBoxLogo.TabIndex = 29;
            this.pictureBoxLogo.TabStop = false;
            // 
            // groupBox2
            // 
            this.groupBox2.BackColor = System.Drawing.SystemColors.GradientInactiveCaption;
            this.groupBox2.Controls.Add(this.btAdd);
            this.groupBox2.Controls.Add(this.label5);
            this.groupBox2.Controls.Add(this.checkBoxLowPower);
            this.groupBox2.Controls.Add(this.checkBoxPlug);
            this.groupBox2.Controls.Add(this.lbAttachedStatus);
            this.groupBox2.Controls.Add(this.cbDisplayUID);
            this.groupBox2.Controls.Add(this.btBrowse);
            this.groupBox2.Controls.Add(this.tbEDID);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.cbPort);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Location = new System.Drawing.Point(0, 64);
            this.groupBox2.Margin = new System.Windows.Forms.Padding(2);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Padding = new System.Windows.Forms.Padding(2);
            this.groupBox2.Size = new System.Drawing.Size(666, 136);
            this.groupBox2.TabIndex = 30;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Display parameters";
            // 
            // btAdd
            // 
            this.btAdd.Location = new System.Drawing.Point(467, 87);
            this.btAdd.Name = "btAdd";
            this.btAdd.Size = new System.Drawing.Size(75, 23);
            this.btAdd.TabIndex = 34;
            this.btAdd.Text = "Add";
            this.btAdd.UseVisualStyleBackColor = true;
            this.btAdd.Click += new System.EventHandler(this.btAdd_Click);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(381, 93);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(61, 13);
            this.label5.TabIndex = 33;
            this.label5.Text = "Add To List";
            // 
            // checkBoxLowPower
            // 
            this.checkBoxLowPower.AutoSize = true;
            this.checkBoxLowPower.Location = new System.Drawing.Point(532, 33);
            this.checkBoxLowPower.Margin = new System.Windows.Forms.Padding(2);
            this.checkBoxLowPower.Name = "checkBoxLowPower";
            this.checkBoxLowPower.Size = new System.Drawing.Size(101, 17);
            this.checkBoxLowPower.TabIndex = 32;
            this.checkBoxLowPower.Text = "LowPowerState";
            this.checkBoxLowPower.UseVisualStyleBackColor = true;
            // 
            // checkBoxPlug
            // 
            this.checkBoxPlug.AutoSize = true;
            this.checkBoxPlug.Checked = true;
            this.checkBoxPlug.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxPlug.Location = new System.Drawing.Point(437, 33);
            this.checkBoxPlug.Margin = new System.Windows.Forms.Padding(2);
            this.checkBoxPlug.Name = "checkBoxPlug";
            this.checkBoxPlug.Size = new System.Drawing.Size(84, 17);
            this.checkBoxPlug.TabIndex = 31;
            this.checkBoxPlug.Text = "Plug Display";
            this.checkBoxPlug.UseVisualStyleBackColor = true;
            // 
            // lbAttachedStatus
            // 
            this.lbAttachedStatus.AutoSize = true;
            this.lbAttachedStatus.Location = new System.Drawing.Point(322, 33);
            this.lbAttachedStatus.Name = "lbAttachedStatus";
            this.lbAttachedStatus.Size = new System.Drawing.Size(74, 13);
            this.lbAttachedStatus.TabIndex = 30;
            this.lbAttachedStatus.Text = "Device Status";
            // 
            // cbDisplayUID
            // 
            this.cbDisplayUID.FormattingEnabled = true;
            this.cbDisplayUID.Location = new System.Drawing.Point(228, 29);
            this.cbDisplayUID.Name = "cbDisplayUID";
            this.cbDisplayUID.Size = new System.Drawing.Size(76, 21);
            this.cbDisplayUID.TabIndex = 29;
            this.cbDisplayUID.SelectedValueChanged += new System.EventHandler(this.cbDisplayUID_SelectedValueChanged);
            // 
            // btBrowse
            // 
            this.btBrowse.Location = new System.Drawing.Point(232, 82);
            this.btBrowse.Name = "btBrowse";
            this.btBrowse.Size = new System.Drawing.Size(75, 23);
            this.btBrowse.TabIndex = 28;
            this.btBrowse.Text = "Browse";
            this.btBrowse.UseVisualStyleBackColor = true;
            this.btBrowse.Click += new System.EventHandler(this.btBrowse_Click);
            // 
            // tbEDID
            // 
            this.tbEDID.Location = new System.Drawing.Point(61, 84);
            this.tbEDID.Name = "tbEDID";
            this.tbEDID.Size = new System.Drawing.Size(165, 20);
            this.tbEDID.TabIndex = 27;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(22, 87);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(33, 13);
            this.label3.TabIndex = 25;
            this.label3.Text = "EDID";
            // 
            // cbPort
            // 
            this.cbPort.FormattingEnabled = true;
            this.cbPort.Location = new System.Drawing.Point(61, 30);
            this.cbPort.Name = "cbPort";
            this.cbPort.Size = new System.Drawing.Size(154, 21);
            this.cbPort.TabIndex = 24;
            this.cbPort.SelectedValueChanged += new System.EventHandler(this.cbPort_SelectedValueChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(22, 32);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(26, 13);
            this.label2.TabIndex = 23;
            this.label2.Text = "Port";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.label1);
            this.groupBox3.Controls.Add(this.groupBox2);
            this.groupBox3.Controls.Add(this.groupBox1);
            this.groupBox3.Controls.Add(this.btEnableULT);
            this.groupBox3.Controls.Add(this.btDisableULT);
            this.groupBox3.Location = new System.Drawing.Point(9, 10);
            this.groupBox3.Margin = new System.Windows.Forms.Padding(2);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Padding = new System.Windows.Forms.Padding(2);
            this.groupBox3.Size = new System.Drawing.Size(667, 427);
            this.groupBox3.TabIndex = 31;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "DeviceSimulationTool";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 13F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(192)))));
            this.label1.Location = new System.Drawing.Point(235, 17);
            this.label1.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(204, 22);
            this.label1.TabIndex = 31;
            this.label1.Text = "DeviceSimulationTool";
            // 
            // portDataGridViewTextBoxColumn
            // 
            this.portDataGridViewTextBoxColumn.DataPropertyName = "Port";
            this.portDataGridViewTextBoxColumn.HeaderText = "Port";
            this.portDataGridViewTextBoxColumn.Name = "portDataGridViewTextBoxColumn";
            this.portDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // displayUIDDataGridViewTextBoxColumn
            // 
            this.displayUIDDataGridViewTextBoxColumn.DataPropertyName = "DisplayUID";
            this.displayUIDDataGridViewTextBoxColumn.HeaderText = "DisplayUID";
            this.displayUIDDataGridViewTextBoxColumn.Name = "displayUIDDataGridViewTextBoxColumn";
            this.displayUIDDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // plugDataGridViewTextBoxColumn
            // 
            this.plugDataGridViewTextBoxColumn.DataPropertyName = "Plug";
            this.plugDataGridViewTextBoxColumn.HeaderText = "Plug";
            this.plugDataGridViewTextBoxColumn.Name = "plugDataGridViewTextBoxColumn";
            this.plugDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // isLowPowerDataGridViewTextBoxColumn
            // 
            this.isLowPowerDataGridViewTextBoxColumn.DataPropertyName = "IsLowPower";
            this.isLowPowerDataGridViewTextBoxColumn.HeaderText = "IsLowPower";
            this.isLowPowerDataGridViewTextBoxColumn.Name = "isLowPowerDataGridViewTextBoxColumn";
            this.isLowPowerDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // eDIDFileNameDataGridViewTextBoxColumn
            // 
            this.eDIDFileNameDataGridViewTextBoxColumn.DataPropertyName = "EDIDFileName";
            this.eDIDFileNameDataGridViewTextBoxColumn.HeaderText = "EDIDFileName";
            this.eDIDFileNameDataGridViewTextBoxColumn.Name = "eDIDFileNameDataGridViewTextBoxColumn";
            this.eDIDFileNameDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // dataGridViewDetailsBindingSource
            // 
            this.dataGridViewDetailsBindingSource.DataSource = typeof(Intel.VPG.Display.Automation.DataGridViewDetails);
            // 
            // DeviceSimulationTool
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(685, 444);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.btHotplug);
            this.Controls.Add(this.groupBox3);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.Name = "DeviceSimulationTool";
            this.Text = " ";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.Form1_FormClosed);
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewDisplaySnapshot)).EndInit();
            this.groupBox1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxLogo)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewDetailsBindingSource)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btClear;
        private System.Windows.Forms.Button btHotplug;
        private System.Windows.Forms.OpenFileDialog DialogBoxEDID;
        private System.Windows.Forms.Button btEnableULT;
        private System.Windows.Forms.Button btDisableULT;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.DataGridView dataGridViewDisplaySnapshot;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.PictureBox pictureBoxLogo;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button btAdd;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.CheckBox checkBoxLowPower;
        private System.Windows.Forms.CheckBox checkBoxPlug;
        private System.Windows.Forms.Label lbAttachedStatus;
        private System.Windows.Forms.ComboBox cbDisplayUID;
        private System.Windows.Forms.Button btBrowse;
        private System.Windows.Forms.TextBox tbEDID;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ComboBox cbPort;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DataGridViewTextBoxColumn portDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn displayUIDDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn plugDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn isLowPowerDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn eDIDFileNameDataGridViewTextBoxColumn;
        private System.Windows.Forms.BindingSource dataGridViewDetailsBindingSource;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Label label1;
    }
}

