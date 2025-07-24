using System;
namespace PackageInstaller
{
    class ServiceRequest
    {
        static int Main(string[] args)
        {
            AppDomain.CurrentDomain.UnhandledException += new UnhandledExceptionEventHandler(GlobalExceptionHandler);
            Parser.Init(args);
            Log.Init();
            EnvPreparedness.CopyAssemblies();
            EnvPreparedness.RunTask(Parser.ServiceType);
            return 0;
        }

        private static void GlobalExceptionHandler(object sender, UnhandledExceptionEventArgs e)
        {
            Log.Fail("Unhandled exception found.");
            CommonRoutine.Exit(ErrorCode.Fail);
        }
    }
}
