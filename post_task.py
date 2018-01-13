from psychopy import core


class Trial:
    """ Trial for the prime reconition task """
    class DataPoint:
        """ DataPoint for a trial"""

        def __init__(self, image_folder_path, position, task):
            self.image_folder_path = image_folder_path
            self.image_name = image_folder_path.split('/')[-1]
            self.position = position

            self.difficulty = None
            self.user_response = None
            self.response_time = None

            self.parent = task.to_save

    def __init__(self, image_folder_path, position, task):
        """ Create a trial object"""
        self.experiment = task.experiment
        self.window = task.window
        self.config = task.config
        self.to_save = self.DataPoint(image_folder_path, position, task)

    def run(self):
        """ Run the prime image identification task for the images in the folder folder_path """
        folder_path = self.to_save.image_folder_path
        folder_name = folder_path.split('/')[-1]

        timer = core.CountdownTimer(self.config.prime_image_display_time)

        for difficulty in range(8):
            # Show the prime image for this difficulty
            prime_image.image = "{0}/{1}_{2}.png".format(folder_path, folder_name, difficulty + 1)

            prime_image.draw()
            window.flip()

            # Wait for an input by the user, or for a timeout
            timer.reset()
            if wait_for_prompt(timer=timer, key='space'):
                # Get the responce time
                reaction_time = PRIME_IMAGE_DISPLAY_TIME - timer.getTime()

                # User wants to input text, get input and break to next image
                user_responce = get_input_text()

                # Return the experiment_info['data'] we collected
                return [difficulty + 1, user_responce, reaction_time]

        # The user did not react in in time. Get the to identify something
        user_responce = get_input_text()

        return [8, user_responce, 'N/A']


class Task:
    """ A block of the """
    class DataPoint:
        """ A DataPoint for a block"""

class PrimeTask:
    def __init__(self, experiment):
        """ Create a prime task for the given experiment """
        self.experiment = experiment
        self.window = experiment.window
        self.config = experiment.config




    def run(self):
        """ Run the prime task"""
        # Change the section info
        self.experiment.new_section('prime')

        # Randomize how the prime image will be shown
        prime_list = glob.glob('images/prime/task/*/*')
        random.shuffle(prime_list)

        # Show the instructions for this task:
        self.window.show_image_sequence('instructions', 'start')

        # Go through the practice task
        if PRACTICE_RUN:
            self.window.show_image_sequence('instructions', 'practice')
            practice_paths = glob.glob('images/prime/practice/*')
            for practice_path in practice_paths:
                identify_prime_image(practice_path)

        # Tell the user we are gonna start the real deal
                self.window.show_image_sequence('instructions', 'test')
        print(prime_list)
        # Start the tests
        for position in range(len(prime_list) // 2):
            # Get the prime image we will show
            prime_image_path = prime_list[position]
            prime_image_name = prime_image_path.split('/')[-1]

            # Get the user to do the task, and save the experiment_info['data']
            data_point = [experiment_info['Section'],
                          experiment_info['Participant'], experiment_info['Age group'],
                          experiment_info['date'],
                          int(N_BACK_TASK), experiment_info['prime list name'], experiment_info['blocks_reversed'],
                          prime_image_name, position + 1] + identify_prime_image(prime_image_path)
            experiment_info['data'].append(data_point)

        # Take a break
            self.window.show_image_sequence('instructions', 'halfway')

        # Continue the tests
        for position in range(len(prime_list) // 2, len(prime_list)):
            # Get the prime image we will show
            prime_image_path = prime_list[position]
            prime_image_name = prime_image_path.split('/')[-1]

            # Get the user to do the task, and save the experiment_info['data']
            data_point = [experiment_info['Section'],
                          experiment_info['Participant'], experiment_info['Age group'],
                          experiment_info['date'],
                          int(N_BACK_TASK), experiment_info['prime list name'], experiment_info['blocks_reversed'],
                          prime_image_name, position + 1] + identify_prime_image(prime_image_path)
            experiment_info['data'].append(data_point)

        # Save the data we gathered
        self.window.show_image_sequence('instructions', 'end')
        self.window.save_data()
