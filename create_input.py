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

def create_slide_command(song_duration, image_dir, song_cover, song_credit):
    duration = 20
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
    
    #insert song cover
    command = command + "-loop 1 -t 20 -i " + song_cover + ' '
    
    for i in range(0,number_of_pictures-2):
        command = command + "-loop 1 -t 20 -i " + image_dir + '/'+ str(random_list[index]) + '.png ' 
        index = index + 1
        
    #insert song credit
    if(remainder > 0):
        command = command + '-loop 1 -t ' + str(remainder) + " -i " + song_credit + ' '
    else:
        command = command + '-loop 1 -t ' + "10" + " -i " + song_credit + ' '
        
    ##########
    command = command + '-filter_complex "'
    ##########
    command = command + '[0:v]fade=t=out:st=19:d=1[v0];'
    ###########
    for i in range(1, number_of_pictures):
        if( i < number_of_pictures-1):
            command = command + '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=19:d=1[v' + str(i) +'];'
        else: #last image
            if(remainder > 0):
                command = command + '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=' + str(remainder-1) + ':d=1[v' + str(i) +'];'
            else:
                command = command + '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=' + "9" + ':d=1[v' + str(i) +'];'
        
    ############
    for i in range(0,number_of_pictures):
        command = command + '[v' + str(i) + ']'
    ################################
    command = command + 'concat=n=' + str(number_of_pictures) + ':v=1:a=0,format=yuv420p[v]' + '"'
    ###################
    command = command + ' -map "[v]" ./output/slide.mp4'
    print(command)
    return (command)

####
def create_input_file(song_duration, image_dir, song_cover, song_credit, input_song):
    duration = 20
    number_of_pictures = int(song_duration / duration)
    
    #check the remainder seconds
    remainder = 0;
    remainder = (song_duration % duration)
    
    if(remainder > 0):
        number_of_pictures = number_of_pictures + 1
  
    #print("number_of_pictures = " + str(number_of_pictures) + "\n")
  
  
     #pick random pictures from the pool and create a list
    image_list = []
    image_pool = my_util.get_background_list(image_dir)
    
    max_index = len(image_pool)
    #print("max_index = " + str(max_index) + "\n")
    
    random_list = list(range(1, max_index))
    random.shuffle(random_list)
    
  
    
    string_container = input_song.split('.')    
    input_file = image_dir + '/' + string_container[0] + ".txt"
    
    # write data in a file. 
    file1 = open(input_file,"w") 

    index = 0
    command = "ffmpeg " + "\\" + "\n"
    file1.write(command)    
       
    #insert song cover
    command = "-loop 1 -t 20 -i " + song_cover + '  \\\n'   
    file1.write(command)       
  
    
    for i in range(0,number_of_pictures-2):
        command = "-loop 1 -t 20 -i " + image_dir + '/'+ str(random_list[index]) + '.png \\\n' 
        file1.write(command)  
        index = index + 1
        
    #insert song credit
    if(remainder > 0):
        command = '-loop 1 -t ' + str(remainder) + " -i " + song_credit + ' \\\n'
    else:
        command = '-loop 1 -t ' + "10" + " -i " + song_credit + ' \\\n'
        
    file1.write(command)  
       

        
    ##########
    command = '-filter_complex  \\\n'
    file1.write(command) 
    
    
    ##########
    command = '"[0:v]fade=t=out:st=19:d=1[v0]; \\\n'
    file1.write(command) 
    
       
    ###########
    for i in range(1, number_of_pictures):
        if( i < number_of_pictures-1):
            command = '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=19:d=1[v' + str(i) +']; \\\n'
            file1.write(command) 
        else:
            if (remainder > 0):
                command = '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=' + str(remainder-1) + ':d=1[v' + str(i) +']; \\\n'
            else:
                command = '[' + str(i) + ':v]fade=t=in:st=0:d=1,fade=t=out:st=' + "9" + ':d=1[v' + str(i) +']; \\\n'
                
            file1.write(command) 
    ############
    for i in range(0,number_of_pictures):
        command = '[v' + str(i) + ']'
        file1.write(command) 
    ################################
    command = 'concat=n=' + str(number_of_pictures) + ':v=1:a=0,format=yuv420p[v]' + '"' + " \\\n"
    file1.write(command) 
    ###################
    command = ' -map "[v]" ./output/slide.mp4'
    file1.write(command) 
   
    file1.close() #to change file access modes  
 
####
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
        image_name = str(random_list[index]) + '.png' 
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
