from cCPU import BasicCPU


class DivideMutation:
    def __init__(self, ctx, rate):
        self.ctx = ctx

        self.mutation_rate = rate

    def mutation(self, cpu, offspring):
        if self.ctx.random.random() < self.mutation_rate:
            pos = self.ctx.random.randint(0,len(offspring)-1)

            new_inst = self.ctx.random.choice(cpu.inst_set.inst_set.keys())

            offspring[pos] = cpu.inst_set.inst_set[new_inst]

        return offspring
