import cv2
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, AutoImageProcessor

# Load your local model and processor
model_dir = "./model"  # folder with model.safetensors and config.json
model = AutoModelForImageClassification.from_pretrained(model_dir)
processor = AutoImageProcessor.from_pretrained(model_dir)

# Use CPU or CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR (OpenCV) to RGB (PIL expects RGB)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)

    # Preprocess image
    inputs = processor(images=pil_img, return_tensors="pt").to(device)

    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_idx = logits.argmax(-1).item()
        predicted_label = model.config.id2label[predicted_idx]

    # Display prediction on the frame
    cv2.putText(frame, f"{predicted_label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the video feed
    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
