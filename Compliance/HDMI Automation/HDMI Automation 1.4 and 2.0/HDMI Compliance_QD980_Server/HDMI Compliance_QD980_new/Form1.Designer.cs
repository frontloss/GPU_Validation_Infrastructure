namespace HDMI_Compliance_QD980_new
{
    partial class Form1
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
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.checkBox4 = new System.Windows.Forms.CheckBox();
            this.checkBox3 = new System.Windows.Forms.CheckBox();
            this.checkBox2 = new System.Windows.Forms.CheckBox();
            this.checkBox1 = new System.Windows.Forms.CheckBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.checkBox5 = new System.Windows.Forms.CheckBox();
            this.START_Button = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.Platform = new System.Windows.Forms.TextBox();
            this.DriverVersion = new System.Windows.Forms.TextBox();
            this.CLIENT_ADDRESS = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.SERVER_ADDRESS = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.IP_ADDRESS = new System.Windows.Forms.TextBox();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.label1 = new System.Windows.Forms.Label();
            this.Version = new System.Windows.Forms.TextBox();
            this.checkBox8 = new System.Windows.Forms.CheckBox();
            this.checkBox7 = new System.Windows.Forms.CheckBox();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.checkBox4);
            this.groupBox1.Controls.Add(this.checkBox3);
            this.groupBox1.Controls.Add(this.checkBox2);
            this.groupBox1.Controls.Add(this.checkBox1);
            this.groupBox1.Location = new System.Drawing.Point(49, 147);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(200, 141);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "HDMI Standard Compliance";
            this.groupBox1.Enter += new System.EventHandler(this.groupBox1_Enter);
            // 
            // checkBox4
            // 
            this.checkBox4.AutoSize = true;
            this.checkBox4.Location = new System.Drawing.Point(21, 112);
            this.checkBox4.Name = "checkBox4";
            this.checkBox4.Size = new System.Drawing.Size(167, 21);
            this.checkBox4.TabIndex = 3;
            this.checkBox4.Text = "HDMI 2.0 120 Frames";
            this.checkBox4.UseVisualStyleBackColor = true;
            this.checkBox4.CheckedChanged += new System.EventHandler(this.checkBox4_CheckedChanged);
            // 
            // checkBox3
            // 
            this.checkBox3.AutoSize = true;
            this.checkBox3.Location = new System.Drawing.Point(21, 85);
            this.checkBox3.Name = "checkBox3";
            this.checkBox3.Size = new System.Drawing.Size(151, 21);
            this.checkBox3.TabIndex = 2;
            this.checkBox3.Text = "HDMI 2.0 5 Frames";
            this.checkBox3.UseVisualStyleBackColor = true;
            this.checkBox3.CheckedChanged += new System.EventHandler(this.checkBox3_CheckedChanged);
            // 
            // checkBox2
            // 
            this.checkBox2.AutoSize = true;
            this.checkBox2.Location = new System.Drawing.Point(21, 58);
            this.checkBox2.Name = "checkBox2";
            this.checkBox2.Size = new System.Drawing.Size(175, 21);
            this.checkBox2.TabIndex = 1;
            this.checkBox2.Text = "HDMI 1.4b 120 Frames";
            this.checkBox2.UseVisualStyleBackColor = true;
            this.checkBox2.CheckedChanged += new System.EventHandler(this.checkBox2_CheckedChanged);
            // 
            // checkBox1
            // 
            this.checkBox1.AutoSize = true;
            this.checkBox1.Location = new System.Drawing.Point(21, 31);
            this.checkBox1.Name = "checkBox1";
            this.checkBox1.Size = new System.Drawing.Size(159, 21);
            this.checkBox1.TabIndex = 0;
            this.checkBox1.Text = "HDMI 1.4b 5 Frames";
            this.checkBox1.UseVisualStyleBackColor = true;
            this.checkBox1.CheckedChanged += new System.EventHandler(this.checkBox1_CheckedChanged);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.checkBox5);
            this.groupBox2.Location = new System.Drawing.Point(49, 312);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(200, 100);
            this.groupBox2.TabIndex = 1;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Custom Compliance";
            // 
            // checkBox5
            // 
            this.checkBox5.AutoSize = true;
            this.checkBox5.Location = new System.Drawing.Point(21, 34);
            this.checkBox5.Name = "checkBox5";
            this.checkBox5.Size = new System.Drawing.Size(123, 21);
            this.checkBox5.TabIndex = 0;
            this.checkBox5.Text = "Custom Modes";
            this.checkBox5.UseVisualStyleBackColor = true;
            this.checkBox5.CheckedChanged += new System.EventHandler(this.checkBox5_CheckedChanged);
            // 
            // START_Button
            // 
            this.START_Button.Location = new System.Drawing.Point(309, 370);
            this.START_Button.Name = "START_Button";
            this.START_Button.Size = new System.Drawing.Size(151, 65);
            this.START_Button.TabIndex = 2;
            this.START_Button.Text = "START";
            this.START_Button.UseVisualStyleBackColor = true;
            this.START_Button.Click += new System.EventHandler(this.START_Button_Click_1);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(288, 230);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(83, 17);
            this.label2.TabIndex = 5;
            this.label2.Text = "PLATFORM";
            this.label2.Click += new System.EventHandler(this.label2_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(288, 276);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(124, 17);
            this.label3.TabIndex = 6;
            this.label3.Text = "DRIVER VERSION";
            // 
            // Platform
            // 
            this.Platform.Location = new System.Drawing.Point(418, 230);
            this.Platform.Name = "Platform";
            this.Platform.Size = new System.Drawing.Size(201, 22);
            this.Platform.TabIndex = 7;
            // 
            // DriverVersion
            // 
            this.DriverVersion.Location = new System.Drawing.Point(418, 274);
            this.DriverVersion.Name = "DriverVersion";
            this.DriverVersion.Size = new System.Drawing.Size(201, 22);
            this.DriverVersion.TabIndex = 8;
            // 
            // CLIENT_ADDRESS
            // 
            this.CLIENT_ADDRESS.Location = new System.Drawing.Point(194, 67);
            this.CLIENT_ADDRESS.Name = "CLIENT_ADDRESS";
            this.CLIENT_ADDRESS.Size = new System.Drawing.Size(199, 22);
            this.CLIENT_ADDRESS.TabIndex = 10;
            this.CLIENT_ADDRESS.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(50, 70);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(128, 17);
            this.label4.TabIndex = 9;
            this.label4.Text = "CLIENT IP Address";
            // 
            // SERVER_ADDRESS
            // 
            this.SERVER_ADDRESS.Location = new System.Drawing.Point(194, 28);
            this.SERVER_ADDRESS.Name = "SERVER_ADDRESS";
            this.SERVER_ADDRESS.Size = new System.Drawing.Size(199, 22);
            this.SERVER_ADDRESS.TabIndex = 12;
            this.SERVER_ADDRESS.TextChanged += new System.EventHandler(this.textBox2_TextChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(50, 28);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(136, 17);
            this.label5.TabIndex = 11;
            this.label5.Text = "SERVER IP Address";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(50, 109);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(101, 17);
            this.label6.TabIndex = 3;
            this.label6.Text = "QD IP Address";
            this.label6.Click += new System.EventHandler(this.label1_Click);
            // 
            // IP_ADDRESS
            // 
            this.IP_ADDRESS.Location = new System.Drawing.Point(194, 106);
            this.IP_ADDRESS.Name = "IP_ADDRESS";
            this.IP_ADDRESS.Size = new System.Drawing.Size(199, 22);
            this.IP_ADDRESS.TabIndex = 4;
            this.IP_ADDRESS.TextChanged += new System.EventHandler(this.IP_ADDRESS_TextChanged);
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.label1);
            this.groupBox3.Controls.Add(this.Version);
            this.groupBox3.Controls.Add(this.checkBox8);
            this.groupBox3.Controls.Add(this.checkBox7);
            this.groupBox3.Location = new System.Drawing.Point(419, 28);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(200, 171);
            this.groupBox3.TabIndex = 13;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "QD Version";
            this.groupBox3.Enter += new System.EventHandler(this.groupBox3_Enter);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(29, 96);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(94, 17);
            this.label1.TabIndex = 15;
            this.label1.Text = "Enter Version";
            // 
            // Version
            // 
            this.Version.Location = new System.Drawing.Point(29, 119);
            this.Version.Name = "Version";
            this.Version.Size = new System.Drawing.Size(165, 22);
            this.Version.TabIndex = 14;
            // 
            // checkBox8
            // 
            this.checkBox8.AutoSize = true;
            this.checkBox8.Location = new System.Drawing.Point(17, 58);
            this.checkBox8.Name = "checkBox8";
            this.checkBox8.Size = new System.Drawing.Size(57, 21);
            this.checkBox8.TabIndex = 1;
            this.checkBox8.Text = "New";
            this.checkBox8.UseVisualStyleBackColor = true;
            this.checkBox8.CheckedChanged += new System.EventHandler(this.checkBox8_CheckedChanged);
            // 
            // checkBox7
            // 
            this.checkBox7.AutoSize = true;
            this.checkBox7.Location = new System.Drawing.Point(17, 21);
            this.checkBox7.Name = "checkBox7";
            this.checkBox7.Size = new System.Drawing.Size(52, 21);
            this.checkBox7.TabIndex = 0;
            this.checkBox7.Text = "Old";
            this.checkBox7.UseVisualStyleBackColor = true;
            this.checkBox7.CheckedChanged += new System.EventHandler(this.checkBox7_CheckedChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(631, 483);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.SERVER_ADDRESS);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.CLIENT_ADDRESS);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.DriverVersion);
            this.Controls.Add(this.Platform);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.IP_ADDRESS);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.START_Button);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = "HDMI Compliance ";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.CheckBox checkBox4;
        private System.Windows.Forms.CheckBox checkBox3;
        private System.Windows.Forms.CheckBox checkBox2;
        private System.Windows.Forms.CheckBox checkBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.CheckBox checkBox5;
        private System.Windows.Forms.Button START_Button;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox Platform;
        private System.Windows.Forms.TextBox DriverVersion;
        private System.Windows.Forms.TextBox CLIENT_ADDRESS;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox SERVER_ADDRESS;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox IP_ADDRESS;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox Version;
        private System.Windows.Forms.CheckBox checkBox8;
        private System.Windows.Forms.CheckBox checkBox7;
    }
}

