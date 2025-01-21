from imagedominantcolor import DominantColor

file_path = 'cropped_map.jpg'
dominant_colour = DominantColor(file_path)

print(dominant_colour.dominant_color)
print(dominant_colour.r, dominant_colour.g, dominant_colour.b)