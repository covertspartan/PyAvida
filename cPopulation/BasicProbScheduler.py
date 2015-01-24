from cContext import ccontext
import random

# A quick and dirty probabilistic priority queue scheduler, based on a d-ary heap
# edge cases for size 10,000 block size 10 have been checked
# @todo:test this class for different population and block sizes
class BasicProbScheduler:

    @staticmethod
    def find_le(a, x):
        index = 0

        while a[index] <= x:
            index += 1

        return index

        # i = bisect_left(a,x)
        # if i:
        #     return i
        # else:
        #     return 0

    @staticmethod
    def cumulative_sum(array):
        result = [0.0] * len(array)

        for i in xrange(0, len(array)):
            if i is 0:
                result[i] = array[i]
            else:
                result[i] = array[i] + result[i-1]

        return result

    def __init__(self, merit_array, ctx, block_size=10):

        # size of the blocks to search
        self.block_size = block_size

        # context object for access to RNG
        self.ctx = ctx

        # build the leafs of the heap
        master_schedule = [[BasicProbScheduler.cumulative_sum(merit_array[start_position:start_position+self.block_size])
                           for start_position in xrange(0, len(merit_array), self.block_size)]]

        # build the interior nodes of the heap
        while len(master_schedule[-1]) is not self.block_size:
            master_schedule.append([BasicProbScheduler.cumulative_sum([sub_block[-1] for sub_block in master_schedule[-1][start_position:start_position+self.block_size]])
                                    for start_position in xrange(0, len(master_schedule[-1]), self.block_size)])

        # build the root of the heap
        master_schedule.append(BasicProbScheduler.cumulative_sum([sub_block[-1] for sub_block in master_schedule[-1]]))

        # this is probably bad practice, consider refactoring
        self.master_schedule = master_schedule

        # save the total merit for quick access
        self.total_merit = master_schedule[-1][-1]

        # save a copy of the population's merit array for quick rebuilding
        self.merit_array = merit_array

    # update the merit of a particular entry -- this is where the major speed up comes from
    # should be able to update the heap in big-Oh(block size * (log(pop size) / log (block size))) time
    def update_merit(self, index, new_merit):

        self.reschedule = True

        # update our list of raw merits
        self.merit_array[index] = new_merit

        # get the indices of the nodes at each level we will need to update
        indices = [index / self.block_size**level for level in xrange(1, len(self.master_schedule), 1)]

        # update from the leafs to the uppermost interior node
        for level, sub_block_index in enumerate(indices):

            start = sub_block_index * self.block_size
            end = start + self.block_size

            if level is 0:
                self.master_schedule[level][sub_block_index] = BasicProbScheduler.cumulative_sum(self.merit_array[start:end])
            else:
                self.master_schedule[level][sub_block_index] = BasicProbScheduler.cumulative_sum(
                    [sub_block[-1] for sub_block in self.master_schedule[level-1][start:end]])

        # update the root node
        self.master_schedule[-1] = BasicProbScheduler.cumulative_sum(
            [sub_block[-1] for sub_block in self.master_schedule[-2]])

        # update total merit
        self.total_merit = self.master_schedule[-1][-1]

        return None

    def schedule_cpu(self):
        random_search = self.ctx.random.random() * self.total_merit

        index = 0  # running count of the index

        search_array = self.master_schedule[-1]  # current array sub-block being searched

        search_level = len(self.master_schedule) - 1  # what level of the heap is being searched

        step = 0

        while search_level > 0:

            i = BasicProbScheduler.find_le(search_array, random_search)  # find the index of the next sub-block

            # this should never happen -- if it does, we're just scheduling random CPUs
            if i == self.block_size:
                print "ERROR: BasicProbScheduler failed to schedule a valid CPU"
                raise BaseException

            # update the search value, removing the cumulative total of discard parts of the schedule
            # don't need to do this if the search value is in the first sub-block
            if i is not 0:
                random_search -= search_array[i-1]

            # update the index with the value on this search level
            if step is 0:
                index = i
            else:
                index = i + index * self.block_size

            search_array = self.master_schedule[search_level - 1][index]  # get the next sub-block to search

            search_level -= 1  # go to the next search level
            step += 1


        index = BasicProbScheduler.find_le(search_array, random_search) + index*self.block_size

        return index

def scheduler_dry_run(scheduler):

    test_count = 0

    for i in xrange(1, 300000):
        cpu_index = scheduler.schedule_cpu()

        if cpu_index == 876:
            test_count += 1

    print "Target CPU was scheduled {:d} times.".format(test_count)


# test code, left in for future unit test framework
if __name__ == "__main__":
    ctx = ccontext.cContext(81083)

    dummy_merit_array = [1.0] * 1000

    cumulative_dummy_array = BasicProbScheduler.cumulative_sum(dummy_merit_array)

    scheduler = BasicProbScheduler(dummy_merit_array, ctx)

    # this cpu will have merit equal to the rest of the cpus combined
    # should be scheduled ~50% of the time
    scheduler.update_merit(876, 1001.0)

    print "scheduler {:f}".format(scheduler.total_merit)

    import cProfile

    cProfile.run('scheduler_dry_run(scheduler)')


