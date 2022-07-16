import io
import os
import re
import math
import subprocess

####utility#######
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def create_slide(video,output):
    # ffmpeg -framerate 1/10 -i ./images1/image%d.jpg -vf "scale=800:600,setsar=1" -r 5 -c:v libx264 -crf 25 -preset slow scan-video.mp4
    #command = "ffmpeg -f concat -i ./images1/input.txt -vf mpdecimate -r 5 -c:v libx264 -crf 25 -preset slow scan-video.mp4" 
    #command = "ffmpeg -f concat -i ./images1/input.txt -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4"
    command = "ffmpeg -f concat -i ./images1/input.txt  -pix_fmt yuv420p -movflags +faststart output.mp4"
    #print(command)
    #command = "ffmpeg -i {video} -ac 1  -f flac -vn {output}".format(video=video, output=output)
    subprocess.call(command,shell=True)


def create_video(video,output):
    #command = "ffmpeg  -stream_loop -1 -i scan-video.mp4 -i ./sounds/silent_night.mp3 -shortest -map 0:v:0 -map 1:a:0 -y out.mp4"
    #we let the video run longer than the audio so will not use -shortest
    command = "ffmpeg  -i output.mp4 -i ./sounds/silent_night.mp3 -map 0:v:0 -map 1:a:0 -y finalVideo.mp4"
    subprocess.call(command,shell=True)

#get song information and duration
def get_song_duration():
    args=("ffprobe","-show_entries", "format=duration","-i", "./sounds/silent_night.mp3")
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    #print (output)

    #convert output to text and get duration
    txt = output.decode()
    #print(txt)
    index = txt.find("=")

    #get duration in second
    duration = txt[index+1:index+4:1]
    #print(duration)

    #calculate slide show duration
    slide_duration = math.ceil(int(duration) / 11);
    return (slide_duration + 1)
 
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
        if file.endswith(".jpg"):
            image_list.append(file)
 
    image_list.sort(key = natural_keys)
    return(image_list)
 
my_sound_list = get_sound_list("./sounds")
#print(my_sound_list)

my_image_list = get_background_list("./images1")
#print(my_image_list)
 
time = get_song_duration()

# call create_input.py script
command = "python3 create_input.py " + str(time)
os.system(command)

create_slide('100','dm-new.flac')
#create_slide(time,'dm-new.flac')
create_video('one', 'two')


#create_slide('dm.MOV','dm-new.flac')

#create_video('one', 'two')
