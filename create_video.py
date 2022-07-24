import io
import os
import json
import math

import logging
import subprocess

import my_util
import create_input

#Global Variables
my_audio_dir = ""
my_image_dir = ""

def init_program():
    logging.basicConfig(filename='tvtl.log', filemode='w', \
    format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('Started')
    
    #read our config file
    logging.info('Extract data from config file tvtl.json')
    with open("tvtl.json", "r") as jsonfile:
        data = json.load(jsonfile)
        #print("Read successful")
        
    #extract data field from the config file
    global my_audio_dir, my_image_dir
    
    my_audio_dir = data['audio_dir']
    my_image_dir = data['image_dir']

    #my_util.do_something()
    #logging.info('Finished')
    
    

init_program()

print("my_audio_dir = " + my_audio_dir)
print("my_image_dir = " + my_image_dir)

############################

def create_slide(imageDir,output):
    # ffmpeg -framerate 1/10 -i ./images1/image%d.jpg -vf "scale=800:600,setsar=1" -r 5 -c:v libx264 -crf 25 -preset slow scan-video.mp4
    #command = "ffmpeg -f concat -i ./images1/input.txt -vf mpdecimate -r 5 -c:v libx264 -crf 25 -preset slow scan-video.mp4" 
    #command = "ffmpeg -f concat -i ./images1/input.txt -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4"
    command = "ffmpeg -f concat -i {imageDir}/input.txt  -pix_fmt yuv420p -movflags +faststart ./output/slide.mp4".format(imageDir=imageDir, output=output)
    #command = "ffmpeg -i {video} -ac 1  -f flac -vn {output}".format(video=video, output=output)
    subprocess.call(command,shell=True)

def create_slide2(inputFile,output):
    command = "rm ./output/slide.mp4"
    subprocess.call(command,shell=True)

    # ffmpeg -framerate 1/10 -i ./images1/image%d.jpg -vf "scale=800:600,setsar=1" -r 5 -c:v libx264 -crf 25 -preset slow scan-video.mp4
    #command = "ffmpeg -f concat -i ./images1/input.txt -vf mpdecimate -r 5 -c:v libx264 -crf 25 -preset slow scan-video.mp4" 
    #command = "ffmpeg -f concat -i ./images1/input.txt -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4"
    command = "ffmpeg -f concat -i \"{inputFile}\"  -pix_fmt yuv420p -movflags +faststart ./output/slide.mp4".format(inputFile=inputFile, output=output)
    #command = "ffmpeg -i {video} -ac 1  -f flac -vn {output}".format(video=video, output=output)
    print("command = " + command)
    subprocess.call(command,shell=True)

def create_video(video,output):
    #command = "ffmpeg  -stream_loop -1 -i scan-video.mp4 -i ./sounds/silent_night.mp3 -shortest -map 0:v:0 -map 1:a:0 -y out.mp4"
    #we let the video run longer than the audio so will not use -shortest
    command = "ffmpeg  -i ./output/slide.mp4 -i ./sounds/silent_night.mp3 -map 0:v:0 -map 1:a:0 -y ./output/finalVideo.mp4"
    subprocess.call(command,shell=True)

def create_video2(soundInput,vidOutput):
    #command = "ffmpeg  -stream_loop -1 -i scan-video.mp4 -i ./sounds/silent_night.mp3 -shortest -map 0:v:0 -map 1:a:0 -y out.mp4"
    #we let the video run longer than the audio so will not use -shortest
    command = "ffmpeg  -i ./output/slide.mp4 -i \"{soundInput}\" -map 0:v:0 -map 1:a:0 -y \"{vidOutput}\"".format(soundInput=soundInput, vidOutput=vidOutput)
    subprocess.call(command,shell=True)
    
def create_video3(commandx, soundInput,vidOutput):
    command = "rm ./output/slide.mp4"
    subprocess.call(command,shell=True)
    
    subprocess.call(commandx,shell=True)
    
    command = "ffmpeg  -i ./output/slide.mp4 -i \"{soundInput}\" -map 0:v:0 -map 1:a:0 -y \"{vidOutput}\"".format(soundInput=soundInput, vidOutput=vidOutput)
    subprocess.call(command,shell=True)
    
    
 
#get song information and duration
def get_song_duration2(song_title):    
    song_path = my_audio_dir + '/' + song_title
    print(song_path)
    args=("ffprobe","-show_entries", "format=duration","-i", song_path)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print (output)

    #convert output to text and get duration
    txt = output.decode()
    print(txt)
    index = txt.find("=")

    #get duration in second
    duration = txt[index+1:index+6:1]
    
    #round up
    d = math.ceil(float(duration))
    print(d)

    return (d)
 
 
my_sound_list = my_util.get_sound_list(my_audio_dir)
#print(my_sound_list)

my_image_list = my_util.get_background_list(my_image_dir)
#print(my_image_list)
 
song_name = my_sound_list[1]
 
time = get_song_duration2(song_name)

command = create_input.create_slide_command(time, my_image_dir)
################
input_song = my_audio_dir + '/' + song_name
#print("input_song = " + input_song + "\n")

string_container = song_name.split('.')
output_video = "./video/" +  string_container[0] + ".mp4"
# print("output_video = " + output_video + "\n")

create_video3(command, input_song, output_video)
#####################
logging.info('Finished')
