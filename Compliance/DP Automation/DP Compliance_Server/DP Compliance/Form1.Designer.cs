namespace DP_Compliance
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
            this.DPR120 = new System.Windows.Forms.GroupBox();
            this.DPR120_Applet = new System.Windows.Forms.CheckBox();
            this.DPR120_LINK = new System.Windows.Forms.CheckBox();
            this.DPR100 = new System.Windows.Forms.GroupBox();
            this.DPR100_Applet = new System.Windows.Forms.CheckBox();
            this.DPR100_HDCP = new System.Windows.Forms.CheckBox();
            this.DPR100_AUDIO = new System.Windows.Forms.CheckBox();
            this.DPR100_LINK = new System.Windows.Forms.CheckBox();
            this.NETWORK = new System.Windows.Forms.GroupBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.START = new System.Windows.Forms.Button();
            this.textBox2_Iteration = new System.Windows.Forms.TextBox();
            this.labe3 = new System.Windows.Forms.Label();
            this.Platform = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.Driver_Version = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.BDW = new System.Windows.Forms.CheckBox();
            this.SKL = new System.Windows.Forms.CheckBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.DP_PORT_B = new System.Windows.Forms.CheckBox();
            this.DP_PORT_C = new System.Windows.Forms.CheckBox();
            this.DP_PORT_D = new System.Windows.Forms.CheckBox();
            this.DPR120.SuspendLayout();
            this.DPR100.SuspendLayout();
            this.NETWORK.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // DPR120
            // 
            this.DPR120.Controls.Add(this.DPR120_Applet);
            this.DPR120.Controls.Add(this.DPR120_LINK);
            this.DPR120.Location = new System.Drawing.Point(13, 27);
            this.DPR120.Name = "DPR120";
            this.DPR120.Size = new System.Drawing.Size(129, 138);
            this.DPR120.TabIndex = 0;
            this.DPR120.TabStop = false;
            this.DPR120.Text = "DPR120";
            // 
            // DPR120_Applet
            // 
            this.DPR120_Applet.AutoSize = true;
            this.DPR120_Applet.Location = new System.Drawing.Point(7, 44);
            this.DPR120_Applet.Name = "DPR120_Applet";
            this.DPR120_Applet.Size = new System.Drawing.Size(108, 17);
            this.DPR120_Applet.TabIndex = 1;
            this.DPR120_Applet.Text = "APPLET TESTS ";
            this.DPR120_Applet.UseVisualStyleBackColor = true;
            this.DPR120_Applet.CheckedChanged += new System.EventHandler(this.DPR120_Applet_CheckedChanged);
            // 
            // DPR120_LINK
            // 
            this.DPR120_LINK.AutoSize = true;
            this.DPR120_LINK.Location = new System.Drawing.Point(7, 20);
            this.DPR120_LINK.Name = "DPR120_LINK";
            this.DPR120_LINK.Size = new System.Drawing.Size(50, 17);
            this.DPR120_LINK.TabIndex = 0;
            this.DPR120_LINK.Text = "LINK";
            this.DPR120_LINK.UseVisualStyleBackColor = true;
            this.DPR120_LINK.CheckedChanged += new System.EventHandler(this.DPR120_LINK_CheckedChanged);
            // 
            // DPR100
            // 
            this.DPR100.Controls.Add(this.DPR100_Applet);
            this.DPR100.Controls.Add(this.DPR100_HDCP);
            this.DPR100.Controls.Add(this.DPR100_AUDIO);
            this.DPR100.Controls.Add(this.DPR100_LINK);
            this.DPR100.Location = new System.Drawing.Point(240, 27);
            this.DPR100.Name = "DPR100";
            this.DPR100.Size = new System.Drawing.Size(134, 138);
            this.DPR100.TabIndex = 1;
            this.DPR100.TabStop = false;
            this.DPR100.Text = "DPR100";
            // 
            // DPR100_Applet
            // 
            this.DPR100_Applet.AutoSize = true;
            this.DPR100_Applet.Location = new System.Drawing.Point(16, 92);
            this.DPR100_Applet.Name = "DPR100_Applet";
            this.DPR100_Applet.Size = new System.Drawing.Size(108, 17);
            this.DPR100_Applet.TabIndex = 3;
            this.DPR100_Applet.Text = "APPLET TESTS ";
            this.DPR100_Applet.UseVisualStyleBackColor = true;
            this.DPR100_Applet.CheckedChanged += new System.EventHandler(this.DPR100_Applet_CheckedChanged);
            // 
            // DPR100_HDCP
            // 
            this.DPR100_HDCP.AutoSize = true;
            this.DPR100_HDCP.Location = new System.Drawing.Point(16, 68);
            this.DPR100_HDCP.Name = "DPR100_HDCP";
            this.DPR100_HDCP.Size = new System.Drawing.Size(56, 17);
            this.DPR100_HDCP.TabIndex = 2;
            this.DPR100_HDCP.Text = "HDCP";
            this.DPR100_HDCP.UseVisualStyleBackColor = true;
            this.DPR100_HDCP.CheckedChanged += new System.EventHandler(this.DPR100_HDCP_CheckedChanged_1);
            // 
            // DPR100_AUDIO
            // 
            this.DPR100_AUDIO.AutoSize = true;
            this.DPR100_AUDIO.Location = new System.Drawing.Point(16, 44);
            this.DPR100_AUDIO.Name = "DPR100_AUDIO";
            this.DPR100_AUDIO.Size = new System.Drawing.Size(60, 17);
            this.DPR100_AUDIO.TabIndex = 1;
            this.DPR100_AUDIO.Text = "AUDIO";
            this.DPR100_AUDIO.UseVisualStyleBackColor = true;
            this.DPR100_AUDIO.CheckedChanged += new System.EventHandler(this.DPR100_AUDIO_CheckedChanged);
            // 
            // DPR100_LINK
            // 
            this.DPR100_LINK.AutoSize = true;
            this.DPR100_LINK.Location = new System.Drawing.Point(16, 20);
            this.DPR100_LINK.Name = "DPR100_LINK";
            this.DPR100_LINK.Size = new System.Drawing.Size(53, 17);
            this.DPR100_LINK.TabIndex = 0;
            this.DPR100_LINK.Text = "LINK ";
            this.DPR100_LINK.UseVisualStyleBackColor = true;
            this.DPR100_LINK.CheckedChanged += new System.EventHandler(this.DPR100_LINK_CheckedChanged);
            // 
            // NETWORK
            // 
            this.NETWORK.Controls.Add(this.textBox2);
            this.NETWORK.Controls.Add(this.label2);
            this.NETWORK.Controls.Add(this.label1);
            this.NETWORK.Controls.Add(this.textBox1);
            this.NETWORK.Location = new System.Drawing.Point(13, 171);
            this.NETWORK.Name = "NETWORK";
            this.NETWORK.Size = new System.Drawing.Size(361, 99);
            this.NETWORK.TabIndex = 2;
            this.NETWORK.TabStop = false;
            this.NETWORK.Text = "NETWORK";
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(147, 29);
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(167, 20);
            this.textBox2.TabIndex = 4;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(22, 32);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(119, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "SERVER IP ADDRESS";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(22, 57);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(113, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "CLIENT IP ADDRESS";
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(147, 54);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(167, 20);
            this.textBox1.TabIndex = 1;
            // 
            // START
            // 
            this.START.Location = new System.Drawing.Point(154, 142);
            this.START.Name = "START";
            this.START.Size = new System.Drawing.Size(75, 23);
            this.START.TabIndex = 0;
            this.START.Text = "START";
            this.START.UseVisualStyleBackColor = true;
            this.START.Click += new System.EventHandler(this.START_Click);
            // 
            // textBox2_Iteration
            // 
            this.textBox2_Iteration.Location = new System.Drawing.Point(164, 80);
            this.textBox2_Iteration.Name = "textBox2_Iteration";
            this.textBox2_Iteration.Size = new System.Drawing.Size(56, 20);
            this.textBox2_Iteration.TabIndex = 9;
            this.textBox2_Iteration.Text = "1";
            // 
            // labe3
            // 
            this.labe3.AutoSize = true;
            this.labe3.Location = new System.Drawing.Point(164, 61);
            this.labe3.Name = "labe3";
            this.labe3.Size = new System.Drawing.Size(65, 13);
            this.labe3.TabIndex = 10;
            this.labe3.Text = "ITERATION";
            // 
            // Platform
            // 
            this.Platform.Location = new System.Drawing.Point(114, 272);
            this.Platform.Name = "Platform";
            this.Platform.Size = new System.Drawing.Size(135, 20);
            this.Platform.TabIndex = 11;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(17, 275);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(72, 13);
            this.label3.TabIndex = 12;
            this.label3.Text = "Platform/SKU";
            // 
            // Driver_Version
            // 
            this.Driver_Version.Location = new System.Drawing.Point(113, 303);
            this.Driver_Version.Name = "Driver_Version";
            this.Driver_Version.Size = new System.Drawing.Size(135, 20);
            this.Driver_Version.TabIndex = 13;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(7, 306);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(100, 13);
            this.label4.TabIndex = 14;
            this.label4.Text = "GFX Driver Version ";
            // 
            // BDW
            // 
            this.BDW.AutoSize = true;
            this.BDW.Location = new System.Drawing.Point(13, 342);
            this.BDW.Name = "BDW";
            this.BDW.Size = new System.Drawing.Size(52, 17);
            this.BDW.TabIndex = 15;
            this.BDW.Text = "BDW";
            this.BDW.UseVisualStyleBackColor = true;
            this.BDW.CheckedChanged += new System.EventHandler(this.BDW_CheckedChanged);
            // 
            // SKL
            // 
            this.SKL.AutoSize = true;
            this.SKL.Location = new System.Drawing.Point(12, 376);
            this.SKL.Name = "SKL";
            this.SKL.Size = new System.Drawing.Size(93, 17);
            this.SKL.TabIndex = 16;
            this.SKL.Text = "SKL,KBL,BXT";
            this.SKL.UseVisualStyleBackColor = true;
            this.SKL.CheckedChanged += new System.EventHandler(this.SKL_CheckedChanged);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.DP_PORT_D);
            this.groupBox2.Controls.Add(this.DP_PORT_C);
            this.groupBox2.Controls.Add(this.DP_PORT_B);
            this.groupBox2.Location = new System.Drawing.Point(256, 276);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(200, 100);
            this.groupBox2.TabIndex = 0;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "DP Port Configuration";
            // 
            // DP_PORT_B
            // 
            this.DP_PORT_B.AutoSize = true;
            this.DP_PORT_B.Location = new System.Drawing.Point(6, 20);
            this.DP_PORT_B.Name = "DP_PORT_B";
            this.DP_PORT_B.Size = new System.Drawing.Size(73, 17);
            this.DP_PORT_B.TabIndex = 0;
            this.DP_PORT_B.Text = "DP Port B";
            this.DP_PORT_B.UseVisualStyleBackColor = true;
            this.DP_PORT_B.CheckedChanged += new System.EventHandler(this.DP_PORT_B_CheckedChanged);
            // 
            // DP_PORT_C
            // 
            this.DP_PORT_C.AutoSize = true;
            this.DP_PORT_C.Location = new System.Drawing.Point(6, 43);
            this.DP_PORT_C.Name = "DP_PORT_C";
            this.DP_PORT_C.Size = new System.Drawing.Size(73, 17);
            this.DP_PORT_C.TabIndex = 1;
            this.DP_PORT_C.Text = "DP Port C";
            this.DP_PORT_C.UseVisualStyleBackColor = true;
            this.DP_PORT_C.CheckedChanged += new System.EventHandler(this.checkBox2_CheckedChanged);
            // 
            // DP_PORT_D
            // 
            this.DP_PORT_D.AutoSize = true;
            this.DP_PORT_D.Location = new System.Drawing.Point(6, 66);
            this.DP_PORT_D.Name = "DP_PORT_D";
            this.DP_PORT_D.Size = new System.Drawing.Size(74, 17);
            this.DP_PORT_D.TabIndex = 2;
            this.DP_PORT_D.Text = "DP Port D";
            this.DP_PORT_D.UseVisualStyleBackColor = true;
            this.DP_PORT_D.CheckedChanged += new System.EventHandler(this.checkBox3_CheckedChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(474, 405);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.SKL);
            this.Controls.Add(this.BDW);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.Driver_Version);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.Platform);
            this.Controls.Add(this.labe3);
            this.Controls.Add(this.textBox2_Iteration);
            this.Controls.Add(this.NETWORK);
            this.Controls.Add(this.DPR100);
            this.Controls.Add(this.START);
            this.Controls.Add(this.DPR120);
            this.Name = "Form1";
            this.Text = "DP COMPLINACE SERVER";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.DPR120.ResumeLayout(false);
            this.DPR120.PerformLayout();
            this.DPR100.ResumeLayout(false);
            this.DPR100.PerformLayout();
            this.NETWORK.ResumeLayout(false);
            this.NETWORK.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox DPR120;
        private System.Windows.Forms.CheckBox DPR120_LINK;
        private System.Windows.Forms.GroupBox DPR100;
        private System.Windows.Forms.GroupBox NETWORK;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.Button START;
        private System.Windows.Forms.TextBox textBox2_Iteration;
        private System.Windows.Forms.Label labe3;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.CheckBox DPR100_HDCP;
        private System.Windows.Forms.CheckBox DPR100_AUDIO;
        private System.Windows.Forms.CheckBox DPR100_LINK;
        private System.Windows.Forms.TextBox Platform;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox Driver_Version;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.CheckBox DPR120_Applet;
        private System.Windows.Forms.CheckBox DPR100_Applet;
        private System.Windows.Forms.CheckBox BDW;
        private System.Windows.Forms.CheckBox SKL;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.CheckBox DP_PORT_D;
        private System.Windows.Forms.CheckBox DP_PORT_C;
        private System.Windows.Forms.CheckBox DP_PORT_B;

    }
}

