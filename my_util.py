import re
import os

import logging

#####create config structure#####
# tvtl_info = {
    # "audio_dir" : "./sounds",
    # "image_dir" : "./images1",
    # "date" : "11/09/2020",
    # "topic" : "config file"
# }

#create config file --> no longer needed
#with open("tvtl.json", "w") as jsonfile:
#    json.dump(tvtl_info, jsonfile)
###########################

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def do_something():
    logging.info('Doing something')
    
# Get the list of all mp3 in directory
def get_sound_list(path):
    all_files = os.listdir(path)
    mp3_list = [ ]

    for file in all_files:
        if file.endswith(".mp3"):
            mp3_list.append(file)
 
    return(mp3_list)
    
 # Get the list of all the backgrounds
def get_background_list(path):
    all_files = os.listdir(path)
    image_list = [ ]

    for file in all_files:
        if file.endswith(".png"):
            image_list.append(file)
 
    image_list.sort(key = natural_keys)
    return(image_list)