
import tensorflow as tf
import numpy as np
import os
from skimage.transform import resize
from skimage.io import imread
image_directory = 'dataset/images'
mask_directory = 'dataset/masks'
TARGET_SIZE = (128, 128)

def load_images_and_masks(image_directory, mask_directory, target_size):
    images = []
    masks = []

    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg'):  # or .png, .jpeg
            img_path = os.path.join(image_directory, filename)
            mask_path = os.path.join(mask_directory, filename)  # Adjust if mask names differ

            img = imread(img_path)[:,:,:3]  # Assuming RGB images
            img = resize(img, target_size)
            img = img / 255.0  # Normalization to [0, 1]

            mask = imread(mask_path, as_gray=True)
            mask = resize(mask, target_size)
            mask = mask > 0.5  # Binarizing mask
            mask = np.expand_dims(mask, axis=-1)  # Add channel dimension

            images.append(img)
            masks.append(mask)

    return np.array(images), np.array(masks)

images, masks = load_images_and_masks(image_directory, mask_directory, TARGET_SIZE)

from sklearn.model_selection import train_test_split


X_train, X_val, y_train, y_val = train_test_split(images, masks, test_size=0.1)  # Adjust the test size as needed

"""import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate
from tensorflow.keras.models import Model

def unet(input_size=(256, 256, 3)):
    inputs = Input(input_size)

    # Downsample
    c1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(128, (3, 3), activation='relu', padding='same')(p1)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(256, (3, 3), activation='relu', padding='same')(p2)

    # Upsample and concatenate
    u4 = UpSampling2D((2, 2))(c3)
    u4 = Concatenate()([u4, c2])
    c4 = Conv2D(128, (3, 3), activation='relu', padding='same')(u4)

    u5 = UpSampling2D((2, 2))(c4)
    u5 = Concatenate()([u5, c1])
    c5 = Conv2D(64, (3, 3), activation='relu', padding='same')(u5)

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(c5)

    model = Model(inputs=[inputs], outputs=[outputs])
    return model

# Create the U-Net model
unet_model = unet()"""

from sklearn.model_selection import train_test_split

# Assuming 'images' is your array of satellite images and 'masks' is the array of corresponding mask images
# Split the dataset into training and test sets
X_train, X_temp, y_train, y_temp = train_test_split(images, masks, test_size=0.3, random_state=42)

# Split the remaining data into validation and test sets
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose, concatenate

def build_unet(input_shape=(128, 128, 3)):
    inputs = Input(input_shape)

    # Contraction path
    c1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(128, (3, 3), activation='relu', padding='same')(p1)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(256, (3, 3), activation='relu', padding='same')(p2)

    # Expansion path
    u4 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c3)
    u4 = concatenate([u4, c2])
    c4 = Conv2D(128, (3, 3), activation='relu', padding='same')(u4)

    u5 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c4)
    u5 = concatenate([u5, c1])
    c5 = Conv2D(64, (3, 3), activation='relu', padding='same')(u5)

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(c5)

    model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
    return model

# Create the U-Net model
model = build_unet()

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
# Replace 'X_train', 'y_train', 'X_val', and 'y_val' with your training and validation data
history = model.fit(X_train, y_train, batch_size=32, epochs=25, validation_data=(X_val, y_val))

# Evaluate the model on the test set
# Replace 'X_test' and 'y_test' with your test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)

print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

from skimage.io import imread
from skimage.transform import resize
import numpy as np
import os

def preprocess_new_images(image_directory, target_size):
    new_images = []
    for filename in os.listdir(image_directory):
        if filename.endswith('.jpeg'):  # Adjust the file extension as needed
            img_path = os.path.join(image_directory, filename)
            img = imread(img_path)[:,:,:3]  # Assuming RGB images
            img = resize(img, target_size)
            img = img / 255.0  # Normalizing to the range [0, 1]
            new_images.append(img)
    return np.array(new_images)

# Usage example
new_images_directory = 'bing_maps_images_new_images'
target_size = (128, 128)  # or (256, 256), depending on your model's input size
new_images = preprocess_new_images(new_images_directory, target_size)
print(new_images.shape)

#new_images = preprocess_new_images(new_images_directory, (128, 128))
predicted_masks = model.predict(new_images)
predicted_masks = (predicted_masks > 0.5).astype("float32")

import matplotlib.pyplot as plt

# Display the original and segmented images
def display_segmentation(original_images, predicted_masks, num_images=2):
    plt.figure(figsize=(10, 5))

    for i in range(num_images):
        plt.subplot(2, num_images, i + 1)
        plt.imshow(original_images[i])
        plt.title("Original Image")
        plt.axis('off')

        plt.subplot(2, num_images, num_images + i + 1)
        plt.imshow(original_images[i])
        plt.imshow(predicted_masks[i].squeeze(), cmap='jet', alpha=0.5)  # Overlay with transparency
        plt.title("Segmented Image")
        plt.axis('off')

    plt.show()

# Call the function with your images and masks
display_segmentation(new_images, predicted_masks, num_images=2)

import matplotlib.pyplot as plt
from skimage.io import imread
import os

def display_original_images(image_directory, num_images=2):
    fig, axes = plt.subplots(1, num_images, figsize=(10, 5))

    for i, filename in enumerate(os.listdir(image_directory)):
        if i >= num_images:
            break
        if filename.endswith('.jpg'):  # Adjust the file extension as needed
            img_path = os.path.join(image_directory, filename)
            img = imread(img_path)
            axes[i].imshow(img)
            axes[i].axis('off')
            axes[i].set_title(f"Image {i+1}")

    plt.show()

# Usage example
image_directory = 'bing_maps_images_new_images'
display_original_images(image_directory, num_images=2)

import cv2
import numpy as np

def post_process_masks(predicted_masks):
    processed_masks = []
    for mask in predicted_masks:
        mask = mask.squeeze()  # Remove channel dimension
        mask = cv2.threshold(mask, 0.5, 1, cv2.THRESH_BINARY)[1]
        # Apply morphological operations like opening or closing if needed
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        processed_masks.append(mask)
    return np.array(processed_masks)

processed_masks = post_process_masks(predicted_masks)

