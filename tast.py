class NBackTask:
    def __init__(self):
        """

        """
        pass

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
        experiment_info['prime list name'] = 'A' if (int(experiment_info['participant number']) // 2) % 2 == 0 else 'B'

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
