from cContext import ccontext

# 0 = genotype id
# 1 = ancestor id
# 2 = update born
# 3 = update died
# 4 = number living
# 5 = number that ever lived
# 5 = fitness
# 6 = merit
# 7 = gestation time
# 8 = phenotypic depth
# 9 = genome -- only needed on

class genebank:
    def __init__(self, ctx):
        self.genebank = {}

        self.curr_id = 0

        assert isinstance(ctx, ccontext.cContext)

        self.ctx = ctx

    def add_entry(self, immutable_genotype, cpu):
        if immutable_genotype in self.genebank:
            self.genebank[immutable_genotype][4] += 1
            self.genebank[immutable_genotype][5] += 1
        else:
            self.genebank[immutable_genotype] = \
                [self.curr_id, cpu.id, self.ctx.update, 0,
                 1, 1, cpu.fitness, cpu.merit, cpu.gestation_time, cpu.num_divides]

            self.curr_id += 1

        return self.genebank[immutable_genotype][0]

    def record_deactivation(self, immutable_genotype):
        self.genebank[immutable_genotype][4] -= 1
        if self.genebank[immutable_genotype][4] is 0:
            self.genebank[immutable_genotype][3] = self.ctx.update
        return None

    def inject_hook(self, parent_cpu, target_cpu, offspring):
        self.record_deactivation(target_cpu.original_genome)
        genome_id = self.add_entry(tuple(offspring), parent_cpu)
        target_cpu.id = genome_id
        return None

    def attach_population(self, population):
        for cpu in population.pop_list:
            genome_id = self.add_entry(cpu.original_genome, cpu)
            cpu.id = genome_id

