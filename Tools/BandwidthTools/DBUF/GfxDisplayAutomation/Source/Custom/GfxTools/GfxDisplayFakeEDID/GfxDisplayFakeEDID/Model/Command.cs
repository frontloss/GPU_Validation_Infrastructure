namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Windows.Input;

    public class Command : ICommand
    {
        private Action action = default(Action);
        private Predicate<object> condition = default(Predicate<object>);

        public event EventHandler CanExecuteChanged;

        public Command(Action action, Predicate<object> condition = default(Predicate<object>))
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
        public void Execute(object parameter)
        {
            if (action != default(Action))
                this.action();
        }
    }
}
