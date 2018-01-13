""" A package that focuses on the user interaction"""

from psychopy import visual, event, gui, core
import sys
from glob import glob


def ask_user_info(title):
    """ A method used to ask the user for their participant id and their age group.
        Will quit if the user presses 'cancel'

        @param str title: The title of the pop-up box
        @return (str, str): A tuple with of (participant id, age group)
    """
    info = {'Participant': '', 'Age group': ''}

    # Store info about the experiment session
    dialogue = gui.DlgFromDict(dictionary=info, title=title)

    # User pressed cancel, so quit!
    if dialogue.OK is False:
        sys.exit()

    # Return the results
    return info['Participant'], info['Age group']


class Window:
    """ A class used to interface the interaction with the user"""

    def __init__(self, experiment):
        """ Initializes the window class"""
        self.experiment = experiment
        self.config = experiment.config

        # Create the window
        self._window = visual.Window(fullscr=True, monitor="testMonitor", units='norm', color=1)

        # Create an image to show full-screen images
        self._instruction_image = visual.ImageStim(win=self._window, units='norm', size=(2, 2))

        # The prime images have the same dimensions, so we can use one object for all of them
        self._prime_image = visual.ImageStim(win=self._window, units='cm')
        self._prime_image.size *= self.config.n_back_focal_image_height / self._prime_image.size[1]

        # Create an image to show the n-back focal image, important as they do not have the same dimensions
        self._n_back_images = []
        for i in range(8):
            image = visual.ImageStim(win=self._window, units='cm', image="images/n-back/task/{}.gif".format(i + 1))
            image.size *= self.config.n_back_focal_image_height / image.size[1]
            self._n_back_images += [image]

    def show_image_sequence(self, genre, subgenre='', task=None, extension='.png'):
        """ Shows all the images which follow the pattern
        'image/{task}/{genre}/{subgenre}/*{extension}', in ascending order.
        The images will be shown one after another.

        @param genre:
        @param subgenre:
        @param task:
        @param extension:
        @return:
        """
        if task is None:
            task = self.experiment.section
        image_paths = glob("images/{0}/{1}/{2}/*{3}".format(task, genre, subgenre, extension))
        image_paths.sort()

        for image_path in image_paths:
            self._instruction_image.image = image_path
            self._instruction_image.draw()
            self._window.flip()
            self.wait_for_prompt()

    def n_back_show(self, n_back_image_id, prime_image_path):
        """ Draws the given n-back image and prime image """
        n_back_image = self._n_back_images[n_back_image_id - 1]
        self._prime_image.image = prime_image_path

        if self.config.n_back_image_overlap:
            n_back_image.pos = (0, self.config.n_back_focal_image_height / 2)
            self._prime_image.pos = (0, -self.config.n_back_focal_image_height / 2)
        else:
            n_back_image.pos = (0, self.config.n_back_focal_image_height / 2)
            self._prime_image.pos = (0, -self.config.n_back_focal_image_height / 2)

        n_back_image.draw()
        self._prime_image.draw()
        self._window.flip()

    def show_text(self, text, size=None):
        """ Shows the text text on the main screen"""
        text_element = visual.TextStim(self._window, text=text, wrapWidth=None, color=-1, font='Times New Roman', height=size)
        text_element.draw()
        self._window.flip()

    def wait_for_choice(self, prompt, choices, size=None):
        """ Displays the given choices in lst choices with the given str prompt,
            and waits until one is picked. """
        # Display choices
        button_width = 2 / (len(choices) + 1.0)
        buttons = []
        for i in range(len(choices)):
            x_loc = 2 * ((i + 1.0) / (len(choices) + 1)) - 1

            text = visual.TextStim(self._window, text=choices[i], wrapWidth=button_width/1.1, color=-1,
                                   font='Times New Roman', pos=(x_loc, -0.5), height=size)
            text_width, text_height = text.boundingBox
            text_width = 2.0 * text_width / self._window.size[0]
            text_height = 2.0 * text_height / self._window.size[1]
            rect = visual.Rect(self._window, min(1.5 * text_width, button_width), 1.5 * text_height, lineColor=-1, pos=(x_loc, -0.5))
            buttons += [rect]
            rect.draw()
            text.draw()

        # Display the prompt
        text = visual.TextStim(self._window, text=prompt, wrapWidth=2, color=-1, font='Times New Roman', height=size)
        text.draw()

        # Tell the user to use their mouse
        text = visual.TextStim(self._window, text="Use your mouse to click:", wrapWidth=2, color=-1,
                               font='Times New Roman', alignHoriz='left', pos=(-0.9, -text_height), height=size)
        text.draw()

        self._window.flip()

        mouse = event.Mouse(win=self._window)
        # Wait for the user to click on one of them
        while True:
            for i in range(len(buttons)):
                if mouse.isPressedIn(buttons[i], buttons=[0]):
                    return choices[i]

            if len(event.getKeys(keyList=["escape"])) != 0:
                self.experiment.save_data()
                sys.exit()

            core.wait(0.01, hogCPUperiod=0)

    def wait_for_prompt(self, timer=None, keys='space'):
        """ Waits indefinitely until a key in keys is pressed. Return the key that was pressed.

            If a timer is provided, will wait for prompt until the timer runs out. If the timer runs out,
            None will be returned.

            @rtype: str|None
        """
        # Clear the key's buffer:
        event.clearEvents()

        if isinstance(keys, str):
            keys = [keys]

        keys = [k.lower() for k in keys] + [k.upper() for k in keys]

        # Wait for input
        while timer is None or timer.getTime() >= 0:
            # Get the keys that were pressed that we are watching
            keys_pressed = event.getKeys(keyList=keys)
            if len(keys_pressed) != 0:
                return keys_pressed[0]

            if len(event.getKeys(keyList=["escape"])) != 0:
                self.experiment.save_data()
                sys.exit()

        return None

    def close(self):
        """ Closes this window"""
        self._window.close()

    def get_input_text(self):
        """

        @return: The text the user inputted until they pressed the key '0'
        @rtype: str
        """
        # Clear the keys buffer
        event.getKeys()

        # Set up a text box for instructions
        text = "Please type in your answer, press the key '0' to submit it:"
        text_instr = visual.TextStim(win=self._window, text=text, color=-1, alignHoriz='left', alignVert='top',
                                     units='norm', pos=(-1, 1))

        # Set up a textbox for user input
        input_text = ""
        input_box = visual.TextStim(win=self._window, text=input_text, color=-1)

        # Get user input
        inputting = True

        while inputting:
            keys = event.getKeys()
            for key in keys:
                if key == '0':
                    inputting = False
                    break
                elif key == 'escape':
                    self.experiment.save_data()
                    core.quit()

                elif key == 'space':
                    input_text += ' '

                elif key == 'backspace':
                    if len(input_text) > 0:
                        input_text = input_text[:-1]
                elif len(key) == 1 and key.isalpha():
                    input_text += key
            input_box.text = input_text
            input_box.draw()
            text_instr.draw()
            self._window.flip()

        return input_text

    def clear(self, time):
        """ Clears the screen and pauses execution for the given amount of time"""
        self._window.flip()
        core.wait(time)
