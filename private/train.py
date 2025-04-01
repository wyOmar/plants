import os
import glob
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np

# ----- Configuration -----
dataDir = "private/images"  # Path to your dataset folder
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 10

# ----- Mapping Function for Recycling Categories -----
# This function assigns each category folder a label corresponding to:
# 0: Blue Bag (Paper and Cardboard)
# 1: Red Bag (Plastic and Cans)
# 2: Brown Bin (Food)
# 3: Blue Bin (Glass)
def mapCategory(categoryName):
    cat = categoryName.lower()
    # Check for Paper and Cardboard first
    if "paper" in cat or "cardboard" in cat:
        return 0  # Blue Bag
    # Check for Glass
    elif "glass" in cat:
        return 3  # Blue Bin
    # Check for Organic items (e.g. food waste)
    elif "organic" in cat or "food" in cat:
        return 2  # Brown Bin
    # Check for Plastic or cans or metal (assumed to be recycled together)
    elif "plastic" in cat or "can" in cat or "metal" in cat:
        return 1  # Red Bag
    else:
        # If a category doesn't match any rule, default to Red Bag
        return 1

# ----- Collect Image Paths and Labels -----
print("Collecting image paths and labels...")
imagePaths = []
imageLabels = []

# Iterate through each waste category (folder) in the dataset
for category in os.listdir(dataDir):
    categoryPath = os.path.join(dataDir, category)
    if os.path.isdir(categoryPath):
        label = mapCategory(category)
        # Each category folder contains subfolders "default" and "real_world"
        for subfolder in os.listdir(categoryPath):
            subfolderPath = os.path.join(categoryPath, subfolder)
            if os.path.isdir(subfolderPath):
                for imgFile in glob.glob(os.path.join(subfolderPath, '*.png')):
                    imagePaths.append(imgFile)
                    imageLabels.append(label)

print(f"Found {len(imagePaths)} images.")

# Convert labels into a NumPy array
imageLabels = np.array(imageLabels)

# ----- Train/Test Split -----
trainPaths, testPaths, trainLabels, testLabels = train_test_split(
    imagePaths, imageLabels, test_size=0.2, random_state=42
)

# ----- Utility Function to Load and Preprocess Images -----
def loadAndPreprocessImage(path, label):
    # Read the image file
    image = tf.io.read_file(path)
    # Decode PNG and ensure the image has 3 channels (RGB)
    image = tf.image.decode_png(image, channels=3)
    # Resize the image
    image = tf.image.resize(image, [IMG_HEIGHT, IMG_WIDTH])
    # Normalise the pixel values to [0, 1]
    image = image / 255.0
    return image, label

# ----- Create TensorFlow Datasets for Training and Validation -----
trainDataSet = (
    tf.data.Dataset.from_tensor_slices((trainPaths, trainLabels))
    .map(loadAndPreprocessImage, num_parallel_calls=tf.data.AUTOTUNE)
    .shuffle(buffer_size=1000)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

testDataSet = (
    tf.data.Dataset.from_tensor_slices((testPaths, testLabels))
    .map(loadAndPreprocessImage, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

# ----- Define the Model Architecture -----
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", 
                  input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(4, activation="softmax")  # 4 classes for recycling categories
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ----- Train the Model -----
history = model.fit(
    trainDataSet,
    validation_data=testDataSet,
    epochs=EPOCHS
)

# ----- Save the Model -----
modelSavePath = "private/waste_classifier_multiclass.h5"
model.save(modelSavePath)
print(f"Model saved to {modelSavePath}")
