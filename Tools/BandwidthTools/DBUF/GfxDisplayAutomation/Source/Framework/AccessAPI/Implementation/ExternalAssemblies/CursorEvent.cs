namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Drawing;
    using System.Runtime.InteropServices;

    internal class CursorEvent : FunctionalBase, ISetMethod, IGetMethod
    {
        private uint _flagRetry = 0;

        public bool SetMethod(object argMessage)
        {           
            Point argToBeSet = (Point)argMessage;
            Point argGot;
            Log.Verbose("Set the cursor position to {0},{1}", argToBeSet.X, argToBeSet.Y);
            Interop.SetCursorPos(argToBeSet.X, argToBeSet.Y);
            Thread.Sleep(1000);
            Interop.GetCursorPos(out argGot);
            if (VerifyCursorPosition(argToBeSet, argGot))
                return true;
            else
                return false;
        }
        public object GetMethod(object argMessage)
        {
            Log.Verbose("Get the current cursor info.");
            cursorInfo ci = new cursorInfo();
            ci.cbSize = Marshal.SizeOf(ci);
            if (Interop.GetCursorInfo(out ci))
                return ci;
            else
                return null;
        }
        private bool VerifyCursorPosition(Point argToBeSet, Point argGot)
        {
            if ((argToBeSet.X != argGot.X) || (argToBeSet.Y != argGot.Y))
            {
                Log.Sporadic(false, "Cursor position not set properly.Performing a Retry.");
                return (Retry(argToBeSet,argGot));
            }
            else
            {
                _flagRetry = 0;
            }
            return true;
        }
        private bool Retry(Point argToBeSet, Point argGot)
        {
            _flagRetry++;
            if (_flagRetry > 3)
            {
                Log.Fail(false, "Failed in setting the cursor position more than thrice.");
                _flagRetry = 0;
                return false;
            }
            else
            {
                Log.Verbose("Trying to reset");
                Interop.SetCursorPos(argToBeSet.X, argToBeSet.Y);
                Thread.Sleep(1000);
                Interop.GetCursorPos(out argGot);
                return (VerifyCursorPosition(argToBeSet, argGot));
            }
        }
    }
}