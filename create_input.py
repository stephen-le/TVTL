import os
import re
import sys

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#get the number of second from the first
#command argument
duration = sys.argv[1]

#read all images in the directory and store in a list
image_list = []
for image_name in os.listdir("./images1"):
    if image_name.endswith(".jpg"):
        image_list.append(image_name)

#sort all images in the list
image_list.sort(key = natural_keys)

# write data in a file. 
file1 = open("./images1/input.txt","w") 

for fname in image_list:
    file_name = "file '" + fname + "'\n"
    file1.write(file_name)
    
    if fname != image_list[-1]:
        file_duration = "duration " + duration + "\n"
    else:
        file_duration = "duration " + str(int(duration) + 5) + "\n"
        
    file1.write(file_duration)


file1.close() #to change file access modes 