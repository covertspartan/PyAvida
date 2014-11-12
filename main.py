from cCPU import BasicCPU
from cContext import ccontext
from cCPU.basic_instruction_set import BasicInstructionSet
from cPopulation import BasicPopulation

import cProfile

def build_genome(inst_set, string):

    genome = []

    for x in string:
        genome.append(inst_set.inst_set[x])

    return genome

#wrapped in a fuction so that we can profile each update
def run_update(cpu_cycles, population):
    #print id(population)
    for tick in xrange(0,cpu_cycles):
        population.step()
    return None

def main():
    ctx = ccontext.cContext(1)

    inst_set = BasicInstructionSet()

    cpu = BasicCPU.CPU(ctx, inst_set, build_genome(inst_set, 'rucavccccccccccccccccccccccccccccccccccccutycasvab'))

    population = BasicPopulation.BasicPopulation(ctx, cpu, 100, 100)

    for updates in range(0,1000):
        #print id(population)
        run_update(300000, population)
        print "Update {:d}, orgs born: {:d}".format(updates,population.divide_count)

    print cpu.ip, cpu.flow
    return None

if __name__=="__main__":
    #cProfile.run('main()')
    main()