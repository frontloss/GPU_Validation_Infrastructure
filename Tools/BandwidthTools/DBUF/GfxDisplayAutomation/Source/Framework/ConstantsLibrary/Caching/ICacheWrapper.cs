namespace Intel.VPG.Display.Automation
{
    using System.Reflection;

    public interface ICacheWrapper
    {
        void Add(Message argMessage);
        MethodInfo Get(Message argMessage);
        void Purge();
    }
}
