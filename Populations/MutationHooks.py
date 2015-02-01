from CPUs import BasicCPU

class DivideMutation:
    def __init__(self, ctx, rate, population=None):
        self.ctx = ctx

        self.mutation_rate = rate

        if population is not None:
            population.register_mutation_hook(self.mutation)



    def mutation(self, cpu, offspring):
        if self.ctx.random.random() < self.mutation_rate:
            pos = self.ctx.random.randint(0,len(offspring)-1)

            new_inst = self.ctx.random.choice(cpu.inst_set.inst_set.keys())

            offspring[pos] = cpu.inst_set.inst_set[new_inst]

        return offspring
