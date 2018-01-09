import random
from psychopy import core
import glob
import re
import pandas


class Trial:
    """ Used to run and save the results of a single n-back trial"""
    class DataPoint:
        """ A class used to store data about a trial. Passed in to the experiment class to be saved."""

        def __init__(self, block):
            """ Create a data point builder
            @param Block block: The block this DataPoint's trial is in
            """
            self.position_in_block = block.get_current_position()
            self.focal_image_id = block.get_current_focal_image_id()
            self.prime_image_path = block.get_current_prime_image_path()
            self.prime_image_id = re.split('[/\\\\]', self.prime_image_path)[-1]
            self.n_back_image_id = block.get_n_back_image_id()
            self.lure, self.lure_kind = self.get_lure_info(block)
            self.expected_response = (self.focal_image_id == self.n_back_image_id)

            # The user has to fill these in
            self.user_response = False
            self.user_correct = None
            self.reaction_time = None

            self.__parent = block.to_save

        def get_lure_info(self, block):
            """ Return if there is a lure, and information about the lure if it exists. A lure happens when an i-back
            focal image is the same as the current focal image, and i is not the n-back difficulty for the block

            @param Block block: the block that this DataPoint's trial belongs to
            @return: (bool, str | None)
            """
            lure = False
            lure_kind = None
            for i in range(1, 4):
                if i == block.to_save.n_back_type:
                    continue
                i_back = block.get_i_back_image_id(i)
                if i_back is not None and i_back == self.focal_image_id:
                    lure = True
                    lure_kind = "{}-back".format(i + 1)
                    return lure, lure_kind
            return lure, lure_kind

    def __init__(self, block):
        """ Creates an n-back trial for the given NBackBlock
        @param Block block: the block this trial is for
        """
        self.block = block
        self.experiment = block.experiment
        self.window = block.window
        self.config = block.config
        self.to_save = self.DataPoint(block)

    def show_n_back(self):
        """ Show one screen of the n-back task for a certain amount of time and record the results"""
        self.window.n_back_show(self.to_save.focal_image_id, self.to_save.prime_image_path)
        timer = core.CountdownTimer(self.config.n_back_display_time)
        # Catch user input
        if self.window.wait_for_prompt(timer, 'a'):
            # User pressed the key 'a'
            self.to_save.reaction_time = self.config.n_back_display_time - timer.getTime()
            self.to_save.user_response = True
            core.wait(timer.getTime())

        self.to_save.user_correct = (self.to_save.user_response == self.to_save.expected_response)

    def run(self):
        """ Run this n-back trial, along with pre and post trial tasks."""
        self.show_n_back()
        self.window.clear(self.config.n_back_interstimulus_interval)   # Wait for the ISI


