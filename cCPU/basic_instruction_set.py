from cContext import context
from cCPU import BasicCPU


#every instruction in the assembly language gets a reference to the cpu it runs on
#every instruction is responsible for advancing the CPUs flow control head
#so let it be written, so let it be done
class BasicInstructionSet:

    def nop_a(self, cpu):
        cpu.increment_flow()
        return 1

    def nop_b(self, cpu):
        cpu.increment_flow()
        return 2

    #a comment
    def nop_c(self, cpu):
        cpu.increment_flow()
        return 3

    #figure out which operands we must use and return their register values
    #@AWC should these helper function be part of the CPU?
    def get_two_registers(self, cpu):
        op1 = None
        op2 = None
        step = 0

        nop = cpu.nops.get(str(cpu.genome[cpu.flow+1]), None)
        if nop is not None:
            op1 = cpu.registers[nop]
            op2 = cpu.registers[cpu.nop_complement[nop]]
            step = 1
        else:
            op1 = cpu.registers[1]
            op2 = cpu.registers[2]

        return op1, op2, step

    #figure out which register to use
    def which_register(self, cpu):
        nop = cpu.nops.get(str(cpu.genome[cpu.flow+1]), None)

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

        cpu.increment_flow(step)
        return None


    def if_less(self, cpu):
        step = 1
        op1, op2, extra_step = self.get_two_registers(cpu)

        if op1 < op2:
            step += extra_step
        else:
            step += extra_step + 1

        cpu.increment_flow(step)
        return None

    def pop(self, cpu):
        register, step = self.which_register(cpu)

        cpu.registers[register] = cpu.stacks[cpu.curr_stack][0]

        del cpu.stacks[cpu.curr_stack][0]

        print cpu.registers
        print cpu.stacks

        cpu.increment_flow(step)
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

        #let's define nops and nop complements for  quick lookup
        self.nops = {str(self.nop_a): 0, str(self.nop_b): 1, str(self.nop_c):2 }

        self.nop_complement = (1, 2, 0)


