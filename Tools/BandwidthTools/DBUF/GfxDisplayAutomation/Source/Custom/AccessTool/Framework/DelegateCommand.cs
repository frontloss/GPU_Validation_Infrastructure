using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Input;

namespace Intel.VPG.Display.Automation
{
    public class DelegateCommand:ICommand
    {
        private Action<object> action = default(Action<object>);
        private Predicate<object> condition = default(Predicate<object>);

        public DelegateCommand(Action<object> action,
            Predicate<object> condition = default(Predicate<object>))
        {
            this.action = action;
            this.condition = condition;
        }

        public bool CanExecute(object parameter)
        {
            if (this.condition == default(Predicate<object>))
                return true;

            return this.condition(parameter);
        }

        public event EventHandler CanExecuteChanged;

        public void Execute(object parameter)
        {
            if (action != default(Action<object>))
                this.action(parameter);            
        }
    }
}
