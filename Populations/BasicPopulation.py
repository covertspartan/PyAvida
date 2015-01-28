from BasicProbScheduler import BasicProbScheduler

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

            # The BasicCPU has no divide checks by default, we'll give it some.
            # Let's make sure the Offspring genome has copied a significant
            # chunk of its genome before we let it try a divide
            self.pop_list[-1].divide_check = lambda cpu: \
                False if cpu.executed_length < (len(cpu.genome[cpu.read:cpu.write]) * 0.5) or \
                (len(cpu.genome[0:cpu.read]) * 2) < len(cpu.genome[cpu.read:cpu.write]) or \
                (len(cpu.genome[0:cpu.read]) * 0.5) > len(cpu.genome[cpu.read:cpu.write]) else True

            self.pop_list[-1].id = x

        self.fitness = [cpu.fitness for cpu in self.pop_list]
        self.merit = [cpu.merit for cpu in self.pop_list]
        self.generation = [cpu.num_divides for cpu in self.pop_list]

        self.speculative_execution = [0] * self.max_pop_size

        self.scheduler = BasicProbScheduler(self.merit, self.ctx)
        self.curr = 0

        self.inject_hooks = []
        self.mutation_hooks = []

    def register_inject_hook(self, func):
        self.inject_hooks.append(func)

    def register_mutation_hook(self, func):
        self.mutation_hooks.append(func)

    # basic step, schedule and run one CPU for one clock tick
    def step(self):
        self.pop_list[self.scheduler.schedule_cpu()].step()

    # execute a speculative step
    # schedule and speculatively run a cpu
    # runs CPUs 30 clock ticks ahead of where they're suppose to be, or until they need to interact with the environment
    # avoids pulling CPUs in and out of memory until they actually need to interact with the environment
    def speculative_step(self):
        scheduled_id = self.scheduler.schedule_cpu()

        if self.speculative_execution[scheduled_id] > 0:
            self.speculative_execution[scheduled_id] -= 1
        else:
            self.speculative_execution[scheduled_id] += self.pop_list[scheduled_id].execute_ahead()

    # helper function for divide hook
    # inject a genome into a random point in the population
    # this is what makes us a mass action population
    def inject(self, cpu, fitness, merit, offspring):
        inject_id = self.ctx.random.choice(self.pop_list).id

        self.fitness[inject_id] = fitness
        self.merit[inject_id] = merit
        self.generation[inject_id] = cpu.num_divides
        self.speculative_execution[inject_id] = 0

        for inject_hook in self.inject_hooks:
            inject_hook(cpu, self.pop_list[inject_id], offspring)

        if self.pop_list[inject_id].inject_genome(offspring, self.generation[inject_id], fitness, merit):
            self.scheduler.update_merit(inject_id, merit)

    # divide hook to randomly place an offspring
    def divide_hook(self, cpu, offspring):

        self.divide_count += 1

        # calculate fitness
        if self.environment is not None:
            fitness, merit = self.environment.calculate_fitness(cpu, offspring)
        else:
            fitness, merit = 1.0 / cpu.gestation_time, 1.0

        old_merit = cpu.merit

        cpu.fitness = fitness
        cpu.merit = merit
        cpu.num_divides += 1

        self.fitness[cpu.id] = fitness
        self.merit[cpu.id] = merit
        self.generation[cpu.id] = cpu.num_divides

        if old_merit is not merit:
            self.scheduler.update_merit(cpu.id, merit)

        if self.mutation_hooks is not None:
            for func in self.mutation_hooks:
                offspring = func(cpu, offspring)

        self.inject(cpu, fitness, merit, offspring)

        # if not all(map(lambda (x, y): x is y, zip(cpu.genome, offspring))):
        #     print "Well shit"

        return None

    # Run a single update of the simulation
    # Schedule and run thirty cpu cycles per living organisms
    def run_update(self, cpu_cycles):
        for tick in xrange(0, cpu_cycles):
            self.speculative_step()
        self.end_update()
        return None

    def end_update(self):
        length = float(len(self.pop_list))

        self.average_fitness = sum(self.fitness) / length
        self.average_merit = sum(self.merit) / length
        self.average_generation = sum(self.generation) / length

        self.ctx.update += 1

        return None