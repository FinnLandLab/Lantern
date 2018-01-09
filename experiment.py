import time
import os
import sys
import visual
from config import Configuration
from pandas import DataFrame

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
        self._data = {}
        self._data_type = None
        self.section = 'setup'
        self.window = visual.Window(self)

    def push_data(self, data_point):
        """ Adds a data point to be saved later.

            @param lst data_point: The data point to be saved
            @rtype None
        """
        if self._data_type is None:
            self._data_type = type(data_point)
        elif type(data_point) != self._data_type or data_point is None:
            raise ValueError("data_point ", data_point, "has the wrong type")

        to_save = vars(data_point)
        while '__parent' in to_save:
            parent = to_save.pop('__parent')
            to_save.update(vars(parent))

        for key in to_save:
            if key not in self._data:
                self._data[key] = []
            self._data[key].append(to_save[key])

    def new_section(self, section_name):
        """ Start a new section of the experiment"""
        self.section = section_name
        self._data = {}
        self._data_type = None

    def save_data(self):
        """ Saves the data data that was pushed since the last time new section was called to:
        "{section}.csv" and resets the data to be saved

        """

        dir_loc = "{0}/{1}/{2}/{3}/".format(self.config.output_location,
                                            self.section, self.age_group, self.participant)
        # Make sure the file directory exists
        if not os.path.exists(dir_loc):
            os.makedirs(dir_loc)

        # Get the output file
        file_loc = dir_loc + self.section + ".csv"
        df = DataFrame.from_dict(self._data)
        df.to_csv(file_loc)

    def close(self):
        """ Ends the experiment. Does not save any data"""
        self.window.close()
