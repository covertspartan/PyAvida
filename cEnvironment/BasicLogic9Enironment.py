class BasicLogic9Environment:

    # each function is defined by a tuple of three things
    # one) a lambda function to define it's result (as a binary number here)
    # 2a) a single bit unique ID (for record keeping) to pass to the callback function
    # 2b) a bonus to pass to the call back function
    # in this environment, only execution pre genome is rewarded

    @staticmethod
    def f_env_callback(bonus, id, cpu):
        cpu.func_triggers |= id
        return None

    def __init__(self):
        self.one_input_functions = [
            (lambda A: ~A & 0xffffffff,                       (0x1, 2))     # Not
        ]
        self.two_input_functions = [
            (lambda A, B: ~(A & B) & 0xffffffff,              (0x2, 2)),    # Nand
            (lambda A, B: (A & B) & 0xffffffff,               (0x4, 4)),    # And
            (lambda A, B: (~A | B) & 0xffffffff,              (0x8, 4)),    # OrNot 1
            (lambda A, B: (A | ~B) & 0xffffffff,              (0x8, 4)),    # OrNot 2
            (lambda A, B: (A | B) & 0xffffffff,               (0x10, 8)),   # Or
            (lambda A, B: (~A & B) & 0xfffffff,               (0x20, 8)),   # AndNot 1
            (lambda A, B: (A & ~B) & 0xfffffff,               (0x20, 8)),   # AndNot 2
            (lambda A, B: (~A & ~B) & 0xffffffff,             (0x40, 16)),  # Nor
            (lambda A, B: ((A & ~B) | (~A & B)) & 0xffffffff, (0x80, 16)),  # Xor
            (lambda A, B: ((A & B) | (~A & ~B)) & 0xffffffff, (0x100, 32))  # Equ
        ]
        self.three_input_functons = []

        self.population_array = []

    # this defines the set of outputs that are valid for any given input state
    # functionally it becomes a giant hash function implemented with lists and dicts
    def attach_population(self, population):
        for cpu in population.pop_list:
            input_array = [{} for state in cpu.input_states]
            # state 1
            for x, state in enumerate(input_array):
                input_state = cpu.input_states[x]
                A = cpu.inputs[input_state[0]] if input_state[0] is not None else None
                B = cpu.inputs[input_state[1]] if input_state[1] is not None else None
                C = cpu.inputs[input_state[2]] if input_state[2] is not None else None
                if A:
                    self.attach_one_input_functions(state,A)
                if A and B:
                    self.attach_two_input_functions(state,A,B)

            cpu.output_dict = input_array

            print cpu.output_dict[2]

    # helper function that adds all one input functions to the environment
    def attach_one_input_functions(self, output_dict, A):
        for func, bonus in self.one_input_functions:
            output_dict[func(A)] = bonus

    # helper function that adds all two input functions to the environment
    def attach_two_input_functions(self, output_dict, A, B):
        for func, bonus in self.two_input_functions:
            if output_dict.get(func(A, B), None):
                print "Collision -- not sure what to do here."
            output_dict[func(A, B)] = bonus

    def output_hook(self, cpu):

        ID, bonus = cpu.output_dict[cpu.input_state].get(cpu.outputs[-1], (None, None))

        if bonus is not None:
            BasicLogic9Environment.f_env_callback(bonus, ID, cpu)

        return None
