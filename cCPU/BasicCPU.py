from cContext import ccontext

from sys import getsizeof

#the instruction set has been de-coupled from the cpu for two reasons
#1 so that we don't have to instantiate all of those functions ad infinitum and have load them in and out of memory
#2 to create a slightly more flexible way of changing the cpu
#in actuality this is more like a "cpu interface"

class BasicCPU:

    def __init__(self, ctx, inst_set, genome=None):

        self.ctx = ctx

        self.registers = [0, 0, 0]

        self.inst_set = inst_set
        self.nops = inst_set.nops
        self.nop_complement = inst_set.nop_complement

        self.genome = genome
        self.genome_len = len(genome)
        self.genome_max_len = 1024

        self.read = 0
        self.write = 0
        self.flow = 0
        self.ip = 0

        self.heads = [self.ip, self.read, self.write]

        self.stackA = []
        self.stackB = []

        self.inputs = (int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)))
        self.input_ptr = 0
        self.input_len = len(self.inputs)
        self.outputs = []
        self.copy_buffer = []

        self.stacks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_stack = 0



    def next_input(self):
        curr = self.input_ptr
        self.input_ptr = (curr + 1) % self.input_len
        return self.inputs[curr]

    def increment_ip(self, steps=1):
        self.ip = (self.ip + steps) % self.genome_len

    def changeHead(self, head, value):
        if head is 0:
            self.ip = value
        elif head is 1:
            self.read = value
        elif head is 2:
            self.write = value

    def getHead(self, head):
        if head is 0:
            return self.ip
        elif head is 1:
            return self.read
        elif head is 2:
            return self.write

    #resets the CPUs state, including reinitializing inputs, but it does NOT change the instruction set.
    def reset(self):
        self.read = 0
        self.write = 0
        self.flow = 0
        self.ip = 0

        self.inputs = (int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)),
                       int(self.ctx.random.getrandbits(32)))

        self.input_ptr = 0
        self.input_len = len(self.inputs)
        self.outputs = []
        self.copy_buffer = []

        self.stackA = []
        self.stackB = []

        self.stacks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_stack = 0

        self.registers = [0, 0, 0]

    def step(self):
        print getsizeof(self.genome[self.ip]), self.genome[self.ip]
        self.genome[self.ip](self)