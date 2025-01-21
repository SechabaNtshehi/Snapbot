from PIL import Image
from collections import Counter

class ColourBot:
	def getColour(self, crop_path):
		# Load the image
		image = Image.open(crop_path)

		# Resize the image to reduce processing time
		#image = image.resize((100, 100))

		# Convert image to RGB
		image = image.convert("RGB")

		# Get all pixels
		pixels = list(image.getdata())
	
		# Count the frequency of each color
		most_common_color = Counter(pixels).most_common(1)[0][0]

		print(f"The most common color is: {most_common_color}")
		
		return most_common_color