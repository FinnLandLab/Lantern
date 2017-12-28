""" Code for running the Lantern experiment.
"""
# import some libraries from PsychoPy
from psychopy import visual, core, event, gui
import os
import sys
import glob
import csv
import time



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
    if not N_BACK_OVERLAP:
        image.pos = (0, N_BACK_TASK_IMG_HEIGHT / 2)
    n_back_images += [image]


# Make a prime image template to use later.
# Make sure it exists, and has the same ratio as the prime images

image_file = "images/prime/practice/airplane/airplane_8.png"
prime_image = visual.ImageStim(win=window, image=image_file)
prime_image.size *= PRIME_TASK_IMG_HEIGHT / prime_image.size[1]
if not N_BACK_OVERLAP:
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














# ---------------- MAIN PROGRAM --------------------

if N_BACK_TASK:
    n_back_task()

if PRIME_TASK:
    prime_task()
# cleanup
window.close()
core.quit()
