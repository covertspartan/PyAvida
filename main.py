from CPUs import BasicCPU
from Context import ccontext
from CPUs.basic_instruction_set import BasicInstructionSet
from Populations import BasicPopulation
from Populations import MutationHooks
from Environments import BasicLogic9Enironment
from TestingTools import fGetBasicTestOrgs
from Observers import Genebank

import cProfile

def build_genome(inst_set, string):

    genome = []

    for x in string:
        genome.append(inst_set.inst_set[x])

    return genome

def revert_genome(inst_set, genome):
    
    return genome_string

# wrapped in a function so that we can profile each update
def run_update(cpu_cycles, population):
    for tick in xrange(0, cpu_cycles):
        # population.step()
        population.speculative_step()

    population.end_update()
    return None

def main():
    ctx = ccontext.cContext(1)

    inst_set = BasicInstructionSet()

    environment = BasicLogic9Enironment.BasicLogic9Environment()

    genebank = Genebank.genebank(ctx)

    cpu = BasicCPU.CPU(ctx, inst_set, build_genome(inst_set, fGetBasicTestOrgs.getDefaultGenome()))

    population = BasicPopulation.BasicPopulation(ctx, cpu, 100, 100, environment)

    mutatator = MutationHooks.DivideMutation(ctx, 0.25)

    # tell the genebank and the population to talk to one another
    population.register_inject_hook(genebank.inject_hook)
    genebank.attach_population(population)

    environment.attach_population(population)

    population.register_mutation_hook(mutatator.mutation)

    print "Update {:d}, orgs born: {:d}, average fitness: {:f}, average generation: {:f}".format(ctx.update, population.divide_count, population.average_fitness, population.average_generation)
    for updates in range(0, 100):
        run_update(300000, population)
        print "Update {:d}, orgs born: {:d}, average fitness: {:f}, average generation: {:f}".format(ctx.update, population.divide_count, population.average_fitness, population.average_generation)



    # a little code to verify self-replication
    random_cpu = ctx.random.choice(population.pop_list)

    def decode_genome(x): return inst_set.decode_inst_set[x]

    decoded_genome = map(decode_genome, random_cpu.genome)

    print "Random genome {:s} which underwent {:d} self-replication cycles".format(str(decoded_genome), random_cpu.num_divides)
    print "Random genome hash: {:d}".format(hash(random_cpu))

    print cpu.ip, cpu.flow

    fp = open("detail-100.spop","w")
    genebank.dump_spop_file(fp)
    fp.close()


    return None

if __name__=="__main__":
    # cProfile.run('main()')
    main()
