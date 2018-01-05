import time
import os
import sys
import visual
from config import Configuration

# ---------------- VERIFICATION --------------------
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(
    os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# ---------------------------------------------------
# -------------------  MAIN CODE  -------------------
# ---------------------------------------------------


class Experiment:
    """ A general experiment class containing all the information for the experiment.
    """

    def __init__(self):
        """ Initializes a experiment class. """
        self.name = "Lantern"

        self.participant, self.age_group = visual.ask_user_info(self.name)

        # Get the numbers from the participant_id string
        self.participant_num = int("".join([c for c in self.participant if c.isdigit()]))

        self.config = Configuration(self.participant_num)

        self.date = time.strftime('%c')
        self._data = []
        self.section = 'setup'
        self.window = visual.Window(self)

    def push_data(self, data_point):
        """ Adds a data point to be saved later.

            @param lst data_point: The data point to be saved
            @rtype None
        """
        self._data.append(data_point)

    def new_section(self, section_name):
        """ Start a new section of the experiment"""
        self.section = section_name
        self._data = []

    def save_data(self):
        """ Saves the data data that was pushed since the last time new section was called to:
        "{section}.csv" and resets the data to be saved

        """

        location = "{0}/{1}/{2}/{3}/".format(self.config.output_location,
                                             self.section, self.age_group, self.participant)
        # Make sure the file directory exists
        if not os.path.exists(location):
            os.makedirs(location)

        # Get the output file
        output_file = open(location + self.section + ".csv", 'w')

        # Write the header for the csv file
        if self.section == 'task':
            output_file.write(DATA_HEADER_TASK)
        elif self.section == 'post-task':
            output_file.write(DATA_HEADER_POST)
        else:
            raise Exception("Section name is '{}'".format(self.section))

        # End the line
        output_file.write("\n")

        # Output the answers, and close the file
        for row in self._data:
            row = ",".join(str(entry) for entry in row)
            output_file.write(row)
            output_file.write("\n")
        output_file.close()

        self._data = []

    def close(self):
        """ Ends the experiment. Does not save any data"""
        self.window.close()
