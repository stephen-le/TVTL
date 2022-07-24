import os
import re
import sys
import math
import my_util

import random

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def get_number_of_picture_for_a_song(song_duration):
    duration = 20
    print("song_duration = " + str(song_duration) + "\n")
    number_of_pictures = math.ceil(int(song_duration) / duration)
    return number_of_pictures    

def create_slide_command(song_duration, image_dir):
    duration = 20
    #number_of_pictures = get_number_of_picture_for_a_song(song_duration)
    number_of_pictures = int(song_duration / duration)
    
    #check the remainder seconds
    remainder = 0;
    remainder = (song_duration % duration)
    
    if(remainder > 0):
        number_of_pictures = number_of_pictures + 1
  
    print("number_of_pictures = " + str(number_of_pictures) + "\n")
  
  
     #pick random pictures from the pool and create a list
    image_list = []
    image_pool = my_util.get_background_list(image_dir)
    
    max_index = len(image_pool)
    print("max_index = " + str(max_index) + "\n")
    
    random_list = list(range(1, max_index))
    random.shuffle(random_list)
    
    index = 0
    command = "ffmpeg "
    for i in range(0,number_of_pictures):
        if( i < number_of_pictures-1):
            command = command + "-loop 1 -t 20 -i " + image_dir + '/'+ str(random_list[index]) + '.jpg ' 
        else:
            command = command + '-loop 1 -t ' + str(remainder) + " -i " + image_dir + '/'+ str(random_list[index]) + '.jpg ' 
        index = index + 1
        
     #########
    command = command + '-filter_complex "'
    ##########
    command = command + '[0:v]fade=t=out:st=19:d=1[v0];'
    ###########
    for i in range(1, number_of_pictures):
        if( i < number_of_pictures-1):
            command = command + '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=19:d=1[v' + str(i) +'];'
        else:
            command = command + '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=' + str(remainder-1) + ':d=1[v' + str(i) +'];'
        
    ############
    for i in range(0,number_of_pictures):
        command = command + '[v' + str(i) + ']'
    ################################
    command = command + 'concat=n=' + str(number_of_pictures) + ':v=1:a=0,format=yuv420p[v]' + '"'
    ###################
    command = command + ' -map "[v]" ./output/slide.mp4'
    #print(command)
    return (command)

def create_slide_input(song_duration, song_name, song_path, image_dir):
    #default duration for each picture in the slide is #20 seconds
    #determine number of pictures needed for this video
    duration = 20
    print("song_duration = " + str(song_duration) + "\n")
    number_of_pictures = math.floor(int(song_duration) / duration)
    
    print("number_of_pictures = " + str(number_of_pictures) + "\n")
    
    #pick random pictures from the pool and create a list
    image_list = []
    image_pool = my_util.get_background_list(image_dir)
    
    max_index = len(image_pool)
    #print("max_index = " + str(max_index) + "\n")
    
    random_list = list(range(1, max_index))
    random.shuffle(random_list)
    
    index = 0
    for i in range(0,number_of_pictures):
        image_name = str(random_list[index]) + '.jpg' 
        image_list.append(image_name)
        index = index + 1

    #print("image_list: \n")
    #print(image_list)

    #sort all images in the list
    #image_list.sort(key = natural_keys)
    string_container = song_name.split('.')
    
    song_input = image_dir + '/' + string_container[0] + ".txt"
    #print("song_input = " + song_input + "\n")
    
    # write data in a file. 
    file1 = open(song_input,"w") 

    for fname in image_list:
        file_name = "file '" + fname + "'\n"
        file1.write(file_name)    
        if fname != image_list[-1]:
            file_duration = "duration " + str(duration) + "\n"
        else:
            file_duration = "duration " + str(int(duration) + 5) + "\n"
        
        file1.write(file_duration)
        
    file1.close() #to change file access modes 
    
    return song_input