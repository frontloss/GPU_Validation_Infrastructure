namespace Intel.VPG.Display.Automation
{
    using System.ComponentModel;

    public class BaseEntity : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void Notify(string propertyName)
        {
            if (!string.IsNullOrEmpty(propertyName) && PropertyChanged != default(PropertyChangedEventHandler))
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
