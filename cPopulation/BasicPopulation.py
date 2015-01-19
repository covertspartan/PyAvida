from BasicProbScheduler import BasicProbScheduler
from bisect import bisect_left

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

        self.scheduler = BasicProbScheduler(self.merit, self.ctx)
        self.curr = 0

    def recalculte_cumulative_merit_array(self):
        self.cumulative_sum = BasicPopulation.cumulative_sum(self.merit)
        merit_sum = float(self.cumulative_sum[-1])
        self.cumulative_sum = map(lambda x: x/merit_sum, self.cumulative_sum)


    @staticmethod
    def cumulative_sum(array):
        result = [0.0] * len(array)
        for i, element in enumerate(array):
            if i is 0:
                result[i] = element
            else:
                result[i] = element + result[i-1]

        return result


    @staticmethod
    def find_le(a, x):
        i = bisect_left(a,x)
        if i:
            return i
        else:
            return 0
        raise ValueError

    def step(self):
        self.pop_list[self.scheduler.schedule_cpu()].step()
        # self.ctx.random.choice(self.pop_list).step()

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

        if old_merit is not merit:
            self.scheduler.update_merit(cpu.id, merit)

        if old_inject_merit is not merit:
            self.scheduler.update_merit(inject_id, merit)

        return None

    def end_update(self):
        length = float(len(self.pop_list))

        self.average_fitness = sum(self.fitness) / length
        self.average_merit = sum(self.merit) / length
        self.average_generation = sum(self.generation) / length
        return None