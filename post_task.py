from psychopy import core
import glob
import random
import re


class Trial:
    """ Trial for the prime reconition task """
    class DataPoint:
        """ DataPoint for a trial"""

        def __init__(self, image_folder_path, position, config):
            self.image_folder_path = image_folder_path
            self.image_name = re.split('[/\\\\]', image_folder_path)[-1]
            self.position = position

            self.difficulty = None
            self.user_response = None
            self.response_time = None

            self.__parent = config

    def __init__(self, image_folder_path, position, task):
        """ Create a trial object"""
        self.experiment = task.experiment
        self.window = task.window
        self.config = task.config
        self.to_save = self.DataPoint(image_folder_path, position, self.config)

    def run(self):
        """ Run the prime image identification task for the images in the folder folder_path """
        timer = core.CountdownTimer(self.config.prime_image_display_time)

        for self.to_save.difficulty in range(1, 9):
            # Show the prime image for this difficulty
            folder_path = self.to_save.image_folder_path
            image_name = self.to_save.image_name
            prime_image_path = "{0}/{1}_{2}.png".format(folder_path, image_name, self.to_save.difficulty)
            self.window.post_task_show(prime_image_path)

            # Wait for an input by the user, or for a timeout
            timer.reset()
            if self.window.wait_for_prompt(timer, 'space'):
                # Get the response time
                self.to_save.reaction_time = self.config.prime_image_display_time - timer.getTime()

                # User wants to input text, get input and return
                self.to_save.user_response = self.window.get_input_text()
                return

        # The user did not react in in time. Get the to identify something
        self.to_save.user_response = self.window.get_input_text()


class Task:
    def __init__(self, experiment):
        """ Create a prime task for the given experiment """
        self.experiment = experiment
        self.window = experiment.window
        self.config = experiment.config

    def run(self):
        """ Run the prime task"""
        # Change the section info
        self.experiment.new_section('prime')

        # Show the instructions for this task:
        self.window.show_image_sequence('instructions', 'start')

        # Go through the practice task
        if self.config.practice_run:
            self.window.show_image_sequence('instructions', 'practice')
            practice_paths = glob.glob('images/prime/practice/*')
            for practice_path in practice_paths:
                trial = Trial(practice_path, -1, self)
                trial.run()

        # Tell the user we are gonna start the real deal
        self.window.show_image_sequence('instructions', 'test')

        # Randomize how the prime image will be shown
        prime_list = glob.glob('images/prime/task/*/*')
        random.shuffle(prime_list)

        # Show first half of prime images
        for position in range(len(prime_list) // 2):
            prime_image_path = prime_list[position]
            trial = Trial(prime_image_path, position, self)
            trial.run()
            self.experiment.push_data(trial.to_save)

        # Take a break
        self.window.show_image_sequence('instructions', 'halfway')

        # Show the second half
        for position in range(len(prime_list) // 2, len(prime_list)):
            prime_image_path = prime_list[position]
            trial = Trial(prime_image_path, position, self)
            trial.run()
            self.experiment.push_data(trial.to_save)

        # Say thanks
        self.window.show_image_sequence('instructions', 'end')

        # Save the data we gathered
        self.window.save_data()
