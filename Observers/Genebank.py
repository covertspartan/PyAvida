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
# 8 = phentypic depth
# 9 = genome -- only needed on

class genebank:
    def __init__(self, ctx):
        self.genebank = {}

        self.curr_id = 0

        assert isinstance(ctx, ccontext)

        self.ctx = ctx

    def add_entry(self, immutable_genotype, cpu):
        if immutable_genotype in self.genebank:
            self.genebank[immutable_genotype][4] += 1
            self.genebank[immutable_genotype][5] += 1
        else:
            self.genebank[immutable_genotype] = \
                [self.curr_id, cpu.parent_id, ctx.update, 0,
                 1, 1, cpu.fitness, cpu.merit, cpu.gestation_time, cpu.num_divides]

            self.curr_id += 1

        return self.genebank[immutable_genotype][0]

    def record_deactivation(self, immutable_genotype):
        self.genebank[immutable_genotype][4] -= 1
        return None

