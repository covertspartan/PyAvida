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

    def add_entry(self, immutable_genotype, target_cpu):
        if immutable_genotype in self.genebank:
            self.genebank[immutable_genotype][4] += 1
            self.genebank[immutable_genotype][5] += 1
        else:
            readable_genome_string = ""
            for func_pointer in immutable_genotype:
                readable_genome_string += target_cpu.inst_set.decode_inst_set[func_pointer]
            parent_id = target_cpu.genome_id
            if parent_id is None:
                parent_id = -1
            self.genebank[immutable_genotype] = \
                [self.curr_id, parent_id, self.ctx.update, -1,
                 1, 1, target_cpu.fitness, target_cpu.merit, target_cpu.gestation_time, target_cpu.num_divides, readable_genome_string]
            target_cpu.genome_id = self.curr_id

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
        target_cpu.genome_id = genome_id
        return None

    def attach_population(self, population):
        for curr_cpu in population.pop_list:
            genome_id = self.add_entry(curr_cpu.original_genome, curr_cpu)
            curr_cpu.genome_id = genome_id

    def dump_spop_file(self, file_pointer):
        string_format = "{:d},{:d},{:d},{:d},{:d},{:d},{:f},{:f},{:d},{:d},{:s}\n"
        for genome, entry in self.genebank.items():
            file_pointer.write(string_format.format(*entry))