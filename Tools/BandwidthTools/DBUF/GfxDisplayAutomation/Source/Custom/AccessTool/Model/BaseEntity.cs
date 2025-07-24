using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;

namespace Intel.VPG.Display.Automation
{
    public abstract class BaseEntity : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void Notify(string propertyName)
        {
            if (!string.IsNullOrEmpty(propertyName) &&
                PropertyChanged != default(PropertyChangedEventHandler))
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
