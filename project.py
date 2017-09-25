""" Code for running the Lantern experiment.
"""
# import some libraries from PsychoPy
from psychopy import visual, core, event, gui
import os
import sys
import random
import glob
import csv
import time


# ---------------- CONSTANTS --------------------

# The relative directory that data will be saved to.
OUTPUT_LOCATION = "data"

# The names of the variables being recorded for the n-back task. Corresponds to DATA_HEADER_N_BACK
DATA_NAMES_N_BACK = ["experiment",
                     "participant id", "age group",
                     "date",
                     "blocks reversed",
                     "prime list name", "prime image",
                     "n-back type", "order set", "position in block",
                     "image id", "n-back image",
                     "lure", "lure kind",
                     "expected response",
                     "user response", "reaction time"]


# The header for the csv file being saved for the n-back task
DATA_HEADER_N_BACK = ",".join(DATA_NAMES_N_BACK)

# The names of the variables being recorded for the post task. Corresponds to DATA_HEADER_PRIME
DATA_NAMES_PRIME = ["experiment",
                    "participant id", "age group",
                    "date",
                    "n-back task", "prime list", "n-back reversed",
                    "prime image", "trial number", "image difficulty",
                    "user response", "reaction time"]

# The header for the csv file being saved for the post task
DATA_HEADER_PRIME = ",".join(DATA_NAMES_PRIME)

# For the n-back task. Both in seconds
N_BACK_IMAGE_DISPLAY_TIME = 1
N_BACK_INTERSTIMULUS_INTERVAL = 0.5

# For the post-task. In seconds
PRIME_IMAGE_DISPLAY_TIME = 1.5

# Name will be shown on the pop-up before the experiment
EXPERIMENT_NAME = "Lantern"

# Go through a practice run?
PRACTICE_RUN = True

# Go through the n-back task?
N_BACK_TASK = False

# Go through the prime task? (Prime images will still appear in the n-back task)
PRIME_TASK = True

# How many n-back tasks to go through? (At most 4)
NUMBER_OF_BLOCKS = 4

# The first n-back task is a (START_N_BACK_DIFFICULTY)-task. Make sure it is
# either 1,2 or 3
START_N_BACK_DIFFICULTY = 1

# The minimum amount of errors needed to decrease the difficulty of the
# n-back task. If the user commits more than MIN_ERRORS_RELAX_DIFF,
# the difficulty decreases
MIN_ERRORS_LOWER_DIFF = 5

# The maximum amount of errors needed to increase the difficulty of the
# n-back task. If the user commits less than MIN_ERRORS_RELAX_DIFF,
# the difficulty increases
MAX_ERRORS_RISE_DIFF = 3

# The height of the n-back images in centimeters
N_BACK_TASK_IMG_HEIGHT = 10

# The height of the prime images in centimeters
PRIME_TASK_IMG_HEIGHT = 10


# ---------------- VERIFICATION --------------------
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(
    os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)


# ---------------- SETUP --------------------

experiment_info = {'Participant': '', 'Age group': ''}
# Store info about the experiment session
dialogue = gui.DlgFromDict(dictionary=experiment_info, title=EXPERIMENT_NAME)

# User pressed cancel, so cancel!
if dialogue.OK is False:
    core.quit()

# Get the participant number
experiment_info['participant number'] = int("".join([c for c in experiment_info['Participant'] if c.isdigit()]))

# Get the experiment_info['date'] and time
experiment_info['date'] = time.strftime('%c')

# create a window
window = visual.Window(fullscr=True, monitor="testMonitor", units="cm", color=1)

# Define some n-back images for quick access later
n_back_images = []
for i in range(8):
    image = visual.ImageStim(win=window, image="images/n-back/task/{}.gif".format(i + 1))
    image.size *= N_BACK_TASK_IMG_HEIGHT / image.size[1]
    image.pos = (0, N_BACK_TASK_IMG_HEIGHT / 2)
    n_back_images += [image]