class Block:
    """ Used to run and save the results of a block of n-back trials"""
    class Configuration:
        """ A class used to store the configuration info of a NBackBlock"""
        def __init__(self, n_back_type, order_set, save, prime_folder, loop_prime):
            """ Creates a configuration for a Block

            @param int n_back_type: The type of n-back in this block
            @param order_set: what order set to pull the ordering info from
            @param bool save: whether we should save data collected in this block or not
            @param bool loop_prime: if there are less primes than the size of the block, should we
            loop the images we do have or crash
            """
            self.n_back_type = n_back_type
            self.order_set = order_set
            self.prime_folder = prime_folder
            self.loop_primes = loop_prime
            self.save = save

        def get_focal_image_id_order(self):
            df = pandas.read_csv("ordering/" + self.order_set)
            return df['img_numb']

        def get_prime_image_path_order(self, do_not_start_with=None):
            """ Return a list of paths to prime images, from the folder self.prime_folder. Optional argument
            do_not_start_with indicates a path in the directory that should not be the first one in the ordering

            @param str|None do_not_start_with: don't start the prime image path order with the given path
            @return: lst(str)
            """
            paths = glob.glob(self.prime_folder + '/*/*_8.png')
            if do_not_start_with is not None:
                paths.remove(do_not_start_with)
                first = random.choice(paths)
                paths.remove(first)
                paths.append(do_not_start_with)
                random.shuffle(paths)
                return [first] + paths

            random.shuffle(paths)
            return paths

    class DataPoint:
        """ A class used to store data about a n-back block. Passed in to the experiment class to be saved"""
        def __init__(self, task, block_number, block_config):
            """ Create a data point object

            @param: Task task: the task this DataPoint's Block belongs to
            @param int block_number: how many blocks came before this one
            @param Block.Configuration block_config: the config that this DataPoint's Block is built from
            """
            self.n_back_type = block_config.n_back_type
            self.block_number = block_number
            self.order_set = block_config.order_set
            self.prime_folder = block_config.prime_folder
            self.__parent = task.config

    def __init__(self, task, block_number, block_config):
        """ Creates an n-back block for the given NBackTask

        @param Task task: the task this block belongs to
        @param int block_number: The number of the current block
        @param Block.Configuration block_config: The way this block should be configured """
        self.task = task
        self.experiment = task.experiment
        self.window = task.window
        self.config = task.config
        self.block_config = block_config

        # Internal variables, not to be saved
        self.focal_image_order = block_config.get_focal_image_id_order()
        self.prime_image_order = block_config.get_prime_image_path_order()

        self.trial_number = None
        self.error_tally = None

        # Variables to be saved, along with self.config
        self.to_save = self.DataPoint(task, block_number, block_config)

    def get_i_back_image_id(self, i):
        """ Finds the id of the focal image that was displayed i trials ago,
        where 1 <= i <= the current trial number.

        @param int i:
        @return: None|int"""
        if 1 <= i <= self.trial_number:
            return self.focal_image_order[self.trial_number - i]
        return None

    def get_n_back_image_id(self):
        """ Finds the id of the focal image that was displayed n (or n_back_type) trials ago,
        where n is the n-back difficulty.

        @return: None|int"""
        return self.get_i_back_image_id(self.to_save.n_back_type)

    def run(self):
        """ Runs before a single task in a block"""
        # Counter for wrong answers
        self.error_tally = 0
        for self.trial_number in range(len(self.focal_image_order)):
            trial = Trial(self)
            trial.run()
            if not trial.to_save.user_correct:
                self.error_tally += 1
            if self.block_config.save:
                self.experiment.push_data(trial.to_save)

    def get_current_position(self):
        return self.trial_number

    def get_current_focal_image_id(self):
        return self.focal_image_order[self.trial_number]

    def get_current_prime_image_path(self):
        if self.block_config.loop_primes and self.trial_number >= len(self.prime_image_order):
            last_path = self.prime_image_order[len(self.prime_image_order) - 1]
            self.prime_image_order.extend(self.block_config.get_prime_image_path_order(do_not_start_with=last_path))
        return self.prime_image_order[self.trial_number]


class Task:
    def __init__(self, experiment):
        """ Create a n-back task for the given experiment """
        self.experiment = experiment
        self.window = experiment.window
        self.config = experiment.config

    def run(self):
        """ Run the n-back task"""
        # Start the n-back section of the experiment
        self.experiment.new_section('n-back')

        # Show the user some instructions
        self.window.show_images('instructions', 'start')

        if self.config.practice_run:
            # Show practice instructions
            self.window.show_images('instructions', 'practice')

            for i in range(2):
                prac_config = Block.Configuration(n_back_type=i + 1, order_set="{}_practice.csv".format(i + 1),
                                                  prime_folder="images/prime/practice", save=False, loop_prime=True)
                # Get the file with the data for the image ordering
                block = Block(task=self, block_number=-1, block_config=prac_config)

                # Draw the instruction screen for this type of block
                self.window.show_images('prompts', '{}-back'.format(i + 1))

                # Go through this block without saving the data
                block.run()

        # Show instructions before actual test
        self.window.show_images("instructions", "test")

        # Load the blocks, in the order we'll run them.
        blocks = [[], [], []]
        for difficulty in range(3):
            for j in range(self.config.n_back_block_total):
                blocks[difficulty].append("{}_{}.csv".format(difficulty + 1, j + 1))

            # Reverse the blocks half of the time
            if self.config.n_back_blocks_reversed:
                blocks[difficulty].reverse()

        # Se the starting n_back difficulty
        num_back = self.config.n_back_start_difficulty

        # Start tests
        for test_number in range(self.config.n_back_block_total):

            order_set = blocks[num_back - 1][test_number]

            config = Block.Configuration(n_back_type=num_back, order_set=order_set,
                                         prime_folder="images/prime/task/{}".format(self.config.n_back_prime_list_name),
                                         save=True, loop_prime=False)

            block = Block(task=self, block_number=test_number, block_config=config)

            # Draw the instruction screen for this type of block
            self.window.show_images('prompts', '{}-back'.format(num_back))

            # Go through this block without saving the data
            block.run()

            errors = block.error_tally

            if errors >= self.config.n_back_min_errors_to_lower_difficulty and num_back > 1:
                num_back -= 1

            elif errors <= self.config.n_back_max_errors_to_raise_difficulty and num_back < 3:
                num_back += 1

        # Store the data we gathered in experiment_info['data']
        self.experiment.save_data()

        # Put up the end of experiment screen
        self.window.show_images('instructions', 'end')
