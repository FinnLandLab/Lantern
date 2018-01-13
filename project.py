""" Code for running the Lantern experiment.
"""
import task
import post_task
from experiment import Experiment

# ---------------- SETUP --------------------
experiment = Experiment()

# ---------------- MAIN PROGRAM --------------------
if experiment.config.n_back_task:
    n_back = task.Task(experiment)
    n_back.run()

if experiment.config.prime_task:
    prime = post_task.Task(experiment)
    prime.run()

experiment.close()


