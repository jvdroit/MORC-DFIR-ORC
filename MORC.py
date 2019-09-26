#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
from .seeker import Seeker

# To be put in config file
# Base directory
BASE_DIR = "/mnt/MORC/"
# Directory with the DFIR-ORCs
IN_DIR = BASE_DIR + "INPUT/"
# Directory for the working process
WORK_DIR = BASE_DIR + "WORKSPACE/"
# Directory for the output result
OUT_DIR = BASE_DIR + "OUTPUT/"

DIRECTORIES = [BASE_DIR,IN_DIR,WORK_DIR,OUT_DIR]

# Base name for our DFIR-ORCs
BASE_NAME = "ORCSYS"

# Check time in the IN_DIR (milliseconds)
CHECK_TIME = 500

if __name__ == '__main__':

    # Directory initiation
    for d in DIRECTORIES:
        if not os.path.exists(d):
            os.makedirs(d)

    # Queues initiation
    queue_dis = queue.Queue()
    queue_extrac = queue.Queue()
    queue_av = queue.Queue()


    see = seeker(queue_dis,IN_DIR,BASE_NAME,CHECK_TIME)
    #dis = dispatcher(queue_dis,queue_extrac,queue_av,IN_DIR,WORK_DIR,OUT_DIR)
    #ext = extractor(queue_extrac,IN_DIR,WORK_DIR)
    #tim = timeliner(queue_extrac,WORK_DIR,OUT_DIR)
    #avc = avcheck(queue_av,WORK_DIR,OUT_DIR)

    see.start()
    #dis.start()
    #ext.start()
    #tim.start()
    #avc.start()

    input()

    see.stop()
    #dis.stop()
    #ext.stop()
    #tim.stop()
    #avc.stop()
