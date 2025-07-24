namespace Intel.VPG.Display.Automation
{
    using System;

    public class TestException : Exception
    {
        public Exception OriginalException { get; private set; }
        public bool CaptureScreenshot { get; private set; }
        public TestException(string argData, params object[] args)
            : this(null, argData, args)
        { }
        public TestException(bool argCaptureScreenshot, string argData, params object[] args)
            : this(null, argCaptureScreenshot, argData, args)
        { }

        public TestException(Exception argOriginalEx, string argData, params object[] args)
            : base(string.Format(argData, args))
        {
            this.OriginalException = argOriginalEx ?? this.GetBaseException();
        }
        public TestException(Exception argOriginalEx, bool argCaptureScreenshot, string argData, params object[] args)
            : this(argOriginalEx, argData, args)
        {
            this.CaptureScreenshot = argCaptureScreenshot;
        }
    }
}
