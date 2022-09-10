import os

#Change current working directory and print out it's location
working_location = os.chdir("./images2")
working_location = os.getcwd()
print(working_location)

i = 1
for fileName in os.listdir("."):
    #os.rename(fileName, fileName.replace("ThuVienTinLanh_img-", ""))
    new_name = str(i) + '.png'
    os.rename(fileName, new_name)
    i = i + 1