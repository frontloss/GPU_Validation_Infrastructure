namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;

    public interface IAccessInterface
    {
        R GetFeature<R>(Features argFeature, Action argAction);
        R GetFeature<R, C>(Features argFeature, Action argAction, C argContext);
        R GetFeature<R>(Features argFeature, Action argAction, Source argSource);
        R GetFeature<R, D>(Features argFeature, Action argAction, Source argSource, D argData);
        R GetFeature<R, D, C>(Features argFeature, Action argAction, Source argSource, D argData, C argContext);
        void SetFeature<V>(Features argFeature, Action argAction, V argValue);
        void SetFeature<V, C>(Features argFeature, Action argAction, V argValue, C argContext);
        void SetFeature<V>(Features argFeature, Action argAction, Source argSource, V argValue);
        R SetFeature<R>(Features argFeature, Action argAction);
        R SetFeature<R>(Features argFeature, Action argAction, Source argSource);
        R SetFeature<R, D>(Features argFeature, Action argAction, Source argSource, D argData);
        R SetFeature<R, V>(Features argFeature, Action argAction, V argValue);
        R SetFeature<R, V, C>(Features argFeature, Action argAction, Source argSource, V argValue, C argContext);
        void Navigate(Features argFeature);
        int CurrentMethodIndex { set; }
        int OverrideMethodIndex { set; }
    }
}