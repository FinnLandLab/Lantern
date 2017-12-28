class Configuration:
    """ The configuration for an experiment """
    def __init__(self):
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
