using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_4k2k:SB_Dbuf_Base
    {
        List<DisplayType> displayList = new List<DisplayType>();
         List<DisplayModeList> allModeList =new List<DisplayModeList>();
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            base.ApplyConfig(base.CurrentConfig);
             allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);

           displayList = allModeList.Where(dI => dI.supportedModes.Any(dI2 => dI2.HzRes > 4000)).Select(dI=> dI.display).ToList();
          if (displayList.Count() == 0)
              Log.Abort("Test needs atleast one display to support 4KX2K");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            //List<PipeDbufInfo> dbufList = base.ReadYTilingInfo(base.CurrentConfig);  
            //dbufList.ForEach(curDisp=>
            //    {
                   
            //    });     
            //List<DisplayMode> modeList=  allModeList.Where(dI => dI.display == curDisp.DisplayType).Select(dI => dI.supportedModes).FirstOrDefault();
            //      DisplayMode maxMode = modeList.Last();                    
            //      if (maxMode.HzRes > 4000)
            //      {
            //          Log.Message("{0} is supporting higher resolution {0}", maxMode.GetCurrentModeStr(false));
            //          if (curDisp.PlaneA.TileFormat != TileFormat.Tile_X_Memory)
            //              Log.Fail("{0} is not XTile", curDisp.DisplayType);
            //          else
            //              Log.Success("{0} is XTile", curDisp.DisplayType);
            //      }
            //      else
            //      {
            //          Log.Message("{0} is supporting {0}", maxMode.GetCurrentModeStr(false));
            //      }                  
            //    });
        }
        
    }
}
