namespace Intel.VPG.Display.Automation
{
    public interface ISDK
    {
        object Get(object args);
        object Set(object args);
        object GetAll(object args);
    }
}
