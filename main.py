from cCPU import BasicCPU
from cContext import context
from cCPU.basic_instruction_set import BasicInstructionSet


def build_genome(inst_set, string):

    genome = []

    for x in string:
        genome.append(inst_set.inst_set[x])

    return genome


def main():
    ctx = context.context(1)

    inst_set = BasicInstructionSet()



    cpu = BasicCPU.BasicCPU(ctx, inst_set, build_genome(inst_set, 'pkiagfbcccc'))

    for x in xrange(50):
        cpu.step()
        print cpu.flow

    return None

if __name__=="__main__":
    main()