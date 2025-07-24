namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Xml.Linq;
    using System.Collections.Generic;

    public static class EnvPreparedness
    {
        public static void Init(IApplicationManager argManager, bool argIsReboot)
        {
            InitEnvironment initType = null;
            List<EnvironmentParams> envInitList = GetEnvInitList();
            envInitList.ForEach(eP =>
                {
                    if (!eP.RunSeperate && (!argIsReboot || argIsReboot == eP.RunOnReboot))
                    {
                        Log.Verbose("Processing {0} from {1}", eP.Class, eP.Source);
                        initType = eP.Class.Activate(eP.Source, argManager) as InitEnvironment;
                        initType.DoWork();
                    }
                });
        }
        public static void RunTask(IApplicationManager argManager, Features argFeature)
        {
            InitEnvironment initType = null;
            List<EnvironmentParams> envInitList = GetEnvInitList();
            EnvironmentParams envObj = envInitList.Where(eP => eP.Class == argFeature).FirstOrDefault();
            if (null != envObj)
            {
                Log.Verbose("Processing {0} from {1}", envObj.Class, envObj.Source);
                initType = envObj.Class.Activate(envObj.Source, argManager) as InitEnvironment;
                initType.DoWork();
            }
        }

        private static List<EnvironmentParams> GetEnvInitList()
        {
            string envInitMap = string.Format(@"{0}\Mapper\EnvironmentInit.map", Directory.GetCurrentDirectory());
            return
                (from i in XDocument.Load(envInitMap).Descendants("Init")
                 select new EnvironmentParams
                     {
                         Class = (Features)Enum.Parse(typeof(Features), i.Attribute("class").Value, true),
                         Source = (Source)Enum.Parse(typeof(Source), i.Attribute("source").Value, true),
                         RunOnReboot = Convert.ToBoolean(i.Attribute("runOnReboot").Value),
                         RunSeperate = Convert.ToBoolean(i.Attribute("runSeperate").Value)
                     })
                     .ToList();
        }
    }
}
