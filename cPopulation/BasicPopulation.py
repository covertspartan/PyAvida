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

    def step(self):
        self.pop_list[self.scheduler.schedule_cpu()].step()

    def speculative_step(self):
        scheduled_id = self.scheduler.schedule_cpu()

        if self.speculative_execution[scheduled_id] > 0:
            self.speculative_execution[scheduled_id] -= 1
        else:
            self.speculative_execution[scheduled_id] += self.pop_list[scheduled_id].execute_ahead()

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

        inject_id = self.ctx.random.choice(self.pop_list).id

        old_inject_merit = self.merit[inject_id]

        self.fitness[inject_id] = fitness
        self.merit[inject_id] = merit
        self.generation[inject_id] = cpu.num_divides
        self.speculative_execution[inject_id] = 0

        self.pop_list[inject_id].inject_genome(offspring, self.generation[inject_id], fitness, merit)

        if old_merit is not merit:
            self.scheduler.update_merit(cpu.id, merit)

        if old_inject_merit is not merit:
            self.scheduler.update_merit(inject_id, merit)

        if not all(map(lambda (x, y): x is y, zip(cpu.genome, offspring))):
            print "Well shit"

        return None

    def end_update(self):
        length = float(len(self.pop_list))

        self.average_fitness = sum(self.fitness) / length
        self.average_merit = sum(self.merit) / length
        self.average_generation = sum(self.generation) / length

        return None