import time


class Configuration:
    """ The configuration for an experiment """
    def __init__(self, participant_num):
        """ Creates a configuration with the following values"""
        self.output_location = "data"

        self.practice_run = True

        self.n_back_task = True
        self.n_back_block_total = 4
        self.n_back_start_difficulty = 1
        self.n_back_min_errors_to_lower_difficulty = 5
        self.n_back_max_errors_to_raise_difficulty = 3
        self.n_back_focal_image_height = 10
        self.n_back_prime_image_height = 10
        self.n_back_image_overlap = False
        self.n_back_display_time = 1
        self.n_back_interstimulus_interval = 0.5

        self.prime_task = True
        self.prime_image_display_time = 1.5

        # The following are counter-balanced for the participant
        self.condition = participant_num % 4
        if self.n_back_task:
            self.n_back_blocks_reversed = self.condition % 2 == 0
            self.n_back_prime_list_name = 'A' if ((self.condition // 2) % 2 == 0) else 'B'
        else:
            self.n_back_blocks_reversed = None
            self.n_back_prime_list_name = None

        self.date = time.strftime('%c')
