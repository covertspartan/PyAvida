# REALLY basic population class
#@TODO: implement a full scheduler (once we have a concept of merit)
class BasicPopulation:

    def __init__(self, ctx, cpu, x=100, y=100, env=None):
        self.ctx = ctx
        self.x_size = x
        self.y_size = y
        self.sample_cpy = cpu

        self.max_pop_size = self.x_size * self.y_size

        self.divide_count = 0

        self.pop_list = []

        for x in range(0, self.max_pop_size):
            self.pop_list.append(cpu.copy())
            self.pop_list[-1].register_divide_hook(self.divide_hook)
            if env is not None:
                self.pop_list[-1].register_output_hook(env.output_hook)

        self.curr = 0

    def step(self):
        self.ctx.random.choice(self.pop_list).step()

    #divide hook to randomly place an offspring
    def divide_hook(self, cpu, offspring):
        self.divide_count += 1

        cpu.num_divides += 1

        self.ctx.random.choice(self.pop_list).inject_genome(offspring, cpu.num_divides)
        #print "Divide!"

        return None