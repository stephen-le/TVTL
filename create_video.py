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
my_video = ""

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
    song_path = song_title
    
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
    

    
def SelectSong(songDir):
    global my_video
    
    my_sound_list = my_util.get_sound_list(songDir)
    print(my_sound_list)
    
    print("\nPlease enter the song name, end with mp3")
    song_name = input()
    my_video = song_name
    
    song_full_name = my_audio_dir + '/' + song_name
    #print("input_song = " + song_full_name + "\n")
    return song_full_name
    
 
def SelectSongCover(songCoverDir):
    cover_image_list = my_util.get_background_list(songCoverDir)
    print(cover_image_list)
    
    print("\nPlease enter the cover image, end with png")
    cover_image_file = input()
    cover_image_file_fname = my_audio_dir + '/' + cover_image_file
    #print("input_song = " + cover_image_file_fname + "\n")
    return cover_image_file_fname

def SelectSongCredit(songCoverDir):
    credit_image_list = my_util.get_background_list(songCoverDir)
    print(credit_image_list)
    
    print("\nPlease enter the credit image, end with png")
    credit_image_file = input()
    credit_image_file_fname = my_audio_dir + '/' + credit_image_file
    #print("input_song = " + credit_image_file_fname + "\n")
    return credit_image_file_fname



flag = True
while flag:
    print("**********************************\n")
    input_song = SelectSong(my_audio_dir)
    print(input_song)
    print("**********************************\n")
    song_cover = SelectSongCover(my_audio_dir)
    print(song_cover)
    print("**********************************\n")
    song_credit = SelectSongCredit(my_audio_dir)
    print(song_credit)
    print("**********************************\n")
    time = get_song_duration2(input_song)
    
    if(time > 350): #when duration is more than 6min, it is often wrong
        print("Please verify the song duration and enter it here: ")
        time = input()
    
    command = create_input.create_slide_command(time, my_image_dir, song_cover, song_credit)
    create_input.create_input_file(time, my_image_dir, song_cover, song_credit, my_video)    
    
    string_container = my_video.split('.')
    output_video = "./video/" +  string_container[0] + ".mp4"
    #print("output_video = " + output_video + "\n")
    
    create_video3(command, input_song, output_video)
    
    
    flag = False
        
 
 



################





#####################
logging.info('Finished')
