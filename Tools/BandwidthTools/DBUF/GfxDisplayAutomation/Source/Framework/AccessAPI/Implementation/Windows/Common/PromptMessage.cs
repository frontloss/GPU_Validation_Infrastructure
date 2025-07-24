namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Drawing;
    using System.Windows.Forms;

    public class PromptMessage : FunctionalBase, ISetMethod
    {
        public bool SetMethod(Object pMessage)
        {
            Log.Message("Prompting Message : {0}" , pMessage);

            String message = pMessage as String;
            bool result = false;

            // creating Label for Prompt 
            Label lable = new Label();
            lable.Text = message;
            lable.Size = new Size(500,25);
            lable.Location = new Point(100,20);

            // Creating Acceptance Buttons for the Modal Window
            Button ok = new Button();
            ok.Text = "Ok";
            ok.DialogResult = DialogResult.OK;           
            ok.Location = new Point(150 , lable.Bottom + 25);

            // Creating Rejection Buttons for the Modal Window
            Button cancel = new Button();
            cancel.Text = "cancel";
            cancel.DialogResult = DialogResult.Cancel;            
            cancel.Location = new Point(ok.Right + 10 ,lable.Bottom + 25 );
            
            // Creating Modal window Form
            Form form1 = new Form();
            form1.Text = "Semi Automated Action";
            form1.FormBorderStyle = FormBorderStyle.FixedDialog;
            form1.AcceptButton = ok;
            form1.CancelButton = cancel;
            form1.StartPosition = FormStartPosition.CenterScreen;
            form1.Controls.Add(lable);
            form1.Controls.Add(ok);
            form1.Controls.Add(cancel);
            form1.Size = new Size(500,150);

            // Prompt Dialogbox
            form1.ShowDialog();

            if (form1.DialogResult == DialogResult.OK)
            {
                Log.Message("User Accepted the Semi Automated Request");
                form1.Dispose();
                result  = true ;
            }
            else
            {
                Log.Message("User Rejected the Semi Automated Request");
                form1.Dispose();
                result = false;
            }

            return result ;
        }
       
    }
}