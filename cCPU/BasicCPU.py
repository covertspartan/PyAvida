from cContext import context


#the instruction set has been de-coupled from the cpu for two reasons
#1 so that we don't have to instantiate all of those functions ad infinitum and have load them in and out of memory
#2 to create a slightly more flexible way of changing the cpu
#in actuality this is more like a "cpu interface"

class BasicCPU:


    def __init__(self, ctx, inst_set, genome=[]):

        self.ctx = ctx

        self.registers = [0,0,0]

        self.inst_set = inst_set
        self.nops = inst_set.nops
        self.nop_complement = inst_set.nop_complement

        self.genome = genome
        self.genome_len = len(genome)

        self.read = 0
        self.write = 0
        self.flow = 0

        self.inputs = (int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)))
        self.input_ptr = 0
        self.input_len = len(self.inputs)
        self.outputs = []

        self.stacks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_stack = 0



    def next_input(self):
        curr = self.input_ptr
        self.input_ptr = (curr + 1) % self.input_len
        return self.inputs[curr]

    def increment_flow(self,steps=1):
        self.flow = (self.flow + steps) % self.genome_len

    #resets the CPUs state, including reinitializing inputs, but it does NOT change the instruction set.
    def reset(self):
        self.read = 0
        self.write = 0
        self.flow = 0

        self.inputs = (int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)))

        self.input_ptr = 0
        self.input_len = len(self.inputs)
        self.outputs = []

        self.stackA = []
        self.stackB = []

        self.stacks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_stack = 0

        self.registers = [0, 0, 0]


    def step(self):
        self.genome[self.flow](self)