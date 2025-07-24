using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_HDR_Multimetadata : SB_HDR_Base
    {
        
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.ApplicationManager.VerifyTDR = false;
            
            base.ApplyConfigOS(base.CurrentConfig);

            // removed aapply 4k@60 mode

            LaunchMDAPlayer();
            Thread.Sleep(2000);
            ValidateMetadata("multimetadata1");
            Thread.Sleep(15000);
            ValidateMetadata("multimetadata2");
            Thread.Sleep(25000);
            ValidateMetadata("multimetadata3");
                     
        }
    }
}
