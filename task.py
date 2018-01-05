import csv
from random import shuffle
from psychopy import core
from glob import glob



class NBackDataPointBuilder:
    """ A class used to build up a data point, one piece at a time """
    def __init__(self):
        """ Create a data point builder"""
        self._data = {}

    def set_prime_name(self, prime_name):
        self._data['prime image id'] = prime_name

    def set_num_back(self, num_back):
        self._data['n-back type'] = num_back

    def set_order_set(self, order_set):
        self._data['order set'] = order_set

    def set_position_in_block(self, position):
        self._data['position in block'] = position

    def set_image_id(self, focal_image_id):
        self._data['image id'] = focal_image_id

    def set_n_back_image_id(self, n_back_image_id):
        self._data['n-back image'] = n_back_image_id

    def set_lure(self, lure):
        self._data['lure'] = lure

    def set_lure_kind(self, lure_kind):
        self._data['lure kind'] = lure_kind

    def set_expected_response(self, expected_response):
        self._data['expected response'] = expected_response

    def set_user_response(self, user_response):
        self._data['user response'] = user_response

    def set_reaction_time(self, reaction_time):
        self._data['reaction time'] = reaction_time


class NBackTask:
    def __init__(self, experiment):
        """ Create a n-back task for the given experiment """
        self.experiment = experiment
        self.window = experiment.window
        self.config = experiment.config

    def show_n_back(self, image_id, prime_path):
        """

        @param image_id:
        @param prime_path:
        @param timer:
        @return:
        @rtype:
        """
        self.window.n_back_show(image_id, prime_path)
        timer = core.CountdownTimer(self.config.n_back_display_time)

        # Catch user input
        if self.window.wait_for_prompt(timer, 'a'):
            # User pressed the key 'a'
            reaction_time = self.config.n_back_display_time - timer.getTime()
            core.wait(timer.getTime())
            return 1, reaction_time

        return 0, ''

    def get_n_back_image_id(self, num_back, last_image_ids):
        """

        @param num_back:
        @param last_image_ids:
        @return:
        """
        if len(last_image_ids) < num_back:
            return ''

        return last_image_ids[num_back - 1]

    def get_lure_info(self, num_back, image_id, last_image_ids):
        """ Return

        @param num_back:
        @param image_id:
        @param last_image_ids:
        @return:
        @rtype: (int, str)
        """
        for i in range(len(last_image_ids)):
            if i != num_back - 1 and last_image_ids[i] == image_id:
                return 1, "{}-back".format(i + 1)

        return 0, ''

    def show_n_back_block(self, block, num_back, test_number, image_id_column=2, save=True):
        """ Shows a block of images in the n-back tasks

        @param lst block: A matrix containing the ordering info for this block
        @param int num_back: The type of n-back task
        @param int test_number: What test number this is, used only for output
        @param int image_id_column: the column of the block matrix with the image_id information
        @param bool save: Whether the data should be saved to experiment['data'] or not
        @return: the number of wrong answers
        @rtype: int
        """
        # Get the prime images we'll use
        prime_images = glob('images/prime/task/{}/*/*_8.png'.format(self.config.n_back_prime_list_name))

        # Randomize the order in which the the prime images will be displayed
        shuffle(prime_images)

        # Counter for wrong answers
        wrong_answers = 0

        # A list containing the most recently viewed images
        last_image_ids = []

        for position_in_block in range(len(block)):
            # Get the prime
            prime_path = prime_images[position_in_block]
            prime_name = prime_path.split('/')[-1][:-6]

            # Rename some data for easier usage
            order_set = (self.config.n_back_block_total - test_number) if self.config.n_back_blocks_reversed else (test_number + 1)
            image_id = int(block[position_in_block][image_id_column])

            # Get what the user should answer
            n_back_image_id = self.get_n_back_image_id(num_back, last_image_ids)
            expected_response = int(image_id == n_back_image_id)

            # Get the lure information
            lure, lure_kind = self.get_lure_info(num_back, image_id, last_image_ids)

            # Get the user response
            user_response, reaction_time = self.show_n_back(image_id, prime_path)

            if user_response != expected_response:
                wrong_answers += 1

            # Save some data
            if save:
                data_point = [prime_name,
                              num_back, order_set, position_in_block + 1,
                              image_id, n_back_image_id,
                              lure, lure_kind,
                              expected_response,
                              user_response, reaction_time]
                self.experiment.push_data(data_point)

            # Add image_id to last_image_ids limiting it's size to 3
            last_image_ids = [image_id] + last_image_ids[:2]

            # Clear the window and wait for the ISI
            self.window.clear(self.config.n_back_interstimulus_interval)

        return wrong_answers

    def run(self):
        """ Run the n-back task"""
        # Start the n-back section of the experiment
        self.experiment.new_section('n-back')

        # Show the user some instructions
        self.window.show_images('instructions', 'start')

        if self.config.practice_run:
            # Show practice instructions
            self.window.show_images('instructions', 'practice')

            # PRACTICE RUN
            for i in range(2):
                # Get the file with the data for the image ordering
                block = get_csv_data("{}_practice.csv".format(i + 1))

                # Draw the instruction screen for this type of block
                self.window.show_images('prompts', '{}-back'.format(i + 1))

                # Go through this block without saving the data
                self.show_n_back_block(block, i + 1, i + 1, image_id_column=0, save=False)

        # Show instructions before actual test
        self.window.show_images("instructions", "test")

        # Load the blocks, in the order we'll run them.
        blocks = [[], [], []]
        for difficulty in range(3):
            for j in range(self.config.n_back_block_total):
                blocks[difficulty].append(get_csv_data("{}_{}.csv".format(difficulty + 1, j + 1)))

            # Reverse the blocks half of the time
            if self.config.n_back_blocks_reversed:
                blocks[difficulty].reverse()

        # Se the starting n_back difficulty
        num_back = self.config.n_back_start_difficulty

        # Start tests
        for test_number in range(self.config.n_back_block_total):
            # Get the block we will be using
            block = blocks[num_back - 1][test_number]

            # Show the instruction image
            self.window.show_images('prompts', '{}-back'.format(num_back))

            errors = self.show_n_back_block(block, num_back, test_number)

            if errors >= self.config.n_back_min_errors_to_lower_difficulty and num_back > 1:
                num_back -= 1

            elif errors <= self.config.n_back_max_errors_to_raise_difficulty and num_back < 3:
                num_back += 1

        # Store the data we gathered in experiment_info['data']
        self.experiment.save_data()

        # Put up the end of experiment screen
        self.window.show_images('instructions', 'end')


def get_csv_data(file_name, header=True):
    """ Return the information in the file_name csv file. Organized like [row0, row1, row2,...],
    where a row looks like [value1, value2,...]

    @param file_name: The name of the csv file to be parsed
    @param header: Is there a header in the csv file?
    @return: A list of lists
    """
    block_file = open("ordering/{}".format(file_name), 'rU')
    reader = csv.reader(block_file)
    lines = [l for l in reader]
    block_file.close()
    return lines[1:] if header else lines
