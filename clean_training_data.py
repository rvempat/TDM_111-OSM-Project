import os

def extract_id(filename, folder):
    if folder == 'images':
        return filename.split('_')[0]
    elif folder == 'masks':
        return filename.split('_')[-1].split('.')[0]

def get_ids(folder_path, folder):
    ids = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            ids.append(extract_id(filename, folder))
    return set(ids)

def remove_unmatched_images(folder_path, ids_to_keep):
    for filename in os.listdir(folder_path):
        file_id = extract_id(filename, 'images') if 'image_' in filename else extract_id(filename, 'masks')
        if file_id not in ids_to_keep:
            os.remove(os.path.join(folder_path, filename))
            print(f"Removed: {filename}")

# Folder paths
images_folder = "D:/training_dataset/images"
masks_folder = "D:/training_dataset/masks"

# Get ids from both folders
images_ids = get_ids(images_folder, 'images')
masks_ids = get_ids(masks_folder, 'masks')

# Find ids to keep (intersection of both sets)
ids_to_keep = images_ids.intersection(masks_ids)

# Remove unmatched images
remove_unmatched_images(images_folder, ids_to_keep)
remove_unmatched_images(masks_folder, ids_to_keep)

print("Unmatched images removed.")
