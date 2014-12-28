class BasicLogic9Environment:

    #each function in the environment must have two function
    #one) to define it's result (as a binary number here)
    #two) a callback to define how it effects the organism who executed it
    #in this environment, only execution pre genome is rewarded

    #@TODO finish implementing logic nine environment
    #one input functions
    @staticmethod
    def f_not(A):
        return ~A & 0xffffffff

    @staticmethod
    def f_not_callback(cpu):
        cpu.func_triggers |= 0x1
        return None

    #two input tasks
    @staticmethod
    def f_nand(A, B):
        return ~(A & B) & 0xffffffff

    @staticmethod
    def f_nand_callback(cpu):
        cpu.func_triggers |= 0x2
        return None

    def __init__(self):
        self.one_input_functions = []
        self.two_input_functions = []
        self.three_input_functons = []

        self.one_input_functions.append((self.f_not, self.f_not_callback))

        self.two_input_functions.append((self.f_nand, self.f_nand_callback))

        self.population_array = []

    #this defines the set of output that are valid for any given input state
    #functionally it becomes a giant hash function implemented with lists and dicts
    def attach_population(self, population):
        for cpu in population.pop_list:
            input_array = [{} for state in cpu.input_states]
            #state 1
            for x, state in enumerate(input_array):
                input_state = cpu.input_states[x]
                A = cpu.inputs[input_state[0]] if len(input_state) > 0 else None
                B = cpu.inputs[input_state[1]] if len(input_state) > 1 else None
                C = cpu.inputs[input_state[2]] if len(input_state) > 2 else None
                if A:
                    self.attach_one_input_functions(state,A)
                if A and B:
                    self.attach_two_input_functions(state,A,B)

            cpu.output_dict = input_array

    def attach_one_input_functions(self, output_dict, A):
        for func, bonus in self.one_input_functions:
            output_dict[func(A)] = bonus

    def attach_two_input_functions(self, output_dict, A, B):
        for func, bonus in self.two_input_functions:
            output_dict[func(A,B)] = bonus

    def output_hook(self, cpu):

        callback = cpu.output_dict[cpu.input_state].get(cpu.outputs[-1], None)

        if callback is not None:
            callback(cpu)

        return None
