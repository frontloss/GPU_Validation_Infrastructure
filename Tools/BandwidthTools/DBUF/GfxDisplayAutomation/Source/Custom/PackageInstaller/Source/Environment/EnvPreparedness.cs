using System;
using System.Linq;
using System.Reflection;
using System.IO;

namespace PackageInstaller
{
    public static class EnvPreparedness
    {
        public static void RunTask(Services argFeature)
        {
            InitEnvironment initType = null;
            initType = Activate(argFeature.ToString()) as InitEnvironment;
            initType.SystemInfo = InitRoutine.Run();
            if (initType.Run() == true)
                CommonRoutine.Exit(ErrorCode.Success);
            else
                CommonRoutine.Exit(ErrorCode.Fail);
        }

        public static void CopyAssemblies()
        {
            if (IntPtr.Size.Equals(8))
            {
                if (Directory.Exists(Directory.GetCurrentDirectory() + "\\x64"))
                {
                    Log.Messege("Copying 64 bit assemblies to root");
                    CommonRoutine.StartProcess("xcopy", ".\\x64 . /S /E /R /Y");
                }
            }
            else
            {
                if (Directory.Exists(Directory.GetCurrentDirectory() + "\\x86"))
                {
                    Log.Messege("Copying 32 bit assemblies to root");
                    CommonRoutine.StartProcess("xcopy", ".\\x86 . /S /E /R /Y");
                }
            }
        }

        private static object Activate(string argTypeName)
        {
            Assembly assembly = null;
            Type type = null;

            assembly = Assembly.Load("PackageInstaller");
            type = type.Locate(assembly, argTypeName);
            return Activator.CreateInstance(type);
        }

        private static Type Locate(this Type argContext, Assembly argAssembly, string argInstance)
        {
            argContext = GetTypeInstance(argAssembly, argInstance);
            if (null == argContext)
            {
                Log.Fail("Could not locate Type:: {0}!", argInstance);
                CommonRoutine.Exit(ErrorCode.Fail);
            }
            return argContext;
        }

        private static Type GetTypeInstance(Assembly argAssembly, string argInstanceName)
        {
            return (from type in argAssembly.GetTypes()
                    where type.Name.ToLower().Equals(argInstanceName.ToLower())
                    select type).SingleOrDefault();
        }
    }
}
