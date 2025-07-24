namespace Intel.VPG.Display.Automation
{
    internal class DTCMAction : BaseAction
    {
        [ActionTarget(Action.Get)]
        public void Get(Message argMessage)
        {
            IGet getValue = this.GetContext<IGet>(argMessage);
            argMessage.Value = getValue.Get;
        }
        [ActionTarget(Action.Set)]
        public void Set(Message argMessage)
        {
            ISet setValue = this.GetContext<ISet>(argMessage);
            setValue.Set = argMessage.Value;
        }
        [ActionTarget(Action.VisibleMethod)]
        public void VisibleMethod(Message argMessage)
        {
            IVisibleMethod status = this.GetContext<IVisibleMethod>(argMessage);
            argMessage.Value = status.VisibleMethod(argMessage.Data);
        }
        [ActionTarget(Action.GetAll)]
        public void GetAll(Message argMessage)
        {
            IGetAll getAllValue = this.GetContext<IGetAll>(argMessage);
            argMessage.Value = getAllValue.GetAll;
        }

        private T GetContext<T>(Message argMessage)
        {
            object type = base.GetCaptureInstance(argMessage);
            ((ISetMethod)type).SetMethod(argMessage.Context);
            return (T)type;
        }
    }
}
