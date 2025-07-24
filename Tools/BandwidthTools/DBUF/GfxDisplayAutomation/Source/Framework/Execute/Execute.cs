namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Reflection;
    using System.Diagnostics;
    using System.Collections.Generic;
    using System.Security.Principal;

    internal class Execute
    {
        private static TestBase _context = null;
        private static int _methodInvocationIdx = 0;
        private static IApplicationManager _appManager = null;
        private static List<MethodInfo> _methodInvocationLst = null;
        private static bool _exceptionLogged = false;
        private const string QuickBuildVersion = "version.txt";

        //[STAThread]
        public static void Main(string[] args)
        {
            AppDomain.CurrentDomain.UnhandledException += new UnhandledExceptionEventHandler(GlobalExceptionHandler);
            IApplicationSettings appSettings = ApplicationSettings.Instance;
            CommandLineParser parser = new CommandLineParser();
            CommonExtensions.Init(appSettings, args);
            UIExtensions.Load(appSettings);

            parser.Parse<string>(args, ArgumentType.TestName);
            string testName = parser.ParamInfo.Get<string>(ArgumentType.TestName);
            bool rebootFileExists = CommonExtensions.HasRebootFile();
            if(appSettings.AlternateLogFile)
                Log.Init(testName, appSettings.ReportLogLevel, true, rebootFileExists, true, true);
            else
                Log.Init(testName, appSettings.ReportLogLevel, true, rebootFileExists, true, false);

            if (!new WindowsPrincipal(WindowsIdentity.GetCurrent()).IsInRole(WindowsBuiltInRole.Administrator))
                Log.Abort("Run the test in Administrator mode!");
            if (!rebootFileExists)
            {
                Log.Message(true, "Test Command Line:: Execute.exe {0}", string.Join(" ", args));
                if (testName.ToLower().StartsWith("mp_"))
                    Log.Verbose("Build:: {0}", FileVersionInfo.GetVersionInfo(Assembly.GetExecutingAssembly().Location).FileVersion);
                else if (testName.ToLower().StartsWith("sb_"))
                    Log.Verbose("Build:: {0}", FileVersionInfo.GetVersionInfo(Assembly.GetExecutingAssembly().Location).ProductVersion);

                if (System.IO.File.Exists(QuickBuildVersion))
                {
                    string [] stVersionInfo = System.IO.File.ReadAllLines(QuickBuildVersion);

                    if(stVersionInfo.Length !=0)
                    Log.Verbose("Quick Build version:: {0}", stVersionInfo[0]);
                }
            }
            CommonExtensions.FlushRecordedLogMsgs();

            EnvPreparedness.RunTask(_appManager, Features.InitAssemblies);
            _appManager = new ApplicationManager(parser.ParamInfo, appSettings);
            DisplayExtensions.InitAccessInterface(_appManager.AccessInterface);
            Log.CaptureScreenOnError = () => _appManager.AccessInterface.GetFeature<string>(Features.CaptureScreenImage, Action.Get);

            EnvPreparedness.Init(_appManager, rebootFileExists);

            UIExtensions.Load(appSettings, _appManager.MachineInfo.Driver.DriverBaseLine);
            if ((testName.ToLower().StartsWith("mp_")) || (testName.ToLower().StartsWith("sb_")))
            {
                EnvPreparedness.RunTask(_appManager, Features.InitCheckDriverVerify);
                EnvPreparedness.RunTask(_appManager, Features.InitRebootAnalysis);
                parser.Parse<DisplayConfigList>(args, ArgumentType.Config);
                parser.Parse<DisplayList>(args, ArgumentType.Display);

                _context = _context.Load(testName);
                _context.EnableReference(_appManager, ComponentType.ApplicationManager);

                if (!_context.HasAttribute(TestType.HasPlugUnPlug) && !CommonExtensions._rebootAnalysysInfo.IsBasicDisplayAdapter)
                {
                    List<DisplayType> cmdlineDisplays = (List<DisplayType>)parser.ParamInfo[ArgumentType.Display];
                    if (null != cmdlineDisplays)
                    {
                        EnvPreparedness.RunTask(_appManager, Features.InitPlugDVMUDisplays);
                        EnvPreparedness.RunTask(_appManager, Features.InitPlugSimulatedDisplays);
                        EnvPreparedness.RunTask(_appManager, Features.InitEnumerateDisplays);
                        List<DisplayInfo> enumeratedDisplays = (List<DisplayInfo>)parser.ParamInfo[ArgumentType.Enumeration];

                        cmdlineDisplays.ForEach(cmdDisplays =>
                        {
                            if ((cmdDisplays != DisplayType.None) && (cmdDisplays != DisplayType.WIDI) &&
                               (enumeratedDisplays.Where(dI => dI.DisplayType == cmdDisplays).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None))
                                Log.Abort("Required display {0} is not enumerated, hence test is aborting", cmdDisplays);
                        });
                    }
                }
                else if (_context.HasAttribute(TestType.HasPlugUnPlug) && !CommonExtensions._rebootAnalysysInfo.IsBasicDisplayAdapter)
                {
                    if (!(_appManager.ApplicationSettings.UseULTFramework || _appManager.ApplicationSettings.UseDivaFramework || _appManager.ApplicationSettings.UseSHEFramework))   //SHE
                    {
                        List<DisplayType> DpDisplaysList = new List<DisplayType> { DisplayType.DP, DisplayType.DP_2, DisplayType.DP_3 };
                        List<DisplayType> cmdlineDisplays = (List<DisplayType>)parser.ParamInfo[ArgumentType.Display];
                        if (null != cmdlineDisplays)
                        {
                            List<DisplayInfo> enumeratedDisplays = (List<DisplayInfo>)parser.ParamInfo[ArgumentType.Enumeration];

                            cmdlineDisplays.Intersect(DpDisplaysList).ToList().ForEach(cmdDisplays =>
                            {
                                if ((cmdDisplays != DisplayType.None) && (cmdDisplays != DisplayType.WIDI) &&
                                   (enumeratedDisplays.Where(dI => dI.DisplayType == cmdDisplays).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None))
                                    Log.Abort("Required display {0} is not enumerated, hence test is aborting", cmdDisplays);
                            });
                        }
                    }
                }
                _methodInvocationLst = _context.LoadMethods();

                _methodInvocationIdx = CommonExtensions.ReadRebootInfo();
                CommonExtensions.ClearRebootFile();
                InvokeMethods();
            }
            else
            {
                CommonExtensions.ClearRebootFile();
                Features feature;
                if (Enum.TryParse<Features>(testName, true, out feature))
                {
                    _appManager.AccessInterface.SetFeature(feature, Action.Parse, args.Skip(1).ToArray());
                    CommonExtensions.Exit(0);
                }
                else
                    Log.Abort("Unable to identify functionality:: {0}", testName);
            }
        }

        private static void InvokeMethods()
        {
            try
            {
                int overrideIndex = 0;
                for (int idx = _methodInvocationIdx; idx < _methodInvocationLst.Count; idx++)
                {
                    overrideIndex = _context.GetSkipToMethodIndex();
                    if (!overrideIndex.Equals(-1))
                    {
                        idx = overrideIndex;
                        _context.ResetSkipMethodIndex();
                    }
                    _context.EnableReference(idx, ComponentType.CurrentMethodIndex);
                    _methodInvocationLst[idx].Invoke(_context, null);
                }
                EnvPreparedness.RunTask(_appManager, Features.InitTestCleanUp);
                CommonExtensions.Exit(0);
            }
            catch (Exception ex)
            {
                HandleException(ex);
            }
        }
        private static void GlobalExceptionHandler(object sender, UnhandledExceptionEventArgs e)
        {
            HandleException(e.ExceptionObject as Exception);
        }
        private static void HandleException(object argException)
        {
            if (!_exceptionLogged)
            {
                _exceptionLogged = true;
                Exception exception = argException as Exception;
                if (null != exception.InnerException)
                    exception = exception.InnerException;
                if (typeof(TestException).Equals(argException.GetType()))
                {
                    TestException testException = exception as TestException;
                    exception = testException.OriginalException;
                    if (null != exception.InnerException)
                    {
                        Log.Verbose("InnerException.Message:: {0}{1}", Environment.NewLine, exception.InnerException.Message);
                        Log.Verbose("{0}", exception.InnerException.StackTrace);
                    }
                }
                Log.Verbose("{0}", exception.StackTrace);
                Log.Fail(exception.Message);
            }
            EnvPreparedness.RunTask(_appManager, Features.InitTestCleanUp);
            CommonExtensions.Exit(-1);
        }
    }
}
