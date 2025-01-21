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

target_url = "http://localhost:5555/"
data_path = "traffic-data/" + datetime.today().strftime("%A") + "-" +str(date.today().day) + "-" + str(date.today().month) + "-" + str(date.today().year) + "(Master File).csv"

def extract_data():
	minutes_in_day = 1440
	interval_in_minutes = 1440/2 #5
	total_snaps = minutes_in_day/interval_in_minutes
	interval_counter = 0

	location_index = 0
	number_of_locations = queryBot.query_number_of_locations()['total_locations']

	day = 0
	week = 7

	while day < 1:#week:
		while interval_counter < 1 :#total_snaps:
			while location_index < number_of_locations:
				response = queryBot.query_location_name(location_index)
				if response['status'] == "success":
					res = queryBot.set_next_location(response['name'])

					if res['status'] == 'success':
						snap_path = "data/" + response['name'] + "/" + str(date.today().year) + "/" + str(date.today().month)


						if not os.path.exists(snap_path):
							print("directory " + snap_path + " does not exist, making one now...")
							os.makedirs(snap_path)

						crop_path = snap_path + "/" + response['name'] + "_cropped.jpg"
						# data_path = "traffic-data/" + datetime.today().strftime("%A") + "-" +str(date.today().day) + "-" + str(date.today().month) + "-" + str(date.today().year) + "(Master File).csv"
						#.strftime("%A") include day name
						#data_path points to one place -- don't forget the zip section
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

			interval_counter += 1
			location_index = 0



		# file_counter = 0
		file_paths = []
		# while file_counter < number_of_locations:
		# response = queryBot.query_location_name(file_counter)
		# if response['status'] == "success":
		# 	res = queryBot.set_next_location(response['name'])

		# 	if res['status'] == 'success':
		# snap_path = "data/" + response['name'] + "/" + str(date.today().year) + "/" + str(date.today().month)
		
		file_paths.append(data_path)
			# file_counter += 1

		zip_path = "data/history/"+ "/" + str(date.today().year) + "/" + str(date.today().month)
		if not os.path.exists(zip_path):
			print("directory " + zip_path + " does not exist, making one now...")
			os.makedirs(zip_path)

		zip_path += "/" + datetime.today().strftime("%A") + str(date.today().day) + "-" + str(date.today().month) + "-" + str(date.today().year) + ".zip"
		with ZipFile (zip_path, 'w') as zip:
			for file in file_paths:
				print(file)
				zip.write(file)

		mailBot.sendData(zip_path)
		day += 1

def snap_location(index):
	response = queryBot.query_location_name(index)
	if response['status'] == "success":
		res = queryBot.set_next_location(response['name'])

		if res['status'] == 'success':
			snap_path = "data/" + response['name'] + "/" + str(date.today().year) + "/" + str(date.today().month)


			if not os.path.exists(snap_path):
				print("directory " + snap_path + " does not exist, making one now...")
				os.makedirs(snap_path)

			crop_path = snap_path + "/" + response['name'] + "_cropped.jpg"
			# data_path = snap_path + "/" + str(date.today().day) + "-" + str(date.today().month) + "-" + str(date.today().year) + "(" + response['name'] +").csv"
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








