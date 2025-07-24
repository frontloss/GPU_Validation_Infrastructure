namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Reflection;
    using System.Collections.Generic;

    public class AccessInterface : IAccessInterface
    {
        private IApplicationManager _appManager = null;
        private ICacheWrapper _cache = null;
        private string _tile = string.Empty;
        private int _currentMethodIndex = -1;
        private int _overrideMethodIndex = -1;

        public AccessInterface(IApplicationManager argAppManager, ICacheWrapper argCache)
        {
            this._appManager = argAppManager;
            this._cache = argCache;
        }
        public int CurrentMethodIndex
        {
            set { this._currentMethodIndex = value; }
        }
        public int OverrideMethodIndex
        {
            set { this._overrideMethodIndex = value; }
        }
        public void Navigate(Features argFeature)
        {

            Dictionary<string, string> navigationList = CommonExtensions.GetNavigationList(argFeature);
            string sourceFromAppConfig = _appManager.ApplicationSettings.UIAutomationPath;
            Source source;
            if (!(Enum.TryParse<Source>(sourceFromAppConfig, out source)))
                source = Source.AccessUI;
            if (string.IsNullOrEmpty(this._tile))
                this._tile = navigationList.First().Key;
            else if (this._tile.Equals(navigationList.First().Key))
                navigationList.Remove(navigationList.First().Key);
            navigationList.ToList().ForEach(kV =>
            {
                INavigate action;
                if (source == Source.AccessUI)
                {
                    action = (INavigate)argFeature.Activate(Source.AccessUI, kV.Key);
                }
                else
                {
                    UIExtensions.setUIAEntity(kV.Key);
                    action = (INavigate)argFeature.Activate(source, "NavigationHandler", kV.Key);
                }
                action.Navigate();
            });
        }
        public R GetFeature<R>(Features argFeature, Action argAction)
        {
            return this.GetFeature<R>(argFeature, argAction, Source.Default);
        }
        public R GetFeature<R, C>(Features argFeature, Action argAction, C argContext)
        {
            return GetFeature<R, object, C>(argFeature, argAction, Source.Default, null, argContext);
        }
        public R GetFeature<R>(Features argFeature, Action argAction, Source argSource)
        {
            return GetFeature<R, object>(argFeature, argAction, argSource, null);
        }
        public R GetFeature<R, D>(Features argFeature, Action argAction, Source argSource, D argData)
        {
            return GetFeature<R, D, object>(argFeature, argAction, argSource, argData, null);
        }
        public R GetFeature<R, D, C>(Features argFeature, Action argAction, Source argSource, D argData, C argContext)
        {
            Message msg = new Message();
            msg.Feature = argFeature;
            msg.Action = argAction;
            if ((argSource == Source.AccessUI) && _appManager.ApplicationSettings.UIAutomationPath.Equals("WindowsAutomationUI"))
                argSource = Source.WindowsAutomationUI;
            msg.Source = argSource;
            msg.Data = argData;
            msg.Context = argContext;
            msg.AppManager = this._appManager;
            msg.CurrentMethodIndex = this._currentMethodIndex;
            msg.EnumeratedDisplays = this._appManager.ParamInfo.Get<List<DisplayInfo>>(ArgumentType.Enumeration);
            msg.OverrideMethodIndex = this._overrideMethodIndex;
            this.InvokeFeature(msg, false);
            return (R)msg.Value;
        }
        public R SetFeature<R>(Features argFeature, Action argAction)
        {
            return this.SetFeature<R, object>(argFeature, argAction, null);
        }
        public R SetFeature<R>(Features argFeature, Action argAction, Source argSource)
        {
            return this.SetFeature<R, object, object>(argFeature, argAction, argSource, null, null);
        }
        public R SetFeature<R, D>(Features argFeature, Action argAction, Source argSource, D argData)
        {
            return this.SetFeature<R, D, object>(argFeature, argAction, argSource, argData, null);
        }
        public void SetFeature<V>(Features argFeature, Action argAction, V argValue)
        {
            this.SetFeature<V>(argFeature, argAction, Source.Default, argValue);
        }
        public void SetFeature<V, C>(Features argFeature, Action argAction, V argValue, C argContext)
        {
            this.SetFeature<V, V, C>(argFeature, argAction, Source.Default, argValue, argContext);
        }
        public void SetFeature<V>(Features argFeature, Action argAction, Source argSource, V argValue)
        {
            this.SetFeature<V, V, object>(argFeature, argAction, argSource, argValue, null);
        }
        public R SetFeature<R, V>(Features argFeature, Action argAction, V argValue)
        {
            return this.SetFeature<R, V, object>(argFeature, argAction, Source.Default, argValue, null);
        }
        public R SetFeature<R, V, C>(Features argFeature, Action argAction, Source argSource, V argValue, C argContext)
        {
            if (argFeature == Features.LaunchCUI)
                this._tile = string.Empty;
            Message msg = new Message();
            msg.Feature = argFeature;
            msg.Action = argAction;
            if (argAction == Action.Parse)
                msg.CurrentConfig = this.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            msg.Value = argValue;
            if ((argSource == Source.AccessUI) && _appManager.ApplicationSettings.UIAutomationPath.Equals("WindowsAutomationUI"))
                argSource = Source.WindowsAutomationUI;
            msg.Source = argSource;
            msg.Context = argContext;
            msg.AppManager = this._appManager;
            msg.CurrentMethodIndex = this._currentMethodIndex;
            msg.EnumeratedDisplays = this._appManager.ParamInfo.Get<List<DisplayInfo>>(ArgumentType.Enumeration);
            msg.OverrideMethodIndex = this._overrideMethodIndex;
            this.InvokeFeature(msg, true);
            this.InvokeCommonVerification(msg);
            return (R)msg.Value;
        }

        private void InvokeCommonVerification(Message argMessage)
        {
            if (argMessage.Feature == Features.VerifySystemState)
                return;
            Message msg = new Message();
            msg.Feature = Features.VerifySystemState;
            msg.Action = Action.Get;
            msg.Source = Source.AccessAPI;
            msg.AppManager = this._appManager;
            msg.EnumeratedDisplays = this._appManager.ParamInfo.Get<List<DisplayInfo>>(ArgumentType.Enumeration);
            InvokeFeature(msg, true);
        }
        private void InvokeFeature(Message argMessage, bool argIsSet)
        {
            try
            {
                Type targetType = null;
                argMessage.Name = argMessage.Feature.GetElementValue("actionClass", argMessage.Source);
                targetType = Type.GetType(string.Concat(this._appManager.ApplicationSettings.DefaultNamespace, argMessage.Name));
                if (null == targetType)
                    Log.Abort("Unable to locate action type {0} for {1}:{2}", argMessage.Name, argMessage.Action, argMessage.Feature);
                MethodInfo targetMethod = this._cache.Get(argMessage);
                if (null == targetMethod)
                {
                    targetMethod = (from method in targetType.GetMethods(BindingFlags.Instance | BindingFlags.Public)
                                    from attribute in method.GetCustomAttributes(typeof(ActionTargetAttribute), false) as ActionTargetAttribute[]
                                    where attribute.Target == argMessage.Action
                                    select method).SingleOrDefault();
                    if (null == targetMethod)
                        Log.Abort("Unable to locate action method {0} for {1}", argMessage.Action, argMessage.Feature);

                    argMessage.Target = targetMethod;
                    this._cache.Add(argMessage);
                }
                ((Action<Message>)Delegate.CreateDelegate(typeof(Action<Message>), Activator.CreateInstance(targetType), targetMethod))(argMessage);
            }
            catch (Exception ex)
            {
                Log.Verbose("AccessInterface:: {0}", ex.Message);
                Log.Verbose("{0}", ex.StackTrace);
                if (null != ex.InnerException)
                {
                    Log.Verbose("AccessInterface. InnerEx:: {0}", ex.InnerException.Message);
                    Log.Verbose("{0}", ex.InnerException.StackTrace);
                }
                Log.Abort(ex, "Unable to {0} the {1} feature{2}", argMessage.Action, argMessage.Feature, argIsSet ? string.Format(" with {0}", argMessage.Value) : string.Empty);
            }
        }
    }
}