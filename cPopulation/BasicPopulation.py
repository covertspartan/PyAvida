# REALLY basic population class
#@TODO: implement a full scheduler (once we have a concept of merit)
class BasicPopulation:

    def __init__(self, ctx, cpu, x=100, y=100, env=None):
        self.ctx = ctx
        self.x_size = x
        self.y_size = y
        self.sample_cpy = cpu
        self.environment = env

        self.max_pop_size = self.x_size * self.y_size

        self.divide_count = 0

        self.pop_list = []

        self.average_generation = 0.0
        self.average_fitness = 0.0
        self.average_merit = 0.0

        for x in range(0, self.max_pop_size):
            self.pop_list.append(cpu.copy())
            self.pop_list[-1].register_divide_hook(self.divide_hook)

            if env is not None:
                self.pop_list[-1].register_output_hook(env.output_hook)

            self.pop_list[-1].id = x

        self.fitness = [cpu.fitness for cpu in self.pop_list]
        self.merit = [cpu.merit for cpu in self.pop_list]
        self.generation = [cpu.num_divides for cpu in self.pop_list]

        self.curr = 0

    def step(self):
        self.ctx.random.choice(self.pop_list).step()

    # divide hook to randomly place an offspring
    def divide_hook(self, cpu, offspring):
        self.divide_count += 1

        # calculate fitness
        if self.environment is not None:
            fitness, merit = self.environment.calculate_fitness(cpu, offspring)
        else:
            fitness, merit = 1.0, 1.0

        cpu.fitness = fitness
        cpu.merit = merit
        cpu.num_divides += 1

        self.fitness[cpu.id] = fitness
        self.merit[cpu.id] = merit
        self.generation[cpu.id] = cpu.num_divides
        #print "Executed length: {:f}".format(cpu.gestation_time)
        self.ctx.random.choice(self.pop_list).inject_genome(offspring, cpu.num_divides, fitness, merit)

        return None

    def end_update(self):
        length = float(len(self.pop_list))

        #sum_fit = sum(map(lambda cpu: cpu.fitness, self.pop_list))
        #self.average_fitness = sum(map(lambda cpu: cpu.fitness, self.pop_list)) / length
        #self.average_merit = sum(map(lambda cpu: cpu.merit, self.pop_list)) / length
        #self.average_generation = sum(map(lambda cpu: cpu.num_divides, self.pop_list)) / length

        self.average_fitness = sum(self.fitness) / length
        self.average_merit = sum(self.merit) / length
        self.average_generation = sum(self.generation) / length
        return None