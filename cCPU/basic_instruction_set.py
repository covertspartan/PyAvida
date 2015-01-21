from cContext import ccontext
from cCPU import BasicCPU


#every instruction in the assembly language gets a reference to the cpu it runs on
#every instruction is responsible for advancing the CPUs flow control head
#so let it be written, so let it be done
class BasicInstructionSet:

    @staticmethod
    def nop_a(cpu):
        cpu.increment_ip()
        return 1

    @staticmethod
    def nop_b(cpu):
        cpu.increment_ip()
        return 2

    @staticmethod
    def nop_c(cpu):
        #print "nop_c"
        cpu.increment_ip()
        return 3

    #figure out which operands we must use and return their register values
    #@AWC should these helper function be part of the CPU?
    @staticmethod
    def get_two_registers(cpu):
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
    @staticmethod
    def findLabel(cpu):
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
    @staticmethod
    def findLabelStartPos(cpu, search_label):

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
            return start_pos + match_len

        return None

    #figure out which register to use
    @staticmethod
    def which_register(cpu):
        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)

        if nop is not None:
            return nop, 1
        else:
            return 1, 0

    @staticmethod
    def if_n_equ(cpu):
        step = 1
        op1, op2, extra_step = BasicInstructionSet.get_two_registers(cpu)

        if op1 == op2:
            step += extra_step + 1
        else:
            step += extra_step

        cpu.increment_ip(step)
        return None


    @staticmethod
    def if_less(cpu):
        step = 1
        op1, op2, extra_step = BasicInstructionSet.get_two_registers(cpu)

        if op1 < op2:
            step += extra_step
        else:
            step += extra_step + 1

        cpu.increment_ip(step)
        return None

    @staticmethod
    def pop(cpu):
        register, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[register] = cpu.stacks[cpu.curr_stack][-1]

        del cpu.stacks[cpu.curr_stack][-1]

        #print cpu.registers
        #print cpu.stacks

        cpu.increment_ip(1+extra_step)
        return None

    @staticmethod
    def push(cpu):
        register, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.stacks[cpu.curr_stack].append(cpu.registers[register])

        #print cpu.registers
        #print cpu.stacks

        cpu.increment_ip(1+extra_step)
        return None

    @staticmethod
    def swap_stk(cpu):

        cpu.curr_stack = int(~cpu.curr_stack)

        cpu.increment_ip(1)

        return None

    @staticmethod
    def swap(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)
        reg2 = cpu.nop_complement[reg1]

        val1 = cpu.registers[reg1]
        val2 = cpu.registers[reg2]

        cpu.registers[reg2] = val1
        cpu.registers[reg1] = val2

        cpu.increment_ip(1+extra_step)

        #print cpu.registers

        return None

    @staticmethod
    def shift_r(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[reg1] >>= 1

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def shift_l(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[reg1] <<= 1
        cpu.registers[reg1] &= 0xffffffff

        #print bin(cpu.registers[reg1])

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def inc(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[reg1] += 1
        cpu.registers[reg1] &= 0xffffffff

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def dec(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[reg1] -= 1
        cpu.registers[reg1] &= 0xffffffff

#        #print bin(cpu.registers[1])

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def add(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[reg1] = cpu.registers[1] + cpu.registers[2]
        cpu.registers[reg1] &= 0xffffffff

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def sub(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.registers[reg1] = cpu.registers[2] - cpu.registers[1]
        cpu.registers[reg1] &= 0xffffffff

        #print cpu.registers

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def nand(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)
        #print bin(cpu.registers[1])
        #print bin(cpu.registers[2])
        cpu.registers[reg1] = ~(cpu.registers[1] & cpu.registers[2]) & 0xffffffff

        #print bin(cpu.registers[reg1])

        cpu.increment_ip(1+extra_step)

        return None

    @staticmethod
    def io(cpu):
        reg1, extra_step = BasicInstructionSet.which_register(cpu)

        cpu.outputs.append(cpu.registers[reg1])

        #conceptually, the output hooks should be handled before the input state is changed
        for func in cpu.output_hooks:
            func(cpu)

        cpu.registers[reg1] = cpu.next_input()


        cpu.increment_ip(1+extra_step)
        return None

    #allocate genome space -- need a max length so that we don't run off the rails
    @staticmethod
    def h_alloc(cpu):
        #print cpu.genome
        new_len = cpu.genome_len * 2
        if new_len > cpu.genome_max_len:
            new_len = cpu.genome_max_len

        cpu.genome += [BasicInstructionSet.nop_c] * cpu.genome_len
        #for i in xrange(cpu.genome_len, new_len):
        #    cpu.genome.append(BasicInstructionSet.nop_c)

        cpu.execution_trace += [0] * cpu.genome_len
        cpu.registers[0] = new_len
        cpu.genome_len = new_len


        cpu.increment_ip()

        return None

    #big finish
    @staticmethod
    def h_divide(cpu):
        #@TODO Some evloved orgs from big-avida rely on restrictions here to self-replicate at the usual time, consider adding such restrictions back in
        # this only works if the write head is in the correct place and the divide checks return true
        if cpu.write is not cpu.read:

            # what do the offspring and parent look like so far?
            if not cpu.divide_check(cpu):
                cpu.increment_ip()
                return False

            offspring = cpu.genome[cpu.read:cpu.write]
            cpu.genome = cpu.genome[0:cpu.read]
            cpu.genome_len = len(cpu.genome)

            for func in cpu.divide_hooks:
                func(cpu, offspring)

            cpu.reset()

            #print "offspring ({:d}): {:s}".format(len(offspring), offspring)
            #print "genome ({:d}): {:s}".format(len(cpu.genome), cpu.genome)
            #quit()

        return None

    @staticmethod
    def h_copy(cpu):
        cpu.genome[cpu.write] = cpu.genome[cpu.read]
        cpu.copy_buffer.append(cpu.genome[cpu.read])

        cpu.write += 1
        cpu.read += 1
        cpu.increment_ip()

        return None

    @staticmethod
    def h_search(cpu):
        label, extra_steps = BasicInstructionSet.findLabel(cpu)

        #this will only happen if complement label is not found
        if label is None:
            cpu.registers[1] = 0
            cpu.registers[2] = 0
            cpu.flow = cpu.ip + 1 % cpu.genome_len
            cpu.increment_ip(extra_steps+1)
            return None



        complement_label = [cpu.nop_complement[i] for i in label]
        #print label
        #print complement_label

        search_pos = BasicInstructionSet.findLabelStartPos(cpu, complement_label)
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

    @staticmethod
    def mov_head(cpu):
        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)
        step = 2

        if nop is None:
            step = 1
            nop = 0

        cpu.changeHead(nop,cpu.flow)

        #ONLY increment the IP IF we haven't already moved it.
        if nop is not 0:
            cpu.increment_ip(step)

        return None

    @staticmethod
    def jmp_head(cpu):
        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)
        step = 2

        if nop is None:
            step = 1
            nop = 0

        cpu.changeHead(nop, cpu.getHead(2) + cpu.registers[2] % cpu.genome_len)

        #do not increment the IP if we just moved it
        if nop is not 0:
            cpu.increment_ip(step)
        return None

    @staticmethod
    def get_head(cpu):
        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)
        step = 2

        if nop is None:
            step = 1
            nop = 0

        cpu.registers[2] = cpu.getHead(nop)

        cpu.increment_ip(step)
        return None

    @staticmethod
    def if_label(cpu):
        label, extra_steps = BasicInstructionSet.findLabel(cpu)
        #print "here"
        if label is None:
            cpu.increment_ip()
            return None

        complement_label = [cpu.nop_complement[i] for i in label]

        label_len = len(complement_label)

        #are we going to find a match?
        for i in xrange(1, label_len+1):
            nopNum = cpu.nops.get(cpu.copy_buffer[-i], None)
            if len(cpu.copy_buffer) > 48:
                None
            if complement_label[-i] is not nopNum:
                #no match, break out
                cpu.increment_ip(extra_steps+2)
                return None

        #if we're here, then a match was found
        #increment IP past the label and execute the function there
        cpu.increment_ip(extra_steps+1)

        return None

    @staticmethod
    def set_flow(cpu):
        nop = cpu.nops.get(cpu.genome[cpu.ip+1], None)
        step = 2

        #default to the CX register
        if nop is None:
            nop = 2
            step = 1

        #pressumbably, we mod the
        cpu.flow = cpu.registers[nop] % cpu.genome_len

        cpu.increment_ip(step)
        return None

    #for now we will keep the instruction set simply as a list
    #this function will return a dict with all of the instructions in set
    #it will also return a list of nops and nop complements for pattern matching
    #if you wish you use a different instruction set, simply override this function
    def __init__(self):
        print "Help! Help! I'm being oppressed!"
        self.inst_set = dict()

        self.inst_set['a'] = BasicInstructionSet.nop_a
        self.inst_set['b'] = BasicInstructionSet.nop_b
        self.inst_set['c'] = BasicInstructionSet.nop_c

        self.inst_set['d'] = BasicInstructionSet.if_n_equ
        self.inst_set['e'] = BasicInstructionSet.if_less

        self.inst_set['f'] = BasicInstructionSet.pop
        self.inst_set['g'] = BasicInstructionSet.push
        self.inst_set['h'] = BasicInstructionSet.swap_stk
        self.inst_set['i'] = BasicInstructionSet.swap

        self.inst_set['j'] = BasicInstructionSet.shift_r
        self.inst_set['k'] = BasicInstructionSet.shift_l

        self.inst_set['l'] = BasicInstructionSet.dec
        self.inst_set['m'] = BasicInstructionSet.inc

        self.inst_set['n'] = BasicInstructionSet.add
        self.inst_set['o'] = BasicInstructionSet.sub

        self.inst_set['p'] = BasicInstructionSet.nand

        self.inst_set['q'] = BasicInstructionSet.io

        self.inst_set['r'] = BasicInstructionSet.h_alloc
        self.inst_set['s'] = BasicInstructionSet.h_divide
        self.inst_set['t'] = BasicInstructionSet.h_copy
        self.inst_set['u'] = BasicInstructionSet.h_search

        #@todo:check with big-avida to see how it implements these commands -- I think they're working properly now, but want to double check
        self.inst_set['v'] = BasicInstructionSet.mov_head
        self.inst_set['w'] = BasicInstructionSet.jmp_head
        self.inst_set['x'] = BasicInstructionSet.get_head

        self.inst_set['y'] = BasicInstructionSet.if_label

        self.inst_set['z'] = BasicInstructionSet.set_flow


        #let's define nops and nop complements for  quick lookup
        self.nops = {BasicInstructionSet.nop_a: 0, BasicInstructionSet.nop_b: 1, BasicInstructionSet.nop_c: 2}

        self.interactive_inst = set((BasicInstructionSet.io, BasicInstructionSet.h_divide))

        self.nop_complement = (1, 2, 0)

        #reverse the instruction set for fast decoding.
        self.decode_inst_set = {}
        for inst in self.inst_set.viewkeys():
            self.decode_inst_set[self.inst_set[inst]] = inst
