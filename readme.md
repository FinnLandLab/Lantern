# What file do I run?

Run the "project.py" file. You can open it with psychopy.

# Files

## config.py

This file has all the configurations for the project. Feel free to mess around with different configurations. These will all be saved along with the data output by the experiment. The variables that can be changed are the following, with a description of what they do:

- self.output_location = "data"
	- Output directory for data collected during experiment
- self.animation_time_between_frames
	- The number of seconds to wait after showing an image that is marked with "\_animation". 
- self.practice_run = True
	- Complete a practice run before the main task and the post-task.
- self.n_back_task
	- Whether or not to run the main task (n-back task).
- self.n_back_block_total = 4
	- The number of blocks that the n-back task will run through. At most 4. 
- self.n_back_start_difficulty = 1
	- The difficulty of the first n-back block 
- self.n_back_min_errors_to_lower_difficulty
	- The threshold of errors where if you hit it or go over it, the difficulty is lowered. 
- self.n_back_max_errors_to_raise_difficulty = 3
	- The threshold of errors where if you hit it or go under it, the difficulty is raised. 
- self.n_back_focal_image_height = 10
	- The height of the n-back image you need to focus on during the n-back.
- self.n_back_prime_image_height = 10
	- The height of the prime image that is meant to distract you during the n-back
- self.n_back_image_overlap = True
	- Whether the prime and focal image in the n-back task will overlap
- self.n_back_display_time = 1
	- The amount of time that an n-back image is shown for during the n-back task
- self.n_back_interstimulus_interval = 0.5
	- How long to hold for on a blank screen between n-back trials.
- self.n_back_task_critical_age = 6
	- The oldest you can be and still get the easier version of the n-back task where difficulty is capped.
- self.prime_task = True
	- Whether or not to run the post-task (recall task).
- self.prime_image_display_time = 1.5
	- The amount of time to display the prime image at a specific difficulty at the recall task.



## experiment.py

Contains data about the whole experiment. Contains an instance of config and is accessible from everywhere within the code. Responsible for saving data. The data is saved at a path like "/section/name.csv" in the output_location directory from config.py

## project.py

Ties everything together. Creates an experiment object with all the data about the experiment and its configuration and calls on task.py and post_task.py to run the task and posttask.

## task.py

Runs the main task for the experiment. It is run with the run(experiment) function. The general ideal is that the task contains blocks, which contain trials. So task > block > trial. Each of these object will have an associated run method, where for example task.run runs an experiment which runs many blocks and block.run runs a block which runs many experiments. Along these, there is also the datapoint class. **The only things that will be saved are in the datapoint classes and in the config class**. These are saved using experiment.py's push_data and save_data methods.

There are two sets of priming images, A and B. Each set needs to contain exactly 23 images. Participants will be exposed to exactly on of these in the main task (n-back task). These images need to be located in /images/prime/task under folders A and B. They need to be saved in folders with their names and there needs to be eight of them labeled 1 - 8 where image 1 shows the least and 8 the most detail.

The task is split into at most 4 blocks. Each block contains exactly 23 stimuli. The stimuli are in /images/n-back/task/

Each stimuli is presented alongside with a distractor or priming image. This image might be displayed on top of or beneath the stimuli.

The participant is shown a sequence of images, and is supposed to press 'a' whenever the image is the same as one that was shown n-back before it, where n can be 1,2 or 3 depending on the difficulty of the block.

The order of the images in the n-back task is determined by ordering files saved at /ordering/n_i.csv where n denotes the difficulty of the n-back task and i denotes what block number it is. However these are run through backwards half of the time.

### Data

Along with all the config variables, the following things are also saved for the main task:

#### Trial data
- self.position_in_block
	- The position of the trials within it's block 
- self.focal_image_id 
	- The id of the n-back image being shown for this trial
- self.prime_image_path
	- The path to the prime image being shown for this trial
- self.prime_image_id
	- The id of the prime image being shown for this trial
- self.n_back_image_id
	- The id of the image that was n-back relative to this trial if there was one
- self.lure
	- If there is a lure, a lure happens when an i-back focal image is the same as the current focal image, and i is not the n-back difficulty for the block
- self.lure_kind
	- The kind of lure if there is one. A lure happens when an i-back focal image is the same as the current focal image, and i is not the n-back difficulty for the block (kind would be i)
- self.expected_response
	- The expected or correct response for this trial
- self.user_response
	- What the user responded for this trial
- self.user_correct
	- If the user was correct for this trial
- self.reaction_time = None
	- The reaction time for the user for this trial, if they reacted.

#### Block data

- self.n_back_type
	- The type of n-back for this block (1,2, or 3 back)
- self.block_number = block_number
	- The position of this block within the trial (ie ith block shown)
- self.order_set = block_config.order_set
	- The order set being used for this block
- self.prime_folder = block_config.prime_folder
	- The folder where prime images are being taken from for this block.


## post_task.py

Will ask the participant to identify images from sets A and B, one of which they were exposed to if they completed the main task. These images have 8 levels of detail, 1 being the lowest and 8 being the highest where 8 denotes the full picture.

Participants are shown all images from sets A and B in 46 trials. Each trial starts at the lowest detail for it's image and increasing the amount of detail until they recognize it or are seeing the full image.

When the user wants to identify something, they press space and type in what they think it is. If they reach the full image, the prompt automatically comes up.

### Data
Along with all the config variables, the following things are also saved for the post task:

#### Trial data
- self.image_folder_path
	- The path to the folder containing the images for this trial
- self.image_name
	- The name of the image being shown in this trial
- self.set
	- The set of images that the image being shown for this trial is from (A or B)
- self.appeared_in_n_back_task
	- Whether this image was shown in the n-back task or not
- self.position
	- The position of this trial relative to all other trials for the experiment (i if this is the ith trial) 
- self.difficulty
	- The difficulty level where the participant wrote what they thought the image was.
- self.user_response = None
	- What the participants thought the image was
- self.reaction_time = None
	- How long it took for the participants to press space indicating they want to write what they think the image is. Calculated from when the most recent resolution of the image was shown. If they did not press space ever, will be none.

## visual.py

Controls how the experiment is displayed. All drawing and visual related functions are here but none of the experiment logic. If you want to change how the experiment looks, try to change how the function is called first as the whole experiment is affected by changing this file.





























