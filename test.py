import os

def remove_image_strings(directory):
    for filename in os.listdir(directory):
        if 'image_' in filename:
            new_filename = filename.replace('image_', '')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        elif '_image' in filename:
            new_filename = filename.replace('_image', '')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

# Replace 'path/to/your/directory' with the directory path containing your files
directory_path = 'bing_maps_images_mask/bing_maps_images_completed_mask'
remove_image_strings(directory_path)