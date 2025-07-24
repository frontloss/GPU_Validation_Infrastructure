using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_Overlay_Modeset : SB_Overlay_ExtendedDrag
    {
        protected PowerStates powerState;
        protected List<List<DisplayModeList>> modesList;
      public SB_Overlay_Modeset():base()
      {
          this.modesList = new List<List<DisplayModeList>>();
      }

        [Test(Type = TestType.Method, Order = 0)]
      public override void TestStep0()
      {
          if (base.CurrentConfig.DisplayList.Count() == 0)
              Log.Abort("This test requires atleast 1 displays , current display count: {0}", base.CurrentConfig.DisplayList.Count());
            
          ApplyConfig(base.CurrentConfig);
          VerifyConfig(base.CurrentConfig);
      }

        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            DisplayType primaryDisp = base.CurrentConfig.CustomDisplayList.First();

            base.PlayAndMoveVideo(DisplayExtensions.GetDispHierarchy(base.CurrentConfig, primaryDisp), base.CurrentConfig);
            modesList.Add(base.GetMinModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig()));
            modesList.Add(base.GetIntermediateModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig()));
            modesList.Add(base.GetMaxModeForConfig(base.CurrentConfig.CustomDisplayList, base.CurrentConfig.ConfigType.GetUnifiedConfig()));

            foreach (List<DisplayModeList> displayModetype in modesList)
            {
                foreach (DisplayModeList displayModelist in displayModetype)
                {
                    foreach (DisplayMode mode in displayModelist.supportedModes)
                    {
                        base.ApplyMode(mode, mode.display);

                        displayInfo = this.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == mode.display);
                        base.VerifyRegisterForDisplay(primaryDisp, false);
                        
                        //Verify Secondary & ternary display
                        foreach (DisplayType display in base.CurrentConfig.CustomDisplayList)
                        {
                            if (display != primaryDisp)
                            {
                                base.VerifyRegisterForDisplay(display, true);
                            }
                        }


                    }
                }

            }

            base.StopVideo();
        }
    }
}
