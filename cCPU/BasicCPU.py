from cContext import ccontext
from copy import deepcopy

# the instruction set has been de-coupled from the cpu for two reasons
# 1 so that we don't have to instantiate all of those functions ad infinitum and have load them in and out of memory
# 2 to create a slightly more flexible way of changing the cpu
# in actuality this is more like a "cpu interface"
class CPU:
    def __init__(self, ctx, inst_set, genome=None, orig=None, id = None):

        # handel copy constructor operation
        if orig is not None:
            self.ctx = orig.ctx
            self.inst_set = orig.inst_set
            self.genome = deepcopy(orig.genome)
            self.genome_len = len(self.genome)
            self.execution_trace = deepcopy(orig.execution_trace)
            self.num_divides = orig.num_divides
        else:
            self.ctx = ctx
            self.inst_set = inst_set
            self.genome = genome
            self.genome_len = len(self.genome)
            self.execution_trace = [0] * self.genome_len
            self.num_divides = 0

        self.original_genome = tuple(self.genome)
        self.registers = [0, 0, 0]

        self.nops = inst_set.nops
        self.nop_complement = inst_set.nop_complement

        self.genome_max_len = 1024

        self.gestation_time = 0

        self.read = 0
        self.write = 0
        self.flow = 0
        self.ip = 0

        self.heads = [self.ip, self.read, self.write]

        self.stackA = []
        self.stackB = []

        # @todo: make I/O environment specific -- push the initialization of these to the env class (if any)
        self.inputs = (int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)))
        self.input_ptr = 0
        self.input_len = len(self.inputs)
        self.input_state = 0
        self.input_states = ((None, None, None), #0
                             (0, None, None),    #1
                             (1, 0, None),       #2
                             (2, 1, 0),          #3
                             (0, 2, 1),          #4
                             (1, 0, 2))          #5
        self.outputs = []
        self.copy_buffer = []

        self.stacks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_stack = 0

        # This is used by the environment, if it exists
        self.output_dict = None

        self.divide_hooks = []

        self.output_hooks = []

        # binary number representing which functions have been triggered
        self.func_triggers = 0x0

        self.env_bonus = 1
        self.merit = 1.0
        self.fitness = self.merit / self.genome_len

        self.executed_length = 0

        self.id = id

        self.divide_check = lambda cpu: True

    def __hash__(self):
        return hash(self.original_genome)

    def copy(self):
        return CPU(self.ctx, self.inst_set, orig=self)

    def inject_genome(self, genome, num_divides, fitness, merit):

        old_merit = self.merit

        self.genome = genome
        self.original_genome = tuple(genome)
        self.genome_len = len(genome)
        self.num_divides = num_divides
        self.fitness = fitness
        self.merit = merit
        self.reset()

        if old_merit is not merit:
            return True

        return False

    def next_input(self):
        curr = self.input_ptr
        self.input_ptr = (curr + 1) % self.input_len
        self.input_state += 1
        if self.input_state > 5:
            self.input_state = 3

        return self.inputs[curr]

    def increment_ip(self, steps=1):
        self.ip = (self.ip + steps) % self.genome_len

    def changeHead(self, head, value):
        if head is 0:       #nop-a
            self.ip = value
        elif head is 1:     #nop-b
            self.read = value
        elif head is 2:     #nop-c
            self.write = value

    def getHead(self, head):
        if head is 0:
            return self.ip
        elif head is 1:
            return self.read
        elif head is 2:
            return self.write

    # resets the CPUs state, but it does NOT change the instruction set.
    # a full reset also purges fitness, num_divides and merit data.
    def reset(self, full_reset = False):
        self.read = 0
        self.write = 0
        self.flow = 0
        self.ip = 0

        if full_reset:
            self.merit = 1
            self.fitness = self.merit / self.genome_len
            self.num_divides = 0

        # self.inputs = (int(self.ctx.random.getrandbits(32)),
        #                int(self.ctx.random.getrandbits(32)),
        #                int(self.ctx.random.getrandbits(32)))

        self.input_ptr = 0
        self.input_len = len(self.inputs)
        self.input_state = 0
        self.outputs = []
        self.copy_buffer = []

        self.stackA = []
        self.stackB = []

        self.stacks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_stack = 0

        self.registers = [0, 0, 0]

        self.func_triggers = 0

        self.gestation_time = 0

        self.env_bonus = 1

        self.executed_length = 0
        del self.execution_trace
        self.execution_trace = [0] * self.genome_len

    # execute the next thing that the IP head is on
    def step(self):
        # book keeping
        self.gestation_time += 1
        if self.execution_trace[self.ip] is 0:
            self.executed_length += 1
        self.execution_trace[self.ip] += 1

        # execute the next instruction
        self.genome[self.ip](self)

    def execute_ahead(self, number_steps=30):
        count = 1
        self.step()

        while self.genome[self.ip] not in self.inst_set.interactive_inst and count < number_steps:
            self.step()
            count += 1

        return count

    def register_divide_hook(self, func):
        self.divide_hooks.append(func)

    def register_output_hook(self, func):
        self.output_hooks.append(func)