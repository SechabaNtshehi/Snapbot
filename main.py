from time import sleep

import csv
from datetime import date
from datetime import datetime
import pytz
import os
from zipfile import ZipFile 

import snap
import crop
import colour
import mail
import json_handler

snapBot = snap.SnapBot()
cropBot = crop.CropBot()
colourBot = colour.ColourBot()
mailBot = mail.MailBot()
queryBot = json_handler.Querier()

def make_dir(path_):
	if not os.path.exists(path_):
		print("directory " + path_ + " does not exist, making one now...")
		os.makedirs(path_)

target_url = "http://localhost:8080/"
data_directory = "traffic-data/"
make_dir(data_directory)
data_path = data_directory + datetime.today().strftime("%A") + "-" +str(date.today().day) + "-" + str(date.today().month) + "-" + str(date.today().year) + "(Master File).csv"



def extract_data():
	number_of_locations = queryBot.query_number_of_locations()['total_locations']
	wait_interval = 1
	minute = 60

	
	try:
		while True:
			now = datetime.now()

			if now.minute % wait_interval == 0:
				if now.hour == 0 and now.minute == 0:
					share_data()
				else:
					collect_data(number_of_locations)

			sleep(minute)
	except KeyboardInterrupt:
			choice = input("program cancelled. Share data collected so far?(Input number)\n 1. Yes\n 2.No\n")
			if choice == 1:
				share_data()
				print("Data shared successfully, terminating program\n")
			else:
				print("Terminating program\n")



def collect_data(number_of_locations):
	location_index = 0

	while location_index < number_of_locations:
		response = queryBot.query_location_name(location_index)
		if response['status'] == "success":
			res = queryBot.set_next_location(response['name'])

			if res['status'] == 'success':
				snap_path = "data/" + response['name'] + "/" + str(date.today().year) + "/" + str(date.today().month)

				make_dir(snap_path)

				crop_path = snap_path + "/" + response['name'] + "_cropped.jpg"
				snap_path = snap_path + "/" + response['name'] + ".png"
				snapBot.snapSite(target_url, snap_path)
				
				image_coordinates = queryBot.query_image_coordinates()
				if image_coordinates['status'] == 'success':
					print(image_coordinates)
					cropBot.cropSnap(image_coordinates, snap_path, crop_path)



					with open(data_path, mode='a') as traffic_file:
						data_writer = csv.writer(traffic_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						rgb_tuple = colourBot.getColour(crop_path)
						current_time = datetime.now(pytz.timezone('Africa/Johannesburg'))
						data_writer.writerow( [response['name'], current_time,  datetime.today().strftime("%A"), rgb_tuple])

				print("done")
		else:
			print(response)

		location_index += 1

def share_data():
	file_paths = []
	
	file_paths.append(data_path)

	zip_path = "data/history/"+ "/" + str(date.today().year) + "/" + str(date.today().month)
	make_dir(zip_path)

	zip_path += "/" + datetime.today().strftime("%A") + str(date.today().day) + "-" + str(date.today().month) + "-" + str(date.today().year) + ".zip"
	with ZipFile (zip_path, 'w') as zip:
		for file in file_paths:
			print(file)
			zip.write(file)

	mailBot.sendData(zip_path)

# For debuggin purposes
def snap_location(index):
	response = queryBot.query_location_name(index)
	if response['status'] == "success":
		res = queryBot.set_next_location(response['name'])

		if res['status'] == 'success':
			snap_path = "data/" + response['name'] + "/" + str(date.today().year) + "/" + str(date.today().month)

			make_dir(snap_path)

			snap_path = snap_path + "/" + response['name'] + ".png"
			snapBot.snapSite(target_url, snap_path)	

while True:
	choice = input("1. Extract data\n 2. Snap a location\n3. Quit\n")

	if choice == '1':
		extract_data()
	elif choice == '2':
		index = input("Enter location Index")
		index = int(index)
		if index < 0 or index >= queryBot.query_number_of_locations()['total_locations']:
			print("invalid index")
		else:
			snap_location(index)
	elif choice == '3':
		break
	else:
		print("Invalid input")

	cont = input("1. Continue\n 2. Quit\n")

	if cont == '2':
		break
	else:
		continue








