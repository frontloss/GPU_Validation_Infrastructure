namespace Intel.VPG.Display.Automation
{
    public interface IView
    {
        void FormatActionMessage(MessageFormatType argFormatType);
        void ResetControls();
        void SetEnumeratedDisplayToDefault();
    }
}
