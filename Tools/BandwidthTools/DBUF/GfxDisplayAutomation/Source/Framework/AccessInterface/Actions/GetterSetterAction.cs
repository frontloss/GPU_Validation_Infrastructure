namespace Intel.VPG.Display.Automation
{
    internal class GetterSetterAction : BaseAction
    {
        [ActionTarget(Action.Get)]
        public void Get(Message argMessage)
        {
            IGet getValue = (IGet)base.GetCaptureInstance(argMessage);
            argMessage.Value = getValue.Get;
        }
        [ActionTarget(Action.GetMethod)]
        public void GetMethod(Message argMessage)
        {
            IGetMethod getValue = (IGetMethod)base.GetCaptureInstance(argMessage);
            argMessage.Value = getValue.GetMethod(argMessage.Data);
        }
        [ActionTarget(Action.GetAll)]
        public void GetAll(Message argMessage)
        {
            IGetAll getAllValue = (IGetAll)base.GetCaptureInstance(argMessage);
            argMessage.Value = getAllValue.GetAll;
        }
        [ActionTarget(Action.GetAllMethod)]
        public void GetAllMethod(Message argMessage)
        {
            IGetAllMethod getAllValue = (IGetAllMethod)base.GetCaptureInstance(argMessage);
            argMessage.Value = getAllValue.GetAllMethod(argMessage.Data);
        }
        [ActionTarget(Action.Set)]
        public void Set(Message argMessage)
        {
            ISet setValue = (ISet)base.GetCaptureInstance(argMessage);
            setValue.Set = argMessage.Value;
        }
        [ActionTarget(Action.SetMethod)]
        public void SetMethod(Message argMessage)
        {
            ISetMethod setValue = (ISetMethod)base.GetCaptureInstance(argMessage);
            argMessage.Value = setValue.SetMethod(argMessage.Value);
        }
        [ActionTarget(Action.SetNoArgs)]
        public void SetNoArgs(Message argMessage)
        {
            ISetNoArgs setValue = (ISetNoArgs)base.GetCaptureInstance(argMessage);
            argMessage.Value = setValue.SetNoArgs();
        }
        [ActionTarget(Action.Visible)]
        public void Visible(Message argMessage)
        {
            IVisible status = (IVisible)base.GetCaptureInstance(argMessage);
            argMessage.Value = status.Visible;
        }
        [ActionTarget(Action.Parse)]
        public void Parse(Message argMessage)
        {
            IParse parse = (IParse)base.GetCaptureInstance(argMessage);
            parse.Parse((string[])argMessage.Value);
        }
        [ActionTarget(Action.EnabledMethod)]
        public void EnabledMethod(Message argMessage)
        {
            IEnabledMethod status = (IEnabledMethod)base.GetCaptureInstance(argMessage);
            argMessage.Value = status.EnabledMethod(argMessage.Value);
        }
        [ActionTarget(Action.VisibleMethod)]
        public void VisibleMethod(Message argMessage)
        {
            IVisibleMethod status = (IVisibleMethod)base.GetCaptureInstance(argMessage);
            argMessage.Value = status.VisibleMethod(argMessage.Value);
        }
    }
}