<<<<<<< HEAD
# Make a prime image template to use later. Changed from accordion to ball since accordion is no longer image in set A
image_file = "images/prime/task/A/ball/ball_8.png"
=======
# Make a prime image template to use later.
# Make sure it exists, and has the same ratio as the prime images

image_file = "images/prime/practice/airplane/airplane_8.png"
>>>>>>> 3f8f38a02f57de10ab9873b9045baaac77bc3b92
prime_image = visual.ImageStim(win=window, image=image_file)
prime_image.size *= PRIME_TASK_IMG_HEIGHT / prime_image.size[1]
prime_image.pos = (0, -PRIME_TASK_IMG_HEIGHT / 2)

# Make a template image to show announcements to the user
instruction_image = visual.ImageStim(win=window, units='norm', size=(2, 2))

# Add some experiment info to be used later
experiment_info['blocks_reversed'] = ''

# Which prime distractor list will we use?
experiment_info['prime list name'] = ''


# ---------------- FUNCTIONS --------------------

def save_data():
    """ Saves the data in experiment_info['data'] in the list my_answers into a file with the name:
    "{name}.csv"

    """
    # Get where we will store the data
    age_group = experiment_info["Age group"]
    participant_id = experiment_info["Participant"]

    location = "{}/{}/{}/".format(OUTPUT_LOCATION, age_group, participant_id)

    # Make sure the file directory exists
    if not os.path.exists(location):
        os.makedirs(location)

    # Get what section of the experiment we are in:
    data_name = experiment_info['Section']

    # Get the output file
    output_file = open(location + data_name + ".csv", 'w')

    if data_name == 'n-back':
        output_file.write(DATA_HEADER_N_BACK)
    elif data_name == 'prime':
        output_file.write(DATA_HEADER_PRIME)
    else:
        raise Exception("Section name is not 'n-back' or 'prime'")

    output_file.write("\n")

    # Output the answers, and close the file
    for row in experiment_info['data']:
        row = ",".join(str(entry) for entry in row)
        output_file.write(row)
        output_file.write("\n")
    output_file.close()


def timer_is_running(timer):
    """ Return True if timer is None, otherwise return True iff
    timer.getTime() >= 0

    @param timer: The timer to be checked
    @type timer: CountdownTimer|None
    @rtype: bool
    """
    return timer.getTime() >= 0 if timer is not None else True


def wait_for_prompt(timer=None, key='space'):
    """ Waits indefinitely unttil the user strikes the {key}, or until
    esc is pressed exiting the program or until the timer runs out if there
    is one. Return True iff the user precessed {key} to exit

    @rtype: bool
    """
    # Clear the key's buffer:
    event.getKeys()

    # Wait for input
    while timer_is_running(timer):
        if len(event.getKeys(keyList=[key.lower(), key.upper()])) != 0:
            return True
        if len(event.getKeys(keyList=["escape"])) != 0:
            save_data()
            core.quit()
            return False

    return False


def show_images(genre, subgenre, task=None, extension='.png'):
    """ Shows all the instructions which follow the pattern
    '{image}/{task}/{genre}/{subgenre}/*{extension}', in ascending order.

    @param genre:
    @param subgenre:
    @param task:
    @param extension:
    @return:
    """
    if task is None:
        task = experiment_info['Section']
    image_paths = glob.glob("images/{0}/{1}/{2}/*{3}".format(task, genre, subgenre, extension))
    image_paths.sort()

    for image_path in image_paths:
        instruction_image.image = image_path
        instruction_image.draw()
        window.flip()
        wait_for_prompt()


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

    if header:
        # Get rid of the header
        lines = lines[1:]

    return lines


