namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Windows;
    using System.Diagnostics;
    using System.Windows.Media;

    public partial class FakeEDID : Window, IView
    {
        public FakeEDID()
        {
            InitializeComponent();
            CommonExtensions.StartProcess("xcopy", string.Format(".\\x{0} . /R /Y", IntPtr.Size.Equals(8) ? "64" : "86"));
        }
        
        public void FormatActionMessage(MessageFormatType argFormatType)
        {
            switch (argFormatType)
            {
                case MessageFormatType.Information:
                    this.blkMessage.Background = Brushes.Wheat;
                    break;
                case MessageFormatType.Warning:
                    this.blkMessage.Background = Brushes.OrangeRed;
                    break;
                default:
                    this.blkMessage.Background = Brushes.White;
                    break;
            }
        }
        public void ResetControls()
        {
            this.cboEnumeratedDisplays.SelectedIndex = 0;
            this.cboEDIDBlockList.SelectedIndex = 0;
            this.cboReadEDIDRegKey.SelectedIndex = 0;
            this.cboFakeEDIDRegKey.SelectedIndex = 0;
            this.FormatActionMessage(MessageFormatType.None);
        }
        public void SetEnumeratedDisplayToDefault()
        {
            base.Dispatcher.Invoke((Action)(() => this.cboEnumeratedDisplays.SelectedIndex = 0));
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            this.ResetControls();
        }
    }
}
