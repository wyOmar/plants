import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

if len(sys.argv) < 2:
    print("Error: No image file path provided")
    sys.exit(1)

imagePath = sys.argv[1]

# Load the trained multi-class model
try:
    model = load_model("private/waste_classifier_multiclass.h5")
except Exception as e:
    print("Error loading waste classification model:", e)
    sys.exit(1)

try:
    img = Image.open(imagePath).convert("RGB")
    img = img.resize((224, 224))
    imgArray = img_to_array(img) / 255.0
    imgArray = np.expand_dims(imgArray, axis=0)
except Exception as e:
    print("Error processing image:", e)
    sys.exit(1)

try:
    prediction = model.predict(imgArray)
    predictedIdx = np.argmax(prediction[0])
    mapping = {
        0: "Blue Bag (Paper & Cardboard)",
        1: "Red Bag (Plastic & Cans)",
        2: "Brown Bin (Food)",
        3: "Blue Bin (Glass)"
    }
    result = mapping.get(predictedIdx, "Unknown")
    print("Prediction:", result)
    print(result)
except Exception as e:
    print("Error making prediction:", e)
    sys.exit(1)
