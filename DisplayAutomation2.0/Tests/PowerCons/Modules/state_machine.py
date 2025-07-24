#######################################################################################################################
# @file         state_machine.py
# @brief        Contains definitions for multiple classes required to build a state machine
#
# @author       Rohit Kumar
#######################################################################################################################


##
# @brief        Exposed object class for State
# @details      An instance of State class represents a state in the state machine. User can directly use this class or
#               inherit it, to add more properties or functions.
class State(object):
    ##
    # @brief        Initializes State object
    # @param[in]    name name of the state. It is recommended to keep unique names for states with-in state machine.
    # @param[in]    data [optional] any additional data to be stored in state
    def __init__(self, name, data=None):
        self.name = name
        self.data = data

    ##
    # @brief        Overridden str function
    # @return       Name of the State
    def __str__(self):
        return self.name


##
# @brief        Exposed object class for Input
# @details       An instance of Input class represents a state input in a state machine. StateMachine class determines
#               the next state based on this input. The same Input object is passed to every transition function, where
#               it can be used to detect any unexpected behavior. This class can be used directly or user can inherit
#               Input class, to add custom properties or functions.
class Input(object):
    ##
    # @brief        Initializes Input object
    # @param[in]    name name of the input. It is recommended to keep unique names for all possible inputs.
    # @param[in]    time_stamp [optional]
    def __init__(self, name, time_stamp=None):
        self.name = name
        self.time_stamp = time_stamp

    ##
    # @brief        Overridden str function
    # @return       Name of the input
    def __str__(self):
        return self.name


##
# @brief        Exposed class for creating StateMachine
class StateMachine(object):
    ##
    # @brief        Initializes StateMachine
    # @param[in]    initial_state
    # @param[in]    transition_table
    def __init__(self, initial_state, transition_table):
        self.state = initial_state
        self.transition_table = transition_table

    ##
    # @brief        Exposed API to process the input and transit to next state
    # @param[in]    state_input
    # @return       True if operation is successful, False otherwise
    def next_state(self, state_input):
        for table_entry in self.transition_table:
            if self.state != table_entry[0]:
                continue
            transition_input = table_entry[1]
            transition_test = table_entry[2]
            transition = table_entry[3]
            transition_state = table_entry[4]

            if transition_input == state_input.name:
                if transition_test is not None:
                    if not transition_test(state_input):
                        continue

                if transition is not None:
                    transition(self.state, transition_state, state_input)

                self.state = transition_state
                return True
        return False