def show_n_back(image_id, prime_path, timer):
    """

    @param image_id:
    @param prime_path:
    @param timer:
    @return:
    @rtype:
    """
    # Draw the n-back image and the prime image
    n_back_images[image_id - 1].draw()

    prime_image.image = prime_path
    prime_image.draw()

    window.flip()
    timer.reset()

    # Catch user input
    if wait_for_prompt(timer, 'a'):
        # User pressed the key 'a'
        reaction_time = N_BACK_IMAGE_DISPLAY_TIME - timer.getTime()
        core.wait(timer.getTime())
        return 1, reaction_time

    return 0, ''


def get_n_back_image_id(num_back, last_image_ids):
    """

    @param num_back:
    @param last_image_ids:
    @return:
    """
    if len(last_image_ids) < num_back:
        return ''

    return last_image_ids[num_back - 1]


def get_lure_info(num_back, image_id, last_image_ids):
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


def show_n_back_block(block, num_back, test_number, image_id_column=2, save=True):
    """ Shows a block of images in the n-back tasks

    @param lst block: A matrix containing the ordering info for this block
    @param int num_back: The type of n-back task
    @param int test_number: What test number this is, used only for output
    @param int image_id_column: the column of the block matrix with the image_id information
    @param bool save: Whether the data should be saved to experiment['data'] or not
    @return: the number of wrong answers
    @rtype: int
    """
    # Timer for this task
    timer = core.CountdownTimer(N_BACK_IMAGE_DISPLAY_TIME)

    # Get the prime images we'll use
    prime_images = glob.glob('images/prime/task/{}/*/*_8.png'.format(experiment_info['prime list name']))

    # Randomize the order in which the the prime images will be displayed
    random.shuffle(prime_images)

    # Counter for wrong answers
    wrong_answers = 0

    # A list containing the most recently viewed images
    last_image_ids = []

    for position_in_block in range(len(block)):
        # Get the prime
        prime_path = prime_images[position_in_block]
        prime_name = prime_path.split('/')[-1][:-6]

        # Rename some data for easier usage
        order_set = (NUMBER_OF_BLOCKS - test_number) if experiment_info['blocks_reversed'] else (test_number + 1)
        image_id = int(block[position_in_block][image_id_column])

        # Get what the user should answer
        n_back_image_id = get_n_back_image_id(num_back, last_image_ids)
        expected_responce = int(image_id == n_back_image_id)

        # Get the lure information
        lure, lure_kind = get_lure_info(num_back, image_id, last_image_ids)

        # Get the user responce
        user_responce, reaction_time = show_n_back(image_id, prime_path, timer)

        if user_responce != expected_responce:
            wrong_answers += 1

        # Save some data
        if save:
            data_point = [experiment_info['Section'],
                          experiment_info['Participant'], experiment_info['Age group'],
                          experiment_info['date'],
                          experiment_info['blocks_reversed'],
                          experiment_info['prime list name'], prime_name,
                          num_back, order_set, position_in_block + 1,
                          image_id, n_back_image_id,
                          lure, lure_kind,
                          expected_responce,
                          user_responce, reaction_time]
            experiment_info['data'].append(data_point)

        # Add image_id to last_image_ids limiting it's size to 3
        last_image_ids = [image_id] + last_image_ids[:2]

        # Wait N_BACK_INTERSTIMULUS_INTERVAL seconds before the next stimulus
        window.flip()
        core.wait(N_BACK_INTERSTIMULUS_INTERVAL)

    return wrong_answers


