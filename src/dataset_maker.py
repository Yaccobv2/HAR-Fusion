"""
Module responsible for making dataset
"""
import os
import cv2


def save_data(class_name: str, frames: list, gyro_data: list):

    if not os.path.isdir('dataset'):
        os.mkdir("dataset")
    if not os.path.isdir(str("dataset/" + class_name)):
        os.mkdir(str("dataset/" + class_name))

    last_data = fast_scandir("dataset/" + class_name)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, 'dataset/' + class_name + '/' + str(last_data+1))
    if os.path.exists(final_directory):
        print("Dir already exist")
        print("FAILED TO SAVE DATA")
    else:
        os.mkdir(final_directory)
        os.mkdir(final_directory+'/imgs')

        textfile = open(final_directory + "/gyro.txt", "w")
        for data in gyro_data:
            textfile.write(str(data) + "\n")
        textfile.close()

        for i, frame in enumerate(frames):
            cv2.imwrite(final_directory+'/imgs/'+str(i)+'.png', frame)

        print("SAVED DATA SUCCESSFULLY")


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    if len(subfolders) == 0:
        last = 0
    else:
        last = len(subfolders)
    return last
