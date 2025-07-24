namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.IO;
    using System.Threading;
    using System.Diagnostics;

    public struct cursorInfo
    {
        public Int32 cbSize;        // Specifies the size, in bytes, of the structure. 
        public Int32 flags;         // Specifies the cursor state. This parameter can be one of the following values:
        public IntPtr hCursor;          // Handle to the cursor. 
        public pointApi ptScreenPos;       // A POINT structure that receives the screen coordinates of the cursor. 
    }
    public struct pointApi
    {
        public int x;
        public int y;
    }

    public class CursorInfo
    {
        public cursorInfo cursorInfo { get; set; }
    }
}
