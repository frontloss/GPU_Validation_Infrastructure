using System.IO;
using System.Linq;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    public class VerifySystemState : FunctionalBase, IGet
    {
        public object Get
        {
            get
            {
                #region Verify PIPE Underrun
                VerifyUnderrun underrunCheck = base.CreateInstance<VerifyUnderrun>(new VerifyUnderrun());
                underrunCheck.GetMethod(null);
                #endregion

                #region TDR/Minidump Check

                if (base.AppManager.VerifyTDR)
                {
                    Thread.Sleep(2000);
                    this.MoveDumps(DumpCategory.WatchDogdump, "TDR");
                    this.MoveDumps(DumpCategory.Minidump, DumpCategory.Minidump.ToString());
                }

                #endregion

                //Any other common verification should be added here.
                return true;
            }
        }

        private void MoveDumps(DumpCategory argCategory, string argMessage)
        {
            if (Directory.Exists(CommonExtensions.DumpPaths[argCategory]))
            {
                string[] files = Directory.GetFiles(CommonExtensions.DumpPaths[argCategory], "*.dmp");
                if (files.Count() > 0)
                {
                    Log.Verbose("Copying dump file {0}", files.First());
                    File.Move(files.First(), string.Concat(Directory.GetCurrentDirectory(), files.First().Substring(files.First().LastIndexOf('\\'))));
                }
            }
        }
    }
}
