import os
from PIL import Image

def change_color(image_path, target_color, replacement_color):
    # Open the image
    img = Image.open(image_path)

    # Get the image data
    pixels = img.load()

    # Iterate through each pixel
    for i in range(img.width):
        for j in range(img.height):
            # Get the current pixel color
            current_color = pixels[i, j]

            # Check if the current pixel color is NOT equal to the target color
            if current_color != target_color:
                # Replace the color with the specified replacement color
                pixels[i, j] = replacement_color

    # Save the modified image
    img.save(image_path.replace('bing_maps_images_mask', 'bing_maps_images_mask/modified_images'))

if __name__ == "__main__":
    # Folder containing the images
    folder_path = "bing_maps_images_mask"

    # Specify the target ARGB color (pink in this case)
    target_color = (255, 80, 100)  # Pink

    # Specify the replacement ARGB color (black in this case)
    replacement_color = (0, 0, 0)  # Black

    # Create a folder for modified images if it doesn't exist
    output_folder = os.path.join(folder_path, 'modified_images')
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            # Get the path of each image file
            image_path = os.path.join(folder_path, filename)

            # Call the function for each image
            change_color(image_path, target_color, replacement_color)
