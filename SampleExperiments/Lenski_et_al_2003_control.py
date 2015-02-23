"""
A sample PyAvida Experiment based on the Lesnki et al 2003 control runs
"""
import sys
sys.path.append("..")

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
    """
    setup a context object -- this hold the random number generators
    make sure to seed it with a random number
    :rtype : object
    """
    ctx = ccontext.cContext(1)

    # before we can define a CPU we need an instruction set for the organisms
    inst_set = BasicInstructionSet()

    # now we can build a CPU, initialized with the default ancestor (a basic self replicator)
    cpu = CPU(ctx, inst_set, inst_set.encode_genome(fGetBasicTestOrgs.getDefaultGenome()))

    # our population of CPUs will need an environment
    # this gives the digital organisms the ability to be rewarded for performing certain functions
    environment = BasicLogic9Environment()

    #environment.only_equals()

    # Finally we need a way to see what happened in the experiment
    # The genebank will track every organism and can dump a file at the end
    genebank = Genebank.genebank(ctx)

    # next let's assemble a population of 10,000 CPUs all seeded with the default ancestor
    # avida populations are defined as X,Y grids
    # we also want to tell the population what environment it's in, and give it a genebank to use
    # population = BasicPopulation(ctx, cpu, 100, 100, environment, genebank)
    population = BasicPopulation(ctx, cpu, 100, 100, environment)

    # we need a mutator to cause mutations to happen
    # this mutator will mutate a genome 25% of the time it is called
    # make sure to pass it the population it will apply it's mutations to.
    DivideMutation(ctx, 0.25, population)

    # ready to roll!
    for update in xrange(0, 50000):
        # if ctx.update % 1000 == 0:
        #     import cProfile
        #     print cProfile.runctx("population.run_update()", globals(), locals())

        population.run_update(30 * population.max_pop_size)
        print "Update {:d}, orgs born: {:d}, average fitness: {:e}, average generation: {:f}".format(ctx.update, population.divide_count, population.average_fitness, population.average_generation)

    # dump out every organism that ever lived for post run analysis
    with open("detail-10000","w") as file_pointer:
        genebank.dump_spop_file(file_pointer)

    return None

if __name__=="__main__":
    main()