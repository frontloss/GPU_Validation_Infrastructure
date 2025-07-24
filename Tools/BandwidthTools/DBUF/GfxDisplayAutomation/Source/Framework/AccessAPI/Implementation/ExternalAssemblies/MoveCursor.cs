namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Runtime.InteropServices;

    public class MoveCursor : FunctionalBase, ISetMethod, ISet
    {
        public bool SetMethod(object argMessage)
        {
            MoveCursorPos cursorPositionObject = argMessage as MoveCursorPos;
            int displayHierarchy = (int) cursorPositionObject.displayHierarchy;
            DisplayMode mode = base.GetDisplayModeByDisplayType(cursorPositionObject.displayType);
            uint left = (mode.HzRes);
            for (int i = 0; i < displayHierarchy; i++)
                left += base.GetDisplayModeByDisplayType(cursorPositionObject.currentConfig.CustomDisplayList.ElementAt(i)).HzRes;
            Interop.SetCursorPos((int)left, (int)10);
            return true;
        }
        public object Set
        {
            set
            {

                MoveCursorPos cursorPositionObject =(MoveCursorPos)value;
                int displayHierarchy = (int)cursorPositionObject.displayHierarchy;
                DisplayMode mode = base.GetDisplayModeByDisplayType(cursorPositionObject.displayType);
                uint left = (mode.HzRes)/4;
                Interop.SetCursorPos((int)left, (int)20);
            }
        }
    }
}