def n_back_task():
    """ Run the n-back task"""
    # Set the experiment name
    experiment_info['Section'] = 'n-back'

    # Create a place to store the data
    experiment_info['data'] = []

    # Show the user some instructions
    show_images('instructions', 'start')

    experiment_info['blocks_reversed'] = experiment_info['participant number'] % 2
    experiment_info['prime list name'] = 'A' if (experiment_info['participant number'] // 2) % 2 == 0 else 'B'

    if PRACTICE_RUN:
        # Show practice instructions
        show_images('instructions', 'practice')

        # PRACTICE RUN
        for i in range(2):
            # Get the file with the data for the image ordering
            block = get_csv_data("{}_practice.csv".format(i + 1))

            # Draw the instruction screen for this type of block
            show_images('prompts', '{}-back'.format(i + 1))

            # Go through this block without saving the data
            show_n_back_block(block, i + 1, i + 1, image_id_column=0, save=False)

    # Show instructions before actual test
    show_images("instructions", "test")

    # Check if we'll reverse the blocks we'll be using:
    experiment_info['blocks_reversed'] = experiment_info['participant number'] % 2

    # Load the blocks, in the order we'll run them.
    blocks = [[], [], []]
    for diff in range(3):
        for j in range(NUMBER_OF_BLOCKS):
            blocks[diff].append(get_csv_data("{}_{}.csv".format(diff + 1, j + 1)))

        # Reverse the blocks half of the time
        if experiment_info['blocks_reversed']:
            blocks[diff].reverse()

    # Se the starting n_back difficulty
    num_back = START_N_BACK_DIFFICULTY

    # START TESTS
    for test_number in range(NUMBER_OF_BLOCKS):
        # Get the block we will be using
        block = blocks[num_back - 1][test_number]

        # Show the instruction image
        show_images('prompts', '{}-back'.format(num_back))

        errors = show_n_back_block(block, num_back, test_number)

        if errors >= MIN_ERRORS_LOWER_DIFF and num_back > 1:
            num_back -= 1

        elif errors <= MAX_ERRORS_RISE_DIFF and num_back < 3:
            num_back += 1

    # Store the data we gathered in experiment_info['data']
    save_data()

    # Put up the end of experiment screen
    show_images('instructions', 'end')


def get_input_text():
    """

    @return: The text the user inputted until they pressed the key '0'
    @rtype: str
    """
    # Clear the keys buffer
    event.getKeys()

    # Set up a text box for instructions
    text = "Please type in your answer, press the key '0' to submit it:"
    text_instr = visual.TextStim(win=window, text=text, color=-1, alignHoriz='left', alignVert='top', units='norm', pos=(-1, 1))

    # Set up a textbox for user input
    input_text = ""
    input_box = visual.TextStim(win=window, text=input_text,  color=-1)

    # Get user input
    inputting = True

    while inputting:
        keys = event.getKeys()
        for key in keys:
            if key == '0':
                inputting = False
                break
            elif key == 'escape':
                save_data()
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
        window.flip()

    return input_text


def identify_prime_image(folder_path):
    """ Run the prime image identification task for the images in the folder folder_path

    @param folder_path:
    @return:
    @rtype:
    """
    folder_name = folder_path.split('/')[-1]

    timer = core.CountdownTimer(PRIME_IMAGE_DISPLAY_TIME)

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


def prime_task():
    """ Run the prime task"""
    # Change the section info
    experiment_info['Section'] = 'prime'

    # Reset/Initalize the data in experiment_info['data']
    experiment_info['data'] = []

    # Center the prime image we'll display
    prime_image.pos = (0, 0)

    # Randomize how the prime image will be shown
    prime_list = glob.glob('images/prime/task/*/*')
    random.shuffle(prime_list)

    # Show the instructions for this task:
    show_images('instructions', 'start')

    # Go through the practice task
    if PRACTICE_RUN:
        show_images('instructions', 'practice')
        practice_paths = glob.glob('images/prime/practice/*')
        for practice_path in practice_paths:
            identify_prime_image(practice_path)

    # Tell the user we are gonna start the real deal
    show_images('instructions', 'test')
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
    show_images('instructions', 'halfway')

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
    save_data()
    show_images('instructions', 'end')


# ---------------- MAIN PROGRAM --------------------

if N_BACK_TASK:
    n_back_task()

if PRIME_TASK:
    prime_task()
# cleanup
window.close()
core.quit()
