using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_XVYCC : SB_WideGamut_Base
    {
        protected Features _feature;
        protected string _enableEvent;
        protected string _disableEvent;
        protected string _edidFile;
        protected ColorType _colorType;

        int _infValue = 0;
        protected List<DisplayType> _wideGamutDisplay = null;
        public SB_WideGamut_XVYCC()
        {
            _feature = Features.XvYcc;
            _colorType = ColorType.XvYCC;
            _enableEvent = "XVYCC_ENABLE";
            _disableEvent = "XVYCC_DISABLE";
            _edidFile = "HDMI_DELL_U2711_XVYCC.EDID";
        }
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.DisplayList.Intersect(base._pluggableDisplay.Keys).ToList().Count() == 0)
                Log.Abort("Display List does not contain pluggable display");
             
            Log.Message(true, "Disabling Driver Signature Enforcement");
            SetBCDEditOptions("-set loadoptions DDISABLE_INTEGRITY_CHECKS", "-set TESTSIGNING ON");          
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message("Verify Disabling Driver Signature Enforcement");
            CheckBCDEditOptions("loadoptions DDISABLE_INTEGRITY_CHECKS", "testSigning Yes");
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {           
            _wideGamutDisplay = new List<DisplayType>();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (!base._pluggableDisplay.Keys.Contains(curDisp))
                {
                    _infValue = _infValue + _wideGamutInfValue[curDisp];
                    _wideGamutDisplay.Add(curDisp);
                }
            });
            base.WideGamutDriver(_infValue);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            base.InitializeHotplugFramework();
            base.CurrentConfig.DisplayList.Intersect(base._pluggableDisplay.Keys).ToList().ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Any(dI=> dI.DisplayType==curDisp))
                {
                    base.HotUnPlug(curDisp);
                }
            });
            base.CurrentConfig.DisplayList.Intersect(base._pluggableDisplay.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, _edidFile);
            });
            base.ApplyConfigOS(base.CurrentConfig);

            _wideGamutDisplay = new List<DisplayType>();
           // _infValue = 0;
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (!base._pluggableDisplay.Keys.Contains(curDisp))
                {
                   // _infValue = _infValue + _wideGamutInfValue[curDisp];
                    _wideGamutDisplay.Add(curDisp);
                }
            });
           // base.VerifyInfValue(_infValue, _wideGamutDisplay.First());
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            ColorFeature(_feature, 1);

        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            ApplyAllWideGamutVerifyColorFeature(_enableEvent);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public virtual void TestStep6()
        {
            ColorFeature(_feature, 0);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public virtual void TestStep7()
        {
            ApplyAllWideGamutVerifyColorFeature(_disableEvent);
        }
        [Test(Type = TestType.Method, Order = 8)]
        public virtual void TestStep8()
        {
            base.WideGamutDriver(0);
        }
        protected void ColorFeature(Features argColorFeature, int argStatus)
        {
            string status = "Disable";
            if (argStatus == 1)
                status = "Enable";

            base.CurrentConfig.DisplayList.Intersect(base._pluggableDisplay.Keys).ToList().ForEach(curDisp =>
            {
                Log.Message(true, "{0} {1} for {2}", status, argColorFeature, curDisp);
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                if ((argColorFeature == Features.XvYcc && displayInfo.ColorInfo.IsXvYcc) || (argColorFeature == Features.YCbCr && displayInfo.ColorInfo.IsYcBcr))
                {
                    XvYccYcbXr xvyccObj = new XvYccYcbXr()
                    {
                        displayType = displayInfo.DisplayType,
                        currentConfig = base.CurrentConfig,
                        colorType = _colorType,
                        isEnabled = argStatus
                    };
                    if (AccessInterface.SetFeature<bool, XvYccYcbXr>(argColorFeature, Action.SetMethod, xvyccObj))
                    {
                        Log.Success("{0} IS {1} FOR {2}", argColorFeature, status, curDisp);
                    }
                    else
                    {
                        Log.Fail("Failed to {0} {1} for {2}", status, argColorFeature, curDisp);
                    }
                }
            });
        }
        protected void VerifyColorFeature(string argEvent)
        {
            base.CurrentConfig.DisplayList.Intersect(base._pluggableDisplay.Keys).ToList().ForEach(curDisp =>
            {
                Log.Message(true, "Verifying {0} for {1}", _feature, curDisp);
                PipePlaneParams pipePlane1 = new PipePlaneParams(curDisp);
                pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
                Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", curDisp, pipePlane1.Pipe, pipePlane1.Plane);

                base.VerifyRegisters(argEvent, pipePlane1.Pipe, PLANE.NONE, PORT.NONE);
            });
        }
        protected void ApplyAllWideGamutVerifyColorFeature(string argEvent)
        {
            _wbLevelEventMap.Keys.ToList().ForEach(curWbLevel =>
            {
                _wideGamutDisplay.ForEach(curDisp =>
                {
                    ApplyWideGamutToDisplay(curDisp, curWbLevel);
                    VerifyWideGamutValue(curDisp, curWbLevel);
                    VerifyColorFeature(argEvent);
                });
            });
        }
    }
}
