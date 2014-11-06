from cCPU import BasicCPU
from cContext import ccontext
from cCPU.basic_instruction_set import BasicInstructionSet

def build_genome(inst_set, string):

    genome = []

    for x in string:
        genome.append(inst_set.inst_set[x])

    return genome


def main():
    ctx = ccontext.cContext(1)

    inst_set = BasicInstructionSet()

    cpu = BasicCPU.BasicCPU(ctx, inst_set, build_genome(inst_set, 'rucavccccccccccccccccccccccccccccccccccccutycasvab'))

    for x in xrange(200):
        print cpu.ip, cpu.flow
        cpu.step()

    print cpu.ip, cpu.flow
    return None

if __name__=="__main__":
    main()