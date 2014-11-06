from cContext import ccontext
from cCPU import BasicCPU


#every instruction in the assembly language gets a reference to the cpu it runs on
#every instruction is responsible for advancing the CPUs flow control head
#so let it be written, so let it be done
class BasicInstructionSet:

    def nop_a(self, cpu):
        cpu.increment_ip()
        return 1

    def nop_b(self, cpu):
        cpu.increment_ip()
        return 2

    #a comment
    def nop_c(self, cpu):
        #print "nop_c"
        cpu.increment_ip()
        return 3

    #figure out which operands we must use and return their register values
    #@AWC should these helper function be part of the CPU?
    def get_two_registers(self, cpu):
        op1 = None
        op2 = None
        step = 0

        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)
        if nop is not None:
            op1 = cpu.registers[nop]
            op2 = cpu.registers[cpu.nop_complement[nop]]
            step = 1
        else:
            op1 = cpu.registers[1]
            op2 = cpu.registers[2]

        return op1, op2, step

    #@TODO: Check and see if there is a reason why big-avida counts labels as an execution
    def findLabel(self, cpu):
        label = []
        len = 0
        pos = cpu.ip + 1

        while pos < cpu.genome_len:
            nop = cpu.nops.get(cpu.genome[pos], None)
            if nop is not None:
                label.append(nop)
                len += 1
                #max label length hard-coded at 3
                if len >= 3:
                    break
            #both of these are invalid states, label not started, label must be longer than 1
            elif nop is None and len is 0:
                return None, 0
            elif nop is None and len == 1:
                return None, 0
            #end of valid label (len > 1 & len <= 3)
            elif nop is None and len > 1:
                break
            pos += 1
        #print "lenght: {:d}".format(len)
        return label, len

    #search for a given label, normally used with h_search
    def findLabelStartPos(self, cpu, search_label):

        match_len = len(search_label)
        start_pos = cpu.ip + match_len
        curr_pos = 0

        #search to the end of the string until we find the matching label
        while start_pos + curr_pos < cpu.genome_len and curr_pos is not match_len:
            nop = cpu.nops.get(cpu.genome[start_pos + curr_pos], None)
            if nop is search_label[curr_pos]:
                curr_pos += 1
            #if the current position is not a nop, it cannot be a label, so we can
            #skil past the current search position
            elif nop is None:
                start_pos = start_pos + curr_pos + 1
                curr_pos = 0
            #otherwise, the lable could be embedded in other nops and we can go no further
            else:
                start_pos += 1
                curr_pos = 0

        if curr_pos is match_len:
            return start_pos

        return None

    #figure out which register to use
    def which_register(self, cpu):
        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)

        if nop is not None:
            return nop, 1
        else:
            return 1, 0


    def if_n_equ(self, cpu):
        step = 1
        op1, op2, extra_step = self.get_two_registers(cpu)

        if op1 == op2:
            step += extra_step + 1
        else:
            step += extra_step

        cpu.increment_ip(step)
        return None


    def if_less(self, cpu):
        step = 1
        op1, op2, extra_step = self.get_two_registers(cpu)

        if op1 < op2:
            step += extra_step
        else:
            step += extra_step + 1

        cpu.increment_ip(step)
        return None

    def pop(self, cpu):
        register, extra_step = self.which_register(cpu)

        cpu.registers[register] = cpu.stacks[cpu.curr_stack][-1]

        del cpu.stacks[cpu.curr_stack][-1]

        #print cpu.registers
        #print cpu.stacks

        cpu.increment_ip(1+extra_step)
        return None

    def push(self, cpu):
        register, extra_step = self.which_register(cpu)

        cpu.stacks[cpu.curr_stack].append(cpu.registers[register])

        #print cpu.registers
        #print cpu.stacks

        cpu.increment_ip(1+extra_step)
        return None

    def swap_stk(self, cpu):

        cpu.curr_stack = int(~cpu.curr_stack)

        cpu.increment_ip(1)

        return None

    def swap(self, cpu):
        reg1, extra_step = self.which_register(cpu)
        reg2 = cpu.nop_complement[reg1]

        val1 = cpu.registers[reg1]
        val2 = cpu.registers[reg2]

        cpu.registers[reg2] = val1
        cpu.registers[reg1] = val2

        cpu.increment_ip(1+extra_step)

        #print cpu.registers

        return None

    def shift_r(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.registers[reg1] >>= 1

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    def shift_l(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.registers[reg1] <<= 1
        cpu.registers[reg1] &= 0xffffffff

        #print bin(cpu.registers[reg1])

        cpu.increment_ip(1+extra_step)

        return None

    def inc(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.registers[reg1] += 1
        cpu.registers[reg1] &= 0xffffffff

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    def dec(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.registers[reg1] -= 1

        #print bin(cpu.registers[1])

        cpu.increment_ip(1+extra_step)

        return None

    def add(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.registers[reg1] = cpu.registers[1] + cpu.registers[2]
        cpu.registers[reg1] &= 0xffffffff

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    def sub(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.registers[reg1] = cpu.registers[2] - cpu.registers[1]
        cpu.registers[reg1] &= 0xffffffff

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    def nand(self, cpu):
        reg1, extra_step = self.which_register(cpu)
        #print bin(cpu.registers[1])
        #print bin(cpu.registers[2])
        cpu.registers[reg1] = ~(cpu.registers[1] & cpu.registers[2]) & 0xffffffff

        #print bin(cpu.registers[reg1])

        cpu.increment_ip(1+extra_step)

        return None

    def io(self, cpu):
        reg1, extra_step = self.which_register(cpu)

        cpu.outputs.append(cpu.registers[reg1])
        cpu.registers[reg1] = cpu.next_input()

        cpu.increment_ip(1+extra_step)
        return None

    #allocate genome space -- need a max length so that we don't run off the rails
    def h_alloc(self, cpu):
        #print cpu.genome
        new_len = cpu.genome_len * 2
        if new_len > cpu.genome_max_len:
            new_len = cpu.genome_max_len

        for i in xrange(cpu.genome_len, new_len):
            cpu.genome.append(self.nop_c)

        cpu.registers[0] = new_len
        cpu.genome_len = new_len
        #print cpu.genome
        #print cpu.registers
        #print cpu.genome_len, len(cpu.genome)

        cpu.increment_ip()

        return None

    #this makes no sense until with have a copy operation -- implement last
    def h_divide(self, cpu):

        return None

    def h_copy(self, cpu):
        cpu.genome[cpu.write] = cpu.genome[cpu.read]
        cpu.increment_ip()
        return None

    def h_search(self, cpu):
        label, extra_steps = self.findLabel(cpu)

        #this will only happen if complement label is not found
        if label is None:
            cpu.registers[1] = 0
            cpu.registers[2] = 0
            cpu.increment_ip(extra_steps+1)


        complement_label = [cpu.nop_complement[i] for i in label]
        #print label
        #print complement_label

        search_pos = self.findLabelStartPos(cpu, complement_label)
        #print search_pos

        if search_pos is not None:
            #print "Found!!!!"
            cpu.flow = search_pos % cpu.genome_len
            cpu.increment_ip(extra_steps+1)
            cpu.registers[1] = cpu.flow - cpu.ip
            cpu.registers[2] = len(label)
            return None
        else:
            cpu.increment_ip(extra_steps+1)

        return None

    def mov_head(self, cpu):
        cpu.ip = cpu.flow
        return None

    #for now we will keep the instruction set simply as a list
    #this function will return a dict with all of the instructions in set
    #it will also return a list of nops and nop complements for pattern matching
    #if you wish you use a different instruction set, simply override this function
    def __init__(self):
        self.inst_set = dict()

        self.inst_set['a'] = self.nop_a
        self.inst_set['b'] = self.nop_b
        self.inst_set['c'] = self.nop_c

        self.inst_set['d'] = self.if_n_equ
        self.inst_set['e'] = self.if_less

        self.inst_set['f'] = self.pop
        self.inst_set['g'] = self.push
        self.inst_set['h'] = self.swap_stk
        self.inst_set['i'] = self.swap

        self.inst_set['j'] = self.shift_r
        self.inst_set['k'] = self.shift_l

        self.inst_set['l'] = self.dec
        self.inst_set['m'] = self.inc

        self.inst_set['n'] = self.add
        self.inst_set['o'] = self.sub

        self.inst_set['p'] = self.nand

        self.inst_set['q'] = self.io

        self.inst_set['r'] = self.h_alloc
        self.inst_set['s'] = self.h_divide
        self.inst_set['t'] = self.h_copy
        self.inst_set['u'] = self.h_search

        self.inst_set['v'] = self.mov_head

        #let's define nops and nop complements for  quick lookup
        self.nops = {self.nop_a: 0, self.nop_b: 1, self.nop_c: 2}

        self.nop_complement = (1, 2, 0)


