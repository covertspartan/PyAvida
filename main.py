from cCPU import BasicCPU
from cContext import ccontext
from cCPU.basic_instruction_set import BasicInstructionSet
from cPopulation import BasicPopulation
from cEnvironment import BasicLogic9Enironment

import cProfile

def build_genome(inst_set, string):

    genome = []

    for x in string:
        genome.append(inst_set.inst_set[x])

    return genome

def revert_genome(inst_set, genome):
    
    return genome_string

#wrapped in a fuction so that we can profile each update
def run_update(cpu_cycles, population):
    #print id(population)
    for tick in xrange(0,cpu_cycles):
        population.step()
    return None

def main():
    ctx = ccontext.cContext(1)

    inst_set = BasicInstructionSet()

    cpu = BasicCPU.CPU(ctx, inst_set, build_genome(inst_set, 'rucavcccccccccccccccqqcpqbccccccccccccccutycasvab'))
    #cpu = BasicCPU.CPU(ctx, inst_set, build_genome(inst_set, 'rucavcccccccccccccccccccccccccpccchccccccutycasvab'))
    #cpu = BasicCPU.CPU(ctx, inst_set, build_genome(inst_set, 'rucavcozjccscicccccccccccamxelqcnqhccpcqcutycastvab'))

    environment = BasicLogic9Enironment.BasicLogic9Environment()

    population = BasicPopulation.BasicPopulation(ctx, cpu, 1, 1, environment)

    environment.attach_population(population)

    for updates in range(0,1000):
        run_update(300000, population)
        print "Update {:d}, orgs born: {:d}".format(updates,population.divide_count)

    #a little code to verify self-replication
    random_cpu = ctx.random.choice(population.pop_list)

    def decode_genome(x): return inst_set.decode_inst_set[x]

    decoded_genome = map(decode_genome, random_cpu.genome)

    print "Random genome {:s} which underwent {:d} self-replication cycles".format(str(decoded_genome), random_cpu.num_divides)

    print cpu.ip, cpu.flow
    return None

if __name__=="__main__":
    #cProfile.run('main()')
    main()