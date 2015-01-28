"""
A sample PyAvida Experiment based on the Lesnki et al 2003 control runs
"""

# book keeping and random number generator
from Context import ccontext

# tools to build the basic simulation
from CPUs.BasicCPU import CPU
from CPUs.basic_instruction_set import BasicInstructionSet
from TestingTools import fGetBasicTestOrgs
from Populations.BasicPopulation import BasicPopulation
from Environments.BasicLogic9Enironment import BasicLogic9Environment
from Populations.MutationHooks import DivideMutation

# tools for observing the experiment
from Observers import Genebank


def main():
    # setup a context object -- this hold the random number generators
    # make sure to seed it with a random number
    ctx = ccontext.cContext(1)

    # before we can define a CPU we need an instruction set for the organisms
    inst_set = BasicInstructionSet()

    # now we can build a CPU, initialized with the default ancestor (a basic self replicator)
    cpu = CPU(ctx, inst_set, inst_set.encode_genome(fGetBasicTestOrgs.getDefaultGenome()))

    # our population of CPUs will need an environment
    # this gives the digital organisms the ability to be rewarded for performing certain functions
    environment = BasicLogic9Environment()

    # next let's assemble a population of 10,000 CPUs all seeded with the default ancestor
    # avida populations are defined as X,Y grids
    # we also want to tell the population what environment it's in
    population = BasicPopulation(ctx, cpu, 100, 100, environment)

    # setup all the IO for orgs in the population
    environment.attach_population(population)

    # we need a mutator to cause mutations to happen
    # this mutator will mutate a genome 25% of the time it is called
    mutator = DivideMutation(ctx, 0.25)

    # Tell the population when organisms should be mutated
    # easiest to do it when a newly divided organism is being injected
    population.register_mutation_hook(mutator.mutation)

    # Finally we need a way to see what happened in the experiment
    # The genebank will track every organism and can dump a file at the end
    genebank = Genebank.genebank(ctx)

    genebank.attach_population(population)
    population.register_inject_hook(genebank.inject_hook)

    # ready to roll!
    for update in xrange(0,10000):
        population.run_update(30 * population.max_pop_size)
        print "Update {:d}, orgs born: {:d}, average fitness: {:f}, average generation: {:f}".format(ctx.update, population.divide_count, population.average_fitness, population.average_generation)

    with open("detail-10000","w") as file_pointer:
        genebank.dump_spop_file(file_pointer)

    return None

if __name__=="__main__":
    main()