namespace CalculateWatermark
{
    partial class CalculateWM
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
            this.clbPlatformSelect = new System.Windows.Forms.CheckedListBox();
            this.rtbInput = new System.Windows.Forms.RichTextBox();
            this.rtbOutput = new System.Windows.Forms.RichTextBox();
            this.rtbStatus = new System.Windows.Forms.RichTextBox();
            this.bCalculateWM = new System.Windows.Forms.Button();
            this.gbResults = new System.Windows.Forms.GroupBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.textBox3 = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.gbResults.SuspendLayout();
            this.SuspendLayout();
            // 
            // clbPlatformSelect
            // 
            this.clbPlatformSelect.CheckOnClick = true;
            this.clbPlatformSelect.FormattingEnabled = true;
            this.clbPlatformSelect.Items.AddRange(new object[] {
            "SKL",
            "BXT",
            "KBL",
            "GLK",
            "CNL"});
            this.clbPlatformSelect.Location = new System.Drawing.Point(106, 32);
            this.clbPlatformSelect.Name = "clbPlatformSelect";
            this.clbPlatformSelect.Size = new System.Drawing.Size(75, 75);
            this.clbPlatformSelect.TabIndex = 0;
            this.clbPlatformSelect.SelectedIndexChanged += new System.EventHandler(this.clbPlatformSelect_SelectedIndexChanged);
            // 
            // rtbInput
            // 
            this.rtbInput.BackColor = System.Drawing.SystemColors.Info;
            this.rtbInput.Location = new System.Drawing.Point(24, 20);
            this.rtbInput.Name = "rtbInput";
            this.rtbInput.ReadOnly = true;
            this.rtbInput.Size = new System.Drawing.Size(285, 299);
            this.rtbInput.TabIndex = 1;
            this.rtbInput.Text = "";
            // 
            // rtbOutput
            // 
            this.rtbOutput.BackColor = System.Drawing.SystemColors.Info;
            this.rtbOutput.Location = new System.Drawing.Point(350, 21);
            this.rtbOutput.Name = "rtbOutput";
            this.rtbOutput.ReadOnly = true;
            this.rtbOutput.Size = new System.Drawing.Size(329, 297);
            this.rtbOutput.TabIndex = 2;
            this.rtbOutput.Text = "";
            // 
            // rtbStatus
            // 
            this.rtbStatus.BackColor = System.Drawing.SystemColors.InactiveCaption;
            this.rtbStatus.Font = new System.Drawing.Font("Microsoft Sans Serif", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.rtbStatus.Location = new System.Drawing.Point(24, 353);
            this.rtbStatus.Name = "rtbStatus";
            this.rtbStatus.ReadOnly = true;
            this.rtbStatus.Size = new System.Drawing.Size(242, 35);
            this.rtbStatus.TabIndex = 3;
            this.rtbStatus.Text = "";
            // 
            // bCalculateWM
            // 
            this.bCalculateWM.Enabled = false;
            this.bCalculateWM.Location = new System.Drawing.Point(260, 27);
            this.bCalculateWM.Name = "bCalculateWM";
            this.bCalculateWM.Size = new System.Drawing.Size(230, 23);
            this.bCalculateWM.TabIndex = 4;
            this.bCalculateWM.Text = "Calculate Watermark";
            this.bCalculateWM.UseVisualStyleBackColor = true;
            this.bCalculateWM.Click += new System.EventHandler(this.bCalculateWM_Click);
            // 
            // gbResults
            // 
            this.gbResults.Controls.Add(this.label4);
            this.gbResults.Controls.Add(this.label3);
            this.gbResults.Controls.Add(this.label2);
            this.gbResults.Controls.Add(this.label1);
            this.gbResults.Controls.Add(this.rtbStatus);
            this.gbResults.Controls.Add(this.rtbOutput);
            this.gbResults.Controls.Add(this.rtbInput);
            this.gbResults.Location = new System.Drawing.Point(41, 111);
            this.gbResults.Name = "gbResults";
            this.gbResults.Size = new System.Drawing.Size(706, 419);
            this.gbResults.TabIndex = 5;
            this.gbResults.TabStop = false;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(21, 336);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(50, 13);
            this.label4.TabIndex = 7;
            this.label4.Text = "RESULT";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(347, 336);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(77, 52);
            this.label3.TabIndex = 6;
            this.label3.Text = "Legend:\r\nPipe 1 - Pipe A\r\nPipe 2 - Pipe B\r\nPipe 3 - Pipe C";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(347, 4);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(39, 13);
            this.label2.TabIndex = 5;
            this.label2.Text = "Output";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(21, 4);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(31, 13);
            this.label1.TabIndex = 4;
            this.label1.Text = "Input";
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(562, 3);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(158, 20);
            this.textBox1.TabIndex = 8;
            this.textBox1.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(562, 30);
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(158, 20);
            this.textBox2.TabIndex = 9;
            this.textBox2.TextChanged += new System.EventHandler(this.textBox2_TextChanged);
            // 
            // textBox3
            // 
            this.textBox3.Location = new System.Drawing.Point(562, 60);
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(158, 20);
            this.textBox3.TabIndex = 10;
            this.textBox3.TextChanged += new System.EventHandler(this.textBox3_TextChanged);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(391, 60);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(98, 24);
            this.button1.TabIndex = 11;
            this.button1.Text = "Delay";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // CalculateWM
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(784, 562);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.textBox3);
            this.Controls.Add(this.textBox2);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.gbResults);
            this.Controls.Add(this.bCalculateWM);
            this.Controls.Add(this.clbPlatformSelect);
            this.Name = "CalculateWM";
            this.Text = "Watermark Calculator";
            this.gbResults.ResumeLayout(false);
            this.gbResults.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckedListBox clbPlatformSelect;
        private System.Windows.Forms.RichTextBox rtbInput;
        private System.Windows.Forms.RichTextBox rtbOutput;
        private System.Windows.Forms.RichTextBox rtbStatus;
        private System.Windows.Forms.Button bCalculateWM;
        private System.Windows.Forms.GroupBox gbResults;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        public System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.TextBox textBox3;
        private System.Windows.Forms.Button button1;
    }
}

