import os
import cv2
import numpy as np


print("Welcome!")
print("This image generator program will create a numpy array for you images")
print("Keep all your image folders under a common folder named \"data\"")

folders = []
n = int(input("Enter total no. of folders: "))
for i in range(n):
	folder = input("Enter {}st folder name: ".format(i+1))
	folders.append(folder)
folders = sorted(folders)
print()

height = int(input("Enter height of reqiured image: "))
width = int(input("Enter width of required image: "))
color = int(input("Enter 1 for colored image, 0 for gray image: "))
dimension = (height, width)


print()
print("Starting Process:::::::::::::", end="\n\n")

label_map = {}
num = 0
for folder in folders:
	label_map[folder] = num
	num += 1

path = os.getcwd()
base = path
path = os.path.join(path, "data")

walk = os.walk(path)

for dirpath, dirnames, filenames in walk:
	folder = os.path.basename(dirpath)
	if folder in folders:
		os.chdir(dirpath)
		path = os.getcwd()
		walk = os.walk(path)
		image_count = 0

		for dirpath, dirnames, filenames in walk:
			folder_array = []

			for filename in filenames:
				if not (filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg")):
					os.remove(filename)
				image_count += 1

				image = cv2.imread(os.path.join(dirpath, filename))
				if color == 0:
					image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				image = cv2.resize(image, (256, 256))
				folder_array.append(image)

			folder_array = np.asarray(folder_array, dtype=np.int8)
			array_label = [label_map[folder]] * image_count
			folder_array = np.asarray(array_label, dtype=np.int8)

			os.chdir(base)
			image_filename = folder + "image" + str(height) + str(width) + str(color)
			label_filename = folder + "label" + str(height) + str(width) + str(color)
			np.save(image_filename, folder_array)
			np.save(label_filename, array_label)

		print("{} images found in {} folder".format(image_count, folder), end="\n\n")
print("Process Completed::::::::")
print("Files saved to your project folder", end="\n\n")

for folder in folders:
	print("Label for {} is {}".format(folder, label_map[folder]))