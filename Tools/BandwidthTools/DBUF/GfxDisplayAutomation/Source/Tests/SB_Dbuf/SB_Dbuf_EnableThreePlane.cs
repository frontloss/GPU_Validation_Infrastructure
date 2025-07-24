using System.Collections.Generic;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Win32;
namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_EnableThreePlane:SB_Dbuf_MPO
    {
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            MoveCursor(base.CurrentConfig,base.CurrentConfig.SecondaryDisplay );
            base.LaunchMPO();
            LaunchCharmWindow();           
        }
        private void MoveCursor(DisplayConfig argDispConfig, DisplayType argDispType)
        {            
            MoveCursorPos cursor = new MoveCursorPos();
            cursor.currentConfig = argDispConfig;
            cursor.displayHierarchy = GetDisplayHierarchy(argDispConfig, argDispType); ;
            cursor.displayType = argDispType;
            Log.Message(true,"Moving cursor to {0} {1} ",argDispType,cursor.displayHierarchy);
            AccessInterface.SetFeature<bool, MoveCursorPos>(Features.MoveCursor, Action.SetMethod, cursor);  
        }
        private DisplayHierarchy GetDisplayHierarchy(DisplayConfig argDispConfig, DisplayType argDispType)
        {
            if (argDispConfig.PrimaryDisplay == argDispType)
                return DisplayHierarchy.Display_1;
            else if (argDispConfig.SecondaryDisplay == argDispType)
                return DisplayHierarchy.Display_2;
            else if (argDispConfig.TertiaryDisplay == argDispType)
                return DisplayHierarchy.Display_3;
            return DisplayHierarchy.Unsupported;
        }
        private void LaunchCharmWindow()
        {
            Log.Message(true,"Launching Win C");           
            AccessInterface.SetFeature<bool>(Features.LaunchCharmWindow, Action.SetMethod, Source.WindowsAutomationUI);  
            Thread.Sleep(2000);
        }
    }
}
