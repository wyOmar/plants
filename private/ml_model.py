import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

# Ensure an image file path was provided
if len(sys.argv) < 2:
    print("Error: No image file path provided")
    sys.exit(1)

imagePath = sys.argv[1]

# Load the pre-trained waste classifier model
try:
    model = load_model("private/waste_classifier.h5")
    print("Waste classification model loaded successfully")
except Exception as e:
    print("Error loading waste classification model:", e)
    sys.exit(1)

# Preprocess the input image
try:
    # Open the image and ensure it is in RGB mode
    img = Image.open(imagePath).convert("RGB")
    # Resize to the target dimensions (adjust if your model expects a different size)
    img = img.resize((224, 224))
    imgArray = img_to_array(img)
    imgArray = imgArray / 255.0  # normalise pixel values
    imgArray = np.expand_dims(imgArray, axis=0)
except Exception as e:
    print("Error processing image:", e)
    sys.exit(1)

# Make a prediction using the model
try:
    prediction = model.predict(imgArray)
    # Assuming binary classification with sigmoid activation:
    isRecyclable = prediction[0][0] >= 0.5
    result = "Recyclable" if isRecyclable else "Non-Recyclable"
    print("Prediction:", result)
    # Output only the prediction so that Node.js can parse it
    print(result)
except Exception as e:
    print("Error during prediction:", e)
    sys.exit(1)