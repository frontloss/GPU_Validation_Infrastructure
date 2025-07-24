using System;
using System.Collections.Generic;
using System.Linq;

namespace PackageInstaller
{
    public static class Parser
    {
        public static List<string> CommadData;
        public static Services ServiceType;

        public static Services Init(string[] args)
        {
            CommadData = new List<string>();
            if (Enum.IsDefined(typeof(Services), args[0].Trim()) == false)
            {
                Log.Fail("Undefied Service Type Found");
                CommonRoutine.Exit(ErrorCode.Fail);
            }
            else
            {
                foreach (string inParam in args.Skip(1))
                {
                    CommadData.Add(inParam);
                }
                ServiceType = (Services)Enum.Parse(typeof(Services), args[0].Trim());
                return ServiceType;
            }
            return Services.Undefined;
        }
    }
}
